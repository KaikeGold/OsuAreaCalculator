from CustomTkinterMessagebox import CTkMessagebox
import areacalculator
import keyboard
import webbrowser
import base64
import tempfile
import os
import customtkinter as ctk
# Add icon as base64 string

class TabletAreaGUI:
    """GUI for tablet area calculator application"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("OsuAreaCalculator")
        self.root.geometry("400x420")
        self.root.resizable(False,False)
        self.tracking = False
        self.setup_gui()
        self.setup_bindings()

        # Create temp file for icon
        icon_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ico')
        icon_file.write(base64.b64decode(areacalculator.ICON))
        icon_file.close()
            
        # Set window icon
        self.root.iconbitmap(icon_file.name)
            
        # Clean up temp file
        os.unlink(icon_file.name)

    def setup_bindings(self):
        """Setup keyboard shortcuts"""
        keyboard.on_press_key('f5', lambda _: self.start_tracking())
        keyboard.on_press_key('f6', lambda _: self.stop_tracking())
        
    def setup_gui(self):
        """Initialize GUI components"""
        # Main container
        container = ctk.CTkFrame(self.root)
        container.pack(fill=ctk.BOTH, expand=True)

        # Dimensions Frame
        dim_frame = ctk.CTkFrame(container)
        dim_frame.pack(fill=ctk.X, padx=10, pady=10)
        dim_frame.configure(fg_color="#333333")

        dim_label = ctk.CTkLabel(dim_frame, text="Tablet Dimensions", font=("Arial", 14, "bold"))
        dim_label.pack(anchor='w', padx=5,)

        # Grid layout for dimensions
        width_frame = ctk.CTkFrame(dim_frame)
        width_frame.configure(fg_color="#333333")
        width_frame.pack(fill=ctk.X, padx=5, pady=5)
        width_label = ctk.CTkLabel(width_frame, text="Width (mm): ", font=("Arial", 12, "bold"))
        width_label.pack(side=ctk.LEFT, padx=5)
        self.width_entry = ctk.CTkEntry(width_frame)
        self.width_entry.pack(side=ctk.LEFT)
        def on_width_enter(event):
            self.height_entry.focus()
        self.width_entry.bind('<Return>', on_width_enter)

        height_frame = ctk.CTkFrame(dim_frame)
        height_frame.configure(fg_color="#333333")
        height_frame.pack(fill=ctk.X, padx=5, pady=5)
        height_label = ctk.CTkLabel(height_frame, text="Height (mm):", font=("Arial", 12, "bold"))
        height_label.pack(side=ctk.LEFT, padx=5)
        self.height_entry = ctk.CTkEntry(height_frame)
        self.height_entry.pack(side=ctk.LEFT)
        def on_height_enter(event):
            self.set_dimensions()
        self.height_entry.bind('<Return>', on_height_enter)

        # Status
        self.status_label = ctk.CTkLabel(container, text="Enter your tablet dimensions and click Set.\n" "\n" "You need to provide the full dimensions of your tablet's active area.", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=10, padx=10)
        
        # Buttons
        btn_frame = ctk.CTkFrame(container)
        btn_frame.pack(pady=10)
        btn_frame.configure(fg_color="#2B2B2B")
        self.set_btn = ctk.CTkButton(btn_frame, text="Set", font=("Arial", 14, "bold"),
                                 command=self.set_dimensions, fg_color="#FF7EB8")
        self.set_btn.pack(side=ctk.LEFT, padx=5)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="Start (F5)", font=("Arial", 14, "bold"), 
                                   command=self.start_tracking,
                                   state=ctk.DISABLED, fg_color="#FF7EB8")
        self.start_btn.pack(side=ctk.LEFT, padx=5)
        
        # Instructions
        self.show_instructions(container)
        
        # Credits
        self.my_credits(container)
    
    def create_entry(self, parent, label, row):
        """Create labeled entry field"""
        label_widget = ctk.CTkLabel(parent, text=label)
        label_widget.grid(row=row, column=0, padx=5, pady=5)
        entry = ctk.CTkEntry(parent)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry
    
    def show_instructions(self, parent):
        """Display usage instructions"""
        instructions = (
            "1. Enter tablet dimensions\n"
            "2. Click Set buttom\n"
            "3. Set your tablet to full area\n"
            "4. Press F5 to start tracking\n"
            "5. Press F6 to stop and show results\n"
            "\n"
            "YOUR GAME NEEDS TO BE IN BORDERLESS FULLSCREEN TO WORK\n" 
        )
        instructions_label = ctk.CTkLabel(parent, text=instructions, justify=ctk.LEFT, wraplength=380, anchor='n', font=("Arial", 12, "bold"))
        instructions_label.pack(pady=10, padx=10)
    
    def my_credits(self, parent):
        """Display credits with clickable link"""
        credits = ctk.CTkLabel(parent, text="Made by KeepGrindingOsu", justify=ctk.LEFT, font=("Helvetica", 10, "bold"), text_color="#FF8EE6", cursor="hand2")
        credits.pack(pady=1)
        credits.bind("<Button-1>", lambda e: self.open_link("https://x.com/KeepGrindingOsu"))

    def open_link(self, url):
        """Open a web link in the default browser"""
        webbrowser.open_new(url)

    def set_dimensions(self):
        """Set tablet dimensions and enable tracking"""
        try:
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())

            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive")
                
            if areacalculator.set_tablet_dimensions(width, height):
                self.status_label.configure(text="Dimensions set. Press F5 to start")
                self.start_btn.configure(state=ctk.NORMAL)
            else:
                raise RuntimeError("Failed to set dimensions")
                
        except ValueError as e:
            CTkMessagebox.messagebox("Error", f"Invalid dimensions: You should put numbers there xD")
        except Exception as e:
            CTkMessagebox.messagebox("Error", f"Unexpected error: {e}")
    
    def start_tracking(self):
        """Start tracking cursor movement"""
        if not self.tracking:
            self.tracking = True
            self.status_label.configure(text="Tracking... Press F6 to stop")
            self.root.iconify()
            areacalculator.track_cursor_movement()
    
    def stop_tracking(self):
        """Stop tracking and show results"""
        if self.tracking:
            self.tracking = False
            self.status_label.configure(text="Tracking stopped. Showing results...")
            self.root.deiconify()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TabletAreaGUI()
    app.run()