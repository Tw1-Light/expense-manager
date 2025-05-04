def predict_category(text):
    text = text.lower()
    if any(word in text for word in ["grocery", "supermarket", "mart", "store"]):
        return "Groceries"
    elif any(word in text for word in ["hospital", "pharmacy", "clinic", "medicine"]):
        return "Medical"
    elif any(word in text for word in ["electric", "gas", "water", "internet", "bill"]):
        return "Utilities"
    elif any(word in text for word in ["movie", "netflix", "game", "theatre", "entertainment"]):
        return "Entertainment"
    elif any(word in text for word in ["uber", "taxi", "bus", "train", "transport"]):
        return "Transportation"
    else:
        return "Others"
