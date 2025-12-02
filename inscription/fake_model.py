def predict_scam(data):
    """
    Dummy AI for testing the interface.
    Only uses the "important" fields for prediction.
    """
    if data["revenue"] < 6000 and data["source_of_income"] == "business":
        return 1  # Scam
    return 0  # Safe
