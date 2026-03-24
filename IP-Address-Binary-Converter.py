import tkinter as tk
from tkinter import font as tkfont


class IPBinaryConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address Binary Converter")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(500, screen_width - 100)
        window_height = min(650, screen_height - 100)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(400, 550)

        self.bg_gradient  = "#E0E7FF"
        self.card_bg      = "#FFFFFF"
        self.primary_blue = "#6366F1"
        self.text_dark    = "#1F2937"
        self.text_gray    = "#6B7280"
        self.inactive_bg  = "#E5E7EB"
        self.inactive_text = "#9CA3AF"
        self.section_bg   = "#F9FAFB"
        self.highlight_bg = "#EEF2FF"

        self.root.configure(bg=self.bg_gradient)

        self.octet_entries = []
        self.octet_vars    = []
        self.octet_displays = []

        # outer container
        container = tk.Frame(root, bg=self.bg_gradient)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        main_frame = tk.Frame(container, bg=self.card_bg, relief="flat", bd=0)
        main_frame.pack(fill="both", expand=True)

        self.content_frame = tk.Frame(main_frame, bg=self.card_bg)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # title
        self.title_label = tk.Label(
            self.content_frame,
            text="IP Address Binary Converter",
            bg=self.card_bg, fg=self.text_dark
        )
        self.title_label.pack(pady=(0, 4))

        self.subtitle_label = tk.Label(
            self.content_frame,
            text="Enter an IP address to see its binary representation",
            bg=self.card_bg, fg=self.text_gray
        )
        self.subtitle_label.pack(pady=(0, 8))

        # input label
        self.input_label = tk.Label(
            self.content_frame,
            text="IP Address (0–255 per octet)",
            bg=self.card_bg, fg=self.text_dark
        )
        self.input_label.pack(pady=(0, 6))

        # IP entry row
        ip_frame = tk.Frame(self.content_frame, bg=self.card_bg)
        ip_frame.pack(pady=(0, 8))

        for i in range(4):
            var = tk.StringVar(value="0")
            var.trace_add("write", lambda *a, idx=i: self.validate_octet(idx))
            self.octet_vars.append(var)

            entry = tk.Entry(
                ip_frame, textvariable=var,
                justify="center", relief="solid", borderwidth=2,
                highlightthickness=2,
                highlightbackground="#D1D5DB",
                highlightcolor=self.primary_blue,
                width=4
            )
            entry.pack(side="left", padx=4)
            self.octet_entries.append(entry)

            if i < 3:
                dot = tk.Label(ip_frame, text=".", bg=self.card_bg, fg=self.inactive_text)
                dot.pack(side="left", padx=1)
                self._dot_labels = getattr(self, "_dot_labels", [])
                self._dot_labels.append(dot)

        # full binary strip (packed FIRST so it reserves space at bottom)
        binary_outer = tk.Frame(
            self.content_frame, bg=self.highlight_bg,
            relief="solid", borderwidth=1
        )
        binary_outer.pack(side="bottom", fill="x", pady=(4, 0))

        # octet display area (expands to fill remaining space)
        octets_frame = tk.Frame(self.content_frame, bg=self.card_bg)
        octets_frame.pack(fill="both", expand=True, pady=(4, 8))

        for i in range(4):
            octets_frame.rowconfigure(i, weight=1)
        octets_frame.columnconfigure(0, weight=1)

        for i in range(4):
            display = self._build_octet_display(octets_frame, i)
            display["outer"].grid(row=i, column=0, sticky="nsew", pady=3)
            self.octet_displays.append(display)

        binary_inner = tk.Frame(binary_outer, bg=self.highlight_bg)
        binary_inner.pack(fill="x", padx=16, pady=8)

        self.binary_title_label = tk.Label(
            binary_inner, text="Complete Binary:",
            bg=self.highlight_bg, fg=self.text_dark
        )
        self.binary_title_label.pack(anchor="w", pady=(0, 4))

        self.full_binary_label = tk.Label(
            binary_inner,
            text="00000000.00000000.00000000.00000000",
            bg=self.highlight_bg, fg=self.primary_blue
        )
        self.full_binary_label.pack()

        self.update_all_displays()

        # bind resize
        self.root.bind("<Configure>", self._on_resize)
        self.root.after(100, lambda: self._apply_fonts(
            self.root.winfo_width(), self.root.winfo_height()
        ))

    # Build one octet display row
    def _build_octet_display(self, parent, index):
        outer = tk.Frame(parent, bg=self.section_bg, relief="solid", borderwidth=1)

        inner = tk.Frame(outer, bg=self.section_bg)
        inner.pack(fill="both", expand=True, padx=10, pady=4)

        # header row
        header_frame = tk.Frame(inner, bg=self.section_bg)
        header_frame.pack(anchor="w")

        hdr_lbl = tk.Label(
            header_frame, text=f"Octet {index + 1}: ",
            bg=self.section_bg, fg=self.text_gray
        )
        hdr_lbl.pack(side="left")

        hdr_val = tk.Label(
            header_frame, text="0",
            bg=self.section_bg, fg=self.primary_blue
        )
        hdr_val.pack(side="left")

        # shared grid: row 0 = bit-value labels, row 1 = bit boxes
        # uniform column weighting keeps numbers perfectly centred over boxes
        grid_frame = tk.Frame(inner, bg=self.section_bg)
        grid_frame.pack(fill="both", expand=True)

        for col in range(8):
            grid_frame.columnconfigure(col, weight=1, uniform="bits")
        grid_frame.rowconfigure(0, weight=0)
        grid_frame.rowconfigure(1, weight=1)

        bv_labels = []
        bit_boxes = []
        for col, v in enumerate([128, 64, 32, 16, 8, 4, 2, 1]):
            lbl = tk.Label(
                grid_frame, text=str(v),
                bg=self.section_bg, fg=self.text_gray
            )
            lbl.grid(row=0, column=col, sticky="ew")
            bv_labels.append(lbl)

            box = tk.Label(
                grid_frame, text="0",
                bg=self.inactive_bg, fg=self.inactive_text,
                relief="flat"
            )
            box.grid(row=1, column=col, padx=2, sticky="nsew")
            bit_boxes.append(box)

        bb_frame = grid_frame

        return {
            "outer":      outer,
            "hdr_lbl":    hdr_lbl,
            "hdr_val":    hdr_val,
            "bv_labels":  bv_labels,
            "bb_frame":   bb_frame,
            "bit_boxes":  bit_boxes,
        }

    # Dynamic font / size scaling
    def _on_resize(self, event):
        if event.widget is self.root:
            self._apply_fonts(event.width, event.height)

    def _apply_fonts(self, w, h):
        # Scale everything off the smaller dimension so nothing clips
        scale = min(w, h)

        title_size   = max(10, int(scale * 0.030))
        sub_size     = max(8,  int(scale * 0.016))
        label_size   = max(8,  int(scale * 0.015))
        entry_size   = max(10, int(scale * 0.024))
        dot_size     = max(10, int(scale * 0.026))
        hdr_size     = max(9,  int(scale * 0.018))
        hdr_val_size = max(10, int(scale * 0.021))
        bv_size      = max(8,  int(scale * 0.016))
        bb_size      = max(7,  int(scale * 0.013))
        bin_ttl_size = max(8,  int(scale * 0.017))
        bin_val_size = max(10, int(scale * 0.022))

        # Calculate bit-box height from available space
        fixed_overhead = title_size * 2 + sub_size * 2 + label_size * 2 + entry_size * 2 + bin_val_size * 2 + 120
        octet_h = max(40, (h - fixed_overhead) // 4)
        bb_height = max(1, int(octet_h * 0.28))

        self.title_label.config(
            font=tkfont.Font(family="Arial", size=title_size, weight="bold")
        )
        self.subtitle_label.config(
            font=tkfont.Font(family="Arial", size=sub_size)
        )
        self.input_label.config(
            font=tkfont.Font(family="Arial", size=label_size, weight="bold")
        )
        self.binary_title_label.config(
            font=tkfont.Font(family="Arial", size=bin_ttl_size, weight="bold")
        )
        self.full_binary_label.config(
            font=tkfont.Font(family="Courier New", size=bin_val_size, weight="bold")
        )

        entry_font = tkfont.Font(family="Courier New", size=entry_size, weight="bold")
        for entry in self.octet_entries:
            entry.config(font=entry_font)

        dot_font = tkfont.Font(family="Arial", size=dot_size, weight="bold")
        for dot in getattr(self, "_dot_labels", []):
            dot.config(font=dot_font)

        for d in self.octet_displays:
            d["hdr_lbl"].config(font=tkfont.Font(family="Arial", size=hdr_size))
            d["hdr_val"].config(font=tkfont.Font(family="Arial", size=hdr_val_size, weight="bold"))

            bv_font = tkfont.Font(family="Arial", size=bv_size)
            for lbl in d["bv_labels"]:
                lbl.config(font=bv_font)

            bb_font = tkfont.Font(family="Arial", size=bb_size, weight="bold")
            for box in d["bit_boxes"]:
                box.config(font=bb_font, height=bb_height)

    # Validation & display logic
    def validate_octet(self, index):
        value = self.octet_vars[index].get()
        if value == "":
            self.update_all_displays()
            return
        if not value.isdigit():
            self.octet_vars[index].set(value[:-1])
            return
        if int(value) > 255:
            self.octet_vars[index].set("255")
        self.update_all_displays()

    def decimal_to_binary(self, decimal_str):
        return format(int(decimal_str) if decimal_str else 0, "08b")

    def update_all_displays(self):
        binary_parts = []
        for i in range(4):
            value = self.octet_vars[i].get() or "0"
            binary = self.decimal_to_binary(value)
            binary_parts.append(binary)

            self.octet_displays[i]["hdr_val"].config(text=str(int(value)))

            for j, bit in enumerate(binary):
                box = self.octet_displays[i]["bit_boxes"][j]
                if bit == "1":
                    box.config(bg=self.primary_blue, fg="white", text="1")
                else:
                    box.config(bg=self.inactive_bg, fg=self.inactive_text, text="0")

        self.full_binary_label.config(text=".".join(binary_parts))


if __name__ == "__main__":
    root = tk.Tk()
    app = IPBinaryConverter(root)
    root.mainloop()
