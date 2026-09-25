# COW stateabb is the canonical identifier throughout the pipeline.
# Verify stateabb values against data/raw/cow_trade/Dyadic_COW_4.0.csv
# before running silver scripts.

MVP_COUNTRIES: list[str] = [
    "USA", "UKG", "FRN", "GMY", "ITA", "AUS",
    "HUN", "RUS", "SWD", "NTH", "BEL", "CAN",
    "POR", "SPN",
]
# Note: AUH (Austria-Hungary) splits into AUS + HUN at 1918.
# Scripts must handle this split explicitly.

# Maddison ISO-3 → COW stateabb
MADDISON_TO_COW: dict[str, str] = {
    "USA": "USA", "GBR": "UKG", "FRA": "FRN", "DEU": "GMY",
    "ITA": "ITA", "AUT": "AUS", "HUN": "HUN", "RUS": "RUS",
    "SWE": "SWD", "NLD": "NTH", "BEL": "BEL", "CAN": "CAN",
    "PRT": "POR", "ESP": "SPN",
}

# V-Dem country_text_id → COW stateabb
VDEM_TO_COW: dict[str, str] = {
    "United States of America": "USA",
    "United Kingdom":           "UKG",
    "France":                   "FRN",
    "Germany":                  "GMY",
    "Italy":                    "ITA",
    "Austria":                  "AUS",
    "Austria-Hungary":          "AUH",
    "Hungary":                  "HUN",
    "Russia":                   "RUS",
    "Sweden":                   "SWD",
    "Netherlands":              "NTH",
    "Belgium":                  "BEL",
    "Canada":                   "CAN",
    "Portugal":                 "POR",
    "Spain":                    "SPN",
}

# JST Macrohistory Database R6 (Jordà, Schularick & Taylor) ISO → COW stateabb
# Used for financial data (loans/GDP, investment/GDP) 1870–1949.
JST_ISO_TO_COW: dict[str, str] = {
    'USA': 'USA', 'GBR': 'UKG', 'FRA': 'FRN', 'DEU': 'GMY',
    'ITA': 'ITA', 'NLD': 'NTH', 'BEL': 'BEL', 'SWE': 'SWD',
    'CAN': 'CAN', 'PRT': 'POR', 'ESP': 'SPN',
    'CHE': 'CHE', 'DNK': 'DNK', 'NOR': 'NOR',  # not in MVP_COUNTRIES but include
    'AUS': 'AUS_JST', 'FIN': 'FIN', 'IRL': 'IRL', 'JPN': 'JPN',
}

# Polity5 ccode (numeric) → COW stateabb
POLITY_CCODE_TO_COW: dict[int, str] = {
    2: "USA", 200: "UKG", 220: "FRN", 255: "GMY",
    325: "ITA", 305: "AUS", 310: "HUN", 365: "RUS",
    380: "SWD", 210: "NTH", 211: "BEL", 20: "CAN",
    235: "POR", 230: "SPN",
}

_SOURCE_MAPS = {
    "maddison": MADDISON_TO_COW,
    "vdem":     VDEM_TO_COW,
    "polity":   {str(k): v for k, v in POLITY_CCODE_TO_COW.items()},
    "jst":      JST_ISO_TO_COW,
}


def harmonize_to_cow(code: str, source: str) -> str | None:
    """
    Harmonize a country code from a given source to COW stateabb format.

    Parameters
    ----------
    code : str
        Country code from the source system.
    source : str
        Source system: "maddison", "vdem", or "polity".

    Returns
    -------
    str | None
        COW stateabb if found, None otherwise.
    """
    return _SOURCE_MAPS.get(source, {}).get(str(code))
