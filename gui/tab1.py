import customtkinter as ctk
import pandas as pd
from utils.predict_tab1 import predict_velocity
def open_tab1(main_frame):

    # Clear old page
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Load CSV
    df = pd.read_csv("data/tab1.csv")
    first_row = df.iloc[0]
    calibre_values = sorted(df["Calibre"].dropna().astype(str).unique())
    projectile_values = sorted(df["Projectile Type"].dropna().astype(str).unique())
    shape_values = sorted(df["Shape"].dropna().astype(str).unique())
    stype_values = sorted(df["s_type"].dropna().astype(str).unique())
    material_values = sorted(df["Material"].dropna().astype(str).unique())

    # Title
    title = ctk.CTkLabel(
        main_frame,
        text="🚀 Projectile Design Analyzer",
        font=("Segoe UI", 32, "bold")
    )
    title.pack(pady=(15, 5))

    subtitle = ctk.CTkLabel(
        main_frame,
        text="AI Powered Projectile Velocity Prediction",
        font=("Segoe UI", 14)
    )
    subtitle.pack(pady=(0, 10))

    # Scrollable area
    form = ctk.CTkScrollableFrame(main_frame)
    form.pack(fill="both", expand=True, padx=15, pady=10)

    # Dropdowns
    calibre = ctk.CTkComboBox(form, values=list(calibre_values))
    calibre.pack(fill="x", padx=10, pady=5)
    calibre.set(str(first_row["Calibre"]))

    projectile_type = ctk.CTkComboBox(form, values=list(projectile_values))
    projectile_type.pack(fill="x", padx=10, pady=5)
    projectile_type.set(str(first_row["Projectile Type"]))

    shape = ctk.CTkComboBox(form, values=list(shape_values))
    shape.pack(fill="x", padx=10, pady=5)
    shape.set(str(first_row["Shape"]))

    s_type = ctk.CTkComboBox(form, values=list(stype_values))
    s_type.pack(fill="x", padx=10, pady=5)
    s_type.set(str(first_row["s_type"]))

    material = ctk.CTkComboBox(form, values=list(material_values))
    material.pack(fill="x", padx=10, pady=5)
    material.set(str(first_row["Material"]))
        # Numeric fields
    fields = [
        "Projectile Dimension",
        "DAI",
        "Projectile Mass",
        "Total Mass With Sabbot",
        "Petal Burst Pressure",
        "Powder Mass",
        "Breadth",
        "Height",
        "C Drag",
        "Surface Area",
        "Volume",
        "SA / Vol",
        "Density",
        "Moment Of Inerta",
        "CD",
        "Sabo Length"
    ]

    entries = {}

    default_values = {

    "Projectile Dimension": "10.78",
    "DAI": "10.78",
    "Projectile Mass": "13.56",
    "Total Mass With Sabbot": "15.76",
    "Petal Burst Pressure": "60.59",
    "Powder Mass": "3.45",

    "Breadth": "12.03",
    "Height": "13.12",

    "C Drag": "0.809",
    "Surface Area": "365.079",
    "Volume": "655.926",
    "SA / Vol": "0.557",

    "Density": "19300",
    "Moment Of Inerta": "0.1521",

    "CD": "0.107",

    "Sabo Length": "51.22"
}

    for field in fields:

        entry = ctk.CTkEntry(
        form,
        placeholder_text=field
    )

        entry.insert(
        0,
        default_values[field]
    )

        entry.pack(
        fill="x",
        padx=10,
        pady=5
    )

        entries[field] = entry
    def predict():

        try:

            result = predict_velocity(

                calibre.get(),
                projectile_type.get(),

                float(entries["Projectile Dimension"].get()),
                float(entries["DAI"].get()),
                float(entries["Projectile Mass"].get()),
                float(entries["Total Mass With Sabbot"].get()),
                float(entries["Petal Burst Pressure"].get()),
                float(entries["Powder Mass"].get()),

                shape.get(),
                s_type.get(),

                float(entries["Breadth"].get()),
                float(entries["Height"].get()),

                material.get(),

                float(entries["C Drag"].get()),
                float(entries["Surface Area"].get()),
                float(entries["Volume"].get()),
                float(entries["SA / Vol"].get()),
                float(entries["Density"].get()),
                float(entries["Moment Of Inerta"].get()),
                float(entries["CD"].get()),
                float(entries["Sabo Length"].get())

            )

            if result["dataset_found"]:

                source_label.configure(
                    text="✓ Dataset Record Found"
                )

                actual_label.configure(
                    text=f"Actual Velocity : {result['actual_velocity']} m/s"
                )

                predicted_label.configure(
                    text=f"Predicted Velocity : {result['predicted_velocity']} m/s"
                )

                difference_label.configure(
                    text=f"Difference : {result['difference']} m/s"
                )

                accuracy_label.configure(
                    text=f"Accuracy : {result['accuracy']} %"
                )

            else:

                source_label.configure(
                    text="✗ Dataset Record Not Found"
                )

                actual_label.configure(text="")

                predicted_label.configure(
                    text=f"Predicted Velocity : {result['predicted_velocity']} m/s"
                )

                difference_label.configure(text="")

                accuracy_label.configure(text="")

            confidence_label.configure(
                text=f"Confidence : {result['confidence']} %"
            )

            model_label.configure(
                text=f"Best Model : {result['best_model']}"
            )

        except Exception as e:

            source_label.configure(
                text=f"Error : {str(e)}"
            )
    # Predict Button
    predict_btn = ctk.CTkButton(
        form,
        text="🚀 Predict Velocity",
        height=45,
        command=predict
    )
    predict_btn.pack(fill="x", padx=10, pady=15)

    # Results Section
    result_frame = ctk.CTkFrame(form)
    result_frame.pack(fill="x", padx=10, pady=10)

    result_title = ctk.CTkLabel(
        result_frame,
        text="Prediction Results",
        font=("Segoe UI", 20, "bold")
    )
    result_title.pack(pady=10)

    source_label = ctk.CTkLabel(
    result_frame,
    text="Waiting For Prediction...",
    font=("Segoe UI", 18, "bold")
)
    source_label.pack()

    actual_label = ctk.CTkLabel(result_frame, text="")
    actual_label.pack()

    predicted_label = ctk.CTkLabel(result_frame, text="")
    predicted_label.pack()

    difference_label = ctk.CTkLabel(result_frame, text="")
    difference_label.pack()

    accuracy_label = ctk.CTkLabel(result_frame, text="")
    accuracy_label.pack()

    confidence_label = ctk.CTkLabel(result_frame, text="")
    confidence_label.pack()

    model_label = ctk.CTkLabel(result_frame, text="")
    model_label.pack()