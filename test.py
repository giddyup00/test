import tkinter as tk
import math
import time

def main():
    root = tk.Tk()
    root.title("Spinning Sphere")
    
    # Hide window decorations to make it floating
    root.overrideredirect(True)
    # Keep the window on top of others
    root.attributes('-topmost', True)
    
    # Set black to be the transparent color key for Windows
    root.attributes('-transparentcolor', 'black')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get exact pixel size for 3 inches based on system DPI
    diameter = int(root.winfo_fpixels('3i'))
    radius = diameter // 2
    window_size = diameter + 20 # Add padding so the borders don't clip
    
    cx = window_size // 2
    cy = window_size // 2

    # Center on the desktop screen
    x = (screen_width - window_size) // 2
    y = (screen_height - window_size) // 2
    root.geometry(f'{window_size}x{window_size}+{x}+{y}')

    # Canvas with black background (which will become completely transparent)
    canvas = tk.Canvas(root, width=window_size, height=window_size, bg='black', highlightthickness=0)
    canvas.pack()

    colors = ['red', 'green', 'blue']
    text = "hello there"
    char_spacing = math.radians(12)

    start_time = time.time()

    def update():
        current_time = time.time()
        elapsed = current_time - start_time
        
        # Spin at 1 revolution (2*pi) every 2 seconds -> pi radians per second
        angle = elapsed * math.pi
        
        cycle = int(elapsed / 2.0)
        
        # Cycled indefinitely in the order of red, green, and blue
        color_idx = cycle % 3
        color = colors[color_idx]
        
        canvas.delete('all')
        
        # Draw solid sphere body
        canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=color, outline=color)
        
        # Simple highlight to give it a 3D solid look
        h_radius = radius * 0.4
        canvas.create_oval(cx - radius*0.6, cy - radius*0.6, cx - radius*0.6 + h_radius, cy - radius*0.6 + h_radius, 
                           fill='white', stipple='gray50', outline='')

        # Draw inscribed text horizontally along the equator
        # The text is drawn AFTER the sphere so it appears on top
        for i, char in enumerate(text):
            # Calculate angle for each character.
            char_angle = angle - (i - len(text) / 2.0) * char_spacing
            char_angle = char_angle % (2 * math.pi)
            
            # Check if character is on the front hemisphere (z > 0)
            z = math.sin(char_angle)
            if z > 0:
                char_x = radius * math.cos(char_angle)
                # Scale font slightly based on perspective (further away = smaller)
                scale = 0.8 + 0.2 * z
                font_size = max(10, int(radius / 8 * scale))
                
                canvas.create_text(cx + char_x, cy, text=char, fill='white', 
                                   font=('Consolas', font_size, 'bold'))

        # Schedule next frame update (approx 60 FPS)
        root.after(16, update)

    update()
    
    # Press Escape to close the application safely
    root.bind('<Escape>', lambda e: root.destroy())
    print("Solid spinning sphere running (no blink). Click the sphere and press 'Escape' to exit.")
    
    root.mainloop()

if __name__ == '__main__':
    main()
