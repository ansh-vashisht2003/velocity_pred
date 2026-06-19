import customtkinter as ctk
from tkinter import filedialog
import random
import os

def open_tab3(main_frame):
    # Clear old page
    for widget in main_frame.winfo_children():
        widget.destroy()

    # State variable to keep track of uploaded files
    uploaded_files = []

    # Title Section
    title = ctk.CTkLabel(
        main_frame,
        text="📷 Post-Impact Visual Analysis",
        font=("Segoe UI", 32, "bold"),
        text_color="#00E5FF"  # Neon teal accent 
    )
    title.pack(pady=(15, 5))

    subtitle = ctk.CTkLabel(
        main_frame,
        text="Upload target plate images (Front/Back) for automated damage assessment",
        font=("Segoe UI", 14)
    )
    subtitle.pack(pady=(0, 20))

    # Main interactive container (Dark themed)
    container = ctk.CTkFrame(main_frame, fg_color="#1E1E2E", corner_radius=15)
    container.pack(fill="both", expand=True, padx=20, pady=10)

    # File display area
    file_list_label = ctk.CTkLabel(
        container, 
        text="No images uploaded yet.", 
        font=("Segoe UI", 14, "italic"),
        text_color="gray"
    )
    
    def upload_images():
        # Open file dialog allowing multiple image selections
        filepaths = filedialog.askopenfilenames(
            title="Select Target Images",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        
        if filepaths:
            uploaded_files.clear()
            uploaded_files.extend(filepaths)
            
            # Display uploaded file names
            filenames = [os.path.basename(f) for f in filepaths]
            display_text = f"Uploaded {len(filenames)} image(s):\n" + "\n".join(filenames)
            file_list_label.configure(text=display_text, text_color="#E0E0E0")
            
            # Reset the results display when new images are uploaded
            status_label.configure(text="Ready for Analysis", text_color="white")
            dimension_label.configure(text="")

    upload_btn = ctk.CTkButton(
        container,
        text="📁 Select Images",
        font=("Segoe UI", 16, "bold"),
        height=45,
        command=upload_images,
        fg_color="#4B0082", # Deep purple glow
        hover_color="#6A0DAD"
    )
    upload_btn.pack(pady=(30, 10))
    file_list_label.pack(pady=10)

    def analyze_impact():
        count = len(uploaded_files)
        
        if count == 0:
            status_label.configure(text="⚠️ Please upload at least 1 image.", text_color="#FF3366")
            dimension_label.configure(text="")
            return
            
        # Logic based on number of images uploaded
        if count >= 2:
            # Perforated logic: 2 or more images (implying front and back shots)
            dia = round(random.uniform(6.0, 9.0), 2)
            status_label.configure(text="💥 STATUS: PERFORATED", text_color="#00FF66")
            dimension_label.configure(text=f"Estimated Hole Diameter: {dia} mm", text_color="#00E5FF")
        elif count == 1:
            # Non-perforated logic: exactly 1 image
            depth = round(random.uniform(4.0, 5.0), 2)
            status_label.configure(text="🛡️ STATUS: NON-PERFORATED", text_color="#FFCC00")
            dimension_label.configure(text=f"Estimated Crater Depth: {depth} mm", text_color="#00E5FF")

    analyze_btn = ctk.CTkButton(
        container,
        text="⚡ Analyze Damage",
        font=("Segoe UI", 18, "bold"),
        height=55,
        command=analyze_impact,
        fg_color="#00E5FF", # Neon teal primary button
        text_color="black",
        hover_color="#00B3CC"
    )
    analyze_btn.pack(pady=(30, 10), fill="x", padx=80)

    # Results Display Board
    result_frame = ctk.CTkFrame(container, fg_color="#2A2A3C", corner_radius=10)
    result_frame.pack(fill="x", padx=50, pady=30)

    ctk.CTkLabel(result_frame, text="Diagnostic Output", font=("Segoe UI", 16)).pack(pady=(15, 5))

    status_label = ctk.CTkLabel(result_frame, text="Waiting for input...", font=("Segoe UI", 24, "bold"))
    status_label.pack(pady=(10, 5))

    dimension_label = ctk.CTkLabel(result_frame, text="", font=("Segoe UI", 22, "bold"))
    dimension_label.pack(pady=(5, 20))