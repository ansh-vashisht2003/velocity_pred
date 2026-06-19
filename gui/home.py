import customtkinter as ctk
from gui.tab1 import open_tab1
from gui.tab2 import open_tab2
from gui.tab3 import open_tab3
from gui.tab4 import open_tab4
# ======================================
# THEME SETTINGS
# ======================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ======================================
# MAIN APP
# ======================================

class ProjectileApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Projectile Analysis System")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        # ==========================
        # SIDEBAR
        # ==========================

        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")

        # Title

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="PROJECTILE\nANALYSIS",
            font=("Segoe UI", 28, "bold")
        )

        self.logo_label.pack(pady=(30, 10))

        self.sub_label = ctk.CTkLabel(
            self.sidebar,
            text="AI Powered Detection System",
            font=("Segoe UI", 12)
        )

        self.sub_label.pack(pady=(0, 30))

        # ==========================
        # NAVIGATION BUTTONS
        # ==========================

        self.btn_tab1 = ctk.CTkButton(
            self.sidebar,
            text="Tab 1 - Projectile Design Analyzer",
            height=50,
            corner_radius=15,
            command=self.launch_tab1
        )

        self.btn_tab1.pack(fill="x", padx=15, pady=8)

        self.btn_tab2 = ctk.CTkButton(
            self.sidebar,
            text="Tab 2 - Target Damage Analysis",
            height=50,
            corner_radius=15,
            command=self.launch_tab2
        )

        self.btn_tab2.pack(fill="x", padx=15, pady=8)

        self.btn_tab3 = ctk.CTkButton(
            self.sidebar,
            text="Tab 3 - Image Based Impact Detection",
            height=50,
            corner_radius=15,
            command=self.launch_tab3
        )

        self.btn_tab3.pack(fill="x", padx=15, pady=8)

        self.btn_tab4 = ctk.CTkButton(
            self.sidebar,
            text="Tab 4 - Projectile Shape Reconstruction",
            height=50,
            corner_radius=15,
            command=self.launch_tab4
        )

        self.btn_tab4.pack(fill="x", padx=15, pady=8)

        # Footer

        self.footer = ctk.CTkLabel(
            self.sidebar,
            text="Final Year AIML Project",
            font=("Segoe UI", 11)
        )

        self.footer.pack(side="bottom", pady=20)

        # ==========================
        # MAIN CONTENT AREA
        # ==========================

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=20
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.show_home()

    # ==================================
    # CLEAR FRAME
    # ==================================

    def clear_main(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ==================================
    # HOME PAGE
    # ==================================

    def show_home(self):

        self.clear_main()

        # Main Title

        title = ctk.CTkLabel(
            self.main_frame,
            text="PROJECTILE ANALYSIS SYSTEM",
            font=("Segoe UI", 38, "bold")
        )

        title.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(
            self.main_frame,
            text="AI Powered Detection & Reconstruction Platform",
            font=("Segoe UI", 18)
        )

        subtitle.pack()

        # Welcome Card

        welcome_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20
        )

        welcome_frame.pack(
            fill="x",
            padx=30,
            pady=30
        )

        welcome_title = ctk.CTkLabel(
            welcome_frame,
            text="Welcome",
            font=("Segoe UI", 28, "bold")
        )

        welcome_title.pack(pady=(20, 10))

        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text="""
    This system uses Artificial Intelligence and Computer Vision
    to analyze projectile specifications, target impacts,
    image-based evidence and shape reconstruction.

    Select a module from the left navigation panel
    to begin analysis.
    """,
            justify="center",
            font=("Segoe UI", 15)
        )

        welcome_text.pack(pady=(0, 20))

        # Feature Cards

        cards_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        cards_frame.pack(pady=20)

        card1 = ctk.CTkButton(
            cards_frame,
            text="🚀\nProjectile Design Analyzer",
            width=220,
            height=120,
            corner_radius=20,
             command=self.launch_tab1
        )

        card1.grid(row=0, column=0, padx=15)

        card2 = ctk.CTkButton(
            cards_frame,
            text="🎯\nTarget Damage Analysis",
            width=220,
            height=120,
            corner_radius=20,
                command=self.launch_tab2
        )

        card2.grid(row=0, column=1, padx=15)

        card3 = ctk.CTkButton(
            cards_frame,
            text="📷\nImage Based Impact Detection",
            width=220,
            height=120,
            corner_radius=20,
                command=self.launch_tab3
        )

        card3.grid(row=0, column=2, padx=15)

        card4 = ctk.CTkButton(
            cards_frame,
            text="🛠️\nProjectile Shape Reconstruction",
            width=220,
            height=120,
            corner_radius=20,
                command=self.launch_tab4
        )

        card4.grid(row=0, column=3, padx=15)

    # ==================================
    # TAB 1
    # ==================================

    def show_tab1(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Tab 1 - Projectile Design Analyzer",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(pady=20)

        calibre = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter Calibre"
        )
        calibre.pack(pady=10)

        mass = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter Projectile Mass"
        )
        mass.pack(pady=10)

        material = ctk.CTkComboBox(
            self.main_frame,
            values=["Steel", "Aluminum", "Tungsten"]
        )
        material.pack(pady=10)

        predict_btn = ctk.CTkButton(
            self.main_frame,
            text="Predict Velocity"
        )

        predict_btn.pack(pady=20)

    # ==================================
    # TAB 2
    # ==================================

    def show_tab2(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Tab 2 - Target Damage Analysis",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(pady=20)

        diameter = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Hole Diameter"
        )

        diameter.pack(pady=10)

        depth = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Penetration Depth"
        )

        depth.pack(pady=10)

        analyze_btn = ctk.CTkButton(
            self.main_frame,
            text="Analyze"
        )

        analyze_btn.pack(pady=20)

    # ==================================
    # TAB 3
    # ==================================

    def show_tab3(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Tab 3 - Image Based Impact Detection",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(pady=20)

        upload_btn = ctk.CTkButton(
            self.main_frame,
            text="Upload Image"
        )

        upload_btn.pack(pady=30)

        result = ctk.CTkLabel(
            self.main_frame,
            text="Classification Result"
        )

        result.pack()

    # ==================================
    # TAB 4
    # ==================================

    def show_tab4(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Tab 4 - Projectile Shape Reconstruction",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(pady=20)

        upload_btn = ctk.CTkButton(
            self.main_frame,
            text="Upload Impact Image"
        )

        upload_btn.pack(pady=30)

        result = ctk.CTkLabel(
            self.main_frame,
            text="Generated Sketch Appears Here"
        )

        result.pack()
    def launch_tab1(self):
        open_tab1(self.main_frame)

    def launch_tab2(self):
        open_tab2(self.main_frame)

    def launch_tab3(self):
        open_tab3(self.main_frame)

    def launch_tab4(self):
        open_tab4(self.main_frame)

# ======================================
# RUN APP
# ======================================

if __name__ == "__main__":
    app = ProjectileApp()
    app.mainloop()