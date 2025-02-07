import numpy as np
from matplotlib.widgets import RectangleSelector, ToolHandles
from matplotlib.patches import Polygon
from matplotlib.transforms import Affine2D
from matplotlib.backend_bases import MouseButton


class ParallelogramSelector(RectangleSelector):
    #TODO: write docstring
    def __init__(self, ax, onselect=None, *, minspanx=0,
                 minspany=0, useblit=False,
                 props=None, spancoords='data', button=None, grab_range=10,
                 handle_props=None, interactive=False,
                 state_modifier_keys=None, drag_from_anywhere=False,
                 ignore_event_outside=False, use_data_coordinates=False):
        super().__init__(ax, onselect=onselect, minspanx=minspanx,
                 minspany=minspany, useblit=useblit,
                 props=props, spancoords=spancoords, button=button, grab_range=grab_range,
                 handle_props=handle_props, interactive=interactive,
                 state_modifier_keys=state_modifier_keys, drag_from_anywhere=drag_from_anywhere,
                 ignore_event_outside=ignore_event_outside, use_data_coordinates=use_data_coordinates)
    
        if self._interactive:
            self._shear_point_order = ['Wsh', 'Ssh', 'Esh', 'Nsh']
            xs, ys = self.shear_points
            self._shear_handles = ToolHandles(self.ax, xs, ys, marker='D',
                                            marker_props=self._handle_props,
                                            useblit=self.useblit)

    def _init_shape(self, **props):
        return Polygon([[0, 0], [1, 0], [1, 1], [0, 1]], visible=False, **props)

    def _press(self, event):
        """Button press event handler."""

        # make the drawn box/line visible get the click-coordinates, button, ...
        if self._interactive and self._selection_artist.get_visible():
            self._set_active_handle(event)
        else:
            self._active_handle = None

        xdata, ydata = self._get_data_coords(event)
        self._eventpress.xdata, self._eventpress.ydata = xdata, ydata
        xy = self.ax.transData.transform([xdata, ydata])
        self._eventpress.x, self._eventpress.y = xy

        if ((self._active_handle is None or not self._interactive) and
                not event.button == MouseButton.RIGHT and self._allow_creation):
            # Clear previous selection before drawing new rectangle.
            self.update()

        if (self._active_handle is None and not self.ignore_event_outside and
                not event.button == MouseButton.RIGHT and self._allow_creation):
            self._visible = False
            self.corners = (xdata,) * 4, (ydata,) * 4
            self._visible = True
        else:
            self.set_visible(True)

        self._corners_on_press = self.corners
        self._center_on_press = self.center
        self._set_aspect_ratio_correction()

        return False

    def _release(self, event):
        """Button release event handler."""
        
        if not self._interactive:
            self._selection_artist.set_visible(False)

        if (self._active_handle is None and self._selection_completed and
                self.ignore_event_outside):
            return

        xdata, ydata = self._get_data_coords(event)
        self._eventrelease.xdata, self._eventrelease.ydata = xdata, ydata
        xy = self.ax.transData.transform([xdata, ydata])
        self._eventrelease.x, self._eventrelease.y = xy

        # calculate dimensions of box or line
        if self.spancoords == 'data':
            spanx = abs(self._eventpress.xdata - self._eventrelease.xdata)
            spany = abs(self._eventpress.ydata - self._eventrelease.ydata)
        elif self.spancoords == 'pixels':
            spanx = abs(self._eventpress.x - self._eventrelease.x)
            spany = abs(self._eventpress.y - self._eventrelease.y)
        else:
            _api.check_in_list(['data', 'pixels'],
                               spancoords=self.spancoords)
        # check if drawn distance (if it exists) is not too small in
        # either x or y-direction
        if spanx <= self.minspanx or spany <= self.minspany:
            if self._selection_completed:
                # Call onselect, only when the selection is already existing
                self.onselect(self._eventpress, self._eventrelease)
            else:
                self._clear_without_update()
        else:
            self.onselect(self._eventpress, self._eventrelease)
            self._selection_completed = True

        self.update()
        self._active_handle = None
        self._corners_on_press = None
        self._center_on_press = None

        return False

    def _onmove(self, event):
        """
        Motion notify event handler.

        This can do one of four things:
        - Translate
        - Rotate
        - Re-size
        - Continue the creation of a new shape
        """
        #TODO: deal with move events outside the ax
        #TODO: turn the markers to the right orientation
        #TODO: add minspan functionality

        eventpress = self._eventpress
        state = self._state
        rotate = ('rotate' in state or eventpress.button == MouseButton.RIGHT)
        move = self._active_handle == 'C'
        reshape = self._active_handle and not move

        xdata, ydata = self._get_data_coords(event)

        dx = xdata - eventpress.xdata
        dy = ydata - eventpress.ydata

        corners = np.column_stack(self._corners_on_press)

        # rotate an existing shape
        if rotate:
            # calculate angle abc
            if self._use_data_coordinates:
                a = (eventpress.xdata, eventpress.ydata)
                b = self._center_on_press
                c = (xdata, ydata)
            else:
                a = (eventpress.x, eventpress.y)
                b = self.ax.transData.transform(self._center_on_press)
                c = (event.x, event.y)
                corners = self.ax.transData.transform(corners)

            angle = (np.arctan2(c[1]-b[1], c[0]-b[0]) -
                     np.arctan2(a[1]-b[1], a[0]-b[0]))
            rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                        [np.sin(angle), np.cos(angle)]])
            corners -= b
            corners = np.matmul(rotation_matrix, corners.T).T
            corners += b

            if not self._use_data_coordinates:
                corners = self.ax.transData.inverted().transform(corners)
            xc, yc = corners.T

        elif reshape:
            corner_reshape = self._active_handle in self._corner_order
            edge_reshape = self._active_handle in self._edge_order
            shear_reshape = self._active_handle in self._shear_point_order
            if corner_reshape:
                c_idx = self._corner_order.index(self._active_handle)
            elif edge_reshape:
                c_idx = self._edge_order.index(self._active_handle)
            elif shear_reshape:
                c_idx = self._shear_point_order.index(self._active_handle)

            grabbed_corner = corners[c_idx].copy()
            # vectors from grabbed corner
            vec1 = corners[(c_idx + 1) % 4] - grabbed_corner
            vec2 = corners[(c_idx - 1) % 4] - grabbed_corner
            vec_diag = corners[(c_idx + 2) % 4] - grabbed_corner
            vec_cursor = [xdata, ydata] - grabbed_corner
            # find which coefficients linearly combine vec1 and vec2
            # into the cursor vector
            local_to_global = np.column_stack((vec1, vec2))
            global_to_local = np.linalg.inv(local_to_global)
            local_cursor = np.matmul(global_to_local, vec_cursor)

            def box(bottomleft, topright):
                return np.array([bottomleft, (topright[0], bottomleft[1]), 
                                 topright, (bottomleft[0], topright[1])], dtype=float)

            if shear_reshape:
                local_corners = box((0, 0), (1, 1))
                local_corners[-1, 1] += local_cursor[1] - 3/4
                local_corners[0, 1] += local_cursor[1] - 3/4
                if 'center' in state:
                    local_corners [:, 1] -= (local_cursor[1] - 3/4) / 2

            elif 'square' in state:
                if corner_reshape:
                    margin = np.dot(vec_cursor, vec_diag) / np.dot(vec_diag, vec_diag)
                    local_corners = box((margin, margin), (1, 1))
                elif edge_reshape:
                    margin = local_cursor[0]
                    local_corners = box((margin, margin / 2), (1, 1 - margin / 2))
                if 'center' in state:
                    local_corners = box((margin, margin), (1 - margin, 1 - margin))
            else:
                opposite_corner = (1, 1)
                if corner_reshape:
                    if 'center' in state:
                        opposite_corner = (1, 1) - local_cursor
                    local_corners = box(local_cursor, opposite_corner)
                elif edge_reshape:
                    if 'center' in state:
                        opposite_corner = (1 - local_cursor[0], 1)
                    local_corners = box((local_cursor[0], 0), opposite_corner)

            # transform local corners to global data coordinates and roll them
            # by c_idx, because the local 0 index depends on which corner was grabbed
            corners = np.roll(np.matmul(local_to_global, local_corners.T).T, c_idx, 0)
            corners += grabbed_corner
            xc, yc = corners.T

        elif move:
            xc, yc = self._corners_on_press
            dx = xdata - eventpress.xdata
            dy = ydata - eventpress.ydata
            xc += dx
            yc += dy

        else:
            # Create a new shape

            # Don't create a new rectangle if there is already one when
            # ignore_event_outside=True
            if ((self.ignore_event_outside and self._selection_completed) or
                    not self._allow_creation):
                return

            center = [eventpress.xdata, eventpress.ydata]
            dx = (xdata - center[0]) / 2
            dy = (ydata - center[1]) / 2
        
            # square shape
            if 'square' in state:
                if self._use_data_coordinates:
                    vec_diag = (np.sign(dx), np.sign(dy))
                    scale = np.dot((dx, dy), vec_diag) / 2
                    (dx, dy) = scale * vec_diag
                else:
                    aspect_ratio = self.ax._get_aspect_ratio()
                    scale = (abs(dx) + abs(dy) * aspect_ratio) / 2
                    dx = scale * np.sign(dx)
                    dy = scale * np.sign(dy) / aspect_ratio

            # from center
            if 'center' in state:
                dx *= 2
                dy *= 2

            # from corner
            else:
                center[0] += dx
                center[1] += dy

            x0, x1, y0, y1 = (center[0] - dx, center[0] + dx,
                              center[1] - dy, center[1] + dy)
            xc, yc = (x0, x1, x1, x0), (y0, y0, y1, y1)

        # bound validation and potential shifting back into the field
        xlim = sorted(self.ax.get_xlim())
        ylim = sorted(self.ax.get_ylim())
        xovershoot = [xlim[0] - np.min(xc), np.max(xc) - xlim[1]]
        yovershoot = [ylim[0] - np.min(yc), np.max(yc) - ylim[1]]
        if xovershoot[0] > 0 and xovershoot[0] < -xovershoot[1]:
            xc += xovershoot[0]
        elif xovershoot[1] > 0 and xovershoot[1] < -xovershoot[0]:
            xc -= xovershoot[1]
        if yovershoot[0] > 0 and yovershoot[0] < -yovershoot[1]:
            yc += yovershoot[0]
        elif yovershoot[1] > 0 and yovershoot[1] < -yovershoot[0]:
            yc -= yovershoot[1]
        if not (any([xlim[0] > x or x > xlim[1] for x in xc]) or
                any([ylim[0] > y or y > ylim[1] for y in yc])):  
            self.corners = xc, yc
    

    @property
    def _handles_artists(self):
        return (*self._center_handle.artists, *self._corner_handles.artists,
                *self._edge_handles.artists, *self._shear_handles.artists)

    @property
    def _rect_bbox(self):
        return self._selection_artist.get_bbox().bounds

    @property
    def corners(self):
        """
        Corners of rectangle in data coordinates from lower left,
        moving anti-clockwise.
        """
        return list(zip(*self._selection_artist.get_xy()[:4]))

        # return self._selection_artist.get_xy()[:4].T.copy()
        # I can't figure out why this doesn't work. It acts as if passed by reference, 
        # despite the copy().
        # return np.array(list(zip(*self._selection_artist.get_xy()[:4])))
        # doesn't work either

    @corners.setter
    def corners(self, corners):
        # Update displayed shape
        self._draw_shape(corners)
        if self._interactive:
            # Update displayed handles
            self._corner_handles.set_data(*self.corners)
            self._edge_handles.set_data(*self.edge_centers)
            x, y = self.center
            self._center_handle.set_data([x], [y])
            self._shear_handles.set_data(*self.shear_points)
        self.set_visible(self._visible)
        self.update()

    @property
    def edge_centers(self):
        """
        Midpoint of rectangle edges in data coordinates from left,
        moving anti-clockwise.
        """
        xc, yc = self.corners
        xe = [(xc[i-1] + xc[i]) / 2 for i in range(len(xc))]
        ye = [(yc[i-1] + yc[i]) / 2 for i in range(len(yc))]
        return xe, ye
    
    @property
    def shear_points(self):
        """
        Points one quarter along each edge in data coordinates from left,
        moving anti-clockwise.
        """
        xc, yc = self.corners
        xs = [(xc[i-1] * 3 + xc[i]) / 4 for i in range(len(xc))]
        ys = [(yc[i-1] * 3 + yc[i]) / 4 for i in range(len(yc))]
        return xs, ys

    @property
    def center(self):
        """Center of bounding box in data coordinates."""
        xc, yc = self.corners
        xmin, xmax, ymin, ymax = np.min(xc), np.max(xc), np.min(yc), np.max(yc)
        return (xmin + xmax) / 2, (ymin + ymax) / 2

    def _draw_shape(self, corners):
        xc, yc = corners
        xlim = sorted(self.ax.get_xlim())
        ylim = sorted(self.ax.get_ylim())
        xc_clipped = [min(max(x, xlim[0]), xlim[1]) for x in xc]
        yc_clipped = [min(max(y, ylim[0]), ylim[1]) for y in yc]
        verts = list(zip(xc_clipped, yc_clipped)) + [(xc_clipped[0], yc_clipped[0])]
        self._selection_artist.set_xy(verts)

    def _set_active_handle(self, event):
        """Set active handle based on the location of the mouse event."""
        # Note: event.xdata/ydata in data coordinates, event.x/y in pixels
        c_idx, c_dist = self._corner_handles.closest(event.x, event.y)
        e_idx, e_dist = self._edge_handles.closest(event.x, event.y)
        s_idx, s_dist = self._shear_handles.closest(event.x, event.y)
        m_idx, m_dist = self._center_handle.closest(event.x, event.y)

        if 'move' in self._state:
            self._active_handle = 'C'
        # Set active handle as closest handle, if mouse click is close enough.
        elif m_dist < self.grab_range * 2:
            # Prioritise center handle over other handles
            self._active_handle = 'C'
        elif (c_dist > self.grab_range and e_dist > self.grab_range and 
              s_dist > self.grab_range):
            # Not close to any handles
            if self.drag_from_anywhere and self._contains(event):
                # Check if we've clicked inside the region
                self._active_handle = 'C'
            else:
                self._active_handle = None
                return
        elif c_dist < e_dist and c_dist < s_dist:
            # Closest to a corner handle
            self._active_handle = self._corner_order[c_idx]
        elif e_dist < s_dist:
            # Closest to an edge handle
            self._active_handle = self._edge_order[e_idx]
        else:
            # Closest to a shear handle
            self._active_handle = self._shear_point_order[s_idx]