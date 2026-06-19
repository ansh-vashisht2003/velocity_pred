import customtkinter as ctk
import pandas as pd
from utils.predict_tab2 import predict_perforation

def open_tab2(main_frame):
    # Clear old page
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Load CSV to get dropdown values and defaults
    try:
        df = pd.read_csv("data/tab2.csv")
        first_row = df.iloc[0]
        
        # Categorical features for dropdowns
        cat_features = {
            "Calibre": sorted(df["Calibre"].dropna().astype(str).unique()),
            "Projectile Type": sorted(df["Projectile Type"].dropna().astype(str).unique()),
            "Shape": sorted(df["Shape"].dropna().astype(str).unique()),
            "s_type": sorted(df["s_type"].dropna().astype(str).unique()),
            "Material": sorted(df["Material"].dropna().astype(str).unique()),
            "Plate Material": sorted(df["Plate Material"].dropna().astype(str).unique())
        }
    except Exception as e:
        print(f"Error loading tab2.csv: {e}")
        return

    # Title
    title = ctk.CTkLabel(
        main_frame,
        text="🛡️ Target Perforation Predictor",
        font=("Segoe UI", 32, "bold")
    )
    title.pack(pady=(15, 5))

    subtitle = ctk.CTkLabel(
        main_frame,
        text="AI Powered Armor Penetration Analysis",
        font=("Segoe UI", 14)
    )
    subtitle.pack(pady=(0, 10))

    # Scrollable area
    form = ctk.CTkScrollableFrame(main_frame)
    form.pack(fill="both", expand=True, padx=15, pady=10)

    # Dictionary to hold our input widget references
    dropdowns = {}
    entries = {}

    # Create Dropdowns
    for field, values in cat_features.items():
        dropdown = ctk.CTkComboBox(form, values=list(values))
        dropdown.pack(fill="x", padx=10, pady=5)
        dropdown.set(str(first_row[field]))
        dropdowns[field] = dropdown

    # Numeric fields based on tab2.csv
    num_fields = [
        "Projectile Dimension", "dia", "Projectile Mass", "Total Mass with Sabot", 
        "Petal Burst Pressure", "Powder Mass", "Actual Velocity", "Expected Velocity", 
        "Breadth", "Height", "c_drag", "Surface Area", "Volume", "SA/Vol", "Density", 
        "Moment of Inertia", "cd", "Sabot Length", "Plate Thickness", "Impact Angle", 
        "Kinetic Energy"
    ]

    for field in num_fields:
        entry = ctk.CTkEntry(form, placeholder_text=field)
        entry.insert(0, str(first_row.get(field, "0.0")))
        entry.pack(fill="x", padx=10, pady=5)
        entries[field] = entry

    def predict():
        try:
            # Collect data from GUI
            input_data = {field: dropdown.get() for field, dropdown in dropdowns.items()}
            for field, entry in entries.items():
                input_data[field] = float(entry.get())

            # Call AIML backend
            result = predict_perforation(input_data)

            if result["dataset_found"]:
                source_label.configure(text="✓ Dataset Record Found", text_color="#00FF00")
                actual_label.configure(text=f"Actual Result: {'Perforated' if result['actual_perforated'] == 1 else 'Not Perforated'}")
            else:
                source_label.configure(text="✗ Dataset Record Not Found (New Data)", text_color="#FFA500")
                actual_label.configure(text="")

            prediction_text = "💥 PERFORATED" if result['predicted_perforated'] == 1 else "🛡️ NOT PERFORATED"
            predicted_label.configure(text=f"Prediction: {prediction_text}")
            confidence_label.configure(text=f"Confidence: {result['confidence']:.2f}%")
            model_label.configure(text=f"Model Used: {result['best_model']}")

        except ValueError as ve:
            source_label.configure(text="Error: Please ensure all numeric fields contain valid numbers.", text_color="red")
        except Exception as e:
            source_label.configure(text=f"Error: {str(e)}", text_color="red")

    # Predict Button
    predict_btn = ctk.CTkButton(
        form,
        text="⚡ Analyze Perforation",
        height=45,
        command=predict,
        fg_color="#4B0082", # A deep purple theme accent 
        hover_color="#3A0066"
    )
    predict_btn.pack(fill="x", padx=10, pady=15)

    # Results Section
    result_frame = ctk.CTkFrame(form)
    result_frame.pack(fill="x", padx=10, pady=10)

    result_title = ctk.CTkLabel(result_frame, text="Prediction Results", font=("Segoe UI", 20, "bold"))
    result_title.pack(pady=10)

    source_label = ctk.CTkLabel(result_frame, text="Waiting For Prediction...", font=("Segoe UI", 16, "bold"))
    source_label.pack()

    actual_label = ctk.CTkLabel(result_frame, text="", font=("Segoe UI", 14))
    actual_label.pack()

    predicted_label = ctk.CTkLabel(result_frame, text="", font=("Segoe UI", 18, "bold"))
    predicted_label.pack(pady=5)

    confidence_label = ctk.CTkLabel(result_frame, text="", font=("Segoe UI", 14))
    confidence_label.pack()

    model_label = ctk.CTkLabel(result_frame, text="", font=("Segoe UI", 12))
    model_label.pack(pady=(5, 10))