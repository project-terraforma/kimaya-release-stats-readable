# large dictionary of written context for themes and column definitions

# contextGen.py

CONTEXT = {
    "addresses": {
        "theme_context": (
            "The following data contains structured address information. "
            "Each row represents a physical location associated with an entity."
        ),
        "columns": {
            "street": "Street address including house number and street name.",
            "city": "City where the address is located.",
            "state": "State or province abbreviation.",
            "zip": "Postal or ZIP code.",
            "country": "Country name."
        }
    }
}


def generate_context(theme: str) -> str:
    """Returns formatted context block for a given theme."""
    if theme not in CONTEXT:
        return ""

    theme_data = CONTEXT[theme]

    lines = []
    lines.append(f"Theme: {theme}")
    lines.append(theme_data["theme_context"])
    lines.append("Column Definitions:")

    for col, desc in theme_data["columns"].items():
        lines.append(f"- {col}: {desc}")

    return "\n".join(lines) + "\n\n"
