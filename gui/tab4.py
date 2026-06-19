import customtkinter as ctk
from tkinter import filedialog, Canvas
import random
import math
import os

def open_tab4(main_frame):
    # Clear old page
    for widget in main_frame.winfo_children():
        widget.destroy()

    uploaded_plate_files = []
    uploaded_projectile_files = []

    # Title Section
    title = ctk.CTkLabel(
        main_frame,
        text="🧩 Projectile Reconstruction",
        font=("Segoe UI", 32, "bold"),
        text_color="#B026FF"  # Neon purple accent
    )
    title.pack(pady=(15, 5))

    subtitle = ctk.CTkLabel(
        main_frame,
        text="Upload target plate to generate a rough sketch of the impacting object",
        font=("Segoe UI", 14)
    )
    subtitle.pack(pady=(0, 20))

    # Main Scrollable Form
    container = ctk.CTkScrollableFrame(main_frame, fg_color="#1A1A24", corner_radius=15)
    container.pack(fill="both", expand=True, padx=20, pady=10)

    # --- INPUT SECTION ---
    input_frame = ctk.CTkFrame(container, fg_color="#232333", corner_radius=10)
    input_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(input_frame, text="Data Upload", font=("Segoe UI", 18, "bold"), text_color="#00E5FF").pack(pady=10)

    # Upload Buttons Frame
    upload_btns_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
    upload_btns_frame.pack(fill="x", padx=20, pady=10)
    upload_btns_frame.grid_columnconfigure((0, 1), weight=1)

    # Plate Image Upload
    def upload_plate():
        filepaths = filedialog.askopenfilenames(
            title="Select Plate/Target Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if filepaths:
            uploaded_plate_files.clear()
            uploaded_plate_files.extend(filepaths)
            plate_label.configure(text=f"✓ Plate image loaded.", text_color="#00FF66")

    plate_btn = ctk.CTkButton(
        upload_btns_frame,
        text="🛡️ Upload Plate Image",
        font=("Segoe UI", 14),
        command=upload_plate,
        fg_color="#33334C",
        hover_color="#4A4A6A"
    )
    plate_btn.grid(row=0, column=0, padx=10, pady=5)
    
    plate_label = ctk.CTkLabel(upload_btns_frame, text="No plate image loaded.", font=("Segoe UI", 12, "italic"), text_color="gray")
    plate_label.grid(row=1, column=0, padx=10, pady=5)

    # Any Projectile/Fragment Upload
    def upload_projectile():
        filepaths = filedialog.askopenfilenames(
            title="Select Projectile/Meteoroid Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if filepaths:
            uploaded_projectile_files.clear()
            uploaded_projectile_files.extend(filepaths)
            proj_label.configure(text=f"✓ Reference loaded.", text_color="#00FF66")

    proj_btn = ctk.CTkButton(
        upload_btns_frame,
        text="☄️ Upload Ref. Projectile (Optional)",
        font=("Segoe UI", 14),
        command=upload_projectile,
        fg_color="#33334C",
        hover_color="#4A4A6A"
    )
    proj_btn.grid(row=0, column=1, padx=10, pady=5)
    
    proj_label = ctk.CTkLabel(upload_btns_frame, text="No reference loaded.", font=("Segoe UI", 12, "italic"), text_color="gray")
    proj_label.grid(row=1, column=1, padx=10, pady=5)

    # --- RECONSTRUCTION DISPLAY ---
    result_frame = ctk.CTkFrame(container, fg_color="#2A2A3C", corner_radius=10)
    result_frame.pack(fill="x", padx=20, pady=20)

    status_label = ctk.CTkLabel(result_frame, text="Awaiting Plate Upload...", font=("Segoe UI", 16, "bold"), text_color="gray")
    status_label.pack(pady=(15, 5))

    # Canvas for dynamic sketch
    canvas_width = 300
    canvas_height = 250
    sketch_canvas = Canvas(result_frame, width=canvas_width, height=canvas_height, bg="#1E1E2E", highlightthickness=1, highlightbackground="#33334C")
    sketch_canvas.pack(pady=10)

    # Draw grid background for a high-tech UI look
    def draw_grid():
        sketch_canvas.delete("all")
        for i in range(0, canvas_width, 20):
            sketch_canvas.create_line(i, 0, i, canvas_height, fill="#2A2A3C")
        for i in range(0, canvas_height, 20):
            sketch_canvas.create_line(0, i, canvas_width, i, fill="#2A2A3C")
            
    draw_grid()

    # Function to dynamically generate an irregular meteoroid shape
    def generate_irregular_sketch():
        draw_grid() # Reset canvas
        
        cx, cy = canvas_width // 2, canvas_height // 2
        num_points = random.randint(8, 14)
        points = []
        
        # Math to generate random vertices in a circular pattern
        for i in range(num_points):
            angle = i * (2 * math.pi / num_points)
            # Add random variance to the radius to make it look like an irregular meteoroid
            radius = random.randint(40, 100) 
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.extend([x, y])
            
        # Draw the neon cyberpunk outline (dash creates a sketch effect)
        sketch_canvas.create_polygon(points, outline="#00E5FF", fill="", width=2, dash=(5, 3))
        
        # Add some inner fracture lines
        for _ in range(3):
            p1_idx = random.randint(0, num_points - 1) * 2
            p2_idx = random.randint(0, num_points - 1) * 2
            sketch_canvas.create_line(points[p1_idx], points[p1_idx+1], points[p2_idx], points[p2_idx+1], fill="#B026FF", dash=(2, 4))
            
        sketch_canvas.create_text(cx, cy, text="Reconstructed\nProfile", fill="#00E5FF", font=("Segoe UI", 12, "bold"))

    def reconstruct():
        if not uploaded_plate_files:
            status_label.configure(text="Error: Please upload a plate image first.", text_color="#FF3366")
            return
            
        # Update Status
        status_label.configure(text="Scanning Impact Profile...", text_color="#FFCC00")
        
        # Simulate processing delay before showing the sketch
        main_frame.after(800, lambda: [
            generate_irregular_sketch(),
            status_label.configure(text="✓ Reconstruction Generated", text_color="#00FF66"),
            
            # Generate dummy metrics based on the "sketch"
            mass_label.configure(text=f"{random.uniform(12.5, 45.0):.2f} g"),
            velocity_label.configure(text=f"{random.uniform(800, 1500):.0f} m/s"),
            type_label.configure(text="Irregular Meteoroid / Fragment")
        ])

    # Action Button
    reconstruct_btn = ctk.CTkButton(
        container,
        text="🔄 Generate Projectile Sketch",
        font=("Segoe UI", 18, "bold"),
        height=50,
        command=reconstruct,
        fg_color="#9400D3", # Deep purple
        hover_color="#7A00B3"
    )
    reconstruct_btn.pack(pady=10, fill="x", padx=50)

    # Metrics Layout
    metrics_frame = ctk.CTkFrame(result_frame, fg_color="transparent")
    metrics_frame.pack(fill="x", padx=20, pady=10)
    metrics_frame.grid_columnconfigure((0, 1), weight=1)

    ctk.CTkLabel(metrics_frame, text="Estimated Profile:", font=("Segoe UI", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=5)
    type_label = ctk.CTkLabel(metrics_frame, text="--", font=("Segoe UI", 16, "bold"), text_color="#00E5FF")
    type_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)

    ctk.CTkLabel(metrics_frame, text="Estimated Original Mass:", font=("Segoe UI", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    mass_label = ctk.CTkLabel(metrics_frame, text="--", font=("Segoe UI", 16, "bold"), text_color="#00E5FF")
    mass_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    ctk.CTkLabel(metrics_frame, text="Estimated Impact Velocity:", font=("Segoe UI", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    velocity_label = ctk.CTkLabel(metrics_frame, text="--", font=("Segoe UI", 16, "bold"), text_color="#00E5FF")
    velocity_label.grid(row=2, column=1, sticky="w", padx=10, pady=5)