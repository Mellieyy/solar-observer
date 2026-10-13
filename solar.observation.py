import tkinter as tk
from tkinter import ttk, messagebox
import math

class SmoothScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg="#0B0F19")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Glass.TFrame")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)


class SolarObserverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar Observation Data Reducer")
        self.root.geometry("1100x1020")
        self.root.minsize(740, 720)

        # Theme Color Palette
        self.bg_color = "#0B0F19"          # Deep cosmic dark base
        self.glass_card = "#162032"        # Card background layer
        self.glass_border = "#334155"      # Border highlight edge
        self.primary_color = "#38BDF8"     # Neon Sky Cyan Glow
        self.text_color = "#F8FAFC"        # Bright crisp white
        self.subtext_color = "#94A3B8"     # Soft silver gray
        self.accent_green = "#34D399"      # Aesthetic green color for calculations

        self.root.configure(bg=self.bg_color)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure(".", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("Glass.TFrame", background=self.bg_color)

        # Style for Notebook Tabs
        self.style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#1E293B", foreground=self.text_color, padding=[10, 8], font=("Segoe UI", 9, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", self.primary_color)], foreground=[("selected", "#0F172A")])

        # App Title Banner Frame (Top)
        banner_frame = tk.Frame(
            root, 
            bg=self.glass_card, 
            highlightbackground=self.glass_border, 
            highlightthickness=1, 
            padx=16, 
            pady=12
        )
        banner_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_lbl = tk.Label(banner_frame, text="☀️ Solar Observation Data Reducer", font=("Segoe UI", 14, "bold"), fg=self.text_color, bg=self.glass_card)
        title_lbl.pack(side="left")

        # Notebook (Tabs Container)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab Containers (Scrollable)
        self.tab1_container = SmoothScrollableFrame(self.notebook)
        self.notebook.add(self.tab1_container, text="  Set 1  ")

        self.tab2_container = SmoothScrollableFrame(self.notebook)
        self.notebook.add(self.tab2_container, text="  Set 2  ")

        self.tab3_container = SmoothScrollableFrame(self.notebook)
        self.notebook.add(self.tab3_container, text="  Coordinate Station  ")

        self.tab4_container = SmoothScrollableFrame(self.notebook)
        self.notebook.add(self.tab4_container, text="  Final Reduction  ")

        # Bind Global Mouse Wheel
        self.bind_global_smooth_scroll(self.root)

        # Build Forms inside Tabs
        self.inputs_set1 = self.build_observation_form(self.tab1_container.scrollable_frame, "Observation Set 1", "Proceed to Set 2", lambda: self.notebook.select(1))
        self.inputs_set2 = self.build_observation_form(self.tab2_container.scrollable_frame, "Observation Set 2", "Proceed to Coordinate Station", lambda: self.notebook.select(2))
        self.coord_inputs = self.build_coordinates_form(self.tab3_container.scrollable_frame)
        self.ephemeris_inputs, self.final_inputs = self.build_final_reduction_form(self.tab4_container.scrollable_frame)

    def bind_global_smooth_scroll(self, root_window):
        def _smooth_scroll(event):
            if event.delta:
                units = int(-1 * (event.delta / 120))
            elif event.num == 4:
                units = -1
            elif event.num == 5:
                units = 1
            else:
                return

            try:
                current_tab = self.notebook.select()
                if current_tab == str(self.tab1_container):
                    self.tab1_container.canvas.yview_scroll(units, "units")
                elif current_tab == str(self.tab2_container):
                    self.tab2_container.canvas.yview_scroll(units, "units")
                elif current_tab == str(self.tab3_container):
                    self.tab3_container.canvas.yview_scroll(units, "units")
                else:
                    self.tab4_container.canvas.yview_scroll(units, "units")
            except Exception:
                pass

        root_window.bind_all("<MouseWheel>", _smooth_scroll)
        root_window.bind_all("<Button-4>", _smooth_scroll)
        root_window.bind_all("<Button-5>", _smooth_scroll)

    def build_angle_input(self, parent, label_text):
        row_frame = tk.Frame(parent, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=4, pady=2)
        row_frame.pack(fill="x", pady=2)

        tk.Label(row_frame, text=label_text, font=("Consolas", 9, "bold"), width=16, anchor="w", fg=self.primary_color, bg="#0F172A").pack(side="left")

        deg_entry = tk.Entry(row_frame, width=5, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        deg_entry.pack(side="left", padx=(2, 1), ipady=2)
        tk.Label(row_frame, text="°", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")

        min_entry = tk.Entry(row_frame, width=3, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        min_entry.pack(side="left", padx=(4, 1), ipady=2)
        tk.Label(row_frame, text="'", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")

        sec_entry = tk.Entry(row_frame, width=4, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        sec_entry.pack(side="left", padx=(4, 1), ipady=2)
        tk.Label(row_frame, text="\"", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")

        deg_entry.bind("<KeyRelease>", lambda e: self.trigger_live_updates())
        min_entry.bind("<KeyRelease>", lambda e: self.trigger_live_updates())
        sec_entry.bind("<KeyRelease>", lambda e: self.trigger_live_updates())

        return {"deg": deg_entry, "min": min_entry, "sec": sec_entry}

    def build_min_sec_input(self, parent, label_text):
        row_frame = tk.Frame(parent, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=4, pady=2)
        row_frame.pack(fill="x", pady=2)

        tk.Label(row_frame, text=label_text, font=("Consolas", 9, "bold"), width=16, anchor="w", fg=self.primary_color, bg="#0F172A").pack(side="left")

        min_entry = tk.Entry(row_frame, width=5, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        min_entry.pack(side="left", padx=(2, 1), ipady=2)
        tk.Label(row_frame, text="'", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")

        sec_entry = tk.Entry(row_frame, width=5, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        sec_entry.pack(side="left", padx=(4, 1), ipady=2)
        tk.Label(row_frame, text="\"", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")

        min_entry.bind("<KeyRelease>", lambda e: self.trigger_live_updates())
        sec_entry.bind("<KeyRelease>", lambda e: self.trigger_live_updates())

        return {"min": min_entry, "sec": sec_entry}

    def build_observation_form(self, parent, set_title, btn_text, btn_command):
        card_container = tk.Frame(parent, bg=self.glass_card, highlightbackground=self.glass_border, highlightthickness=1, padx=16, pady=16)
        card_container.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(card_container, text=set_title, font=("Segoe UI", 14, "bold"), fg=self.text_color, bg=self.glass_card).pack(anchor="w", pady=(0, 12))

        ro_box = tk.Frame(card_container, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        ro_box.pack(fill="x", pady=(0, 10))
        tk.Label(ro_box, text="📌 Reference Object (RO) Bearings", font=("Segoe UI", 10, "bold"), fg=self.primary_color, bg="#0F172A").pack(anchor="w", pady=(0, 6))
        fl_ro = self.build_angle_input(ro_box, "FL RO:")
        fr_ro = self.build_angle_input(ro_box, "FR RO:")
        ro_res_lbl = tk.Label(ro_box, text="Mean RO: ---", font=("Consolas", 9, "bold"), fg=self.accent_green, bg="#0F172A")
        ro_res_lbl.pack(anchor="w", pady=(6, 2))

        time_box = tk.Frame(card_container, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        time_box.pack(fill="x", pady=(0, 10))
        tk.Label(time_box, text="⏱️ Time Observations (HH:MM)", font=("Segoe UI", 10, "bold"), fg=self.primary_color, bg="#0F172A").pack(anchor="w", pady=(0, 6))

        time_entries = []
        for i in range(1, 5):
            row_frame = tk.Frame(time_box, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=4, pady=2)
            row_frame.pack(fill="x", pady=2)
            tk.Label(row_frame, text=f"Obs {i}:", font=("Segoe UI", 9), width=6, anchor="w", fg=self.text_color, bg="#0F172A").pack(side="left")
            hr_entry = tk.Entry(row_frame, width=4, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
            hr_entry.pack(side="left", padx=(0, 2), ipady=2)
            tk.Label(row_frame, text=":", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A").pack(side="left")
            min_entry = tk.Entry(row_frame, width=4, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
            min_entry.pack(side="left", padx=(2, 8), ipady=2)
            hr_entry.bind("<KeyRelease>", lambda e: self.trigger_live_updates())
            min_entry.bind("<KeyRelease>", lambda e: self.trigger_live_updates())
            time_entries.append({"hr": hr_entry, "min": min_entry})

        time_res_lbl = tk.Label(time_box, text="Mean Time: ---", font=("Consolas", 9, "bold"), fg=self.accent_green, bg="#0F172A")
        time_res_lbl.pack(anchor="w", pady=(6, 2))

        configs = [
            ("FL  [ ⨀¯ ]", "Face Left (Top/Right)"),
            ("FL  [ ¯⨀ ]", "Face Left (Bottom/Right)"),
            ("FR  [ ¯⨀ ]", "Face Right (Bottom/Left)"),
            ("FR  [ ⨀¯ ]", "Face Right (Top/Left)")
        ]

        hb_box = tk.Frame(card_container, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        hb_box.pack(fill="x", pady=(0, 10))
        tk.Label(hb_box, text="📐 Horizontal Bearings", font=("Segoe UI", 10, "bold"), fg=self.primary_color, bg="#0F172A").pack(anchor="w", pady=(0, 6))
        hb_entries = []
        for sym, desc in configs:
            hb_entries.append(self.build_angle_input(hb_box, sym))
        hb_res_lbl = tk.Label(hb_box, text="Mean Hz Bearing: ---", font=("Consolas", 9, "bold"), fg=self.accent_green, bg="#0F172A")
        hb_res_lbl.pack(anchor="w", pady=(6, 2))

        va_box = tk.Frame(card_container, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        va_box.pack(fill="x", pady=(0, 10))
        tk.Label(va_box, text="🔭 Vertical Angles", font=("Segoe UI", 10, "bold"), fg=self.primary_color, bg="#0F172A").pack(anchor="w", pady=(0, 6))
        va_entries = []
        for sym, desc in configs:
            va_entries.append(self.build_angle_input(va_box, sym))
        va_res_lbl = tk.Label(va_box, text="Mean Vertical Angle: ---", font=("Consolas", 9, "bold"), fg=self.accent_green, bg="#0F172A")
        va_res_lbl.pack(anchor="w", pady=(6, 2))

        ref_box = tk.Frame(card_container, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=12, pady=10)
        ref_box.pack(fill="x", pady=(0, 10))
        tk.Label(ref_box, text="🌐 Refraction and Parallax", font=("Segoe UI", 10, "bold"), fg=self.primary_color, bg="#0F172A").pack(anchor="w", pady=(0, 4))
        remark_text = "Remark: Please refer to the Refraction and Parallax table before keying in data."
        tk.Label(ref_box, text=remark_text, font=("Segoe UI", 8, "italic"), fg=self.subtext_color, bg="#0F172A", wraplength=450, justify="left").pack(anchor="w", pady=(0, 6))
        ref_entry = self.build_min_sec_input(ref_box, "Ref & Parallax:")

        result_box = tk.Frame(card_container, bg="#022C22", highlightbackground="#059669", highlightthickness=1, padx=12, pady=10)
        result_box.pack(fill="x", pady=(0, 10))
        res_label = tk.Label(result_box, text="Mean RO: ---\nMean Time: ---\nMean Hz Bearing: ---\nMean Vertical Angle: ---\nRefraction & Parallax: ---\nAdjusted Vertical: ---", font=("Consolas", 9, "bold"), fg=self.accent_green, bg="#022C22", justify="left")
        res_label.pack(anchor="w")

        nav_btn = tk.Button(
            card_container, 
            text=btn_text, 
            font=("Segoe UI", 10, "bold"), 
            bg=self.primary_color, 
            fg="#0F172A", 
            activebackground="#0EA5E9",
            activeforeground="#0F172A",
            relief="flat", 
            padx=15, 
            pady=10,
            cursor="hand2",
            command=btn_command
        )
        nav_btn.pack(fill="x")

        return {
            "fl_ro": fl_ro, "fr_ro": fr_ro, "ro_res": ro_res_lbl,
            "times": time_entries, "time_res": time_res_lbl,
            "hbs": hb_entries, "hb_res": hb_res_lbl,
            "vas": va_entries, "va_res": va_res_lbl,
            "ref_parallax": ref_entry, "result_lbl": res_label
        }

    def build_coordinates_form(self, parent):
        card_container = tk.Frame(parent, bg=self.glass_card, highlightbackground=self.glass_border, highlightthickness=1, padx=16, pady=16)
        card_container.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(card_container, text="📍 Coordinate Station", font=("Segoe UI", 14, "bold"), fg=self.text_color, bg=self.glass_card).pack(anchor="w", pady=(0, 12))

        coord_box = tk.Frame(card_container, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=12, pady=12)
        coord_box.pack(fill="x", pady=(0, 10))

        tk.Label(coord_box, text="Coord. of Origin N:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=0, column=0, sticky="w", padx=4, pady=6)
        orig_n = tk.Entry(coord_box, width=16, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        orig_n.insert(0, "0.0")
        orig_n.grid(row=0, column=1, sticky="w", padx=4, pady=6, ipady=2)

        tk.Label(coord_box, text="Origin E:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=0, column=2, sticky="w", padx=16, pady=6)
        orig_e = tk.Entry(coord_box, width=16, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        orig_e.insert(0, "0.0")
        orig_e.grid(row=0, column=3, sticky="w", padx=4, pady=6, ipady=2)

        tk.Label(coord_box, text="Coord. of Station N:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=1, column=0, sticky="w", padx=4, pady=6)
        stat_n = tk.Entry(coord_box, width=16, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        stat_n.grid(row=1, column=1, sticky="w", padx=4, pady=6, ipady=2)

        tk.Label(coord_box, text="Station W:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=1, column=2, sticky="w", padx=16, pady=6)
        stat_w = tk.Entry(coord_box, width=16, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        stat_w.grid(row=1, column=3, sticky="w", padx=4, pady=6, ipady=2)

        tk.Label(coord_box, text="Tot/Diff. N:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=2, column=0, sticky="w", padx=4, pady=6)
        tot_diff_n_lbl = tk.Label(coord_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", anchor="w", width=18)
        tot_diff_n_lbl.grid(row=2, column=1, sticky="w", padx=4, pady=6)

        tk.Label(coord_box, text="Tot/Diff. W:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=2, column=2, sticky="w", padx=16, pady=6)
        tot_diff_w_lbl = tk.Label(coord_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", anchor="w", width=18)
        tot_diff_w_lbl.grid(row=2, column=3, sticky="w", padx=4, pady=6)

        tk.Label(coord_box, text="Tot/Diff x 0.03256 (+):", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=3, column=0, sticky="w", padx=4, pady=6)
        tot_diff_calc_lbl = tk.Label(coord_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", anchor="w", width=18)
        tot_diff_calc_lbl.grid(row=3, column=1, sticky="w", padx=4, pady=6)

        tk.Label(coord_box, text="Diff. in Long = Diff. x 0.03246:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=3, column=2, sticky="w", padx=16, pady=6)
        diff_long_lbl = tk.Label(coord_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", anchor="w", width=18)
        diff_long_lbl.grid(row=3, column=3, sticky="w", padx=4, pady=6)

        tk.Label(coord_box, text="Lat. of Origin N:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=4, column=0, sticky="w", padx=4, pady=6)
        lat_frame = tk.Frame(coord_box, bg="#0F172A")
        lat_frame.grid(row=4, column=1, sticky="w", padx=4, pady=6)
        
        lat_orig_deg = tk.Entry(lat_frame, width=4, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        lat_orig_deg.insert(0, "5")
        lat_orig_deg.pack(side="left", padx=(0, 1), ipady=2)
        tk.Label(lat_frame, text="°", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")

        lat_orig_min = tk.Entry(lat_frame, width=3, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        lat_orig_min.insert(0, "57")
        lat_orig_min.pack(side="left", padx=(4, 1), ipady=2)
        tk.Label(lat_frame, text="'", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")

        lat_orig_sec = tk.Entry(lat_frame, width=4, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        lat_orig_sec.insert(0, "55")
        lat_orig_sec.pack(side="left", padx=(4, 1), ipady=2)
        tk.Label(lat_frame, text="\"", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")

        tk.Label(coord_box, text="Diff. in Long x Sine Latitude:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=4, column=2, sticky="w", padx=16, pady=6)
        diff_long_sin_lbl = tk.Label(coord_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", anchor="w", width=18)
        diff_long_sin_lbl.grid(row=4, column=3, sticky="w", padx=4, pady=6)

        tk.Label(coord_box, text="Latitude of Station N:", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=5, column=0, sticky="w", padx=4, pady=6)
        lat_stat_lbl = tk.Label(coord_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", anchor="w", width=18)
        lat_stat_lbl.grid(row=5, column=1, sticky="w", padx=4, pady=6)

        tk.Label(coord_box, text="Convergence E(-) / W(+):", font=("Segoe UI", 9, "bold"), fg=self.text_color, bg="#0F172A", anchor="w").grid(row=5, column=2, sticky="w", padx=16, pady=6)
        conv_lbl = tk.Label(coord_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", anchor="w", width=18)
        conv_lbl.grid(row=5, column=3, sticky="w", padx=4, pady=6)

        nav_btn = tk.Button(
            card_container, 
            text="Proceed to Final Reduction", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.primary_color, 
            fg="#0F172A", 
            activebackground="#0EA5E9",
            activeforeground="#0F172A",
            relief="flat", 
            padx=15, 
            pady=10,
            cursor="hand2",
            command=lambda: self.notebook.select(3)
        )
        nav_btn.pack(fill="x", pady=(15, 0))

        for widget in [orig_n, orig_e, stat_n, stat_w, lat_orig_deg, lat_orig_min, lat_orig_sec]:
            widget.bind("<KeyRelease>", lambda e: self.calculate_coordinates_live())

        return {
            "orig_n": orig_n, "orig_e": orig_e, "stat_n": stat_n, "stat_w": stat_w,
            "tot_diff_n": tot_diff_n_lbl, "tot_diff_w": tot_diff_w_lbl,
            "tot_diff_calc": tot_diff_calc_lbl, "diff_long": diff_long_lbl,
            "lat_deg": lat_orig_deg, "lat_min": lat_orig_min, "lat_sec": lat_orig_sec,
            "diff_long_sin": diff_long_sin_lbl, "lat_stat": lat_stat_lbl, "conv": conv_lbl
        }

    def build_final_reduction_form(self, parent):
        card_container = tk.Frame(parent, bg=self.glass_card, highlightbackground=self.glass_border, highlightthickness=1, padx=16, pady=16)
        card_container.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(card_container, text="☀️ Final Reduction & Classification", font=("Segoe UI", 14, "bold"), fg=self.text_color, bg=self.glass_card).pack(anchor="w", pady=(0, 12))

        remark_text = "Remark: Please refer to star almanac based on the observation day... and dont forget to key in the v value (in seconds) and declination at 0h U.T."
        tk.Label(card_container, text=remark_text, font=("Segoe UI", 9, "italic"), fg=self.primary_color, bg=self.glass_card, wraplength=650, justify="left").pack(anchor="w", pady=(0, 10))

        fin_box = tk.Frame(card_container, bg="#0F172A", highlightbackground="#334155", highlightthickness=1, padx=12, pady=12)
        fin_box.pack(fill="x", pady=(0, 10))

        # Table Column Headers
        tk.Label(fin_box, text="", width=28, bg="#0F172A").grid(row=0, column=0, sticky="w")
        tk.Label(fin_box, text="Set 1", font=("Segoe UI", 10, "bold"), fg=self.primary_color, bg="#0F172A", width=22, anchor="w").grid(row=0, column=1, sticky="w", padx=4)
        tk.Label(fin_box, text="Set 2", font=("Segoe UI", 10, "bold"), fg=self.primary_color, bg="#0F172A", width=22, anchor="w").grid(row=0, column=2, sticky="w", padx=4)

        current_row = 1

        def add_row_label(text):
            nonlocal current_row
            tk.Label(fin_box, text=text, font=("Segoe UI", 9, "bold"), width=28, anchor="w", fg=self.text_color, bg="#0F172A").grid(row=current_row, column=0, sticky="w", pady=4)

        def add_row_vals(lbl1, lbl2):
            nonlocal current_row
            lbl1.grid(row=current_row, column=1, sticky="w", padx=4, pady=4)
            lbl2.grid(row=current_row, column=2, sticky="w", padx=4, pady=4)
            current_row += 1

        # 1. G.T. Obs
        add_row_label("G.T. Obs:")
        gt1_lbl = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        gt2_lbl = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(gt1_lbl, gt2_lbl)

        # 2. Declination at 0h U.T.
        add_row_label("Declination at 0h U.T.:")
        dec1_frame = tk.Frame(fin_box, bg="#0F172A")
        dec1_deg = tk.Entry(dec1_frame, width=4, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        dec1_deg.pack(side="left", padx=(0, 1), ipady=2)
        tk.Label(dec1_frame, text="°", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")
        dec1_min = tk.Entry(dec1_frame, width=3, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        dec1_min.pack(side="left", padx=(4, 1), ipady=2)
        tk.Label(dec1_frame, text="'", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")
        dec1_sec = tk.Entry(dec1_frame, width=4, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        dec1_sec.pack(side="left", padx=(4, 1), ipady=2)
        tk.Label(dec1_frame, text="\"", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")

        dec2_frame = tk.Frame(fin_box, bg="#0F172A")
        dec2_deg = tk.Entry(dec2_frame, width=4, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        dec2_deg.pack(side="left", padx=(0, 1), ipady=2)
        tk.Label(dec2_frame, text="°", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")
        dec2_min = tk.Entry(dec2_frame, width=3, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        dec2_min.pack(side="left", padx=(4, 1), ipady=2)
        tk.Label(dec2_frame, text="'", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")
        dec2_sec = tk.Entry(dec2_frame, width=4, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        dec2_sec.pack(side="left", padx=(4, 1), ipady=2)
        tk.Label(dec2_frame, text="\"", font=("Segoe UI", 9, "bold"), fg=self.subtext_color, bg="#0F172A").pack(side="left")
        add_row_vals(dec1_frame, dec2_frame)

        # 3. v value (sec)
        add_row_label("v value (sec):")
        v1_entry = tk.Entry(fin_box, width=8, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        v1_entry.insert(0, "0.0")
        v2_entry = tk.Entry(fin_box, width=8, font=("Segoe UI", 9), bg="#1E293B", fg=self.text_color, insertbackground="white", relief="flat")
        v2_entry.insert(0, "0.0")
        add_row_vals(v1_entry, v2_entry)

        # 4. Diff (Ephemeris) - mm ss.ss format
        add_row_label("Diff:")
        diff1_lbl = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        diff2_lbl = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(diff1_lbl, diff2_lbl)

        # 5. Decl. at time of obsn
        add_row_label("Decl. at time of obsn:")
        decl_time1_lbl = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        decl_time2_lbl = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(decl_time1_lbl, decl_time2_lbl)

        # 6. Polar Dist = p (90 - Decl. at time of obsn)
        add_row_label("Polar Dist = p:")
        f_pol1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_pol2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_pol1, f_pol2)

        # 7. Latitude = Φ
        add_row_label("Latitude = Φ:")
        f_lat1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_lat2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_lat1, f_lat2)

        # 8. Adj. Vert. = α
        add_row_label("Adj. Vert. = α:")
        f_adj1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_adj2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_adj1, f_adj2)

        # 9. Comp. Azimuth
        add_row_label("Comp. Azimuth:")
        f_comp1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_comp2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_comp1, f_comp2)

        # 10. Obs. Azimuth
        add_row_label("Obs. Azimuth:")
        f_obs1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_obs2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_obs1, f_obs2)

        # 11. Diff = Comp – Obsn
        add_row_label("Diff = Comp – Obsn:")
        f_diff_az1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_diff_az2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_diff_az1, f_diff_az2)

        # 12. Mean Obs. R.O
        add_row_label("Mean Obs. R.O:")
        f_mean_ro1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_mean_ro2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_mean_ro1, f_mean_ro2)

        # 13. True R.O
        add_row_label("True R.O:")
        f_true_ro1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_true_ro2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_true_ro1, f_true_ro2)

        # 14. Convergence
        add_row_label("Convergence:")
        f_conv1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_conv2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_conv1, f_conv2)

        # 15. Grid Brg R.O.
        add_row_label("Grid Brg R.O.:")
        f_grid1 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        f_grid2 = tk.Label(fin_box, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=22, anchor="w")
        add_row_vals(f_grid1, f_grid2)

        # 16. Mean Grid Brg R.O.
        rm = tk.Frame(fin_box, bg="#0F172A")
        rm.grid(row=current_row, column=0, columnspan=3, sticky="w", pady=6)
        tk.Label(rm, text="Mean Grid Brg R.O.:", font=("Segoe UI", 9, "bold"), width=28, anchor="w", fg=self.text_color, bg="#0F172A").pack(side="left")
        f_mean_grid = tk.Label(rm, text="---", font=("Consolas", 10, "bold"), fg=self.accent_green, bg="#0F172A", width=46, anchor="w")
        f_mean_grid.pack(side="left")

        # Calculate Tolerance Button
        tol_btn = tk.Button(
            card_container, 
            text="Calculate the Tolerance", 
            font=("Segoe UI", 10, "bold"), 
            bg="#3B82F6", 
            fg="#F8FAFC", 
            activebackground="#2563EB",
            activeforeground="#F8FAFC",
            relief="flat", 
            padx=15, 
            pady=8,
            cursor="hand2",
            command=self.calculate_tolerance
        )
        tol_btn.pack(fill="x", pady=(10, 5))

        # Dynamic Colored Box for Tolerance Result
        self.class_frame = tk.Frame(card_container, bg="#1E293B", highlightbackground="#334155", highlightthickness=2, padx=16, pady=16)
        self.class_frame.pack(fill="x", pady=(5, 0))

        self.class_lbl = tk.Label(self.class_frame, text="CLICK 'CALCULATE THE TOLERANCE' TO CHECK RESULTS", font=("Segoe UI", 12, "bold"), fg=self.text_color, bg="#1E293B")
        self.class_lbl.pack()

        ephemeris_inputs = {
            "gt1": gt1_lbl, "dec1_deg": dec1_deg, "dec1_min": dec1_min, "dec1_sec": dec1_sec, "v1": v1_entry, "diff1": diff1_lbl, "decl_time1": decl_time1_lbl, "polar1": f_pol1,
            "gt2": gt2_lbl, "dec2_deg": dec2_deg, "dec2_min": dec2_min, "dec2_sec": dec2_sec, "v2": v2_entry, "diff2": diff2_lbl, "decl_time2": decl_time2_lbl, "polar2": f_pol2
        }

        final_inputs = {
            "lat1": f_lat1, "lat2": f_lat2, "adj1": f_adj1, "adj2": f_adj2,
            "pol1": f_pol1, "pol2": f_pol2, "comp1": f_comp1, "comp2": f_comp2,
            "obs1": f_obs1, "obs2": f_obs2, "diff_az1": f_diff_az1, "diff_az2": f_diff_az2,
            "mean_ro1": f_mean_ro1, "mean_ro2": f_mean_ro2, "true_ro1": f_true_ro1, "true_ro2": f_true_ro2,
            "conv1": f_conv1, "conv2": f_conv2, "grid1": f_grid1, "grid2": f_grid2,
            "mean_grid": f_mean_grid
        }

        for widget in [dec1_deg, dec1_min, dec1_sec, v1_entry, dec2_deg, dec2_min, dec2_sec, v2_entry]:
            widget.bind("<KeyRelease>", lambda e: self.trigger_live_updates())

        return ephemeris_inputs, final_inputs

    def calculate_tolerance(self):
        try:
            g1_str = self.final_inputs["grid1"].cget("text")
            g2_str = self.final_inputs["grid2"].cget("text")
            g1 = self.parse_angle_string_to_seconds(g1_str)
            g2 = self.parse_angle_string_to_seconds(g2_str)

            if g1 is not None and g2 is not None:
                diff_g = abs(g1 - g2)

                if diff_g < 10.0:
                    # Gold (1st Class)
                    self.class_frame.config(bg="#B45309", highlightbackground="#FBBF24", highlightthickness=3)
                    self.class_lbl.config(text=f"★ 1ST CLASS OBSERVATION (Diff: {diff_g:.2f}\") ★", font=("Segoe UI", 13, "bold"), fg="#FEF3C7", bg="#B45309")
                elif diff_g < 20.0:
                    # Silver (2nd Class)
                    self.class_frame.config(bg="#475569", highlightbackground="#CBD5E1", highlightthickness=2)
                    self.class_lbl.config(text=f"2ND CLASS OBSERVATION (Diff: {diff_g:.2f}\")", font=("Segoe UI", 12, "bold"), fg="#F8FAFC", bg="#475569")
                elif diff_g < 30.0:
                    # Bronze (3rd Class)
                    self.class_frame.config(bg="#7C2D12", highlightbackground="#FB923C", highlightthickness=2)
                    self.class_lbl.config(text=f"3RD CLASS OBSERVATION (Diff: {diff_g:.2f}\")", font=("Segoe UI", 12, "bold"), fg="#FFEDD5", bg="#7C2D12")
                else:
                    # Red (Rejected)
                    self.class_frame.config(bg="#7F1D1D", highlightbackground="#F87171", highlightthickness=2)
                    self.class_lbl.config(text=f"OBSERVATION REJECTED (Diff: {diff_g:.2f}\")", font=("Segoe UI", 12, "bold"), fg="#FEE2E2", bg="#7F1D1D")
            else:
                messagebox.showwarning("Incomplete Data", "Please complete all observation inputs and reductions before calculating tolerance.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not calculate tolerance: {str(e)}")

    def trigger_live_updates(self):
        self.calculate_set_live(self.inputs_set1)
        self.calculate_set_live(self.inputs_set2)
        self.calculate_coordinates_live()
        self.calculate_ephemeris_and_final_reduction()

    def parse_angle_to_seconds(self, angle_dict):
        d_str = angle_dict["deg"].get().strip()
        m_str = angle_dict["min"].get().strip()
        s_str = angle_dict["sec"].get().strip()
        if d_str.replace('.', '', 1).isdigit() and m_str.replace('.', '', 1).isdigit() and s_str.replace('.', '', 1).isdigit():
            return float(d_str) * 3600 + float(m_str) * 60 + float(s_str)
        return None

    def parse_min_sec_to_seconds(self, min_sec_dict):
        m_str = min_sec_dict["min"].get().strip()
        s_str = min_sec_dict["sec"].get().strip()
        if m_str.replace('.', '', 1).isdigit() and s_str.replace('.', '', 1).isdigit():
            return float(m_str) * 60 + float(s_str)
        return None

    def seconds_to_angle_str(self, total_sec):
        if total_sec is None:
            return "---"
        is_neg = total_sec < 0
        total_sec = abs(total_sec)
        d = int(total_sec // 3600) % 360
        m = int((total_sec % 3600) // 60)
        s = round(total_sec % 60, 2)
        sign = "-" if is_neg else ""
        return f"{sign}{d}° {m:02d}' {s:05.2f}\""

    def seconds_to_hms_str(self, total_sec):
        if total_sec is None:
            return "---"
        is_neg = total_sec < 0
        total_sec = abs(total_sec)
        h = int(total_sec // 3600) % 24
        m = int((total_sec % 3600) // 60)
        s = int(round(total_sec % 60))
        sign = "-" if is_neg else ""
        return f"{sign}{h:02d} : {m:02d} : {s:02d}"

    def seconds_to_min_sec_str(self, total_sec):
        if total_sec is None:
            return "---"
        is_neg = total_sec < 0
        total_sec = abs(total_sec)
        m = int(total_sec // 60)
        s = round(total_sec % 60, 2)
        sign = "-" if is_neg else ""
        return f"{sign}{m:02d}' {s:05.2f}\""

    def calculate_set_live(self, data):
        fl_ro_sec = self.parse_angle_to_seconds(data["fl_ro"])
        fr_ro_sec = self.parse_angle_to_seconds(data["fr_ro"])
        
        mean_ro_sec = None
        mean_ro_str = "---"
        if fl_ro_sec is not None and fr_ro_sec is not None:
            half_circle_sec = 648000
            fr_ro_adjusted = fr_ro_sec - half_circle_sec if fr_ro_sec >= half_circle_sec else fr_ro_sec + half_circle_sec
            mean_ro_sec = (fl_ro_sec + fr_ro_adjusted) / 2.0
            mean_ro_str = self.seconds_to_angle_str(mean_ro_sec)
        data["ro_res"].config(text=f"Mean RO: {mean_ro_str}")

        total_seconds = 0
        time_count = 0
        for t in data["times"]:
            h_str = t["hr"].get().strip()
            m_str = t["min"].get().strip()
            if h_str.isdigit() and m_str.isdigit():
                total_seconds += (int(h_str) * 3600 + int(m_str) * 60)
                time_count += 1

        mean_time_str = "---"
        if time_count == 4:
            avg_sec = total_seconds / 4.0
            h = int(avg_sec // 3600) % 24
            m = int((avg_sec % 3600) // 60)
            s = int(round(avg_sec % 60))
            mean_time_str = f"{h:02d} : {m:02d} : {s:02d}"
        data["time_res"].config(text=f"Mean Time: {mean_time_str}")

        hb_total_sec = 0
        hb_count = 0
        half_circle_sec = 648000
        for idx, hb in enumerate(data["hbs"]):
            sec = self.parse_angle_to_seconds(hb)
            if sec is not None:
                if idx in [2, 3]:
                    sec -= half_circle_sec
                hb_total_sec += sec
                hb_count += 1

        mean_hb_str = "---"
        if hb_count == 4:
            mean_hb_str = self.seconds_to_angle_str(hb_total_sec / 4.0)
        data["hb_res"].config(text=f"Mean Hz Bearing: {mean_hb_str}")

        va_reduced_sec_list = []
        for idx, va in enumerate(data["vas"]):
            sec = self.parse_angle_to_seconds(va)
            if sec is not None:
                if idx in [0, 1]:
                    reduced = 324000 - sec
                else:
                    reduced = sec - 972000
                va_reduced_sec_list.append(reduced)

        mean_va_sec = None
        mean_va_str = "---"
        if len(va_reduced_sec_list) == 4:
            mean_va_sec = sum(va_reduced_sec_list) / 4.0
            mean_va_str = self.seconds_to_angle_str(mean_va_sec)
        data["va_res"].config(text=f"Mean Vertical Angle: {mean_va_str}")

        ref_sec = self.parse_min_sec_to_seconds(data["ref_parallax"])
        ref_str = self.seconds_to_min_sec_str(ref_sec) if ref_sec is not None else "---"

        adjusted_vert_str = "---"
        if mean_va_sec is not None and ref_sec is not None:
            adjusted_sec = mean_va_sec - ref_sec
            adjusted_vert_str = self.seconds_to_angle_str(adjusted_sec)

        summary_text = (
            f"Mean RO: {mean_ro_str}\n"
            f"Mean Time: {mean_time_str}\n"
            f"Mean Hz Bearing: {mean_hb_str}\n"
            f"Mean Vertical Angle: {mean_va_str}\n"
            f"Refraction & Parallax: {ref_str}\n"
            f"Adjusted Vertical: {adjusted_vert_str}"
        )
        data["result_lbl"].config(text=summary_text)

        self.calculate_ephemeris_and_final_reduction()

    def calculate_coordinates_live(self):
        c = self.coord_inputs
        try:
            orig_n_val = float(c["orig_n"].get().strip() or 0)
            orig_e_val = float(c["orig_e"].get().strip() or 0)
            stat_n_val = float(c["stat_n"].get().strip() or 0)
            stat_w_val = float(c["stat_w"].get().strip() or 0)

            lat_d = float(c["lat_deg"].get().strip() or 0)
            lat_m = float(c["lat_min"].get().strip() or 0)
            lat_s = float(c["lat_sec"].get().strip() or 0)

            diff_n = stat_n_val - orig_n_val
            diff_w = stat_w_val - orig_e_val

            c["tot_diff_n"].config(text=f"{diff_n:.3f}")
            c["tot_diff_w"].config(text=f"{diff_w:.3f}")

            tot_diff_sec = diff_n * 0.03256
            c["tot_diff_calc"].config(text=self.seconds_to_angle_str(tot_diff_sec))

            diff_long_sec = diff_w * 0.03246
            c["diff_long"].config(text=self.seconds_to_min_sec_str(diff_long_sec))

            lat_orig_dec = lat_d + (lat_m / 60.0) + (lat_s / 3600.0)
            lat_orig_rad = math.radians(lat_orig_dec)

            diff_long_min = diff_long_sec / 60.0
            conv_sec = diff_long_min * math.sin(lat_orig_rad) * 60.0
            c["diff_long_sin"].config(text=self.seconds_to_min_sec_str(conv_sec))
            c["conv"].config(text=self.seconds_to_min_sec_str(conv_sec))

            lat_orig_total_sec = (lat_d * 3600) + (lat_m * 60) + lat_s
            lat_stat_total_sec = lat_orig_total_sec + tot_diff_sec
            c["lat_stat"].config(text=self.seconds_to_angle_str(lat_stat_total_sec))
            
            self.calculate_ephemeris_and_final_reduction()
        except Exception:
            pass

    def calculate_ephemeris_and_final_reduction(self):
        e = self.ephemeris_inputs
        f = self.final_inputs
        try:
            def get_gt_seconds(set_data):
                total_seconds = 0
                count = 0
                for t in set_data["times"]:
                    h_str = t["hr"].get().strip()
                    m_str = t["min"].get().strip()
                    if h_str.isdigit() and m_str.isdigit():
                        total_seconds += (int(h_str) * 3600 + int(m_str) * 60)
                        count += 1
                if count == 4:
                    avg_sec = total_seconds / 4.0
                    gt_sec = avg_sec - (8 * 3600)
                    return gt_sec
                return None

            gt1_sec = get_gt_seconds(self.inputs_set1)
            gt2_sec = get_gt_seconds(self.inputs_set2)

            gt1_str = self.seconds_to_hms_str(gt1_sec + (8 * 3600)) if gt1_sec is not None else "---"
            gt2_str = self.seconds_to_hms_str(gt2_sec + (8 * 3600)) if gt2_sec is not None else "---"

            e["gt1"].config(text=gt1_str)
            e["gt2"].config(text=gt2_str)

            gt1_hours = (gt1_sec / 3600.0) if gt1_sec is not None else None
            gt2_hours = (gt2_sec / 3600.0) if gt2_sec is not None else None

            polar1_sec = None
            if gt1_hours is not None:
                d1_d = float(e["dec1_deg"].get().strip() or 0)
                d1_m = float(e["dec1_min"].get().strip() or 0)
                d1_s = float(e["dec1_sec"].get().strip() or 0)
                v1_sec_input = float(e["v1"].get().strip() or 0)

                diff1_sec = v1_sec_input * gt1_hours
                e["diff1"].config(text=self.seconds_to_min_sec_str(diff1_sec))

                dec1_total_sec = (d1_d * 3600) + (d1_m * 60) + d1_s + diff1_sec
                e["decl_time1"].config(text=self.seconds_to_angle_str(dec1_total_sec))

                polar1_sec = 324000 - dec1_total_sec
                e["polar1"].config(text=self.seconds_to_angle_str(polar1_sec))

            polar2_sec = None
            if gt2_hours is not None:
                d2_d = float(e["dec2_deg"].get().strip() or 0)
                d2_m = float(e["dec2_min"].get().strip() or 0)
                d2_s = float(e["dec2_sec"].get().strip() or 0)
                v2_sec_input = float(e["v2"].get().strip() or 0)

                diff2_sec = v2_sec_input * gt2_hours
                e["diff2"].config(text=self.seconds_to_min_sec_str(diff2_sec))

                dec2_total_sec = (d2_d * 3600) + (d2_m * 60) + d2_s + diff2_sec
                e["decl_time2"].config(text=self.seconds_to_angle_str(dec2_total_sec))

                polar2_sec = 324000 - dec2_total_sec
                e["polar2"].config(text=self.seconds_to_angle_str(polar2_sec))

            lat_str = self.coord_inputs["lat_stat"].cget("text")
            f["lat1"].config(text=lat_str)
            f["lat2"].config(text=lat_str)

            lat_sec = self.parse_angle_string_to_seconds(lat_str)

            def reduce_set(set_data, pol_sec_val, f_adj, f_comp, f_obs, f_diff_az, f_mean_ro, f_true_ro, f_conv, f_grid):
                va_reduced_sec_list = []
                for idx, va in enumerate(set_data["vas"]):
                    sec = self.parse_angle_to_seconds(va)
                    if sec is not None:
                        if idx in [0, 1]:
                            va_reduced_sec_list.append(324000 - sec)
                        else:
                            va_reduced_sec_list.append(sec - 972000)

                ref_sec = self.parse_min_sec_to_seconds(set_data["ref_parallax"])
                
                adj_sec = None
                if len(va_reduced_sec_list) == 4 and ref_sec is not None:
                    adj_sec = (sum(va_reduced_sec_list) / 4.0) - ref_sec
                    f_adj.config(text=self.seconds_to_angle_str(adj_sec))
                else:
                    f_adj.config(text="---")

                comp_sec = None
                if lat_sec is not None and adj_sec is not None and pol_sec_val is not None:
                    lat_rad = math.radians(lat_sec / 3600.0)
                    adj_rad = math.radians(adj_sec / 3600.0)
                    pol_rad = math.radians(pol_sec_val / 3600.0)
                    try:
                        cos_az = (math.cos(pol_rad) - math.sin(lat_rad) * math.sin(adj_rad)) / (math.cos(lat_rad) * math.cos(adj_rad))
                        cos_az = max(-1.0, min(1.0, cos_az))
                        az_rad = math.acos(cos_az)
                        comp_sec = math.degrees(az_rad) * 3600.0
                        f_comp.config(text=self.seconds_to_angle_str(comp_sec))
                    except Exception:
                        f_comp.config(text="---")

                hb_total_sec = 0
                hb_count = 0
                half_circle_sec = 648000
                for idx, hb in enumerate(set_data["hbs"]):
                    sec = self.parse_angle_to_seconds(hb)
                    if sec is not None:
                        if idx in [2, 3]:
                            sec -= half_circle_sec
                        hb_total_sec += sec
                        hb_count += 1
                obs_sec = None
                if hb_count == 4:
                    obs_sec = hb_total_sec / 4.0
                    f_obs.config(text=self.seconds_to_angle_str(obs_sec))
                else:
                    f_obs.config(text="---")

                diff_az_sec = None
                if comp_sec is not None and obs_sec is not None:
                    diff_az_sec = comp_sec - obs_sec
                    f_diff_az.config(text=self.seconds_to_angle_str(diff_az_sec))
                else:
                    f_diff_az.config(text="---")

                fl_ro = self.parse_angle_to_seconds(set_data["fl_ro"])
                fr_ro = self.parse_angle_to_seconds(set_data["fr_ro"])
                mean_ro_sec = None
                if fl_ro is not None and fr_ro is not None:
                    fr_adj = fr_ro - half_circle_sec if fr_ro >= half_circle_sec else fr_ro + half_circle_sec
                    mean_ro_sec = (fl_ro + fr_adj) / 2.0
                    f_mean_ro.config(text=self.seconds_to_angle_str(mean_ro_sec))
                else:
                    f_mean_ro.config(text="---")

                true_ro_sec = None
                if mean_ro_sec is not None and diff_az_sec is not None:
                    true_ro_sec = mean_ro_sec + diff_az_sec
                    f_true_ro.config(text=self.seconds_to_angle_str(true_ro_sec))
                else:
                    f_true_ro.config(text="---")

                conv_str = self.coord_inputs["conv"].cget("text")
                f_conv.config(text=conv_str)
                conv_sec = self.parse_angle_string_to_seconds(conv_str)

                grid_sec = None
                if true_ro_sec is not None and conv_sec is not None:
                    grid_sec = true_ro_sec + conv_sec
                    f_grid.config(text=self.seconds_to_angle_str(grid_sec))
                else:
                    f_grid.config(text="---")

                return grid_sec

            g1 = reduce_set(self.inputs_set1, polar1_sec, f["adj1"], f["comp1"], f["obs1"], f["diff_az1"], f["mean_ro1"], f["true_ro1"], f["conv1"], f["grid1"])
            g2 = reduce_set(self.inputs_set2, polar2_sec, f["adj2"], f["comp2"], f["obs2"], f["diff_az2"], f["mean_ro2"], f["true_ro2"], f["conv2"], f["grid2"])

            if g1 is not None and g2 is not None:
                mean_grid_sec = (g1 + g2) / 2.0
                f["mean_grid"].config(text=self.seconds_to_angle_str(mean_grid_sec))
            else:
                f["mean_grid"].config(text="---")

        except Exception:
            pass

    def parse_angle_string_to_seconds(self, angle_str):
        try:
            parts = angle_str.replace("°", " ").replace("'", " ").replace("\"", " ").split()
            sign = -1 if "-" in angle_str else 1
            nums = [float(p) for p in parts if p.replace('.', '', 1).isdigit()]
            if len(nums) >= 3:
                return sign * (nums[0] * 3600 + nums[1] * 60 + nums[2])
            elif len(nums) == 2:
                return sign * (nums[0] * 60 + nums[1])
        except Exception:
            pass
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = SolarObserverApp(root)
    root.mainloop()