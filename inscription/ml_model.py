import joblib
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "../risk_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "../scaler.pkl"))
encoder = joblib.load(os.path.join(BASE_DIR, "../encoder.pkl"))

# Les colonnes exactes utilisées pendant l'entraînement
TRAIN_COLUMNS = joblib.load(os.path.join(BASE_DIR, "../train_columns.pkl"))
# (je t'explique juste après si ce fichier manque)

def prepare_features(data_dict):
    df = pd.DataFrame([data_dict])

    # Remove any unexpected columns (like is_sensitive)
    if "is_sensitive" in df.columns:
        df = df.drop(columns=["is_sensitive"])

    # Numerical columns
    num_cols = ["age", "revenue"]

    # Scale numerical values (only those used in training)
    df[num_cols] = scaler.transform(df[num_cols])

    # Encode categorical variables
    cat_cols = ["country", "residence", "profession",
                "source_of_income", "account_purpose"]

    encoded = encoder.transform(df[cat_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(cat_cols))

    # Final dataset = numerical + encoded categorical
    df_final = pd.concat([df[num_cols].reset_index(drop=True),
                          encoded_df.reset_index(drop=True)], axis=1)

    # Keep only columns used during training
    df_final = df_final.reindex(columns=TRAIN_COLUMNS, fill_value=0)

    return df_final

def predict_with_business_rule(data_dict):
    """
    Applique pipeline ML + règle métier.
    """
    df_ready = prepare_features(data_dict)

    pred = model.predict(df_ready)[0]

    # Règle métier
    if df_ready.loc[0, "is_sensitive"] == 1:
        pred = 1

    return int(pred)