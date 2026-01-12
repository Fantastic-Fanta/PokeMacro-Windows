import tkinter as tk
from tkinter import ttk, messagebox
import yaml
from pathlib import Path
from typing import Dict, Tuple, Any
import sys
import re
import platform

# Windows-specific imports for transparency and click-through
if platform.system() == 'Windows':
    try:
        import ctypes
        from ctypes import wintypes
        HAS_WIN32 = True
    except ImportError:
        HAS_WIN32 = False
else:
    HAS_WIN32 = False

class DraggableDot:
    """A draggable green dot widget"""
    def __init__(self, canvas, x, y, label, radius=10):
        self.label = label
        self.radius = radius
        self.x = x
        self.y = y
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.dragging = False
        self.canvas = canvas
        # Get screen dimensions from canvas if stored, otherwise use defaults
        self.screen_width = getattr(canvas, 'screen_width', canvas.winfo_screenwidth() if hasattr(canvas, 'winfo_screenwidth') else 1920)
        self.screen_height = getattr(canvas, 'screen_height', canvas.winfo_screenheight() if hasattr(canvas, 'winfo_screenheight') else 1080)
        
        # Draw a cross/X instead of a dot
        # Use blue color and slightly smaller size
        cross_size = radius - 2  # Make it slightly smaller
        line_width = 3
        
        # Draw the cross - two diagonal lines
        self.cross_line1 = self.canvas.create_line(
            x - cross_size, y - cross_size,
            x + cross_size, y + cross_size,
            fill='#0088FF', width=line_width,
            tags=('dot', label, 'cross')
        )
        
        self.cross_line2 = self.canvas.create_line(
            x - cross_size, y + cross_size,
            x + cross_size, y - cross_size,
            fill='#0088FF', width=line_width,
            tags=('dot', label, 'cross')
        )
        
        # Draw a white outline circle around the cross for better visibility
        self.outline_id = self.canvas.create_oval(
            x - radius - 1, y - radius - 1,
            x + radius + 1, y + radius + 1,
            outline='white', width=1, fill='',
            tags=('dot', label, 'outline')
        )
        
        # Draw label text with white background for visibility
        self.text_id = self.canvas.create_text(
            x, y - radius - 18,
            text=label, fill='white', font=('Arial', 10, 'bold'),
            tags=('label', label)
        )
        
        # Draw text background for better visibility
        bbox = self.canvas.bbox(self.text_id)
        if bbox:
            self.text_bg_id = self.canvas.create_rectangle(
                bbox[0] - 2, bbox[1] - 2,
                bbox[2] + 2, bbox[3] + 2,
                fill='black', outline='#0088FF', width=1,
                tags=('label', label, 'textbg')
            )
            # Move text to front
            self.canvas.tag_raise(self.text_id)
        
        # Store cross line IDs for position updates
        self.cross_ids = [self.cross_line1, self.cross_line2]
        
        # Bind events to the cross lines, outline, label, and text background
        items_to_bind = [self.cross_line1, self.cross_line2, self.text_id]
        if hasattr(self, 'outline_id'):
            items_to_bind.append(self.outline_id)
        if hasattr(self, 'text_bg_id'):
            items_to_bind.append(self.text_bg_id)
            
        for item_id in items_to_bind:
            if item_id:  # Make sure it's not None
                self.canvas.tag_bind(item_id, '<Button-1>', self.on_click)
                self.canvas.tag_bind(item_id, '<B1-Motion>', self.on_drag)
                self.canvas.tag_bind(item_id, '<ButtonRelease-1>', self.on_release)
    
    def on_click(self, event):
        self.dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        # Bring cross to front when clicked
        if hasattr(self, 'cross_ids'):
            for cross_id in self.cross_ids:
                self.canvas.tag_raise(cross_id)
        if hasattr(self, 'outline_id'):
            self.canvas.tag_raise(self.outline_id)
        self.canvas.tag_raise(self.text_id)
        if hasattr(self, 'text_bg_id'):
            self.canvas.tag_raise(self.text_bg_id)
            self.canvas.tag_raise(self.text_id)
    
    def on_drag(self, event):
        if self.dragging:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            
            self.x += dx
            self.y += dy
            
            # Update cross position
            cross_size = self.radius - 2
            if hasattr(self, 'cross_ids') and len(self.cross_ids) >= 2:
                # Update first diagonal line (top-left to bottom-right)
                self.canvas.coords(self.cross_ids[0],
                    self.x - cross_size, self.y - cross_size,
                    self.x + cross_size, self.y + cross_size
                )
                # Update second diagonal line (bottom-left to top-right)
                self.canvas.coords(self.cross_ids[1],
                    self.x - cross_size, self.y + cross_size,
                    self.x + cross_size, self.y - cross_size
                )
            
            # Update outline position
            if hasattr(self, 'outline_id'):
                self.canvas.coords(self.outline_id,
                    self.x - self.radius - 1, self.y - self.radius - 1,
                    self.x + self.radius + 1, self.y + self.radius + 1
                )
            
            # Update label position
            self.canvas.coords(self.text_id,
                self.x, self.y - self.radius - 18
            )
            
            # Update text background position
            if hasattr(self, 'text_bg_id'):
                bbox = self.canvas.bbox(self.text_id)
                if bbox:
                    self.canvas.coords(self.text_bg_id,
                        bbox[0] - 2, bbox[1] - 2,
                        bbox[2] + 2, bbox[3] + 2
                    )
                    self.canvas.tag_raise(self.text_id)
            
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            
            # Ensure position stays within screen bounds
            canvas_width = self.canvas.winfo_width() or self.screen_width
            canvas_height = self.canvas.winfo_height() or self.screen_height
            self.x = max(0, min(self.x, canvas_width))
            self.y = max(0, min(self.y, canvas_height))
    
    def on_release(self, event):
        self.dragging = False
        # Notify position changed callback if it exists
        if hasattr(self, 'on_position_changed'):
            self.on_position_changed()
    
    def get_position(self) -> Tuple[int, int]:
        """Get current position as (x, y) tuple"""
        return (int(self.x), int(self.y))
    
    def set_position(self, x: int, y: int):
        """Set position programmatically"""
        self.x = x
        self.y = y
        
        # Update cross position
        cross_size = self.radius - 2
        if hasattr(self, 'cross_ids') and len(self.cross_ids) >= 2:
            # Update first diagonal line (top-left to bottom-right)
            self.canvas.coords(self.cross_ids[0],
                x - cross_size, y - cross_size,
                x + cross_size, y + cross_size
            )
            # Update second diagonal line (bottom-left to top-right)
            self.canvas.coords(self.cross_ids[1],
                x - cross_size, y + cross_size,
                x + cross_size, y - cross_size
            )
        
        if hasattr(self, 'outline_id'):
            self.canvas.coords(self.outline_id,
                x - self.radius - 1, y - self.radius - 1,
                x + self.radius + 1, y + self.radius + 1
            )
        self.canvas.coords(self.text_id,
            x, y - self.radius - 18
        )
        if hasattr(self, 'text_bg_id'):
            bbox = self.canvas.bbox(self.text_id)
            if bbox:
                self.canvas.coords(self.text_bg_id,
                    bbox[0] - 2, bbox[1] - 2,
                    bbox[2] + 2, bbox[3] + 2
                )
                self.canvas.tag_raise(self.text_id)


class AdvancedConfigTool:
    """Advanced configuration tool with draggable position dots"""
    
    def __init__(self, config_path: str = "configs.yaml"):
        self.config_path = Path(config_path)
        self.original_config = None
        self.current_config = None
        self.dots: Dict[str, DraggableDot] = {}
        self.chat_window_rect_id = None  # ID for the chat window rectangle
        
        # Load configuration first
        self.load_config()
        
        # Create main window - fullscreen transparent overlay
        self.root = tk.Tk()
        self.root.title("Advanced Configuration Tool - Overlay")
        
        # Get screen resolution
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.attributes('-topmost', True)  # Always on top
        
        # Use a transparent color for click-through (magenta)
        self.transparent_color = '#ff00ff'
        self.root.configure(bg=self.transparent_color)
        
        # Set transparent color (Windows only)
        # Don't use alpha - use transparentcolor so only the background is transparent
        # This keeps the dots visible while making the background transparent
        if platform.system() == 'Windows':
            try:
                # Set transparent color - only this color will be transparent
                # The green dots will remain fully visible
                self.root.wm_attributes('-transparentcolor', self.transparent_color)
            except:
                # Fallback: use very low alpha (but this makes dots invisible too)
                # Better to not use alpha at all
                pass
        
        # Create canvas - fullscreen, transparent background
        self.canvas = tk.Canvas(
            self.root,
            bg=self.transparent_color,
            highlightthickness=0,
            width=self.screen_width,
            height=self.screen_height
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Store screen dimensions in canvas for dot access
        self.canvas.screen_width = self.screen_width
        self.canvas.screen_height = self.screen_height
        
        # Create floating control panel (small, always visible)
        self.create_control_panel()
        
        # Configure style
        self.setup_style()
        
        # Create dots for all positions (after canvas is ready)
        self.root.after(150, self.create_dots)
    
    def create_control_panel(self):
        """Create a floating control panel"""
        # Create a small floating window for controls
        self.control_window = tk.Toplevel(self.root)
        self.control_window.overrideredirect(True)
        self.control_window.attributes('-topmost', True)
        self.control_window.attributes('-alpha', 0.9)
        self.control_window.geometry("200x100+10+10")
        self.control_window.configure(bg='#2a2a2a')
        
        # Make it draggable
        def start_drag(event):
            self.control_window.start_x = event.x
            self.control_window.start_y = event.y
        
        def on_drag(event):
            x = self.control_window.winfo_x() + event.x - self.control_window.start_x
            y = self.control_window.winfo_y() + event.y - self.control_window.start_y
            self.control_window.geometry(f"+{x}+{y}")
        
        self.control_window.bind('<Button-1>', start_drag)
        self.control_window.bind('<B1-Motion>', on_drag)
        
        # Title bar
        title_frame = tk.Frame(self.control_window, bg='#1a1a1a', height=25)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(
            title_frame,
            text="Config Tool",
            bg='#1a1a1a',
            fg='white',
            font=('Arial', 9, 'bold')
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = tk.Button(
            title_frame,
            text="×",
            bg='#1a1a1a',
            fg='white',
            font=('Arial', 12, 'bold'),
            border=0,
            command=self.root.quit,
            width=3
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Buttons frame
        button_frame = tk.Frame(self.control_window, bg='#2a2a2a')
        button_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.save_button = tk.Button(
            button_frame,
            text="Save",
            command=self.save_config,
            bg='#0088FF',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.save_button.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        self.save_button.bind('<Enter>', lambda e: self.save_button.config(bg='#00AAFF'))
        self.save_button.bind('<Leave>', lambda e: self.save_button.config(bg='#0088FF'))
        
        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_positions,
            bg='#666666',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.reset_button.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        self.reset_button.bind('<Enter>', lambda e: self.reset_button.config(bg='#777777'))
        self.reset_button.bind('<Leave>', lambda e: self.reset_button.config(bg='#666666'))
    
    def update_chat_window_rectangle(self):
        """Update the chat window rectangle visualization"""
        # Get the two corner positions
        left_corner_dot = self.dots.get('ChatWindow.LeftCorner')
        right_corner_dot = self.dots.get('ChatWindow.RightCorner')
        
        if not left_corner_dot or not right_corner_dot:
            return
        
        # Get positions
        left_x, left_y = left_corner_dot.get_position()
        right_x, right_y = right_corner_dot.get_position()
        
        # Remove old rectangle if it exists
        if self.chat_window_rect_id:
            self.canvas.delete(self.chat_window_rect_id)
        
        # Create new rectangle with semi-transparent blue fill and outline
        # Use the two corners to define the rectangle
        # Ensure proper rectangle coordinates (left < right, top < bottom)
        x1 = min(left_x, right_x)
        y1 = min(left_y, right_y)
        x2 = max(left_x, right_x)
        y2 = max(left_y, right_y)
        
        self.chat_window_rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill='#0088FF',  # Blue fill
            outline='#00AAFF',  # Lighter blue outline
            width=2,
            stipple='gray50',  # Make it semi-transparent
            tags=('chat_window_rect',)
        )
        
        # Keep rectangle behind the crosses
        self.canvas.tag_lower(self.chat_window_rect_id)
    
    def setup_style(self):
        """Configure ttk styles"""
        pass  # Not needed for overlay mode
    
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            if not self.config_path.exists():
                messagebox.showerror("Error", f"Configuration file not found: {self.config_path}")
                sys.exit(1)
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.original_config = yaml.safe_load(f)
            
            # Deep copy to ensure we have a separate instance
            import copy
            self.current_config = copy.deepcopy(self.original_config)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
            sys.exit(1)
    
    
    def create_dots(self):
        """Create draggable dots for all position fields"""
        print(f"Creating dots on canvas size: {self.screen_width}x{self.screen_height}")
        
        # Create dots for Positions section
        positions = self.current_config.get('Positions', {})
        print(f"Found {len(positions)} positions")
        for key, value in positions.items():
            if isinstance(value, list) and len(value) >= 2:
                x, y = int(value[0]), int(value[1])
                # Ensure coordinates are within screen bounds
                x = max(0, min(x, self.screen_width))
                y = max(0, min(y, self.screen_height))
                print(f"Creating cross for {key} at ({x}, {y})")
                # Create cross directly on the canvas with slightly smaller radius
                dot = DraggableDot(self.canvas, x, y, key, radius=10)
                self.dots[key] = dot
        
        # Create dots for ChatWindow section
        chat_window = self.current_config.get('ChatWindow', {})
        print(f"Found {len(chat_window)} chat window positions")
        for key, value in chat_window.items():
            if isinstance(value, list) and len(value) >= 2:
                x, y = int(value[0]), int(value[1])
                # Ensure coordinates are within screen bounds
                x = max(0, min(x, self.screen_width))
                y = max(0, min(y, self.screen_height))
                label = f"ChatWindow.{key}"
                print(f"Creating cross for {label} at ({x}, {y})")
                dot = DraggableDot(self.canvas, x, y, label, radius=10)
                self.dots[label] = dot
                # Store reference to update rectangle when moved (only for chat window corners)
                if 'ChatWindow' in label:
                    # Create a closure to capture the tool instance
                    def make_callback():
                        tool_instance = self
                        return lambda: tool_instance.update_chat_window_rectangle()
                    dot.on_position_changed = make_callback()
        
        # Create the chat window rectangle visualization
        self.update_chat_window_rectangle()
        dot.on_position_changed = lambda: self.update_chat_window_rectangle()
        
        # Create the chat window rectangle visualization
        self.update_chat_window_rectangle()
        
        print(f"Total crosses created: {len(self.dots)}")
        # Force canvas update and bring crosses to front
        self.canvas.update_idletasks()
        for dot in self.dots.values():
            if hasattr(dot, 'cross_ids'):
                for cross_id in dot.cross_ids:
                    self.canvas.tag_raise(cross_id)
            if hasattr(dot, 'outline_id'):
                self.canvas.tag_raise(dot.outline_id)
            self.canvas.tag_raise(dot.text_id)
            if hasattr(dot, 'text_bg_id'):
                self.canvas.tag_raise(dot.text_bg_id)
                self.canvas.tag_raise(dot.text_id)  # Text on top of background
    
    def save_config(self):
        """Save current positions to config file"""
        try:
            # Update Positions section
            positions = self.current_config.get('Positions', {})
            for key, dot in self.dots.items():
                if key.startswith('ChatWindow.'):
                    continue  # Handle separately
                if key in positions:
                    x, y = dot.get_position()
                    positions[key] = [x, y]
            
            # Update ChatWindow section
            chat_window = self.current_config.get('ChatWindow', {})
            for key, dot in self.dots.items():
                if key.startswith('ChatWindow.'):
                    chat_key = key.replace('ChatWindow.', '')
                    if chat_key in chat_window:
                        x, y = dot.get_position()
                        chat_window[chat_key] = [x, y]
            
            # Read original file to preserve comments and structure
            with open(self.config_path, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()
            
            # Update positions in the file content
            output_lines = []
            i = 0
            while i < len(original_lines):
                line = original_lines[i]
                
                # Check if this is a position line
                position_updated = False
                for key, dot in self.dots.items():
                    if key.startswith('ChatWindow.'):
                        chat_key = key.replace('ChatWindow.', '')
                        pattern = rf'^\s*{re.escape(chat_key)}:\s*\[.*?\]'
                        if re.match(pattern, line):
                            x, y = dot.get_position()
                            # Preserve indentation and comments
                            indent = len(line) - len(line.lstrip())
                            comment = ''
                            if '#' in line:
                                comment = ' ' + line.split('#', 1)[1].rstrip()
                            output_lines.append(f"{' ' * indent}{chat_key}: [{x}, {y}]{comment}\n")
                            position_updated = True
                            break
                    else:
                        pattern = rf'^\s*{re.escape(key)}:\s*\[.*?\]'
                        if re.match(pattern, line):
                            x, y = dot.get_position()
                            # Preserve indentation and comments
                            indent = len(line) - len(line.lstrip())
                            comment = ''
                            if '#' in line:
                                comment = ' ' + line.split('#', 1)[1].rstrip()
                            output_lines.append(f"{' ' * indent}{key}: [{x}, {y}]{comment}\n")
                            position_updated = True
                            break
                
                if not position_updated:
                    output_lines.append(line)
                
                i += 1
            
            # Write updated content
            with open(self.config_path, 'w', encoding='utf-8') as f:
                f.writelines(output_lines)
            
            # Update original config
            import copy
            self.original_config = copy.deepcopy(self.current_config)
            
            messagebox.showinfo("Success", f"Configuration saved to {self.config_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def reset_positions(self):
        """Reset positions to original values"""
        try:
            # Reload original config
            import copy
            self.current_config = copy.deepcopy(self.original_config)
            
            # Reset Positions section
            positions = self.current_config.get('Positions', {})
            for key, dot in self.dots.items():
                if key.startswith('ChatWindow.'):
                    continue
                if key in positions and isinstance(positions[key], list) and len(positions[key]) >= 2:
                    x, y = int(positions[key][0]), int(positions[key][1])
                    dot.set_position(x, y)
            
            # Reset ChatWindow section
            chat_window = self.current_config.get('ChatWindow', {})
            for key, dot in self.dots.items():
                if key.startswith('ChatWindow.'):
                    chat_key = key.replace('ChatWindow.', '')
                    if chat_key in chat_window and isinstance(chat_window[chat_key], list) and len(chat_window[chat_key]) >= 2:
                        x, y = int(chat_window[chat_key][0]), int(chat_window[chat_key][1])
                        dot.set_position(x, y)
            
            messagebox.showinfo("Reset", "Positions reset to original values")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset positions: {str(e)}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Advanced Configuration Tool for PokeMacro')
    parser.add_argument('--config', '-c', default='configs.yaml',
                       help='Path to configuration file (default: configs.yaml)')
    
    args = parser.parse_args()
    
    app = AdvancedConfigTool(args.config)
    app.run()


if __name__ == "__main__":
    main()

