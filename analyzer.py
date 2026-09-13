import re


# -------------------------------------------------
# COMMON MEDICAL TEST REFERENCE RANGES
# Demo / basic adult reference ranges.
# These ranges can vary by laboratory and patient.
# -------------------------------------------------

REFERENCE_RANGES = {
    "hemoglobin": {
        "male": (13.5, 17.5),
        "female": (12.0, 15.5),
        "unit": "g/dL"
    },

    "wbc": {
        "all": (4.0, 11.0),
        "unit": "x10^9/L"
    },

    "rbc": {
        "male": (4.5, 5.9),
        "female": (4.1, 5.1),
        "unit": "x10^12/L"
    },

    "platelets": {
        "all": (150, 450),
        "unit": "x10^9/L"
    },

    "glucose": {
        "all": (70, 140),
        "unit": "mg/dL"
    },

    "cholesterol": {
        "all": (0, 200),
        "unit": "mg/dL"
    },

    "creatinine": {
        "male": (0.74, 1.35),
        "female": (0.59, 1.04),
        "unit": "mg/dL"
    },

    "urea": {
        "all": (15, 40),
        "unit": "mg/dL"
    }
}


# -------------------------------------------------
# TEST NAME ALIASES
# -------------------------------------------------

TEST_ALIASES = {
    "hemoglobin": [
        "hemoglobin",
        "haemoglobin",
        "hb"
    ],

    "wbc": [
        "wbc",
        "white blood cells",
        "white blood cell count"
    ],

    "rbc": [
        "rbc",
        "red blood cells",
        "red blood cell count"
    ],

    "platelets": [
        "platelets",
        "platelet count"
    ],

    "glucose": [
        "glucose",
        "blood sugar",
        "fasting glucose"
    ],

    "cholesterol": [
        "cholesterol",
        "total cholesterol"
    ],

    "creatinine": [
        "creatinine",
        "serum creatinine"
    ],

    "urea": [
        "urea",
        "blood urea"
    ]
}


# -------------------------------------------------
# FIND TEST VALUE
# -------------------------------------------------

def find_test_value(text, aliases):
    """
    Find a numeric value appearing after a known
    medical test name.
    """

    for alias in aliases:

        # Example:
        # Hemoglobin: 14.5
        # Glucose - 180
        # WBC = 7.2
        pattern = (
            rf"{re.escape(alias)}"
            r"\s*[:=\-]?\s*"
            r"(\d+(?:\.\d+)?)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return float(match.group(1))

    return None


# -------------------------------------------------
# GET REFERENCE RANGE
# -------------------------------------------------

def get_reference_range(test_name, gender):
    """
    Return the correct reference range according
    to patient gender.
    """

    reference = REFERENCE_RANGES[test_name]

    gender = gender.lower()

    if gender in reference:
        return reference[gender]

    return reference.get("all")


# -------------------------------------------------
# ANALYZE REPORT
# -------------------------------------------------

def analyze_report(report_text, gender="Other"):
    """
    Analyze medical report text and separate results
    into Normal, Abnormal and Unknown categories.
    """

    results = {
        "normal": [],
        "abnormal": [],
        "unknown": []
    }

    for test_name, aliases in TEST_ALIASES.items():

        value = find_test_value(
            report_text,
            aliases
        )

        # If no value was found, skip this test
        if value is None:
            continue

        reference_range = get_reference_range(
            test_name,
            gender
        )

        # No reference range available
        if reference_range is None:

            results["unknown"].append({
                "Test": test_name.title(),
                "Value": value,
                "Status": "Unknown"
            })

            continue

        minimum, maximum = reference_range

        # Check LOW
        if value < minimum:

            results["abnormal"].append({
                "Test": test_name.title(),
                "Value": value,
                "Reference Range": f"{minimum} - {maximum}",
                "Status": "LOW"
            })

        # Check HIGH
        elif value > maximum:

            results["abnormal"].append({
                "Test": test_name.title(),
                "Value": value,
                "Reference Range": f"{minimum} - {maximum}",
                "Status": "HIGH"
            })

        # NORMAL
        else:

            results["normal"].append({
                "Test": test_name.title(),
                "Value": value,
                "Reference Range": f"{minimum} - {maximum}",
                "Status": "NORMAL"
            })

    return results