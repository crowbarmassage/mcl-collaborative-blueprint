# MCL Collaborative Blueprint

Real-time interactive dashboard for the MCL 2026 conference. Attendees answer 3 strategic questions on their phones; a live projector dashboard visualizes the room's collective intelligence and generates AI-powered strategic insights.

## Features (v1)

- **Mobile Input Form** — 3-step wizard: Priority Budget (100 credits), Threat Matrix (scatter plot), AI Alignment (archetype selection)
- **Live Dashboard** — Auto-refreshing Plotly charts: horizontal bar, scatter with quadrants, 2x2 heatmap
- **AI Mirror** — GPT-4o synthesizes a "Guerilla Tactic" from the room's aggregate data with typewriter animation
- **Google Sheets Backend** — Persistent, concurrent storage for 45 attendees
- **Streamlit Cloud** — Free SSL-secured deployment with QR code access

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Cloud service account with Sheets API access
- OpenAI API key

### Installation

```bash
git clone https://github.com/crowbarmassage/mcl-collaborative-blueprint.git
cd mcl-collaborative-blueprint

uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
```

### Configuration

1. Copy the secrets template:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Fill in `.streamlit/secrets.toml` with:
   - Your OpenAI API key
   - Google Sheets service account credentials
   - Google Sheet URL

3. Create a Google Sheet with the column headers from `TECH_SPECS.md` → API Design → Sheet Structure.

### Running Locally

```bash
streamlit run app.py
```

- **Attendee form**: http://localhost:8501
- **Dashboard**: http://localhost:8501/?mode=admin_dashboard

### Running Tests

```bash
pytest tests/ -v
```

## Deployment (Streamlit Community Cloud)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create new app → select this repo → main file: `app.py`
4. Add secrets in the Streamlit Cloud dashboard (paste contents of `secrets.toml`)
5. Share the attendee URL via QR code

## Project Structure

```
mcl-collaborative-blueprint/
├── app.py                      # Streamlit entry point
├── mcl_blueprint/              # Application package
│   ├── config.py               # Constants and categories
│   ├── models.py               # Data models
│   ├── sheets.py               # Google Sheets data layer
│   ├── visualizations.py       # Plotly chart builders
│   ├── ai_mirror.py            # OpenAI synthesis engine
│   └── components/
│       ├── attendee.py         # Mobile wizard form
│       └── dashboard.py        # Projector dashboard
├── tests/                      # pytest test suite
├── .streamlit/                 # Streamlit config and secrets
├── notebooks/                  # Google Colab demo
└── [design docs]               # TECH_SPECS, ATOMIC_STEPS, etc.
```

## Architecture

```
Attendees (Mobile)  ──write──▶  Google Sheets  ◀──read──  Dashboard (Projector)
                                                              │
                                                         OpenAI GPT-4o
                                                              │
                                                      AI Strategic Tactic
```

## Development

```bash
# Lint and format
ruff check . && ruff format .

# Type check
mypy mcl_blueprint/

# Test with coverage
pytest tests/ -v --cov=mcl_blueprint --cov-report=term-missing
```

## License

Private — MCL 2026 internal use.
