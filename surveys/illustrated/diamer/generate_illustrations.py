# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
#     "pyyaml>=6.0",
# ]
# ///
"""
Generate illustrations for the Diamer / Nanga Parbat survey.

Sixteen illustrations spanning multiple visual types:
  1.  Deep-time timeline (timeline) — 250 Ma to present
  2.  Tectonic aneurysm cross-section (cross-section)
  3.  Ibex species plate (species-plate) — petroglyph style
  4.  India drift map-schematic (map) — 180 Ma to 50 Ma
  5.  Indus gorge elevation profile (profile)
  6.  Markhor species plate (species-plate)
  7.  Snow leopard species plate (species-plate)
  8.  Lammergeier species plate (species-plate)
  9.  Petroglyph sites map-schematic (map)
  10. Petroglyph chronology timeline (timeline)
  11. Motif catalogue grid (catalogue)
  12. Nanga Parbat three faces (profile)
  13. Glacier marriage process diagram (diagram)
  14. Flora elevation profile (profile)
  15. Writing systems specimens (catalogue)
  16. Bitan trance process diagram (diagram)

Visual language: parchment, walnut ink, serif typography,
diagrammatic line art. No photorealism.

Run with:  uv run generate_illustrations.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

# Import shared helpers
sys.path.insert(0, str(Path(__file__).parent.parent))
from survey_helpers import *

# ── Output ──────────────────────────────────────────────────────────
OUT = Path(__file__).parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

# ── Diamer Palette (extends base) ──────────────────────────────────
GNEISS        = "#7A7068"
GNEISS_DARK   = "#5A5048"
LEUCOGRANITE  = "#D4A0A0"
KOHISTAN      = "#3A5A3A"
KOHISTAN_LT   = "#5A7A5A"
INDUS_BLUE    = "#5A7888"
INDUS_DARK    = "#3A5868"
THERMAL       = "#C85828"
THERMAL_GLOW  = "#E88848"

JUNIPER       = "#2A4A2A"
BIRCH_GOLD    = "#C8B060"
IBEX_HORN     = "#B08830"
MEADOW        = "#6A8A4A"
APRICOT       = "#E8A0A0"

ROCK_FACE     = "#B8A888"
CARVED_LINE   = "#3A2A1A"
PATINA        = "#6A8A68"

GLACIER_BLUE  = "#8AB0C8"
GLACIER_DARK  = "#5A8098"

# Epoch colours for timeline
TETHYS_BLUE   = "#6A90B0"
COLLISION_RED = "#B07060"
OROGEN_AMBER  = "#C8A060"
SIWALIK_GREEN = "#7A9868"
PLEIST_ICE    = "#A0B8C8"
HOLOCENE_WARM = "#D8B880"

ATTR_TEXT = "Illustrated Survey \u2014 Diamer and Nanga Parbat"


# ═══════════════════════════════════════════════════════════════════
# Figure 1: Deep-Time Timeline (250 Ma to present, log scale)
# ═══════════════════════════════════════════════════════════════════

def deep_time_timeline():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=101)

    title_block(ax, "Deep Time at Nanga Parbat",
                "250 million years on a single page \u2014 log scale")

    # ── Main timeline axis ──
    # Using log scale: x position = mapped from log10(age)
    # Left = old (250 Ma), right = recent (present)
    ax_y = 50  # centre line
    x_left, x_right = 8, 92

    max_age = 250  # Ma
    log_max = math.log10(max_age)

    def age_to_x(ma):
        if ma <= 0.001:
            return x_right
        frac = 1 - math.log10(ma) / log_max
        return x_left + frac * (x_right - x_left)

    # ── Epoch bands ──
    epochs = [
        (250, 50,  "Tethys Sea",       TETHYS_BLUE),
        (50,  5,   "Orogeny",          OROGEN_AMBER),
        (5,   2.6, "Late Miocene",     SIWALIK_GREEN),
        (2.6, 0.012, "Pleistocene",    PLEIST_ICE),
        (0.012, 0.001, "Holocene",     HOLOCENE_WARM),
    ]

    band_h = 8
    for start_ma, end_ma, label, color in epochs:
        x1 = age_to_x(start_ma)
        x2 = age_to_x(end_ma)
        ax.add_patch(FancyBboxPatch(
            (min(x1, x2), ax_y - band_h / 2), abs(x2 - x1), band_h,
            boxstyle="round,pad=0.1",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.5, alpha=0.5, zorder=2))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, ax_y, label, ha="center", va="center",
                fontsize=9, color=INK, fontfamily="serif",
                fontweight="bold", zorder=3)

    # Axis line
    ax.plot([x_left, x_right], [ax_y - band_h / 2 - 1] * 2,
            color=INK_FAINT, linewidth=0.8, zorder=1)

    # Age ticks
    tick_ages = [250, 100, 50, 10, 5, 1, 0.1, 0.01]
    tick_labels = ["250 Ma", "100 Ma", "50 Ma", "10 Ma", "5 Ma",
                   "1 Ma", "100 ka", "10 ka"]
    for ma, label in zip(tick_ages, tick_labels):
        x = age_to_x(ma)
        ax.plot([x, x], [ax_y - band_h / 2 - 1, ax_y - band_h / 2 - 3],
                color=INK_LIGHT, linewidth=0.6, zorder=2)
        ax.text(x, ax_y - band_h / 2 - 4, label, ha="center", va="top",
                fontsize=7, color=INK_LIGHT, fontfamily="serif", zorder=3)

    # ── Events (above the timeline) ──
    events_above = [
        (180, "Gondwana\nbreaks up"),
        (130, "India\nseparates"),
        (66,  "Deccan\nTraps"),
        (55,  "Collision\nbegins"),
        (25,  "Proto-Indus\nestablished"),
        (10,  "Monsoon\nintensifies"),
        (1,   "Decompression\npulse"),
        (0.01, "First\npetroglyphs"),
    ]

    for i, (ma, label) in enumerate(events_above):
        x = age_to_x(ma)
        y_off = 8 + (i % 3) * 7  # stagger heights
        ax.plot([x, x], [ax_y + band_h / 2, ax_y + band_h / 2 + y_off - 2],
                color=INK_FAINT, linewidth=0.5, zorder=2)
        ax.plot(x, ax_y + band_h / 2, "v", color=INK, markersize=4, zorder=4)
        ax.text(x, ax_y + band_h / 2 + y_off, label,
                ha="center", va="bottom", fontsize=7, color=INK,
                fontfamily="serif", fontstyle="italic", zorder=4)

    # ── Events (below the timeline) ──
    events_below = [
        (90,  "India at\n15\u201320 cm/yr"),
        (50,  "Kohistan arc\ntrapped"),
        (18,  "Siwalik\nmegafauna"),
        (2.6, "Glacial\ncycles begin"),
        (0.1, "LGM ice\nstream"),
        (0.003, "Buddhism\narrives"),
    ]

    for i, (ma, label) in enumerate(events_below):
        x = age_to_x(ma)
        y_off = 8 + (i % 3) * 7
        ax.plot([x, x], [ax_y - band_h / 2 - 1, ax_y - band_h / 2 - 1 - y_off + 2],
                color=INK_FAINT, linewidth=0.5, zorder=2)
        ax.plot(x, ax_y - band_h / 2 - 1, "^", color=INK,
                markersize=4, zorder=4)
        ax.text(x, ax_y - band_h / 2 - 1 - y_off, label,
                ha="center", va="top", fontsize=7, color=INK,
                fontfamily="serif", fontstyle="italic", zorder=4)

    # ── Arrow: "you are here" ──
    ax.annotate("now", xy=(x_right + 1, ax_y), fontsize=9,
                color=THERMAL, fontfamily="serif", fontweight="bold",
                va="center", zorder=5)

    # ── Key insight ──
    ax.text(50, 8, "The rock at the summit was once the floor of a warm tropical sea.\n"
            "The river is older than the mountain it cuts through.",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "deep-time-timeline.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 2: Tectonic Aneurysm Cross-Section
# ═══════════════════════════════════════════════════════════════════

def tectonic_aneurysm():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=202)
    rng = np.random.default_rng(42)

    title_block(ax, "The Tectonic Aneurysm",
                "Erosion drives uplift drives erosion \u2014 the mountain unmakes itself to make itself")

    # ── Cross-section frame ──
    cs_left, cs_right = 15, 85
    cs_bot, cs_top = 15, 75

    # Surface (mountain profile)
    xs = np.linspace(cs_left, cs_right, 200)
    # Nanga Parbat as central peak, Kohistan flanks lower
    peak_x = 50
    profile = 45 + 30 * np.exp(-((xs - peak_x) / 12) ** 2)
    # Secondary shoulders
    profile += 8 * np.exp(-((xs - 30) / 10) ** 2)
    profile += 8 * np.exp(-((xs - 70) / 10) ** 2)
    profile = np.clip(profile, cs_bot, cs_top + 10)

    # ── Kohistan arc (flanking material, dark green) ──
    # Left flank
    kohistan_left = np.where(xs < 38, profile, cs_bot)
    ax.fill_between(xs[xs < 42], cs_bot, kohistan_left[xs < 42],
                     color=KOHISTAN, alpha=0.4, zorder=2)
    # Right flank
    kohistan_right = np.where(xs > 62, profile, cs_bot)
    ax.fill_between(xs[xs > 58], cs_bot, kohistan_right[xs > 58],
                     color=KOHISTAN, alpha=0.4, zorder=2)

    # Labels for Kohistan
    ax.text(25, 35, "Kohistan\nIsland Arc", fontsize=9, color=KOHISTAN,
            fontfamily="serif", fontweight="bold", ha="center", zorder=5)
    ax.text(75, 35, "Kohistan\nIsland Arc", fontsize=9, color=KOHISTAN,
            fontfamily="serif", fontweight="bold", ha="center", zorder=5)

    # ── Indian plate gneiss (central core, rising) ──
    gneiss_xs = xs[(xs >= 35) & (xs <= 65)]
    gneiss_profile = profile[(xs >= 35) & (xs <= 65)]
    ax.fill_between(gneiss_xs, cs_bot, gneiss_profile,
                     color=GNEISS, alpha=0.5, zorder=3)

    # Leucogranite veins (young, decompression-melted)
    for _ in range(6):
        vx = rng.uniform(40, 60)
        vy_bot = rng.uniform(cs_bot + 5, 40)
        vy_top = rng.uniform(vy_bot + 5, 55)
        vein_ys = np.linspace(vy_bot, vy_top, 15)
        vein_xs = vx + rng.uniform(-0.8, 0.8, 15)
        ax.plot(vein_xs, vein_ys, color=LEUCOGRANITE, linewidth=1.5,
                alpha=0.6, zorder=4)

    ax.text(50, 28, "Indian Plate\nBasement Gneiss",
            fontsize=10, color=PARCHMENT, fontfamily="serif",
            fontweight="bold", ha="center", zorder=5)
    ax.text(50, 22, "(rising through\nKohistan arc)",
            fontsize=8, color=PARCHMENT_DK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ── Suture zones (fault lines) ──
    for sx in [38, 62]:
        draw_fault_line(ax, sx, cs_bot, profile[np.argmin(np.abs(xs - sx))],
                        color=THERMAL)
    ax.text(38, cs_bot - 2, "MMT", fontsize=7, color=THERMAL,
            fontfamily="serif", ha="center", zorder=5)
    ax.text(62, cs_bot - 2, "Raikot\nFault", fontsize=7, color=THERMAL,
            fontfamily="serif", ha="center", zorder=5)

    # ── Mountain profile (skyline) ──
    ax.plot(xs, profile, color=GNEISS_DARK, linewidth=1.5, zorder=5)
    # Snow caps
    snow_line = 65
    snow_xs = xs[profile > snow_line]
    snow_ys = profile[profile > snow_line]
    if len(snow_xs) > 0:
        ax.fill_between(snow_xs, snow_line, snow_ys,
                         color=SNOW, alpha=0.6, zorder=6)

    # Summit label
    peak_y = profile.max()
    ax.text(peak_x, peak_y + 3, "8,126 m", fontsize=10, color=INK,
            fontfamily="serif", fontweight="bold", ha="center", zorder=7)

    # ── Indus river at base ──
    river_y = cs_bot + 3
    ax.plot([cs_left, cs_right], [river_y, river_y],
            color=INDUS_BLUE, linewidth=3, alpha=0.6, zorder=5)
    ax.text(cs_right + 1, river_y, "Indus\n~1,000 m",
            fontsize=7, color=INDUS_BLUE, fontfamily="serif",
            fontstyle="italic", va="center", zorder=5)

    # ── Feedback loop arrows (the aneurysm cycle) ──
    # Right side: erosion -> uplift -> erosion
    loop_x = 88
    loop_labels = [
        (82, "erosion\ncuts down"),
        (68, "geotherms\nsteepen"),
        (55, "crust\nweakens"),
        (42, "uplift\naccelerates"),
    ]
    for i, (ly, label) in enumerate(loop_labels):
        ax.text(loop_x + 3, ly, label, fontsize=7, color=INK,
                fontfamily="serif", fontstyle="italic",
                ha="left", va="center", zorder=5)
        if i < len(loop_labels) - 1:
            next_ly = loop_labels[i + 1][0]
            ax.annotate("", xy=(loop_x, next_ly + 3),
                        xytext=(loop_x, ly - 3),
                        arrowprops=dict(arrowstyle="->", color=THERMAL,
                                        linewidth=1.2, connectionstyle="arc3,rad=0.2"))

    # Closing arrow: uplift back to erosion (curved)
    ax.annotate("", xy=(loop_x, loop_labels[0][0] - 3),
                xytext=(loop_x, loop_labels[-1][0] + 3),
                arrowprops=dict(arrowstyle="->", color=THERMAL,
                                linewidth=1.2,
                                connectionstyle="arc3,rad=-0.5"))

    # ── Depth scale ──
    scale_x = cs_left - 3
    ax.annotate("", xy=(scale_x, cs_bot),
                xytext=(scale_x, peak_y),
                arrowprops=dict(arrowstyle="<->", color=INK_LIGHT,
                                linewidth=0.8))
    ax.text(scale_x - 2, (cs_bot + peak_y) / 2,
            "10 km\nexhumed\nin 10 Ma",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", va="center",
            rotation=90, zorder=5)

    # ── Decompression melting note ──
    ax.text(50, cs_bot + 8, "\u25b2 decompression melting zone \u25b2",
            fontsize=8, color=LEUCOGRANITE, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)
    ax.text(50, cs_bot + 5, "youngest granite on Earth: 0.7 Ma",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "tectonic-aneurysm.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 3: Ibex Species Plate (petroglyph style)
# ═══════════════════════════════════════════════════════════════════

def ibex_species_plate():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=303)

    title_block(ax, "Himalayan Ibex \u2014 Capra sibirica sakeen",
                "The most sacred animal \u2014 carved for 10,000 years")

    # ── Left panel: petroglyph-style ibex on rock face ──
    rock_face_background(ax, 5, 45, 15, 80, color=ROCK_FACE, seed=50)

    # Panel label
    ax.text(25, 82, "as carved at Thalpan", fontsize=9, color=INK,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=5)

    # Main ibex — large, facing left
    draw_ibex_silhouette(ax, 25, 52, scale=2.5, color=CARVED_LINE,
                         facing_left=True)

    # Smaller ibex (herd) — varying sizes
    draw_ibex_silhouette(ax, 15, 30, scale=1.2, color=CARVED_LINE,
                         facing_left=True)
    draw_ibex_silhouette(ax, 35, 33, scale=1.0, color=CARVED_LINE,
                         facing_left=False)

    # Hunting scene: tiny archer
    archer_x, archer_y = 38, 22
    # Body
    ax.plot([archer_x, archer_x], [archer_y, archer_y + 3],
            color=CARVED_LINE, linewidth=1.5, zorder=4)
    # Head
    ax.add_patch(plt.Circle((archer_x, archer_y + 3.5), 0.8,
                             facecolor="none", edgecolor=CARVED_LINE,
                             linewidth=1.2, zorder=4))
    # Bow
    ts = np.linspace(-0.8, 0.8, 15)
    bow_x = archer_x - 2 + 1.5 * np.cos(ts)
    bow_y = archer_y + 1.5 + 2 * ts
    ax.plot(bow_x, bow_y, color=CARVED_LINE, linewidth=1.0, zorder=4)
    # Arrow
    ax.plot([archer_x - 1.5, archer_x - 4], [archer_y + 1.5, archer_y + 2],
            color=CARVED_LINE, linewidth=0.8, zorder=4)

    # Patina over the carving (age effect)
    for _ in range(5):
        px = np.random.uniform(8, 42)
        py = np.random.uniform(18, 75)
        ax.add_patch(plt.Circle((px, py), np.random.uniform(2, 5),
                                 color=PATINA, alpha=0.08, zorder=5))

    # ── Right panel: annotations ──
    ann_x = 52

    # Horn detail
    ax.text(ann_x, 78, "The Horn", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_x, 74, [
        "Scimitar-curved, up to 100+ cm",
        "Ridged with annual growth rings",
        "Placed on graves across the Dardic world",
        "Most frequent motif in Thalpan petroglyphs",
    ], fontsize=8)

    # Habitat
    ax.text(ann_x, 55, "Habitat", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_x, 51, [
        "Above treeline: 3,500\u20135,500 m",
        "Rocky terrain, steep cliffs",
        "Descends to lower slopes in winter",
        "Males and females segregate except in rut",
    ], fontsize=8)

    # Cultural significance
    ax.text(ann_x, 33, "The Ibex Cult", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_x, 29, [
        "Oldest petroglyphs (~8,000 BCE): ibex",
        "Horns on graves: passage to the afterlife",
        "Jettmar: 'the ibex is the constant'",
        "Sacred across Dardic, Burushaski, Kalasha",
        "Still hunted \u2014 trophy and CITES regulated",
    ], fontsize=8)

    # Size comparison
    ax.text(ann_x, 10, "Male: 88\u2013110 cm shoulder, 60\u2013130 kg",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "ibex-species-plate.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 4: India's Northward Drift (180 Ma to 50 Ma)
# ═══════════════════════════════════════════════════════════════════

def india_drift():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=404)

    title_block(ax, "India\u2019s Northward Drift",
                "180 Ma to 50 Ma \u2014 the fastest continental sprint on record")

    # ── Eurasia (fixed, at top) ──
    eurasia_y = 82
    eurasia_pts = np.array([
        [20, eurasia_y], [80, eurasia_y],
        [85, eurasia_y - 5], [15, eurasia_y - 5], [20, eurasia_y]
    ])
    ax.fill(eurasia_pts[:, 0], eurasia_pts[:, 1],
            color=GNEISS, alpha=0.4, zorder=2)
    ax.plot(eurasia_pts[:, 0], eurasia_pts[:, 1],
            color=GNEISS_DARK, linewidth=1.2, zorder=3)
    ax.text(50, eurasia_y - 2.5, "EURASIA", fontsize=12, color=INK,
            fontfamily="serif", fontweight="bold", ha="center",
            va="center", zorder=4)

    # ── Tethys Sea (blue wash between Eurasia and India positions) ──
    ax.fill_between([10, 90], 30, eurasia_y - 5,
                     color=TETHYS_BLUE, alpha=0.15, zorder=1)
    ax.text(85, 55, "Tethys\nSea", fontsize=10, color=TETHYS_BLUE,
            fontfamily="serif", fontstyle="italic", ha="center",
            va="center", zorder=2)

    # ── India at four positions ──
    # Each India is a trapezoid; width narrows northward (subcontinent shape)
    positions = [
        (180, 15, "#C8B8A0", "180 Ma\n(Gondwana)"),
        (90,  32, "#B8A890", "90 Ma"),
        (66,  48, "#A89880", "66 Ma\n(Deccan Traps)"),
        (50,  62, COLLISION_RED, "50 Ma\n(collision)"),
    ]

    for age, y_base, color, label in positions:
        # Trapezoid: wider at bottom, narrower at top
        hw_bot = 10
        hw_top = 7
        h = 10
        pts = np.array([
            [50 - hw_bot, y_base],
            [50 + hw_bot, y_base],
            [50 + hw_top, y_base + h],
            [50 - hw_top, y_base + h],
            [50 - hw_bot, y_base],
        ])
        alpha = 0.3 if age > 50 else 0.5
        ax.fill(pts[:, 0], pts[:, 1], color=color, alpha=alpha, zorder=2)
        ax.plot(pts[:, 0], pts[:, 1], color=INK_LIGHT, linewidth=0.8,
                zorder=3)
        ax.text(50, y_base + h / 2, "INDIA", fontsize=8, color=INK,
                fontfamily="serif", ha="center", va="center", zorder=4)
        # Label to the left
        ax.text(50 - hw_bot - 2, y_base + h / 2, label, fontsize=8,
                color=INK_LIGHT, fontfamily="serif", fontstyle="italic",
                ha="right", va="center", zorder=4)

    # ── Kohistan Island Arc (small shape in the ocean) ──
    koh_x, koh_y = 50, 70
    koh_pts = np.array([
        [koh_x - 5, koh_y - 1.5], [koh_x + 5, koh_y - 1.5],
        [koh_x + 4, koh_y + 1.5], [koh_x - 4, koh_y + 1.5],
        [koh_x - 5, koh_y - 1.5],
    ])
    ax.fill(koh_pts[:, 0], koh_pts[:, 1], color=KOHISTAN, alpha=0.5,
            zorder=3)
    ax.plot(koh_pts[:, 0], koh_pts[:, 1], color=KOHISTAN_LT,
            linewidth=0.8, zorder=4)
    ax.text(koh_x, koh_y, "Kohistan\nIsland Arc", fontsize=7,
            color=PARCHMENT, fontfamily="serif", ha="center",
            va="center", zorder=5)

    # ── Drift arrow (large, showing direction) ──
    ax.annotate("", xy=(50, 72), xytext=(50, 15),
                arrowprops=dict(arrowstyle="-|>", color=THERMAL,
                                linewidth=2.5, mutation_scale=20))
    ax.text(68, 40, "15\u201320 cm/yr", fontsize=12, color=THERMAL,
            fontfamily="serif", fontweight="bold", ha="center",
            va="center", rotation=90, zorder=5)
    ax.text(68, 33, "(fastest drift\never recorded)", fontsize=8,
            color=INK_LIGHT, fontfamily="serif", fontstyle="italic",
            ha="center", va="center", rotation=90, zorder=5)

    # ── Scale / note ──
    ax.text(50, 7, "Schematic \u2014 not to geographic scale.\n"
            "India separated from Gondwana, crossed 6,000 km of Tethys,\n"
            "and collided with Eurasia, trapping the Kohistan arc between them.",
            fontsize=9, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", va="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=2)
    save_fig(fig, OUT / "india-drift.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 5: Indus Gorge Elevation Profile
# ═══════════════════════════════════════════════════════════════════

def indus_gorge_profile():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=505)

    title_block(ax, "The Indus Gorge \u2014 Deepest on Earth",
                "Nanga Parbat (8,126 m) to Indus (~1,000 m) to Rakaposhi (7,788 m)")

    # Coordinate mapping: x 10-90, y 12-85
    x_left, x_right = 10, 90
    y_river = 18  # Indus at ~1,000m
    y_np = 82     # Nanga Parbat summit
    y_rk = 78     # Rakaposhi summit

    # ── Nanga Parbat profile (left) ──
    xs_np = np.linspace(x_left, 48, 100)
    peak_np = 22
    profile_np = y_river + (y_np - y_river) * np.exp(-((xs_np - peak_np) / 15) ** 2)
    # Add shoulder
    profile_np += 8 * np.exp(-((xs_np - 15) / 8) ** 2)
    profile_np = np.clip(profile_np, y_river, 90)

    ax.fill_between(xs_np, y_river, profile_np, color=GNEISS, alpha=0.4,
                     zorder=2)
    ax.plot(xs_np, profile_np, color=GNEISS_DARK, linewidth=1.5, zorder=3)

    # Snow cap on NP
    snow_np = 65
    mask = profile_np > snow_np
    if np.any(mask):
        ax.fill_between(xs_np[mask], snow_np, profile_np[mask],
                         color=SNOW, alpha=0.6, zorder=4)

    ax.text(peak_np, y_np + 3, "Nanga Parbat\n8,126 m", fontsize=10,
            color=INK, fontfamily="serif", fontweight="bold",
            ha="center", va="bottom", zorder=5)

    # ── Rakaposhi profile (right) ──
    xs_rk = np.linspace(52, x_right, 100)
    peak_rk = 78
    profile_rk = y_river + (y_rk - y_river) * np.exp(-((xs_rk - peak_rk) / 15) ** 2)
    profile_rk += 6 * np.exp(-((xs_rk - 85) / 8) ** 2)
    profile_rk = np.clip(profile_rk, y_river, 90)

    ax.fill_between(xs_rk, y_river, profile_rk, color=KOHISTAN, alpha=0.35,
                     zorder=2)
    ax.plot(xs_rk, profile_rk, color=GNEISS_DARK, linewidth=1.5, zorder=3)

    # Snow cap on Rakaposhi
    mask_rk = profile_rk > snow_np
    if np.any(mask_rk):
        ax.fill_between(xs_rk[mask_rk], snow_np, profile_rk[mask_rk],
                         color=SNOW, alpha=0.6, zorder=4)

    ax.text(peak_rk, y_rk + 3, "Rakaposhi\n7,788 m", fontsize=10,
            color=INK, fontfamily="serif", fontweight="bold",
            ha="center", va="bottom", zorder=5)

    # ── Indus river at bottom ──
    river_xs = np.linspace(x_left, x_right, 100)
    river_ys = np.full_like(river_xs, y_river) + 0.5 * np.sin(river_xs * 0.3)
    ax.plot(river_xs, river_ys, color=INDUS_BLUE, linewidth=3.5,
            alpha=0.7, zorder=5)
    ax.text(50, y_river - 2, "Indus River  ~1,000 m", fontsize=9,
            color=INDUS_DARK, fontfamily="serif", fontweight="bold",
            ha="center", zorder=6)

    # ── Depth annotations ──
    # Left: NP to river
    ax.annotate("", xy=(35, y_river + 1), xytext=(35, y_np - 2),
                arrowprops=dict(arrowstyle="<->", color=THERMAL,
                                linewidth=1.2))
    ax.text(37, (y_river + y_np) / 2, "~4,500\u20135,200 m\nrelief",
            fontsize=9, color=THERMAL, fontfamily="serif",
            fontweight="bold", ha="left", va="center", zorder=5)

    # Right: Rakaposhi to river
    ax.annotate("", xy=(65, y_river + 1), xytext=(65, y_rk - 2),
                arrowprops=dict(arrowstyle="<->", color=THERMAL,
                                linewidth=1.2))
    ax.text(63, (y_river + y_rk) / 2, "~6,000 m\nrelief",
            fontsize=9, color=THERMAL, fontfamily="serif",
            fontweight="bold", ha="right", va="center", zorder=5)

    # ── Hot springs ──
    springs = [
        (40, "Tato"),
        (55, "Tattapani"),
    ]
    for sx, name in springs:
        # Thermal glow circle
        ax.add_patch(plt.Circle((sx, y_river), 2.5,
                                 color=THERMAL_GLOW, alpha=0.4, zorder=6))
        ax.add_patch(plt.Circle((sx, y_river), 1.5,
                                 color=THERMAL, alpha=0.5, zorder=6))
        ax.text(sx, y_river + 4, name, fontsize=8, color=THERMAL,
                fontfamily="serif", fontstyle="italic", ha="center",
                zorder=7)

    ax.text(50, y_river + 7, "hot springs at river level",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ── Incision rate ──
    ax.text(50, 12, "Incision rate: 2\u201312 mm/yr \u2014 among the fastest river incision on Earth",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=7)
    save_fig(fig, OUT / "indus-gorge-profile.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 6: Markhor Species Plate
# ═══════════════════════════════════════════════════════════════════

def markhor_plate():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=606)

    title_block(ax, "Markhor \u2014 Capra falconeri",
                "The snake-eater \u2014 Pakistan\u2019s national animal")

    # ── Left panel: rock face with markhor ──
    rock_face_background(ax, 5, 45, 15, 80, color=ROCK_FACE, seed=60)

    ax.text(25, 82, "near Nanga Parbat", fontsize=9, color=INK,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=5)

    draw_markhor_silhouette(ax, 25, 48, scale=2.5, color=CARVED_LINE,
                            facing_left=True)

    # Patina
    rng = np.random.default_rng(61)
    for _ in range(4):
        px, py = rng.uniform(8, 42), rng.uniform(18, 75)
        ax.add_patch(plt.Circle((px, py), rng.uniform(2, 5),
                                 color=PATINA, alpha=0.08, zorder=5))

    # ── Right panel: annotations ──
    ann_x = 52

    ax.text(ann_x, 78, "The Horn", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_x, 74, [
        "Corkscrew spiral \u2014 up to 160 cm",
        "Tight helix distinguishes from ibex",
        "Unique among wild goats",
    ], fontsize=8)

    ax.text(ann_x, 58, "Etymology", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_x, 54, [
        "mar = snake, khor = eater",
        "Chews on serpents \u2014 or kills with hooves",
        "Connected to n\u0101g / klu serpent cults",
        "The snake-eater guards the mountain passes",
    ], fontsize=8)

    ax.text(ann_x, 36, "Status", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_x, 32, [
        "Pakistan\u2019s national animal",
        "Near Threatened (IUCN)",
        "Range overlaps Nanga Parbat flanks",
        "Trophy hunting generates conservation revenue",
    ], fontsize=8)

    ax.text(ann_x, 14, "Male: 80\u2013115 cm shoulder, 80\u2013110 kg",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "markhor-plate.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 7: Snow Leopard Species Plate
# ═══════════════════════════════════════════════════════════════════

def snow_leopard_plate():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=707)

    title_block(ax, "Snow Leopard \u2014 Panthera uncia",
                "Present but never carved \u2014 the ghost of the mountain")

    # ── Left panel: rock face with dashed leopard (the ghost) ──
    rock_face_background(ax, 5, 45, 15, 80, color=ROCK_FACE, seed=70)

    ax.text(25, 82, "absent from the petroglyphs", fontsize=9,
            color=INK_LIGHT, fontfamily="serif", fontstyle="italic",
            ha="center", zorder=5)

    # The snow leopard is drawn dashed — present but never carved
    draw_snow_leopard_silhouette(ax, 25, 48, scale=2.5, color=INK_LIGHT,
                                 facing_left=True)

    # Ghost effect: faint circles suggesting presence
    rng = np.random.default_rng(71)
    for _ in range(6):
        px, py = rng.uniform(10, 40), rng.uniform(20, 70)
        ax.add_patch(plt.Circle((px, py), rng.uniform(3, 8),
                                 color=SNOW, alpha=0.06, zorder=3))

    # ── Right panel: annotations ──
    ann_x = 52

    ax.text(ann_x, 78, "Ghost of the Mountain", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_x, 74, [
        "Range: 3,000\u20135,500 m elevation",
        "Solitary, crepuscular, elusive",
        "Tail as long as body \u2014 balance and warmth",
    ], fontsize=8)

    ax.text(ann_x, 58, "The Absence", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_x, 54, [
        "30,000 carvings at Diamer sites",
        "Ibex, markhor, hunting scenes, stupas \u2014",
        "but no snow leopard. Not once.",
        "The predator that was always there, never recorded.",
        "Taboo? Invisibility? Or simply too rare to observe?",
    ], fontsize=8)

    ax.text(ann_x, 34, "Modern Record", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_x, 30, [
        "Camera trap studies sparse for Diamer",
        "Known presence on Nanga Parbat flanks",
        "Prey: ibex, markhor, marmot",
        "Estimated 4,000\u20136,500 globally",
    ], fontsize=8)

    # Visual concept note
    ax.text(50, 10, "The dashed outline is the point: present but never carved.",
            fontsize=9, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "snow-leopard-plate.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 8: Lammergeier Species Plate
# ═══════════════════════════════════════════════════════════════════

def lammergeier_plate():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=808)

    title_block(ax, "Lammergeier \u2014 Gypaetus barbatus",
                "The bone-eater \u2014 Homa of Persian mythology")

    # ── Central panel: rock face with bird in flight ──
    rock_face_background(ax, 10, 90, 30, 78, color=ROCK_FACE, seed=80)

    draw_lammergeier_silhouette(ax, 50, 58, scale=2.0, color=CARVED_LINE)

    # Patina
    rng = np.random.default_rng(81)
    for _ in range(5):
        px, py = rng.uniform(15, 85), rng.uniform(35, 75)
        ax.add_patch(plt.Circle((px, py), rng.uniform(3, 8),
                                 color=PATINA, alpha=0.06, zorder=5))

    # ── Annotations (below and flanking) ──
    # Left annotations
    ann_lx = 12
    ax.text(ann_lx, 26, "Bone-Eater", fontsize=10, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_lx, 22, [
        "Drops bones from 50\u201380 m height",
        "Extracts marrow from shattered remains",
        "80% of diet is bone",
        "Stomach acid pH ~1 dissolves bone",
    ], fontsize=8)

    # Centre-right annotations
    ann_rx = 55
    ax.text(ann_rx, 26, "Wingspan & Cosmetics", fontsize=10, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    annotation_plate(ax, ann_rx, 22, [
        "Wingspan: 2.3\u20132.8 m",
        "Cosmetic mud-bathing in iron oxide",
        "Plumage turns russet-orange",
        "Deliberate \u2014 not incidental staining",
    ], fontsize=8)

    # Bottom centre: mythology
    ax.text(50, 10, "Homa (Avestan hum\u0101) \u2014 the mythical bird of Persian lore.\n"
            "Zoroastrian texts: its shadow brings fortune. Ferdowsi\u2019s Shahnameh: it raises the hero Z\u0101l.",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", va="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "lammergeier-plate.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 9: Petroglyph Sites Map
# ═══════════════════════════════════════════════════════════════════

def petroglyph_sites():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=909)

    title_block(ax, "Petroglyph Sites Along the Indus",
                "30,000 carvings, 5,000 inscriptions \u2014 the world\u2019s largest open-air gallery")

    # ── Indus River (flowing from upper-right to lower-left) ──
    river_pts = [
        (82, 78), (72, 70), (60, 60), (50, 52), (42, 45),
        (35, 38), (28, 32), (20, 25), (15, 18),
    ]
    river_arr = np.array(river_pts)
    # Smooth the river with interpolation
    from scipy.interpolate import make_interp_spline
    try:
        t = np.linspace(0, 1, len(river_arr))
        t_smooth = np.linspace(0, 1, 200)
        spl_x = make_interp_spline(t, river_arr[:, 0], k=3)
        spl_y = make_interp_spline(t, river_arr[:, 1], k=3)
        rx, ry = spl_x(t_smooth), spl_y(t_smooth)
    except ImportError:
        rx, ry = river_arr[:, 0], river_arr[:, 1]

    ax.plot(rx, ry, color=INDUS_BLUE, linewidth=4, alpha=0.6,
            solid_capstyle="round", zorder=2)
    ax.plot(rx, ry, color=INDUS_DARK, linewidth=1, alpha=0.3,
            solid_capstyle="round", zorder=3)

    # Flow arrow
    ax.annotate("", xy=(15, 18), xytext=(22, 26),
                arrowprops=dict(arrowstyle="-|>", color=INDUS_DARK,
                                linewidth=1.5))
    ax.text(12, 15, "flow", fontsize=8, color=INDUS_DARK,
            fontfamily="serif", fontstyle="italic", zorder=4)

    # ── Sites along the river ──
    sites = [
        (78, 75, "Thalpan", True),     # largest
        (68, 67, "Chilas", False),
        (58, 58, "Oshibat", False),
        (52, 53, "Shatial Bridge", False),
        (44, 47, "Dadam Das", False),
        (38, 41, "Hodar", False),
        (33, 36, "Gichi Nala", False),
        (26, 30, "Shatial Das", False),
        (22, 27, "Minar Gah", False),
    ]

    for sx, sy, name, is_major in sites:
        r = 1.5 if is_major else 1.0
        color = THERMAL if is_major else CARVED_LINE
        ax.add_patch(plt.Circle((sx, sy), r, facecolor=color,
                                 edgecolor=INK, linewidth=0.8,
                                 alpha=0.8, zorder=5))
        # Label offset alternating sides
        offset_x = 4 if sx % 2 == 0 else -4
        ha = "left" if offset_x > 0 else "right"
        fs = 10 if is_major else 8
        ax.text(sx + offset_x, sy, name, fontsize=fs, color=INK,
                fontfamily="serif", fontweight="bold" if is_major else "normal",
                ha=ha, va="center", zorder=6)
        if is_major:
            ax.text(sx + offset_x, sy - 3, "(largest site:\n~5,000 carvings)",
                    fontsize=7, color=INK_LIGHT, fontfamily="serif",
                    fontstyle="italic", ha=ha, zorder=6)

    # ── Dam threat zone (dashed rectangle) ──
    dam_x, dam_y = 40, 38
    dam_w, dam_h = 30, 20
    ax.add_patch(FancyBboxPatch(
        (dam_x - dam_w / 2, dam_y - dam_h / 2), dam_w, dam_h,
        boxstyle="round,pad=0.3",
        facecolor="none", edgecolor=THERMAL,
        linewidth=1.5, linestyle="--", zorder=4))
    ax.text(dam_x + dam_w / 2 + 2, dam_y + dam_h / 2,
            "DAM THREAT\nZONE", fontsize=8, color=THERMAL,
            fontfamily="serif", fontweight="bold", ha="left",
            va="top", zorder=6)

    # ── Summary stats ──
    ax.text(50, 10, "Total: ~30,000 carvings  |  ~5,000 inscriptions  |  9 major sites\n"
            "Spanning from Prehistoric (~8,000 BCE) to Islamic period (12th c. onward)",
            fontsize=9, color=INK, fontfamily="serif", fontstyle="italic",
            ha="center", va="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "petroglyph-sites.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 10: Petroglyph Chronology
# ═══════════════════════════════════════════════════════════════════

def petroglyph_chronology():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=1010)

    title_block(ax, "Petroglyph Chronology",
                "Five phases of carving \u2014 from prehistoric ibex to Islamic calligraphy")

    # ── Five horizontal bands, stacked vertically ──
    # Phase 1 (bottom/oldest) to Phase 5 (top/newest)
    phases = [
        ("Phase 1: Prehistoric", "pre-1000 BCE", WALNUT_FAINT,
         "Animal motifs: ibex, hunting scenes",
         "No writing \u2014 pure image"),
        ("Phase 2: Proto-historic", "1000\u2013500 BCE", IBEX_HORN,
         "Maskoid faces, ceremonial scenes",
         "Okunev-style faces appear"),
        ("Phase 3: Buddhist", "1st\u20138th c. CE", OROGEN_AMBER,
         "Stupas, Buddha figures, Jataka scenes",
         "Kharoshthi, then Brahmi script"),
        ("Phase 4: Hindu-Brahmanical", "7th\u201312th c.", COLLISION_RED,
         "Tridents, linga, Shiva motifs",
         "Sanskrit, Sharada script"),
        ("Phase 5: Islamic", "12th c. onward", KOHISTAN_LT,
         "Geometric patterns, calligraphy",
         "Arabic, Persian scripts"),
    ]

    band_h = 11
    y_start = 15
    x_left, x_right = 10, 90

    for i, (title, dates, color, motifs, writing) in enumerate(phases):
        y = y_start + i * band_h + i * 2

        # Band background
        ax.add_patch(FancyBboxPatch(
            (x_left, y), x_right - x_left, band_h,
            boxstyle="round,pad=0.3",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.8, alpha=0.3, zorder=2))

        # Phase title and dates
        ax.text(x_left + 2, y + band_h - 2, title, fontsize=10,
                color=INK, fontfamily="serif", fontweight="bold",
                va="top", zorder=4)
        ax.text(x_left + 2, y + band_h - 5, dates, fontsize=8,
                color=INK_LIGHT, fontfamily="serif", fontstyle="italic",
                va="top", zorder=4)

        # Motifs
        ax.text(42, y + band_h / 2, motifs, fontsize=8, color=INK,
                fontfamily="serif", va="center", zorder=4)

        # Writing systems
        ax.text(x_right - 2, y + band_h / 2, writing, fontsize=7,
                color=INK_LIGHT, fontfamily="serif", fontstyle="italic",
                ha="right", va="center", zorder=4)

    # ── Arrow: time direction ──
    ax.annotate("", xy=(7, y_start + 5 * band_h + 8),
                xytext=(7, y_start),
                arrowprops=dict(arrowstyle="-|>", color=INK_LIGHT,
                                linewidth=1.5))
    ax.text(5, y_start + (5 * band_h + 8) / 2, "TIME",
            fontsize=9, color=INK_LIGHT, fontfamily="serif",
            fontweight="bold", ha="center", va="center",
            rotation=90, zorder=5)

    # ── Bottom note ──
    ax.text(50, 10, "Phases overlap \u2014 Buddhist and Hindu carvings coexist at many sites.\n"
            "Earlier carvings were often re-carved or superimposed by later cultures.",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", va="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "petroglyph-chronology.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 11: Motif Catalogue
# ═══════════════════════════════════════════════════════════════════

def motif_catalogue():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=1111)

    title_block(ax, "Petroglyph Motif Catalogue",
                "Six representative carvings from the Diamer corpus")

    # ── 2x3 grid of motifs on rock face ──
    cols, rows = 3, 2
    cell_w = 25
    cell_h = 28
    x_off = 7
    y_off = 12

    motifs = [
        ("Ibex", "~8,000 BCE onward"),
        ("Hunting Scene", "Prehistoric"),
        ("Buddhist Stupa", "1st\u20138th c. CE"),
        ("Maskoid Face", "1000\u2013500 BCE"),
        ("Trident / Linga", "7th\u201312th c."),
        ("Kharoshthi Inscription", "3rd c. BCE\u20133rd c. CE"),
    ]

    for idx, (name, date) in enumerate(motifs):
        col = idx % cols
        row = 1 - idx // cols  # top row first
        cx = x_off + col * (cell_w + 3) + cell_w / 2
        cy = y_off + row * (cell_h + 5) + cell_h / 2

        # Rock face cell
        rock_face_background(ax, cx - cell_w / 2, cx + cell_w / 2,
                             cy - cell_h / 2, cy + cell_h / 2,
                             color=ROCK_FACE, seed=1111 + idx)

        # Draw the motif
        if idx == 0:  # Ibex
            draw_ibex_silhouette(ax, cx, cy, scale=1.2, color=CARVED_LINE,
                                 facing_left=True)
        elif idx == 1:  # Hunting scene: archer + ibex
            draw_ibex_silhouette(ax, cx + 3, cy + 2, scale=0.8,
                                 color=CARVED_LINE, facing_left=True)
            # Archer
            ax.plot([cx - 5, cx - 5], [cy - 2, cy + 2],
                    color=CARVED_LINE, linewidth=1.5, zorder=4)
            ax.add_patch(plt.Circle((cx - 5, cy + 3), 0.8,
                                     facecolor="none", edgecolor=CARVED_LINE,
                                     linewidth=1.2, zorder=4))
            # Bow
            ts = np.linspace(-0.6, 0.6, 12)
            ax.plot(cx - 6 + 1.0 * np.cos(ts), cy + 1.5 * ts,
                    color=CARVED_LINE, linewidth=1.0, zorder=4)
            # Arrow line
            ax.plot([cx - 6, cx - 1], [cy, cy + 1],
                    color=CARVED_LINE, linewidth=0.8, zorder=4)
        elif idx == 2:  # Buddhist stupa
            # Stepped base
            for step in range(3):
                w = 6 - step * 1.5
                y_b = cy - 6 + step * 2
                ax.add_patch(FancyBboxPatch(
                    (cx - w, y_b), 2 * w, 2,
                    boxstyle="round,pad=0.1",
                    facecolor="none", edgecolor=CARVED_LINE,
                    linewidth=1.2, zorder=4))
            # Dome (half circle)
            dome_ts = np.linspace(0, math.pi, 30)
            dome_r = 4
            dome_x = cx + dome_r * np.cos(dome_ts)
            dome_y = cy + dome_r * np.sin(dome_ts)
            ax.plot(dome_x, dome_y, color=CARVED_LINE, linewidth=1.5,
                    zorder=4)
            # Spire
            ax.plot([cx, cx], [cy + dome_r, cy + dome_r + 4],
                    color=CARVED_LINE, linewidth=1.5, zorder=4)
            # Finial
            ax.plot(cx, cy + dome_r + 4.5, "o", color=CARVED_LINE,
                    markersize=3, zorder=4)
        elif idx == 3:  # Maskoid face (Okunev connection)
            # Circular face
            ax.add_patch(plt.Circle((cx, cy), 5, facecolor="none",
                                     edgecolor=CARVED_LINE, linewidth=1.5,
                                     zorder=4))
            # Eyes (dots)
            ax.plot(cx - 2, cy + 1.5, "o", color=CARVED_LINE,
                    markersize=4, zorder=4)
            ax.plot(cx + 2, cy + 1.5, "o", color=CARVED_LINE,
                    markersize=4, zorder=4)
            # Mouth (line)
            ax.plot([cx - 2, cx + 2], [cy - 2, cy - 2],
                    color=CARVED_LINE, linewidth=1.5, zorder=4)
            # Rays / headdress
            for angle in np.linspace(0.3, math.pi - 0.3, 5):
                rx = cx + 6 * math.cos(angle)
                ry = cy + 6 * math.sin(angle)
                ax.plot([cx + 5 * math.cos(angle), rx],
                        [cy + 5 * math.sin(angle), ry],
                        color=CARVED_LINE, linewidth=0.8, zorder=4)
        elif idx == 4:  # Trident / linga
            # Vertical shaft
            ax.plot([cx, cx], [cy - 7, cy + 3], color=CARVED_LINE,
                    linewidth=2.0, zorder=4)
            # Three prongs
            ax.plot([cx, cx], [cy + 3, cy + 7], color=CARVED_LINE,
                    linewidth=2.0, zorder=4)
            ax.plot([cx, cx - 3], [cy + 3, cy + 6], color=CARVED_LINE,
                    linewidth=1.5, zorder=4)
            ax.plot([cx, cx + 3], [cy + 3, cy + 6], color=CARVED_LINE,
                    linewidth=1.5, zorder=4)
            # Base (linga-like rounded base)
            base_ts = np.linspace(math.pi, 2 * math.pi, 20)
            ax.plot(cx + 2 * np.cos(base_ts), cy - 7 + 1.5 * np.sin(base_ts),
                    color=CARVED_LINE, linewidth=1.5, zorder=4)
        elif idx == 5:  # Kharoshthi inscription (stylised marks)
            # Right-to-left wavy text marks suggesting Kharoshthi
            rng_k = np.random.default_rng(555)
            for row_i in range(3):
                y_row = cy + 3 - row_i * 4
                x_start_k = cx + 6
                for ch in range(5):
                    gx = x_start_k - ch * 3
                    # Each "glyph" is a small squiggle
                    g_ts = np.linspace(0, 1, 8)
                    g_xs = gx + rng_k.uniform(-0.3, 0.3, 8)
                    g_ys = y_row + 2 * g_ts + rng_k.uniform(-0.3, 0.3, 8)
                    ax.plot(g_xs, g_ys, color=CARVED_LINE,
                            linewidth=1.2, zorder=4)
                    # Add a crossbar or dot randomly
                    if rng_k.random() > 0.5:
                        ax.plot([gx - 0.5, gx + 0.5],
                                [y_row + 1, y_row + 1],
                                color=CARVED_LINE, linewidth=0.8, zorder=4)

        # Label below cell
        ax.text(cx, cy - cell_h / 2 - 2, name, fontsize=9, color=INK,
                fontfamily="serif", fontweight="bold", ha="center",
                zorder=5)
        ax.text(cx, cy - cell_h / 2 - 5, date, fontsize=7,
                color=INK_LIGHT, fontfamily="serif", fontstyle="italic",
                ha="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "motif-catalogue.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 12: Nanga Parbat Three Faces
# ═══════════════════════════════════════════════════════════════════

def nanga_parbat_faces():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=1212)

    title_block(ax, "Three Faces of Nanga Parbat",
                "Rupal (south) \u2014 Diamir (west) \u2014 Rakhiot (north)")

    # Three side-by-side panels
    panels = [
        ("Rupal Face (South)", 5, 30, "4,600 m rock face\nlargest on Earth",
         0.95, GNEISS),
        ("Diamir Face (West)", 36, 63, "The \u2018Killer Mountain\u2019\nfirst ascent face",
         0.80, GNEISS_DARK),
        ("Rakhiot Face (North)", 68, 95, "Rakhiot Glacier\nMummery\u2019s route",
         0.85, KOHISTAN),
    ]

    y_base = 15
    y_top = 80

    for label, x_left, x_right, note, height_frac, color in panels:
        # Mountain profile
        xs = np.linspace(x_left, x_right, 80)
        peak_x = (x_left + x_right) / 2
        peak_y = y_base + (y_top - y_base) * height_frac
        profile = y_base + (peak_y - y_base) * np.exp(-((xs - peak_x) / ((x_right - x_left) / 4)) ** 2)
        # Add ridges
        rng = np.random.default_rng(int(x_left * 10))
        for _ in range(3):
            ridge_x = rng.uniform(x_left + 3, x_right - 3)
            ridge_h = rng.uniform(5, 12)
            ridge_w = rng.uniform(3, 6)
            profile += ridge_h * np.exp(-((xs - ridge_x) / ridge_w) ** 2)
        profile = np.clip(profile, y_base, 90)

        ax.fill_between(xs, y_base, profile, color=color, alpha=0.4,
                         zorder=2)
        ax.plot(xs, profile, color=INK, linewidth=1.0, zorder=3)

        # Snow cap
        snow_line = y_base + (y_top - y_base) * 0.55
        mask = profile > snow_line
        if np.any(mask):
            ax.fill_between(xs[mask], snow_line, profile[mask],
                             color=SNOW, alpha=0.5, zorder=4)

        # Glacier tongue
        glacier_cx = peak_x
        draw_glacier(ax, glacier_cx - 1, glacier_cx + 0.5,
                     snow_line, y_base + 5,
                     color=GLACIER_BLUE, dark=GLACIER_DARK,
                     seed=int(x_left))

        # Label
        ax.text((x_left + x_right) / 2, y_base - 2, label,
                fontsize=9, color=INK, fontfamily="serif",
                fontweight="bold", ha="center", va="top", zorder=5)

        # Note
        ax.text((x_left + x_right) / 2, y_base - 6, note,
                fontsize=7, color=INK_LIGHT, fontfamily="serif",
                fontstyle="italic", ha="center", va="top", zorder=5)

    # ── Panel dividers ──
    for div_x in [33.5, 65.5]:
        ax.plot([div_x, div_x], [y_base - 8, y_top + 5],
                color=INK_FAINT, linewidth=0.5, linestyle=":",
                zorder=1)

    # ── Summit elevation ──
    ax.text(50, 86, "8,126 m \u2014 ninth highest on Earth",
            fontsize=10, color=INK, fontfamily="serif",
            fontweight="bold", ha="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "nanga-parbat-faces.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 13: Glacier Marriage
# ═══════════════════════════════════════════════════════════════════

def glacier_marriage():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=1313)

    title_block(ax, "Glacier Marriage \u2014 Glacier Grafting",
                "A living tradition \u2014 human-made glaciers from two parents")

    # ── Male glacier (left) — dark, angular, debris-covered ──
    male_x, male_y = 22, 62
    # Angular debris-covered shape
    male_pts = np.array([
        [male_x - 10, male_y - 8],
        [male_x - 6, male_y + 10],
        [male_x + 2, male_y + 12],
        [male_x + 8, male_y + 6],
        [male_x + 10, male_y - 4],
        [male_x + 4, male_y - 10],
        [male_x - 10, male_y - 8],
    ])
    ax.fill(male_pts[:, 0], male_pts[:, 1], color=GLACIER_DARK,
            alpha=0.6, zorder=2)
    ax.plot(male_pts[:, 0], male_pts[:, 1], color=INK, linewidth=1.2,
            zorder=3)
    # Debris marks
    rng = np.random.default_rng(131)
    for _ in range(8):
        dx = male_x + rng.uniform(-6, 6)
        dy = male_y + rng.uniform(-6, 8)
        ax.plot(dx, dy, ".", color=GNEISS_DARK, markersize=rng.uniform(2, 5),
                zorder=3)
    ax.text(male_x, male_y - 13, "Male Glacier", fontsize=10, color=INK,
            fontfamily="serif", fontweight="bold", ha="center", zorder=5)
    ax.text(male_x, male_y - 16, "dark, angular,\ndebris-covered",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ── Female glacier (right) — white, clean, smooth ──
    female_x, female_y = 78, 62
    # Smooth rounded shape
    ts = np.linspace(0, 2 * math.pi, 40)
    fem_r_x = 9 + 2 * np.cos(2 * ts)
    fem_r_y = 10 + 1.5 * np.sin(3 * ts)
    fem_xs = female_x + fem_r_x * np.cos(ts)
    fem_ys = female_y + fem_r_y * np.sin(ts)
    ax.fill(fem_xs, fem_ys, color=GLACIER_BLUE, alpha=0.4, zorder=2)
    ax.plot(fem_xs, fem_ys, color=GLACIER_DARK, linewidth=1.0, zorder=3)
    # Snow highlights
    for _ in range(5):
        sx = female_x + rng.uniform(-5, 5)
        sy = female_y + rng.uniform(-5, 7)
        ax.add_patch(plt.Circle((sx, sy), rng.uniform(1, 3),
                                 color=SNOW, alpha=0.3, zorder=3))
    ax.text(female_x, female_y - 14, "Female Glacier", fontsize=10,
            color=INK, fontfamily="serif", fontweight="bold",
            ha="center", zorder=5)
    ax.text(female_x, female_y - 17, "white, clean,\nsmooth ice",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ── Basket symbol (between them) ──
    basket_x, basket_y = 50, 65
    # Simple basket shape
    b_w, b_h = 4, 3
    basket_pts = np.array([
        [basket_x - b_w, basket_y + b_h],
        [basket_x - b_w * 0.7, basket_y - b_h],
        [basket_x + b_w * 0.7, basket_y - b_h],
        [basket_x + b_w, basket_y + b_h],
    ])
    ax.plot(basket_pts[:, 0], basket_pts[:, 1], color=IBEX_HORN,
            linewidth=2.0, zorder=4)
    # Basket handle
    handle_ts = np.linspace(0, math.pi, 20)
    ax.plot(basket_x + 3 * np.cos(handle_ts),
            basket_y + b_h + 2 * np.sin(handle_ts),
            color=IBEX_HORN, linewidth=1.5, zorder=4)
    # Cross-hatching inside basket
    for i in range(3):
        frac = (i + 1) / 4
        y_line = basket_y - b_h + frac * 2 * b_h
        x_span = b_w * (0.7 + 0.3 * frac)
        ax.plot([basket_x - x_span, basket_x + x_span],
                [y_line, y_line],
                color=IBEX_HORN, linewidth=0.8, alpha=0.6, zorder=4)

    ax.text(basket_x, basket_y - 5, "basket with\nice fragments",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # Arrows from parents to basket
    ax.annotate("", xy=(basket_x - 5, basket_y),
                xytext=(male_x + 10, male_y),
                arrowprops=dict(arrowstyle="-|>", color=INK_LIGHT,
                                linewidth=1.2, connectionstyle="arc3,rad=0.2"))
    ax.annotate("", xy=(basket_x + 5, basket_y),
                xytext=(female_x - 10, female_y),
                arrowprops=dict(arrowstyle="-|>", color=INK_LIGHT,
                                linewidth=1.2, connectionstyle="arc3,rad=-0.2"))

    # ── Timeline: 12-year gestation ──
    tl_y = 32
    tl_x_left, tl_x_right = 20, 80
    ax.plot([tl_x_left, tl_x_right], [tl_y, tl_y], color=INK_FAINT,
            linewidth=1.0, zorder=2)
    for yr in range(13):
        x_tick = tl_x_left + yr * (tl_x_right - tl_x_left) / 12
        ax.plot([x_tick, x_tick], [tl_y - 1, tl_y + 1],
                color=INK_LIGHT, linewidth=0.6, zorder=3)
        if yr % 3 == 0:
            ax.text(x_tick, tl_y - 2.5, f"yr {yr}", fontsize=6,
                    color=INK_LIGHT, fontfamily="serif", ha="center",
                    zorder=4)
    ax.text(50, tl_y + 3, "12-year gestation period", fontsize=10,
            color=INK, fontfamily="serif", fontweight="bold",
            ha="center", zorder=5)

    # Arrow from basket down to timeline
    ax.annotate("", xy=(50, tl_y + 5), xytext=(50, basket_y - 7),
                arrowprops=dict(arrowstyle="-|>", color=INK_LIGHT,
                                linewidth=1.0))

    # ── Newborn glacier (small, at bottom) ──
    baby_x, baby_y = 50, 20
    baby_ts = np.linspace(0, 2 * math.pi, 30)
    baby_r = 5
    baby_xs = baby_x + baby_r * np.cos(baby_ts)
    baby_ys = baby_y + baby_r * 0.6 * np.sin(baby_ts)
    ax.fill(baby_xs, baby_ys, color=GLACIER_BLUE, alpha=0.3, zorder=2)
    ax.plot(baby_xs, baby_ys, color=GLACIER_DARK, linewidth=1.0, zorder=3)
    ax.text(baby_x, baby_y, "newborn\nglacier", fontsize=9, color=INK,
            fontfamily="serif", fontweight="bold", ha="center",
            va="center", zorder=5)

    # Arrow from timeline to newborn
    ax.annotate("", xy=(50, baby_y + 4), xytext=(50, tl_y - 3),
                arrowprops=dict(arrowstyle="-|>", color=INK_LIGHT,
                                linewidth=1.0))

    # ── Success rate ──
    ax.text(85, 20, "~80%\nsuccess\nrate", fontsize=11, color=THERMAL,
            fontfamily="serif", fontweight="bold", ha="center",
            va="center", zorder=5)

    # ── Poetic note ──
    ax.text(50, 8, "One of the most poetic technologies in human history \u2014\n"
            "communities in Baltistan and Gilgit-Baltistan breed glaciers\n"
            "to create water sources for future generations.",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", va="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=2)
    save_fig(fig, OUT / "glacier-marriage.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 14: Flora Elevation Profile
# ═══════════════════════════════════════════════════════════════════

def flora_elevation():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=1414)

    title_block(ax, "Flora by Elevation \u2014 Valley to Summit",
                "Vegetation zones of the Nanga Parbat massif")

    # ── Mountain profile ──
    x_left, x_right = 15, 85
    y_valley = 15   # ~1,000 m
    y_summit = 88   # 8,126 m

    xs = np.linspace(x_left, x_right, 200)
    peak_x = 50
    profile = y_valley + (y_summit - y_valley) * np.exp(-((xs - peak_x) / 25) ** 2)
    profile += 5 * np.exp(-((xs - 35) / 12) ** 2)
    profile += 5 * np.exp(-((xs - 65) / 12) ** 2)
    profile = np.clip(profile, y_valley, 95)

    # Draw mountain outline
    ax.plot(xs, profile, color=GNEISS_DARK, linewidth=1.5, zorder=6)

    # ── Vegetation zones (horizontal bands clipped to mountain) ──
    # Elevations mapped to y coordinates
    # 1,000m = y_valley, 8,126m = y_summit
    m_per_y = (8126 - 1000) / (y_summit - y_valley)

    def elev_to_y(m):
        return y_valley + (m - 1000) / m_per_y

    zones = [
        (1000, 2500, APRICOT, 0.35, "Valley Orchards",
         "apricot, cherry, walnut, mulberry"),
        (2500, 3500, JUNIPER, 0.30, "Montane Juniper",
         "Juniperus excelsa, birch, pine"),
        (3500, 4200, KOHISTAN_LT, 0.30, "Subalpine Scrub",
         "dwarf juniper, rhododendron, willow"),
        (4200, 5200, MEADOW, 0.35, "Alpine Meadow (jut)",
         "the peri\u2019s domain \u2014 wildflowers, grasses"),
        (5200, 8126, SNOW, 0.30, "Nival Zone",
         "lichens, mosses, bare rock, permanent snow"),
    ]

    for elev_bot, elev_top, color, alpha, name, species in zones:
        y_bot = elev_to_y(elev_bot)
        y_top = elev_to_y(elev_top)

        # Fill only within the mountain profile
        band_bot = np.maximum(np.full_like(xs, y_bot), y_valley)
        band_top = np.minimum(np.full_like(xs, y_top), profile)
        mask = band_top > band_bot
        if np.any(mask):
            ax.fill_between(xs[mask], band_bot[mask], band_top[mask],
                             color=color, alpha=alpha, zorder=3)

        # Label on the right side
        label_y = (y_bot + y_top) / 2
        ax.text(x_right + 2, label_y, f"{name}", fontsize=8,
                color=INK, fontfamily="serif", fontweight="bold",
                va="center", zorder=5)
        ax.text(x_right + 2, label_y - 2.5, species, fontsize=7,
                color=INK_LIGHT, fontfamily="serif", fontstyle="italic",
                va="center", zorder=5)

        # Horizontal guide line
        ax.plot([x_left - 1, x_right + 1], [y_bot, y_bot],
                color=INK_FAINT, linewidth=0.3, linestyle=":",
                zorder=2)

    # ── Treeline (dashed) ──
    treeline_y = elev_to_y(3600)  # ~3,500-3,800m
    ax.plot([x_left, x_right], [treeline_y, treeline_y],
            color=JUNIPER, linewidth=1.5, linestyle="--", zorder=5)
    ax.text(x_left - 1, treeline_y, "treeline\n~3,500\u20133,800 m",
            fontsize=8, color=JUNIPER, fontfamily="serif",
            fontweight="bold", ha="right", va="center", zorder=5)

    # ── Elevation scale (left side) ──
    scale_x = x_left - 5
    elevations = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
    for elev in elevations:
        y = elev_to_y(elev)
        if y <= y_summit:
            ax.plot([scale_x, scale_x + 2], [y, y],
                    color=INK_FAINT, linewidth=0.5, zorder=2)
            ax.text(scale_x - 1, y, f"{elev} m", fontsize=6,
                    color=INK_LIGHT, fontfamily="serif", ha="right",
                    va="center", zorder=5)
    ax.plot([scale_x + 1, scale_x + 1], [y_valley, y_summit],
            color=INK_FAINT, linewidth=0.5, zorder=1)

    # ── Summit label ──
    ax.text(peak_x, y_summit + 2, "8,126 m", fontsize=10, color=INK,
            fontfamily="serif", fontweight="bold", ha="center", zorder=7)

    attribution(ax, ATTR_TEXT, y=3)
    save_fig(fig, OUT / "flora-elevation.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 15: Writing Systems
# ═══════════════════════════════════════════════════════════════════

def writing_systems():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=1515)

    title_block(ax, "Writing Systems of the Upper Indus",
                "Eight scripts carved in stone \u2014 the mountain as palimpsest")

    # ── Vertical list of 8 writing systems ──
    scripts = [
        ("Kharoshthi", "3rd c. BCE \u2013 3rd c. CE",
         "right-to-left", "Gandharan trade route", "angular"),
        ("Brahmi", "1st \u2013 6th c. CE",
         "left-to-right", "Indian imperial influence", "rounded"),
        ("Sogdian", "2nd \u2013 8th c. CE",
         "vertical / right-to-left", "Silk Road merchants", "cursive"),
        ("Chinese", "dated inscriptions",
         "top-to-bottom", "Chinese pilgrims and envoys", "logographic"),
        ("Bactrian", "Kushan period",
         "left-to-right", "Greek-derived, Kushan empire", "angular-greek"),
        ("Hebrew", "scattered examples",
         "right-to-left", "Jewish traders on Silk Road", "angular"),
        ("Sharada", "7th \u2013 12th c.",
         "left-to-right", "Hindu-Brahmanical period", "angular-serif"),
        ("Arabic / Persian", "12th c. onward",
         "right-to-left", "Islamic arrival, enduring", "calligraphic"),
    ]

    row_h = 8
    y_start = 82
    x_name = 5
    x_date = 28
    x_dir = 48
    x_glyph = 68

    rng = np.random.default_rng(1515)

    for i, (name, dates, direction, trade, style) in enumerate(scripts):
        y = y_start - i * row_h

        # Subtle background band
        if i % 2 == 0:
            ax.add_patch(FancyBboxPatch(
                (3, y - row_h / 2 + 1), 94, row_h - 2,
                boxstyle="round,pad=0.2",
                facecolor=PARCHMENT_DK, edgecolor="none",
                alpha=0.3, zorder=1))

        # Name
        ax.text(x_name, y, name, fontsize=10, color=INK,
                fontfamily="serif", fontweight="bold", va="center",
                zorder=4)

        # Date range
        ax.text(x_date, y, dates, fontsize=8, color=INK_LIGHT,
                fontfamily="serif", fontstyle="italic", va="center",
                zorder=4)

        # Direction / trade
        ax.text(x_dir, y, f"{direction}", fontsize=7,
                color=INK_LIGHT, fontfamily="serif", va="center",
                zorder=4)

        # Stylised glyphs (artistic squiggles suggesting the script)
        glyph_x = x_glyph
        n_glyphs = 5
        for g in range(n_glyphs):
            gx = glyph_x + g * 5
            if style == "angular":
                # Angular strokes
                pts_x = gx + rng.uniform(-0.5, 2.5, 4)
                pts_y = y + rng.uniform(-1.5, 1.5, 4)
                ax.plot(pts_x, pts_y, color=CARVED_LINE, linewidth=1.2,
                        zorder=4)
            elif style == "rounded":
                # Curved strokes
                ts = np.linspace(0, math.pi, 8)
                ax.plot(gx + 1.5 * np.cos(ts + rng.uniform(0, 2)),
                        y + 1.2 * np.sin(ts + rng.uniform(0, 1)),
                        color=CARVED_LINE, linewidth=1.0, zorder=4)
            elif style == "cursive":
                # Flowing connected strokes
                ts = np.linspace(0, 2, 10)
                ax.plot(gx + ts, y + 0.8 * np.sin(ts * 3 + rng.uniform(0, 3)),
                        color=CARVED_LINE, linewidth=0.9, zorder=4)
            elif style == "logographic":
                # Box-like structures
                bx, by = gx, y - 1
                ax.plot([bx, bx + 2, bx + 2, bx, bx],
                        [by, by, by + 2, by + 2, by],
                        color=CARVED_LINE, linewidth=0.8, zorder=4)
                ax.plot([bx + 0.5, bx + 1.5], [by + 1, by + 1],
                        color=CARVED_LINE, linewidth=0.6, zorder=4)
            elif style == "angular-greek":
                # Angular with Greek influence
                pts_x = [gx, gx + 1, gx + 2, gx + 1.5]
                pts_y = [y - 1, y + 1, y - 0.5, y + 1.5]
                ax.plot(pts_x, pts_y, color=CARVED_LINE, linewidth=1.0,
                        zorder=4)
            elif style == "angular-serif":
                # Angular with serifs (horizontal end strokes)
                ax.plot([gx, gx], [y - 1, y + 1.5], color=CARVED_LINE,
                        linewidth=1.0, zorder=4)
                ax.plot([gx - 0.3, gx + 0.8], [y + 1.5, y + 1.5],
                        color=CARVED_LINE, linewidth=0.8, zorder=4)
                ax.plot([gx + 0.5, gx + 1.5], [y, y + 0.5],
                        color=CARVED_LINE, linewidth=0.8, zorder=4)
            elif style == "calligraphic":
                # Flowing calligraphic strokes
                ts = np.linspace(0, 1.5, 12)
                ax.plot(gx + 2 * ts,
                        y + 1.0 * np.sin(ts * 4 + rng.uniform(0, 4)),
                        color=CARVED_LINE, linewidth=1.3, zorder=4)

    # ── Bottom note ──
    ax.text(50, 8, "The Upper Indus corridor was a crossroads of civilisations.\n"
            "Eight writing systems on a single stretch of river \u2014 "
            "the mountain as palimpsest.",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", va="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=2)
    save_fig(fig, OUT / "writing-systems.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 16: Bitan Trance
# ═══════════════════════════════════════════════════════════════════

def bitan_trance():
    fig, ax = make_fig(width=14, height=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    add_parchment_texture(ax, seed=1616)

    title_block(ax, "The Bitan in Trance",
                "When the peri descend \u2014 spirit possession in the high valleys")

    # ── Central circle: the bitan ──
    centre_x, centre_y = 50, 50
    circle_r = 18
    ax.add_patch(plt.Circle((centre_x, centre_y), circle_r,
                             facecolor=PARCHMENT_DK, edgecolor=INK_FAINT,
                             linewidth=1.5, alpha=0.5, zorder=2))

    # Simple human figure (the bitan)
    bx, by = centre_x, centre_y - 2
    # Head
    ax.add_patch(plt.Circle((bx, by + 8), 2.5, facecolor="none",
                             edgecolor=CARVED_LINE, linewidth=2.0,
                             zorder=4))
    # Body
    ax.plot([bx, bx], [by + 5.5, by - 2], color=CARVED_LINE,
            linewidth=2.0, zorder=4)
    # Arms (raised — trance posture)
    ax.plot([bx, bx - 5], [by + 3, by + 7], color=CARVED_LINE,
            linewidth=1.5, zorder=4)
    ax.plot([bx, bx + 5], [by + 3, by + 7], color=CARVED_LINE,
            linewidth=1.5, zorder=4)
    # Legs
    ax.plot([bx, bx - 3], [by - 2, by - 8], color=CARVED_LINE,
            linewidth=1.5, zorder=4)
    ax.plot([bx, bx + 3], [by - 2, by - 8], color=CARVED_LINE,
            linewidth=1.5, zorder=4)

    # Iron bangle on wrist (small circle)
    ax.add_patch(plt.Circle((bx - 5, by + 7), 0.8, facecolor="none",
                             edgecolor=GNEISS_DARK, linewidth=1.5,
                             zorder=5))
    ax.text(bx - 9, by + 7, "iron\nbangle", fontsize=6, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", ha="center",
            va="center", zorder=5)

    # ── Juniper smoke (above, rising wisps) ──
    smoke_base_y = centre_y + circle_r + 2
    for i in range(5):
        sx = centre_x + (i - 2) * 4
        ts = np.linspace(0, 1, 20)
        wisp_x = sx + 3 * np.sin(ts * math.pi * 2 + i * 0.7)
        wisp_y = smoke_base_y + ts * 15
        alpha = 0.4 - i * 0.05
        ax.plot(wisp_x, wisp_y, color=JUNIPER, linewidth=1.5,
                alpha=max(alpha, 0.1), zorder=3)

    ax.text(centre_x, smoke_base_y + 17, "juniper smoke",
            fontsize=9, color=JUNIPER, fontfamily="serif",
            fontweight="bold", ha="center", zorder=5)

    # ── Surnai player (left) ──
    sp_x, sp_y = 15, 50
    # Stick figure
    ax.add_patch(plt.Circle((sp_x, sp_y + 5), 1.5, facecolor="none",
                             edgecolor=CARVED_LINE, linewidth=1.2,
                             zorder=4))
    ax.plot([sp_x, sp_x], [sp_y + 3.5, sp_y - 2], color=CARVED_LINE,
            linewidth=1.2, zorder=4)
    ax.plot([sp_x, sp_x - 2], [sp_y - 2, sp_y - 6], color=CARVED_LINE,
            linewidth=1.0, zorder=4)
    ax.plot([sp_x, sp_x + 2], [sp_y - 2, sp_y - 6], color=CARVED_LINE,
            linewidth=1.0, zorder=4)
    # Instrument (surnai — elongated cone)
    ax.plot([sp_x + 1, sp_x + 8], [sp_y + 3, sp_y + 1],
            color=IBEX_HORN, linewidth=2.5, zorder=4)
    ax.plot(sp_x + 8, sp_y + 1, ">", color=IBEX_HORN,
            markersize=8, zorder=4)

    ax.text(sp_x, sp_y - 9, "surnai\nplayer", fontsize=8, color=INK,
            fontfamily="serif", fontweight="bold", ha="center", zorder=5)

    # ── The peri descending (right) — ethereal wavy shape ──
    peri_x, peri_y = 85, 55
    for i in range(7):
        ts = np.linspace(0, 1, 15)
        wave_x = peri_x + (i - 3) * 1.5 + 2 * np.sin(ts * math.pi)
        wave_y = peri_y + 15 * ts
        alpha = 0.15 + 0.05 * (3 - abs(i - 3))
        ax.plot(wave_x, wave_y, color=GLACIER_BLUE, linewidth=1.8,
                alpha=alpha, zorder=3)

    # Suggestion of a face in the ethereal shape
    ax.add_patch(plt.Circle((peri_x, peri_y + 12), 2, facecolor="none",
                             edgecolor=GLACIER_BLUE, linewidth=0.8,
                             linestyle=":", alpha=0.4, zorder=3))

    ax.text(peri_x, peri_y - 3, "the peri\ndescending", fontsize=8,
            color=GLACIER_BLUE, fontfamily="serif", fontstyle="italic",
            ha="center", zorder=5)

    # ── 5 specialist categories around the circle ──
    specialists = [
        (20, 78, "d\u0101nyal\n(diviner)"),
        (80, 78, "hakim\n(healer)"),
        (10, 30, "sh\u0101mun\n(rain-caller)"),
        (90, 30, "b\u0113t\u0101l\n(corpse-speaker)"),
        (50, 15, "b\u012bt\u0101n\n(the possessed)"),
    ]

    for sx, sy, label in specialists:
        ax.add_patch(plt.Circle((sx, sy), 4, facecolor=PARCHMENT_DK,
                                 edgecolor=INK_FAINT, linewidth=0.8,
                                 alpha=0.5, zorder=2))
        ax.text(sx, sy, label, fontsize=7, color=INK,
                fontfamily="serif", ha="center", va="center", zorder=5)

    # ── Key insight at bottom ──
    ax.text(50, 6, "\"The peri speak Shina regardless of the bitan\u2019s mother tongue\"",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, ATTR_TEXT, y=2)
    save_fig(fig, OUT / "bitan-trance.png")


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

def main():
    print("Generating illustrations for Diamer survey...")
    print(f"Output: {OUT}\n")
    deep_time_timeline()
    tectonic_aneurysm()
    ibex_species_plate()
    india_drift()
    indus_gorge_profile()
    markhor_plate()
    snow_leopard_plate()
    lammergeier_plate()
    petroglyph_sites()
    petroglyph_chronology()
    motif_catalogue()
    nanga_parbat_faces()
    glacier_marriage()
    flora_elevation()
    writing_systems()
    bitan_trance()
    print(f"\nDone. 16 illustrations generated.")


if __name__ == "__main__":
    main()
