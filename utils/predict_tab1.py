import pandas as pd
import joblib
import numpy as np
# ==========================
# LOAD SAVED FILES
# ==========================

model = joblib.load(
    "models/velocity_model.pkl"
)

best_model = joblib.load(
    "models/best_model_name.pkl"
)

model_score = joblib.load(
    "models/model_score.pkl"
)

# ==========================
# PREDICTION FUNCTION
# ==========================

def predict_velocity(

    calibre,
    projectile_type,
    projectile_dimension,
    dai,
    projectile_mass,
    total_mass_with_sabbot,
    petal_burst_pressure,
    powder_mass,
    shape,
    s_type,
    breadth,
    height,
    material,
    c_drag,
    surface_area,
    volume,
    sa_vol,
    density,
    moment_of_inerta,
    cd,
    sabo_length

):

    input_data = pd.DataFrame([{

        "Calibre": calibre,
        "Projectile Type": projectile_type,
        "Projectile Dimension": projectile_dimension,
        "dai": dai,
        "projectile mass": projectile_mass,
        "total mass with sabbot": total_mass_with_sabbot,
        "Petal burst pressure": petal_burst_pressure,
        "powder mass": powder_mass,
        "Shape": shape,
        "s_type": s_type,
        "Breadth": breadth,
        "Height": height,
        "Material": material,
        "c_drag": c_drag,
        "Surface Area": surface_area,
        "Volume": volume,
        "SA/vol": sa_vol,
        "Density": density,
        "Moment of inerta": moment_of_inerta,
        "cd": cd,
        "sabo length": sabo_length

    }])

    # ==========================
    # PREDICT
    # ==========================

    prediction = float(
        model.predict(input_data)[0]
    )

    confidence = round(
        model_score * 100,
        2
    )

    # ==========================
    # CHECK DATASET
    # ==========================

    df = pd.read_csv("data/tab1.csv")

    df.columns = df.columns.str.strip()
    print("\nINPUT VALUES")
    print("Calibre:", calibre)
    print("Projectile Type:", projectile_type)
    print("Shape:", shape)
    print("s_type:", s_type)
    print("Material:", material)
    match = df[

    (df["Calibre"].astype(str).str.strip().str.lower()
 == str(calibre).strip().lower())
    &
    (df["Projectile Type"].astype(str).str.strip().str.lower()
 == str(projectile_type).strip().lower())
    &
    np.isclose(df["Projectile Dimension"].astype(float), float(projectile_dimension), atol=0.01)
    &
    np.isclose(df["dai"].astype(float), float(dai), atol=0.01)
    &
    np.isclose(df["projectile mass"].astype(float), float(projectile_mass), atol=0.01)
    &
    np.isclose(df["total mass with sabbot"].astype(float), float(total_mass_with_sabbot), atol=0.01)
    &
    np.isclose(df["Petal burst pressure"].astype(float), float(petal_burst_pressure), atol=0.01)
    &
    np.isclose(df["powder mass"].astype(float), float(powder_mass), atol=0.01)
    &
    (df["Shape"].astype(str).str.strip().str.lower()
 == str(shape).strip().lower())
    &
    (df["s_type"].astype(str).str.strip().str.lower()
 == str(s_type).strip().lower())
    &
    np.isclose(df["Breadth"].astype(float), float(breadth), atol=0.01)
    &
    np.isclose(df["Height"].astype(float), float(height), atol=0.01)
    &
    (df["Material"].astype(str).str.strip().str.lower()
 == str(material).strip().lower())
    &
    np.isclose(df["c_drag"].astype(float), float(c_drag), atol=0.01)
    &
    np.isclose(df["Surface Area"].astype(float), float(surface_area), atol=0.01)
    &
    np.isclose(df["Volume"].astype(float), float(volume), atol=0.01)
    &
    np.isclose(df["SA/vol"].astype(float), float(sa_vol), atol=0.01)
    &
    np.isclose(df["Density"].astype(float), float(density), atol=0.01)
    &
    np.isclose(df["Moment of inerta"].astype(float), float(moment_of_inerta), atol=0.01)
    &
    np.isclose(df["cd"].astype(float), float(cd), atol=0.01)
    &
    np.isclose(df["sabo length"].astype(float), float(sabo_length), atol=0.01)

]
    print("Rows Found:", len(match))

    # ==========================
    # DATA FOUND
    # ==========================

    if not match.empty:

        actual_velocity = float(
            match.iloc[0]["Actual Velocity"]
        )

        difference = abs(
            actual_velocity -
            prediction
        )

        accuracy = max(
            0,
            100 -
            (
                difference /
                actual_velocity * 100
            )
        )

        return {

            "dataset_found": True,

            "actual_velocity":
                round(actual_velocity, 2),

            "predicted_velocity":
                round(prediction, 2),

            "difference":
                round(difference, 2),

            "accuracy":
                round(accuracy, 2),

            "confidence":
                confidence,

            "best_model":
                best_model

        }

    # ==========================
    # DATA NOT FOUND
    # ==========================

    return {

        "dataset_found": False,

        "predicted_velocity":
            round(prediction, 2),

        "confidence":
            confidence,

        "best_model":
            best_model

    }