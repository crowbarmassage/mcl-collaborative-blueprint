# FUTURE_FEATURES.md — MCL Collaborative Blueprint

Features explicitly out of scope for v1, documented for future consideration.

---

## Deferred Features

### 1. Box Plot Overlay on Priority Budget Chart

- **What**: Overlay box plots on the Q1 horizontal bar chart to show variance (consensus vs. polarization) per category
- **Why deferred**: Standard bar chart is sufficient for v1. The average alone communicates the room's priority clearly.
- **Complexity**: Low — Plotly supports box plots natively
- **Prerequisites from v1**: Phase 4 (Dashboard Visualizations) complete

### 2. Real-Time WebSocket Updates

- **What**: Replace 7-second polling with WebSocket push for instant dashboard updates
- **Why deferred**: `streamlit_autorefresh` polling is simple and works for 45 users. WebSocket requires a custom Streamlit component.
- **Complexity**: High — requires custom component development
- **Prerequisites from v1**: Full deployment working

### 3. User Authentication / Admin Login

- **What**: Password-protected admin dashboard instead of security-by-obscurity URL parameter
- **Why deferred**: For a 45-person internal conference, URL parameter is sufficient. Auth adds complexity and friction.
- **Complexity**: Medium — Streamlit has `st.secrets`-based auth patterns
- **Prerequisites from v1**: Phase 7 (Deployment) complete

### 4. Multi-Session / Multi-Event Support

- **What**: Support multiple events with separate data, event selection dropdown
- **Why deferred**: This is a single-event tool. Multi-event adds database schema changes and routing.
- **Complexity**: High — requires data partitioning, event management UI
- **Prerequisites from v1**: All phases complete

### 5. Export Data to PDF/CSV

- **What**: "Download Report" button on dashboard that exports charts and data as PDF or CSV
- **Why deferred**: Data lives in Google Sheets which has its own export. PDF generation adds heavy dependencies (weasyprint, reportlab).
- **Complexity**: Medium
- **Prerequisites from v1**: Phase 6 (Integration) complete

### 6. Word Cloud from Reasoning Traces

- **What**: Generate word clouds from the free-text responses (Q1 reasoning, Q2 trigger, Q3 followup)
- **Why deferred**: Nice visual but not core to the strategic analysis. Adds `wordcloud` dependency.
- **Complexity**: Low
- **Prerequisites from v1**: Phase 4 complete

### 7. Streaming AI Response (Server-Sent Events)

- **What**: Stream the OpenAI response token-by-token instead of generating full text then animating
- **Why deferred**: The current typewriter effect (character-by-character from complete response) is simpler and more reliable. True streaming requires `openai` stream mode + Streamlit's `st.write_stream`.
- **Complexity**: Low-Medium
- **Prerequisites from v1**: Phase 5 complete

### 8. Anonymous Demographics Collection

- **What**: Optional pre-survey collecting university name, year, role (student/staff) for richer segmentation
- **Why deferred**: Adds friction to the attendee flow. The 3-question wizard is designed for speed.
- **Complexity**: Low
- **Prerequisites from v1**: Phase 3 complete

### 9. Historical Comparison

- **What**: Compare current session's data against previous years' conferences
- **Why deferred**: No historical data exists yet. First event is MCL 2026.
- **Complexity**: Medium — requires data archiving and comparison logic
- **Prerequisites from v1**: Multiple events completed
