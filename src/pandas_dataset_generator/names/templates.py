"""Name templates and tokens for entity name generation."""

from typing import List, Dict

# === Investor Name Components ===

INVESTOR_PREFIXES: List[str] = [
    # Geographic/Nature
    "Summit", "Northbridge", "Apex", "Horizon", "Pinnacle", "Meridian",
    "Evergreen", "Lighthouse", "Keystone", "Granite", "Ironwood", "Redwood",
    "Bluerock", "Silverstone", "Goldpoint", "Blackridge", "Whitehorse",
    "Greenfield", "Oakwood", "Cedarpoint", "Pinehill", "Riverside", "Lakefront",
    "Mountainview", "Valleypoint", "Highland", "Lowland", "Eastgate", "Westwood",
    "Northstar", "Southpoint", "Midland", "Coastal", "Harbor", "Bayshore",
    # Abstract/Quality
    "Atlas", "Vanguard", "Sterling", "Beacon", "Catalyst", "Endeavor",
    "Genesis", "Insight", "Legacy", "Matrix", "Nexus", "Omega", "Prime",
    "Quantum", "Regal", "Sapphire", "Titan", "Unity", "Vertex", "Zenith",
    "Ascend", "Cascade", "Diamond", "Eclipse", "Frontier", "Guardian",
    "Ignite", "Jubilee", "Kinetic", "Luminous", "Momentum", "Noble",
    # Finance-themed
    "Alpha", "Beta", "Gamma", "Delta", "Sigma", "Capital", "Equity",
    "Crown", "Empire", "Fortune", "Global", "Imperial", "Jupiter", "Kings",
    "Liberty", "Majestic", "National", "Olympic", "Pacific", "Royal",
    # Tech/Modern
    "Vector", "Synergy", "Fusion", "Spectrum", "Aurora", "Nova", "Orion",
    "Phoenix", "Polaris", "Sirius", "Stellar", "Stratos", "Terra", "Venture",
]

INVESTOR_SUFFIXES: List[str] = [
    "Capital", "Partners", "Ventures", "Management", "Holdings", "Group",
    "Investments", "Advisors", "Equity", "Associates", "Fund", "Asset Management",
    "Private Equity", "Growth Partners", "Investment Partners", "Capital Partners",
]

# === Company Name Components ===

COMPANY_PREFIXES: List[str] = [
    # Tech/Digital
    "Quantum", "Cyber", "Data", "Cloud", "Neural", "Vertex", "Nexus", "Synapse",
    "Vector", "Matrix", "Helix", "Prism", "Digital", "Smart", "Nano", "Micro",
    "Meta", "Hyper", "Ultra", "Omni", "Multi", "Poly", "Mono", "Uni",
    # Innovation
    "Zenith", "Kinetic", "Dynamic", "Unified", "Global", "Integrated", "Advanced",
    "Innovative", "Modern", "Premier", "Elite", "Prime", "Core", "Central",
    "Alpha", "Beta", "Gamma", "Delta", "Omega", "Sigma", "Lambda", "Theta",
    # Nature/Elements
    "Solar", "Lunar", "Stellar", "Cosmic", "Terra", "Aqua", "Aero", "Pyro",
    "Crystal", "Diamond", "Pearl", "Ruby", "Emerald", "Sapphire", "Amber",
    "Jade", "Onyx", "Opal", "Topaz", "Granite", "Marble", "Quartz",
    # Abstract
    "Bright", "Clear", "Swift", "Rapid", "Quick", "Fast", "Agile", "Nimble",
    "Sharp", "Keen", "Bold", "Brave", "True", "Pure", "Real", "Vital",
    "Fresh", "New", "Next", "Open", "Free", "Fair", "Just", "Right",
]

COMPANY_DOMAIN_SUFFIXES: List[str] = [
    # Tech
    "Technologies", "Systems", "Labs", "Analytics", "Networks", "Software",
    "Solutions", "Platforms", "AI", "Dynamics", "Innovations", "Digital",
    # Healthcare
    "Health", "Med", "Pharma", "Therapeutics", "Bio", "Life Sciences",
    "Diagnostics", "Medical", "Healthcare", "Wellness",
    # Finance
    "Finance", "Financial", "Payments", "Banking", "Insurance", "Wealth",
    # Other
    "Energy", "Services", "Consulting", "Advisory", "Research", "Industries",
    "Enterprises", "International", "Global", "Group", "Corp",
]

# === Legal Suffixes ===

LEGAL_SUFFIX_DIST: Dict[str, float] = {
    "Inc": 0.25,
    "Ltd": 0.20,
    "PLC": 0.08,
    "LLC": 0.10,
    "GmbH": 0.05,
    "S.A.": 0.05,
    "": 0.27,
}

# Expansion mappings for alias generation
SUFFIX_EXPANSIONS: Dict[str, List[str]] = {
    "Inc": ["Incorporated", "Inc.", "INC", "INCORPORATED"],
    "Ltd": ["Limited", "Ltd.", "LTD", "LIMITED"],
    "Corp": ["Corporation", "Corp.", "CORP", "CORPORATION"],
    "Co": ["Company", "Co.", "CO", "COMPANY"],
    "Intl": ["International", "Int'l", "INTL", "INTERNATIONAL"],
    "Tech": ["Technologies", "Technology", "TECH"],
    "Mgmt": ["Management", "MGMT"],
    "Grp": ["Group", "GRP"],
    "Hldgs": ["Holdings", "HLDGS"],
    "Svcs": ["Services", "SVCS"],
    "PLC": ["Plc", "plc", "P.L.C."],
    "LLC": ["L.L.C.", "Llc", "llc"],
    "GmbH": ["GMBH", "Gmbh"],
    "S.A.": ["SA", "S.A", "Sa"],
}

# Tokens that can be dropped for alias generation
DROPPABLE_TOKENS: List[str] = [
    "Holdings", "Group", "Partners", "The", "International", "Global",
    "Enterprises", "Industries", "Corporation", "Company",
]

# === Public Company Specific ===

EXCHANGE_COUNTRY_MAP: Dict[str, str] = {
    "NYSE": "US",
    "NASDAQ": "US",
    "LSE": "GB",
    "Euronext": "NL",  # Multi-country, use NL as default
    "XETRA": "DE",
    "SIX": "CH",
    "HKEX": "HK",
    "SGX": "SG",
}

# === Unknown Company Templates (for party2 UNKNOWN generation) ===

UNKNOWN_COMPANY_PREFIXES: List[str] = [
    "Acme", "Zenon", "Vortex", "Axiom", "Babel", "Cipher", "Dynamo",
    "Echo", "Flux", "Glide", "Haven", "Ionic", "Joule", "Krypton",
    "Lumen", "Maven", "Neon", "Orbit", "Pulse", "Quark", "Relay",
    "Spark", "Tidal", "Umbra", "Vapor", "Warp", "Xenon", "Yotta", "Zephyr",
]

UNKNOWN_COMPANY_SUFFIXES: List[str] = [
    "Co", "Corp", "LLC", "Ltd", "Inc", "SA", "GmbH",
    "Enterprises", "Industries", "Holdings", "Group", "International",
]
