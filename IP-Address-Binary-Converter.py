import tkinter as tk
from tkinter import font as tkfont

class IPBinaryConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address Binary Converter")
        
        # Get screen dimensions and set window size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(780, screen_width - 100)
        window_height = min(1225, screen_height - 100)
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configure colors matching web version
        self.bg_gradient = "#E0E7FF"
        self.card_bg = "#FFFFFF"
        self.primary_blue = "#6366F1"
        self.text_dark = "#1F2937"
        self.text_gray = "#6B7280"
        self.inactive_bg = "#E5E7EB"
        self.inactive_text = "#9CA3AF"
        self.section_bg = "#F9FAFB"
        self.highlight_bg = "#EEF2FF"
        
        self.root.configure(bg=self.bg_gradient)
        
        # Store octet entry widgets and values
        self.octet_entries = []
        self.octet_vars = []
        
        # Create main container with shadow effect
        container = tk.Frame(root, bg=self.bg_gradient)
        container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Main card with rounded corners effect
        main_frame = tk.Frame(container, bg=self.card_bg, relief="flat", bd=0)
        main_frame.pack(fill="both", expand=True)
        
        # Add padding inside card
        content_frame = tk.Frame(main_frame, bg=self.card_bg)
        content_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Title
        title_font = tkfont.Font(family="Arial", size=24, weight="bold")
        title = tk.Label(
            content_frame, 
            text="IP Address Binary Converter",
            font=title_font,
            bg=self.card_bg,
            fg=self.text_dark
        )
        title.pack(pady=(0, 8))
        
        # Subtitle
        subtitle_font = tkfont.Font(family="Arial", size=11)
        subtitle = tk.Label(
            content_frame,
            text="Enter an IP address to see its binary representation",
            font=subtitle_font,
            bg=self.card_bg,
            fg=self.text_gray
        )
        subtitle.pack(pady=(0, 30))
        
        # IP Address input section
        input_label_font = tkfont.Font(family="Arial", size=10, weight="bold")
        input_label = tk.Label(
            content_frame,
            text="IP Address (0-255 per octet)",
            font=input_label_font,
            bg=self.card_bg,
            fg=self.text_dark
        )
        input_label.pack(pady=(0, 12))
        
        # IP input frame
        ip_frame = tk.Frame(content_frame, bg=self.card_bg)
        ip_frame.pack(pady=(0, 25))
        
        # Create 4 octet inputs with dots between them
        entry_font = tkfont.Font(family="Courier New", size=18, weight="bold")
        for i in range(4):
            var = tk.StringVar(value="0")
            var.trace_add("write", lambda *args, idx=i: self.validate_octet(idx))
            self.octet_vars.append(var)
            
            entry = tk.Entry(
                ip_frame,
                textvariable=var,
                font=entry_font,
                width=4,
                justify="center",
                relief="solid",
                borderwidth=2,
                highlightthickness=2,
                highlightbackground="#D1D5DB",
                highlightcolor=self.primary_blue
            )
            entry.pack(side="left", padx=6)
            self.octet_entries.append(entry)
            
            if i < 3:
                dot_font = tkfont.Font(family="Arial", size=24, weight="bold")
                dot = tk.Label(
                    ip_frame,
                    text=".",
                    font=dot_font,
                    bg=self.card_bg,
                    fg=self.inactive_text
                )
                dot.pack(side="left", padx=2)
        
        # Scrollable frame for octet displays
        canvas_container = tk.Frame(content_frame, bg=self.card_bg)
        canvas_container.pack(fill="both", expand=True, pady=(0, 20))
        
        # Create canvas
        self.canvas = tk.Canvas(canvas_container, bg=self.card_bg, highlightthickness=0)
        
        # Create scrollbars
        self.v_scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(canvas_container, orient="horizontal", command=self.canvas.xview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.card_bg)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.update_scrollbars()
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.on_canvas_scroll_y, xscrollcommand=self.on_canvas_scroll_x)
        
        # Grid layout for scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        
        # Bind canvas resize
        self.canvas.bind('<Configure>', lambda e: self.update_scrollbars())
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Create 4 octet display sections
        self.octet_displays = []
        for i in range(4):
            display = self.create_octet_display(self.scrollable_frame, i)
            self.octet_displays.append(display)
        
        # Full binary display
        binary_outer = tk.Frame(content_frame, bg=self.highlight_bg, relief="solid", borderwidth=1)
        binary_outer.pack(fill="x")
        
        binary_inner = tk.Frame(binary_outer, bg=self.highlight_bg)
        binary_inner.pack(fill="x", padx=20, pady=15)
        
        binary_label_font = tkfont.Font(family="Arial", size=11, weight="bold")
        binary_label = tk.Label(
            binary_inner,
            text="Complete Binary:",
            font=binary_label_font,
            bg=self.highlight_bg,
            fg=self.text_dark
        )
        binary_label.pack(anchor="w", pady=(0, 8))
        
        binary_value_font = tkfont.Font(family="Courier New", size=14, weight="bold")
        self.full_binary_label = tk.Label(
            binary_inner,
            text="00000000.00000000.00000000.00000000",
            font=binary_value_font,
            bg=self.highlight_bg,
            fg=self.primary_blue
        )
        self.full_binary_label.pack()
        
        # Initial update
        self.update_all_displays()
        
        # Schedule scrollbar check after window is fully rendered
        self.root.after(100, self.update_scrollbars)
    
    def on_canvas_configure(self, event):
        # Just update scrollbars, don't resize the canvas window
        self.update_scrollbars()
    
    def on_canvas_scroll_y(self, first, last):
        # Update vertical scrollbar and hide/show based on need
        self.v_scrollbar.set(first, last)
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.v_scrollbar.grid_remove()
        else:
            self.v_scrollbar.grid()
    
    def on_canvas_scroll_x(self, first, last):
        # Update horizontal scrollbar and hide/show based on need
        self.h_scrollbar.set(first, last)
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.h_scrollbar.grid_remove()
        else:
            self.h_scrollbar.grid()
    
    def update_scrollbars(self):
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Force scrollbar visibility check
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0)
    
    def create_octet_display(self, parent, index):
        # Outer frame with border
        outer_frame = tk.Frame(parent, bg=self.section_bg, relief="solid", borderwidth=2, highlightbackground="#E5E7EB")
        outer_frame.pack(fill="both", expand=True, pady=10)
        
        # Inner frame with padding
        frame = tk.Frame(outer_frame, bg=self.section_bg)
        frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Octet header with value
        header_frame = tk.Frame(frame, bg=self.section_bg)
        header_frame.pack(anchor="w", pady=(0, 15))
        
        header_font = tkfont.Font(family="Arial", size=11)
        header_label = tk.Label(
            header_frame,
            text=f"Octet {index + 1}: ",
            font=header_font,
            bg=self.section_bg,
            fg=self.text_gray
        )
        header_label.pack(side="left")
        
        value_font = tkfont.Font(family="Arial", size=14, weight="bold")
        header_value = tk.Label(
            header_frame,
            text="0",
            font=value_font,
            bg=self.section_bg,
            fg=self.primary_blue
        )
        header_value.pack(side="left")
        
        # Bit values row
        bit_values_frame = tk.Frame(frame, bg=self.section_bg)
        bit_values_frame.pack(fill="x", pady=(0, 8))
        
        bit_values = [128, 64, 32, 16, 8, 4, 2, 1]
        bit_value_font = tkfont.Font(family="Arial", size=9)
        
        for value in bit_values:
            label = tk.Label(
                bit_values_frame,
                text=str(value),
                font=bit_value_font,
                bg=self.section_bg,
                fg=self.text_gray,
                width=6
            )
            label.pack(side="left", expand=True)
        
        # Binary digits row
        binary_frame = tk.Frame(frame, bg=self.section_bg)
        binary_frame.pack(fill="x")
        
        bit_box_font = tkfont.Font(family="Arial", size=10, weight="bold")
        bit_boxes = []
        for _ in range(8):
            box = tk.Label(
                binary_frame,
                text="0",
                font=bit_box_font,
                bg=self.inactive_bg,
                fg=self.inactive_text,
                width=6,
                height=2,
                relief="flat"
            )
            box.pack(side="left", padx=4, expand=True, fill="both")
            bit_boxes.append(box)
        
        return {
            'frame': outer_frame,
            'header_value': header_value,
            'bit_boxes': bit_boxes
        }
    
    def validate_octet(self, index):
        value = self.octet_vars[index].get()
        
        # Allow empty or digits only
        if value == "":
            self.update_all_displays()
            return
        
        if not value.isdigit():
            self.octet_vars[index].set(value[:-1])
            return
        
        # Check range
        num = int(value)
        if num > 255:
            self.octet_vars[index].set("255")
        
        self.update_all_displays()
    
    def decimal_to_binary(self, decimal_str):
        if decimal_str == "":
            decimal_str = "0"
        num = int(decimal_str)
        return format(num, '08b')
    
    def update_all_displays(self):
        binary_parts = []
        
        for i in range(4):
            value = self.octet_vars[i].get()
            if value == "":
                value = "0"
            
            decimal = int(value)
            binary = self.decimal_to_binary(value)
            binary_parts.append(binary)
            
            # Update header value
            self.octet_displays[i]['header_value'].config(text=str(decimal))
            
            # Update bit boxes
            for j, bit in enumerate(binary):
                box = self.octet_displays[i]['bit_boxes'][j]
                if bit == '1':
                    box.config(bg=self.primary_blue, fg="white", text="1")
                else:
                    box.config(bg=self.inactive_bg, fg=self.inactive_text, text="0")
        
        # Update full binary display
        full_binary = ".".join(binary_parts)
        self.full_binary_label.config(text=full_binary)
        
        # Update scrollbars after display update
        self.root.after(10, self.update_scrollbars)

if __name__ == "__main__":
    root = tk.Tk()
    app = IPBinaryConverter(root)
    root.mainloop()
