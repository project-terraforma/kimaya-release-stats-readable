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
    },

    "base": {
        "theme_context": (
            "Base theme aggregates fundamental geographic features such as land, water, "
            "land use and infrastructure primitives. Each row summarizes a class or category."
        ),
        "columns": {
            "datasets": "Source dataset or collection identifier.",
            "class": "High-level class or category name (e.g., land, water, infrastructure).",
            "change_type": "Type of change (added, removed, modified).",
            "average_geometry_area_km2": "Average feature area in square kilometers.",
            "total_geometry_area_km2": "Total area covered by features in square kilometers.",
            "average_geometry_length_km": "Average length for linear features in kilometers.",
            "total_geometry_length_km": "Total length for linear features in kilometers.",
            "id_count": "Count of unique identifiers in this aggregated class.",
            "geometry_count": "Number of geometry objects recorded.",
            "version_count": "Number of distinct data versions referenced.",
            "sources_count": "Number of distinct sources contributing to this class.",
            "total_count": "Total number of items/rows in this aggregated record."
        }
    },

    "land": {
        "theme_context": (
            "Land-related datasets record land cover and land use categories, with area "
            "and count metrics per category or tile."
        ),
        "columns": {
            "land_cover_type": "Category of land cover or land use (e.g., urban, forest, agriculture).",
            "coverage_area_km2": "Area covered by this category, in square kilometers.",
            "percent_coverage": "Percent of the study area covered by this category.",
            "average_elevation_m": "Average elevation in meters for features in this class.",
            "id_count": "Count of unique feature identifiers.",
            "geometry_count": "Number of geometries present.",
            "version_count": "Number of dataset versions referenced.",
            "total_count": "Total rows or features aggregated for this class."
        }
    },

    "infrastructure": {
        "theme_context": (
            "Infrastructure records capture engineered features such as bridges, pipes, "
            "powerlines, and other utility or civic structures with capacity and status metrics."
        ),
        "columns": {
            "infra_type": "Type of infrastructure (e.g., bridge, pipeline, powerline, facility).",
            "subtype": "More specific subtype or classification.",
            "capacity": "Reported capacity (units depend on type, e.g., vehicles, volume, MW).",
            "status": "Operational status (e.g., active, decommissioned, planned).",
            "length_km": "Length in kilometers for linear infrastructure.",
            "area_km2": "Area footprint in square kilometers where applicable.",
            "id_count": "Count of unique identifiers for infrastructure items.",
            "geometry_count": "Number of geometry records.",
            "version_count": "Number of data versions referenced.",
            "total_count": "Total aggregated items in this record."
        }
    },

    "buildings": {
        "theme_context": (
            "Building and building-part datasets contain structural attributes for built "
            "objects, including area, height, function, and counts of apartments/units."
        ),
        "columns": {
            "building_type": "Type or class of building (e.g., residential, commercial, industrial).",
            "building_part": "Indicator for building components or parts (if applicable).",
            "area_m2": "Footprint area in square meters.",
            "height_m": "Reported or estimated building height in meters.",
            "levels_count": "Number of levels/floors recorded.",
            "unit_count": "Number of residential/commercial units within the building.",
            "use_type": "Primary use classification (e.g., apartment, office, school).",
            "year_built": "Construction year or best-estimate of construction date.",
            "id_count": "Unique identifier count.",
            "geometry_count": "Number of geometry objects representing building footprints.",
            "total_count": "Total building records aggregated."
        }
    },

    "divisions": {
        "theme_context": (
            "Administrative division datasets summarize polygons such as countries, "
            "states, counties, municipalities and provide area/length metrics and identifiers."
        ),
        "columns": {
            "division_level": "Administrative level (e.g., country, state, county, municipality).",
            "division_name": "Official name of the administrative division.",
            "parent_id": "Identifier for the parent administrative unit where applicable.",
            "area_km2": "Area of the division in square kilometers.",
            "boundary_length_km": "Perimeter length of the division boundary in kilometers.",
            "population": "Population count if available from source metadata.",
            "id_count": "Unique identifier count for division geometries.",
            "geometry_count": "Number of geometries in this aggregation.",
            "version_count": "Number of distinct data versions referenced.",
            "total_count": "Total aggregated division records."
        }
    },

    "places": {
        "theme_context": (
            "Place-level datasets list named places (cities, towns, villages, points of "
            "interest) with population, location, and bounding metrics."
        ),
        "columns": {
            "place_name": "Canonical name of the place or point of interest.",
            "place_type": "Type/class of place (e.g., city, town, village, POI).",
            "population": "Reported population for the place, when available.",
            "centroid_lat": "Latitude of the feature centroid.",
            "centroid_lon": "Longitude of the feature centroid.",
            "bbox_area_km2": "Area of the bounding box in square kilometers.",
            "id_count": "Unique identifier count.",
            "geometry_count": "Number of geometries representing the place.",
            "version_count": "Number of dataset versions referenced.",
            "total_count": "Total place records aggregated."
        }
    },

    "transportation": {
        "theme_context": (
            "Transportation datasets include linear and node features such as road segments, "
            "connectors, and other network elements with length, type, and lane attributes."
        ),
        "columns": {
            "segment_type": "Type of transportation segment (e.g., primary, secondary, footway).",
            "length_km": "Segment length in kilometers.",
            "lanes": "Number of traffic lanes where available.",
            "is_one_way": "Boolean indicator whether the segment is one-way.",
            "surface_type": "Surface classification (e.g., paved, gravel, dirt).",
            "max_speed_kph": "Maximum speed limit in kilometers per hour, if available.",
            "connector_flag": "Indicator for short connectors or interchanges.",
            "geometry_count": "Number of geometry objects in this aggregation.",
            "id_count": "Unique identifier count.",
            "total_count": "Total aggregated transportation records."
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

    # Guidance for summarization consumers (ensure summaries contain the
    # information needed to answer questions in test_sample_questions.csv).
    lines.append("")
    lines.append("Summary guidance: When producing a summary for this theme, include the concrete numeric and categorical facts another model would need to answer evaluation questions (totals, top-N lists, distributions, percentiles, examples of full rows, and per-release change counts). Label sections clearly and include units where applicable.")

    return "\n".join(lines) + "\n\n"
