# Lead Designer — Executive Deliverable
## Branch arena/019fd213-the-bettor-1

### Executive Summary
Redesign moves from scattered AI-styled random explanations to an editorial-grade experience: Bloomberg Terminal discipline meets The Athletic editorial clarity. Deep navy/charcoal with emerald and gold accents (no primary blue). Serif display (Tiempos Headline) creates editorial authority; Inter handles data with surgical clarity. Every claim is provable; empty states are honest illustrations; progressive disclosure guides the user from verdict → why → technical.

### Design System
- Colors: ink-950/charcoal/slate/silver/mist/paper; emerald/deep; gold/gold-soft; coral/rose-deep.
- Typography: Tiempos Headline (display), Inter (body), SF Mono (technical).
- Layout: max-width 840px, centered cards with subtle shadow, progressive disclosure.

### Key Interactions
- Theme toggle (system/default) via localStorage; keyboard nav with aria-labels.
- Collapsible sections: Verdict → Why → Technical details.
- NO CALL card uses honest balance bar (58/18/24) with no calibrated bridge.
- Data drop zone shows staged states (Clean / Held / Rejected) in plain English.
- Country Packs: Mute (soft) vs Purge (hard backup-gated) with pre-purge download.
- Calibration ladder displays masked replay results with artifact provenance.

### Icons & Meanings
Fixed emoji-to-meaning mapping preserved (🛡️ Fortress, 📈↑ trend, 🌍 pivot, ⚡ hot, ❄️ cold, 🔗 chain, ⚖️ balance, 💡 tip, 🔍 provenance) with tooltip context for accessibility.

### Constraints Met
P1 — no market fetch / XHR / odds = 0. A-01 — compute live or silent. D12 — central request. AAA contrast maintained. Single HTML < 1.2MB, zero network fetch.
