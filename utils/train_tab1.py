import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso
)

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor
)

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("data/tab1.csv")

df.columns = df.columns.str.strip()

print("\nDataset Shape:", df.shape)

# ==========================================
# FEATURES
# ==========================================

feature_cols = [

    "Calibre",
    "Projectile Type",
    "Projectile Dimension",
    "dai",
    "projectile mass",
    "total mass with sabbot",
    "Petal burst pressure",
    "powder mass",
    "Shape",
    "s_type",
    "Breadth",
    "Height",
    "Material",
    "c_drag",
    "Surface Area",
    "Volume",
    "SA/vol",
    "Density",
    "Moment of inerta",
    "cd",
    "sabo length"

]

target_col = "Actual Velocity"

# ==========================================
# REMOVE ROWS WHERE TARGET IS MISSING
# ==========================================

df = df.dropna(subset=[target_col])

X = df[feature_cols]
y = df[target_col]

# ==========================================
# CATEGORICAL COLUMNS
# ==========================================

categorical_cols = [

    "Calibre",
    "Projectile Type",
    "Shape",
    "s_type",
    "Material"

]

numeric_cols = [
    col for col in feature_cols
    if col not in categorical_cols
]

# ==========================================
# PREPROCESSOR
# ==========================================

preprocessor = ColumnTransformer(

    transformers=[

        (
            "cat",
            Pipeline([

                (
                    "imputer",
                    SimpleImputer(
                        strategy="most_frequent"
                    )
                ),

                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    )
                )

            ]),
            categorical_cols
        ),

        (
            "num",
            Pipeline([

                (
                    "imputer",
                    SimpleImputer(
                        strategy="median"
                    )
                )

            ]),
            numeric_cols
        )

    ]

)

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,
    random_state=42

)

# ==========================================
# MODELS
# ==========================================

models = {

    "Linear Regression":
        LinearRegression(),

    "Ridge":
        Ridge(),

    "Lasso":
        Lasso(),

    "Decision Tree":
        DecisionTreeRegressor(
            random_state=42
        ),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=300,
            random_state=42
        ),

    "Extra Trees":
        ExtraTreesRegressor(
            n_estimators=300,
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingRegressor(
            random_state=42
        ),

    "XGBoost":
        XGBRegressor(
            random_state=42
        ),

    "LightGBM":
        LGBMRegressor(
            random_state=42
        ),

    "CatBoost":
        CatBoostRegressor(
            verbose=False,
            random_state=42
        )
}

# ==========================================
# TRAIN ALL MODELS
# ==========================================

best_score = -999
best_model = None
best_name = ""

print("\nTraining Models...\n")

for name, model in models.items():

    try:

        pipeline = Pipeline([

            ("preprocessor", preprocessor),

            ("model", model)

        ])

        pipeline.fit(
            X_train,
            y_train
        )

        pred = pipeline.predict(
            X_test
        )

        score = r2_score(
            y_test,
            pred
        )

        print(
            f"{name:<20} : {score:.4f}"
        )

        if score > best_score:

            best_score = score
            best_model = pipeline
            best_name = name

    except Exception as e:

        print(
            f"{name} FAILED -> {e}"
        )

# ==========================================
# CREATE MODELS FOLDER
# ==========================================

import os

os.makedirs(
    "models",
    exist_ok=True
)

# ==========================================
# SAVE BEST MODEL
# ==========================================

joblib.dump(
    best_model,
    "models/velocity_model.pkl"
)

joblib.dump(
    best_name,
    "models/best_model_name.pkl"
)

joblib.dump(
    best_score,
    "models/model_score.pkl"
)

print("\n" + "="*50)

print(
    f"BEST MODEL : {best_name}"
)

print(
    f"BEST SCORE : {best_score:.4f}"
)

print("="*50)

print(
    "\nModel Saved Successfully!"
)