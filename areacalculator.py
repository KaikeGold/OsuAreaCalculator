import pyautogui  # Used for getting the current cursor position
from screeninfo import get_monitors  # Fetches monitor information like resolution and dimensions
import ctypes  # Provides access to Windows API for screen dimensions
import keyboard  # Used for detecting key presses
from ahk import AHK  # Interface for interacting with AutoHotkey scripts
import subprocess  # Enables running external processes
import psutil  # Used for system and process utilities
import matplotlib.pyplot as plt  # For plotting cursor movement
from matplotlib.widgets import RectangleSelector  # Allows interactive area selection in plots
import tkinter as tk  # GUI library for creating input forms
from tkinter import ttk  # Themed widgets for tkinter
import tempfile  # For creating temporary files
import os  # Provides utilities for interacting with the operating system
import threading  # Used for running tasks in parallel
import time  # For adding delays

# Initialize AutoHotkey interface
ahk = AHK()
# Retrieve screen dimensions using Windows API
user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)  # Screen width in pixels
SCREEN_HEIGHT = user32.GetSystemMetrics(1)  # Screen height in pixels
# Global variables for tablet dimensions in millimeters
TABLET_WIDTH_MM = 0
TABLET_HEIGHT_MM = 0

# AutoHotkey script to hide the system cursor
HIDE_CURSOR_SCRIPT = '''
#NoEnv
#Persistent
SetWorkingDir %A_ScriptDir%

if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

VarSetCapacity(AndMask, 128, 0xFF)
VarSetCapacity(XorMask, 128, 0)

CursorIDs := [32512, 32650, 32515, 32649, 32651, 32513, 32648, 32646, 32643, 32645, 32642, 32644, 32516, 32514]

Loop % CursorIDs.Length()
{
    CursorID := CursorIDs[A_Index]
    CursorHandle := DllCall("CreateCursor", "Ptr", 0, "Int", 0, "Int", 0, "Int", 32, "Int", 32, "Ptr", &AndMask, "Ptr", &XorMask)
    DllCall("SetSystemCursor", "Ptr", CursorHandle, "Int", CursorID)
}
ExitApp
'''

# AutoHotkey script to restore the system cursor
SHOW_CURSOR_SCRIPT = '''
#NoEnv
#Persistent
SetWorkingDir %A_ScriptDir%

DllCall("SystemParametersInfo", "UInt", 0x57, "UInt", 0, "Ptr", 0, "UInt", 0)
ExitApp
'''

def hide_cursor():
    """Hides the system cursor using an AutoHotkey script."""
    try:
        # Create temporary script file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ahk') as tf:
            tf.write(HIDE_CURSOR_SCRIPT.encode())
            temp_script = tf.name
        
        # Execute script
        subprocess.Popen([r"C:\Program Files\AutoHotkey\AutoHotkey.exe", temp_script])
        
        # Clean up temp file after a short delay
        def cleanup():
            time.sleep(1)
            try:
                os.unlink(temp_script)
            except:
                pass
        threading.Thread(target=cleanup).start()
        
        return True
    except Exception as e:
        print(f"Error hiding cursor: {e}")
        return False

def show_cursor():
    """Restores the system cursor using an AutoHotkey script."""
    try:
        # Create temporary script file 
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ahk') as tf:
            tf.write(SHOW_CURSOR_SCRIPT.encode())
            temp_script = tf.name
        
        # Execute script
        subprocess.Popen([r"C:\Program Files\AutoHotkey\AutoHotkey.exe", temp_script])
        
        # Clean up temp file after a short delay
        def cleanup():
            time.sleep(1)
            try:
                os.unlink(temp_script)
            except:
                pass
        threading.Thread(target=cleanup).start()
        
        return True
    except Exception as e:
        print(f"Error showing cursor: {e}")
        return False

def get_monitor_info():
    """Retrieves and prints information about all connected monitors."""
    monitors = get_monitors()
    print("Detected Monitors:")
    for i, m in enumerate(monitors):
        print(f"Monitor {i}: {m.width}x{m.height} at ({m.x}, {m.y})")
    return monitors

def get_cursor_position():
    """Prints the current cursor position in screen coordinates."""
    x, y = pyautogui.position()
    print(f"Current cursor position: ({x}, {y})")

def set_tablet_dimensions(width=0, height=0):
    """Sets the tablet dimensions in millimeters."""
    try:
        global TABLET_WIDTH_MM, TABLET_HEIGHT_MM
        TABLET_WIDTH_MM = float(width)
        TABLET_HEIGHT_MM = float(height)
        print(f"Tablet dimensions: {TABLET_WIDTH_MM}x{TABLET_HEIGHT_MM}mm")
        return True
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return False

def cursor_to_mm(x, y):
    """Converts cursor screen coordinates to tablet millimeter dimensions."""
    mm_x = (x / SCREEN_WIDTH) * TABLET_WIDTH_MM
    mm_y = (y / SCREEN_HEIGHT) * TABLET_HEIGHT_MM
    return mm_x, mm_y

def plot_cursor_positions(positions_x, positions_y, measurements):
    """Plots the cursor movement path and allows measuring selected areas."""
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.plot(positions_x, positions_y, 'b-', alpha=0.5, linewidth=1)
    
    def on_select(eclick, erelease):
        """Handles area selection on the plot and displays measurement details."""
        x1, y1 = float(eclick.xdata), float(eclick.ydata)
        x2, y2 = float(erelease.xdata), float(erelease.ydata)
        
        width = abs(x2 - x1) * 1.3333
        height = abs(y2 - y1)
        center_x = min(x1, x2) + abs(x2 - x1) / 2
        center_y = min(y1, y2) + abs(y2 - y1) / 2
        
        selection_text = (
            f"Selected Area:\n"
            f"Width (4:3): {width:.1f}mm\n"
            f"Height: {height:.1f}mm\n"
            f"Center: X={center_x:.1f}mm, Y={center_y:.1f}mm"
        )
        
        if hasattr(ax, 'selection_text'):
            ax.selection_text.remove()
        ax.selection_text = ax.text(0.02, 0.98, selection_text,
            transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.8))
        plt.draw()
    
    rect_selector = RectangleSelector(
        ax, on_select,
        useblit=True,
        button=[1],
        minspanx=5,
        minspany=5,
        spancoords='pixels',
        interactive=True
    )
    
    plt.xlim(min(positions_x) - 5, max(positions_x) + 50)
    plt.ylim(min(positions_y) - 5, max(positions_y) + 5)
    plt.text(max(positions_x) + 5, max(positions_y), 
             measurements,
             bbox=dict(
                 facecolor='white',
                 alpha=0.9,
                 edgecolor='gray',
                 boxstyle='round,pad=1'
             ),
             fontsize=9,
             family='monospace',
             verticalalignment='top')
   
    plt.title('Cursor Movement Path (Click and drag to measure area)')
    plt.xlabel('X Position (mm)')
    plt.ylabel('Y Position (mm)')
    plt.grid(True)
    fig.canvas.manager.set_window_title('Your Area')
    plt.show()

def track_cursor_movement():
    """Tracks the cursor movement in real-time and calculates the tablet area used."""
    tracking = True
    last_x = last_y = 0
    max_mm_x = max_mm_y = float('-inf')
    min_mm_x = min_mm_y = float('inf')
    positions_x = []
    positions_y = []
    
    # Display monitor information
    get_monitor_info()
    # Hide the cursor during tracking
    hide_cursor()
    print("Tracking started! Press F6 to stop")

    try:
        while tracking:
            if keyboard.is_pressed('F6'):
                # Stop tracking when F6 is pressed
                tracking = False
                width = (max_mm_x - min_mm_x) * 1.3333
                height = max_mm_y - min_mm_y
                center_x = min_mm_x + (max_mm_x - min_mm_x) / 2
                center_y = min_mm_y + (max_mm_y - min_mm_y) / 2
                measurements = (
                    f"Final Measurements:\n"
                    f"Width (4:3): {width:.1f}mm\n"
                    f"Height: {height:.1f}mm\n"
                    f"Center: X={center_x:.1f}mm, Y={center_y:.1f}mm\n"
                    f"Min: X={min_mm_x:.1f}mm, Y={min_mm_y:.1f}mm\n"
                    f"Max: X={max_mm_x:.1f}mm, Y={max_mm_y:.1f}mm"
                )
                # Restore the cursor visibility
                show_cursor()
                # Plot the cursor positions
                plot_cursor_positions(positions_x, positions_y, measurements)
                break

            x, y = pyautogui.position()
            if (x != last_x) or (y != last_y):
                # Convert screen coordinates to tablet dimensions
                mm_x, mm_y = cursor_to_mm(x, y)
                positions_x.append(mm_x)
                positions_y.append(mm_y)

                max_mm_x = max(max_mm_x, mm_x)
                max_mm_y = max(max_mm_y, mm_y)
                min_mm_x = min(min_mm_x, mm_x)
                min_mm_y = min(min_mm_y, mm_y)

                width = (max_mm_x - min_mm_x) * 1.3333
                height = max_mm_y - min_mm_y
                center_x = min_mm_x + (max_mm_x - min_mm_x) / 2
                center_y = min_mm_y + (max_mm_y - min_mm_y) / 2

                # Print real-time tracking information
                print(f"Screen: X={x}, Y={y} | "
                      f"Tablet: X={mm_x:.1f}mm, Y={mm_y:.1f}mm | "
                      f"Min: X={min_mm_x:.1f}mm, Y={min_mm_y:.1f}mm | "
                      f"Max: X={max_mm_x:.1f}mm, Y={max_mm_y:.1f}mm | "
                      f"Center: X={center_x:.1f}mm, Y={center_y:.1f}mm | "
                      f"Area: {width:.1f}x{height:.1f}mm  ",
                      end='\r')

                last_x, last_y = x, y

        print(f"\n\nTablet area used:")
        print(f"Minimum coordinates: X={min_mm_x:.1f}mm, Y={min_mm_y:.1f}mm")
        print(f"Maximum coordinates: X={max_mm_x:.1f}mm, Y={max_mm_y:.1f}mm")
        print(f"Center coordinates: X={center_x:.1f}mm, Y={center_y:.1f}mm")
    except KeyboardInterrupt:
        print("\nTracking stopped by user")

if __name__ == "__main__":
    # Set tablet dimensions before starting tracking
    set_tablet_dimensions()
    track_cursor_movement()
