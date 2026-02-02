"""Configuration constants for MCL Collaborative Blueprint."""

# App
APP_TITLE = "MCL 2026 — Collaborative Blueprint"
DASHBOARD_MODE_KEY = "admin_dashboard"
DASHBOARD_REFRESH_INTERVAL_MS = 7000  # 7 seconds

# Q1: Priority Budget
TOTAL_CREDITS = 100
PRIORITY_CATEGORIES: list[str] = [
    "Chaplaincy",
    "Prayer Space",
    "Halal Food",
    "Mental Health",
    "Admin Access",
    "Security/Safety",
    "Legal Defense",
    "Other",
]

# Q2: Threat Matrix
THREAT_OPTIONS: list[str] = [
    "Budget Cuts",
    "Doxxing",
    "Protest Bans",
    "Surveillance",
    "Apathy",
]
LIKELIHOOD_RANGE: tuple[int, int] = (1, 10)
IMPACT_RANGE: tuple[int, int] = (1, 10)

# Q3: AI Alignment Archetypes
ARCHETYPES: dict[str, str] = {
    "The Fortress": "Bans, Detection Software",
    "The Ostrich": "No Policy, Confusion",
    "The Lab": "Experimentation, Training",
    "The Watchtower": "Surveillance, Monitoring",
}

# Conditional follow-up questions per archetype
ARCHETYPE_FOLLOWUPS: dict[str, str] = {
    "The Fortress": "How does the ban hurt advocacy?",
    "The Ostrich": "What risk does this vacuum create?",
    "The Lab": "What experiment would you run first?",
    "The Watchtower": "What specific data do they track?",
}

# Google Sheets worksheet names
WORKSHEET_RESPONSES = "responses"
WORKSHEET_REGISTRATIONS = "registrations"

# Session state keys
SESSION_USER_ID = "user_id"

# Registration profile field options
UNIVERSITY_TYPES: list[str] = [
    "Public 4-year",
    "Private 4-year",
    "Community College",
    "HBCU",
    "HSI",
    "Religious-affiliated",
    "Other",
]

LOCALE_TYPES: list[str] = [
    "Urban",
    "Suburban",
    "Rural",
]

ROLE_OPTIONS: list[str] = [
    "Student",
    "MSA Board Member",
    "Faculty/Staff Advisor",
    "Chaplain/Imam",
    "Administration",
    "Alumni",
    "Community Partner",
    "Other",
]

REGION_OPTIONS: list[str] = [
    "Northeast",
    "Southeast",
    "Midwest",
    "Southwest",
    "West Coast",
    "Pacific Northwest",
    "Other",
]

# OpenAI
OPENAI_MODEL = "gpt-5-mini-2025-08-07"
OPENAI_MAX_TOKENS = 300
