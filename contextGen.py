# large dictionary of written context for themes and column definitions

# contextGen.py

CONTEXT = {
    "addresses": {
        "theme_context": (
            "The following data contains structured address information. "
            "Each row represents a physical location associated with an entity."
        ),
        "columns": {
            "country": "Country code or name for the address record.",
            "datasets": "Identifier of the source dataset or collection.",
            "address_level_1": "Top-level administrative area (e.g., state, province, region).",
            "address_level_2": "Second-level administrative area (e.g., county, district).",
            "address_level_3": "Third-level administrative area (e.g., city, municipality, village).",
            "change_type": "Type of change recorded for this row (e.g., added, removed, modified).",
            "average_geometry_length_km": "Average length of geometries (in kilometers) for these addresses.",
            "total_geometry_length_km": "Total summed geometry length (in kilometers) for these addresses.",
            "average_geometry_area_km2": "Average geometry area in square kilometers.",
            "total_geometry_area_km2": "Total geometry area in square kilometers.",
            "id_count": "Count of unique identifier values in this group.",
            "geometry_count": "Number of geometry objects present.",
            "bbox_count": "Number of bounding boxes calculated.",
            "country_count": "Count of address rows aggregated by country in this group.",
            "postcode_count": "Number of postcode/ZIP code values present.",
            "street_count": "Number of street-level address components present.",
            "number_count": "Number of house/building number values present.",
            "unit_count": "Number of unit/apartment values present.",
            "address_levels_count": "Count of address levels populated for the address (how many of the level fields are non-empty).",
            "postal_city_count": "Number of postal city values present.",
            "version_count": "Number of distinct data versions referenced.",
            "sources_count": "Number of distinct data sources contributing to these rows.",
            "total_count": "Total number of address rows in this aggregated record."
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
