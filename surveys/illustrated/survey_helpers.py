"""
Shared matplotlib primitives for illustrated surveys.

Extends the patterns from story illustration scripts (the-mineral-deposits,
the-weavers-loom) into a reusable toolkit for survey diagrams: geological
cross-sections, deep-time timelines, species plates, petroglyph motifs,
elevation profiles, and schematic maps.

Visual identity: parchment background, walnut ink, serif typography,
diagrammatic line art. No photorealism — the ibex is a petroglyph,
not a photograph.

Import from generate_illustrations.py with:
    import sys; sys.path.insert(0, str(Path(__file__).parent))
    from survey_helpers import *
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np


# ── Base Palette ────────────────────────────────────────────────────

PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"
WALNUT        = "#4A3728"
WALNUT_LIGHT  = "#6B5040"
WALNUT_FAINT  = "#A08B70"
SNOW          = "#E8EEF0"
SKY           = "#D8C8B0"

# Defaults
DPI = 150
W, H = 12, 9  # inches — 1800x1350 px


# ── Canvas Helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H, bg=PARCHMENT):
    """Create a figure with parchment background, axes off, aspect equal."""
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def add_parchment_texture(ax, seed=42, n_spots=8):
    """Subtle circular stains for paper texture."""
    rng = np.random.default_rng(seed)
    for _ in range(n_spots):
        cx, cy = rng.uniform(10, 90), rng.uniform(10, 90)
        r = rng.uniform(5, 15)
        circle = plt.Circle((cx, cy), r, color=PARCHMENT_DK,
                             alpha=rng.uniform(0.15, 0.35), zorder=0)
        ax.add_patch(circle)


def title_block(ax, title, subtitle="", y=95):
    """Centred title + optional subtitle in serif."""
    ax.text(50, y, title, ha="center", va="top",
            fontsize=18, fontweight="bold", color=INK,
            fontfamily="serif")
    if subtitle:
        ax.text(50, y - 4, subtitle, ha="center", va="top",
                fontsize=11, fontstyle="italic", color=INK_LIGHT,
                fontfamily="serif")


def attribution(ax, text="Illustrated Survey — Diamer and Nanga Parbat", y=2):
    """Bottom-centre attribution line."""
    ax.text(50, y, text, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=INK_LIGHT,
            fontfamily="serif")


def save_fig(fig, path, bg=PARCHMENT):
    """Save and close with standard settings."""
    fig.savefig(path, dpi=DPI, bbox_inches="tight",
                facecolor=bg, pad_inches=0.3)
    plt.close(fig)
    print(f"  \u2713 {Path(path).name}")


# ── Geological Helpers ──────────────────────────────────────────────

def draw_strata(ax, x_start, x_end, y_base, layers, wobble_seed=42):
    """Draw horizontal geological strata.

    layers: list of (thickness, color, alpha) tuples, bottom to top.
    Returns y_top after all layers drawn.
    """
    rng = np.random.default_rng(wobble_seed)
    y = y_base
    xs = np.linspace(x_start, x_end, 80)
    for thickness, color, alpha in layers:
        top = y + thickness + rng.uniform(-thickness * 0.1, thickness * 0.1, 80)
        bot = np.full_like(xs, y)
        ax.fill_between(xs, bot, top, color=color, alpha=alpha, zorder=3)
        ax.plot(xs, top, color=INK, linewidth=0.3, alpha=0.3, zorder=4)
        y += thickness
    return y


def draw_fault_line(ax, x, y_start, y_end, color=INK, style="--"):
    """Vertical or near-vertical fault/suture line."""
    ys = np.linspace(y_start, y_end, 40)
    rng = np.random.default_rng(int(x * 100))
    xs = x + rng.uniform(-0.5, 0.5, 40)
    ax.plot(xs, ys, color=color, linewidth=1.2, linestyle=style,
            alpha=0.7, zorder=5)


def draw_cross_section_frame(ax, x_start, x_end, y_start, y_end,
                              label_left="", label_right="",
                              depth_labels=None):
    """Draw a framing box for a geological cross-section with optional
    depth scale on the left."""
    ax.plot([x_start, x_end], [y_start, y_start], color=INK_FAINT,
            linewidth=0.8, zorder=1)
    ax.plot([x_start, x_end], [y_end, y_end], color=INK_FAINT,
            linewidth=0.8, zorder=1)
    if label_left:
        ax.text(x_start - 1, (y_start + y_end) / 2, label_left,
                fontsize=8, color=INK_LIGHT, fontfamily="serif",
                fontstyle="italic", ha="right", va="center",
                rotation=90, zorder=5)
    if label_right:
        ax.text(x_end + 1, (y_start + y_end) / 2, label_right,
                fontsize=8, color=INK_LIGHT, fontfamily="serif",
                fontstyle="italic", ha="left", va="center",
                rotation=90, zorder=5)
    if depth_labels:
        for y_frac, label in depth_labels:
            y = y_start + y_frac * (y_end - y_start)
            ax.plot([x_start - 2, x_start], [y, y], color=INK_FAINT,
                    linewidth=0.5, zorder=1)
            ax.text(x_start - 3, y, label, fontsize=7, color=INK_LIGHT,
                    fontfamily="serif", ha="right", va="center", zorder=5)


# ── Landscape Helpers ───────────────────────────────────────────────

def draw_mountain_ridge(ax, x_start, x_end, y_base, height, n_peaks=5,
                        color="#7A7068", color_dark=None, seed=None,
                        snow_line_frac=0.7):
    """Draw a mountain ridge silhouette with optional snow caps."""
    if color_dark is None:
        # Darken by shifting toward black
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        color_dark = f"#{int(r*0.7):02x}{int(g*0.7):02x}{int(b*0.7):02x}"
    rng = np.random.default_rng(seed)
    xs = np.linspace(x_start, x_end, n_peaks * 10 + 1)
    ys = np.zeros_like(xs) + y_base
    for i in range(n_peaks):
        cx = x_start + (i + 0.5) * (x_end - x_start) / n_peaks
        cx += rng.uniform(-2, 2)
        h = height * rng.uniform(0.6, 1.0)
        w = (x_end - x_start) / n_peaks * 0.8
        ys += h * np.exp(-((xs - cx) / w) ** 2)
    snow_line = y_base + height * snow_line_frac
    ax.fill_between(xs, y_base, ys, color=color, alpha=0.5, zorder=1)
    snow_xs = xs[ys > snow_line]
    snow_ys = ys[ys > snow_line]
    if len(snow_xs) > 0:
        ax.fill_between(snow_xs, snow_line, snow_ys,
                         color=SNOW, alpha=0.4, zorder=2)
    ax.plot(xs, ys, color=color_dark, linewidth=0.8, zorder=2)
    return xs, ys


def draw_river(ax, points, color="#5A7888", width=2.0, alpha=0.6):
    """Draw a river as a smooth curve through waypoints.

    points: list of (x, y) tuples.
    """
    pts = np.array(points)
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=width,
            alpha=alpha, solid_capstyle="round", zorder=3)


def draw_glacier(ax, x_start, x_end, y_start, y_end,
                 color="#8AB0C8", dark="#5A8098", seed=None):
    """Draw a stylised glacier tongue between two elevations."""
    rng = np.random.default_rng(seed)
    n = 40
    ts = np.linspace(0, 1, n)
    # Centre line with slight meander
    cx = x_start + (x_end - x_start) * ts + rng.uniform(-0.5, 0.5, n)
    cy = y_start + (y_end - y_start) * ts
    # Width tapers from head to toe
    widths = 3 * (1 - ts * 0.6)
    left_x = cx - widths
    right_x = cx + widths
    ax.fill_betweenx(cy, left_x, right_x, color=color, alpha=0.5, zorder=2)
    ax.plot(cx, cy, color=dark, linewidth=0.6, alpha=0.5, zorder=3)


# ── Timeline Helpers ────────────────────────────────────────────────

def draw_deep_time_axis(ax, x_start, x_end, y, epochs, fontsize=7):
    """Draw a horizontal deep-time axis with epoch bands.

    epochs: list of (start_ma, end_ma, label, color) tuples.
    The axis is log-scaled: position = log10(age_ma).
    """
    all_ages = [e[0] for e in epochs] + [e[1] for e in epochs]
    max_log = math.log10(max(a for a in all_ages if a > 0) + 1)
    min_log = 0  # log10(1) = 0, representing ~1 Ma or present

    def age_to_x(ma):
        if ma <= 0:
            return x_end
        log_val = math.log10(ma)
        frac = (max_log - log_val) / max_log
        return x_start + frac * (x_end - x_start)

    # Epoch bands
    band_h = 4
    for start_ma, end_ma, label, color in epochs:
        x1 = age_to_x(start_ma)
        x2 = age_to_x(end_ma)
        ax.add_patch(FancyBboxPatch(
            (min(x1, x2), y - band_h / 2), abs(x2 - x1), band_h,
            boxstyle="round,pad=0.1",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.5, alpha=0.6, zorder=3))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y, label, ha="center", va="center",
                fontsize=fontsize, color=INK, fontfamily="serif",
                zorder=4)

    # Axis line
    ax.plot([x_start, x_end], [y - band_h / 2 - 1, y - band_h / 2 - 1],
            color=INK_FAINT, linewidth=0.8, zorder=2)

    return age_to_x


def event_marker(ax, x, y, label, color=INK, fontsize=7, above=True):
    """Place a labelled event marker on a timeline."""
    dy = 3 if above else -3
    ax.plot(x, y, "v" if above else "^", color=color,
            markersize=5, zorder=5)
    ax.text(x, y + dy, label, ha="center",
            va="bottom" if above else "top",
            fontsize=fontsize, color=color, fontfamily="serif",
            fontstyle="italic", rotation=45, zorder=5)


# ── Species Plate Helpers ───────────────────────────────────────────

def rock_face_background(ax, x_start, x_end, y_start, y_end,
                          color="#B8A888", seed=42):
    """Draw a rock face texture for petroglyph-style plates."""
    rng = np.random.default_rng(seed)
    ax.add_patch(FancyBboxPatch(
        (x_start, y_start), x_end - x_start, y_end - y_start,
        boxstyle="round,pad=0.5",
        facecolor=color, edgecolor=INK_FAINT,
        linewidth=1.0, alpha=0.4, zorder=1))
    # Grain lines
    for _ in range(15):
        gx = rng.uniform(x_start + 2, x_end - 2)
        gy = rng.uniform(y_start + 2, y_end - 2)
        gl = rng.uniform(3, 10)
        angle = rng.uniform(-0.2, 0.2)
        ax.plot([gx, gx + gl * math.cos(angle)],
                [gy, gy + gl * math.sin(angle)],
                color=INK_FAINT, linewidth=0.3, alpha=0.3, zorder=1)


def annotation_plate(ax, x, y, lines, fontsize=8, color=INK_LIGHT):
    """Place multi-line annotation text at (x, y)."""
    for i, line in enumerate(lines):
        ax.text(x, y - i * 3.5, line, fontsize=fontsize, color=color,
                fontfamily="serif", fontstyle="italic", zorder=5)


def draw_ibex_silhouette(ax, cx, cy, scale=1.0, color="#3A2A1A",
                          facing_left=True):
    """Draw a stylised ibex in petroglyph style — simple line art.

    This is deliberately crude: curved horn, blocky body, stick legs.
    Petroglyphs are not anatomically precise.
    """
    s = scale
    flip = -1 if facing_left else 1

    # Body (elongated oval)
    body = mpatches.Ellipse((cx, cy), 12 * s, 5 * s,
                             facecolor="none", edgecolor=color,
                             linewidth=1.5 * s, zorder=4)
    ax.add_patch(body)

    # Legs (four sticks)
    for dx in [-4, -2, 2, 4]:
        ax.plot([cx + dx * s * flip, cx + dx * s * flip],
                [cy - 2.5 * s, cy - 6 * s],
                color=color, linewidth=1.2 * s, zorder=4)

    # Neck + head
    neck_x = cx + 5.5 * s * flip
    ax.plot([neck_x, neck_x + 1.5 * s * flip],
            [cy + 1 * s, cy + 5 * s],
            color=color, linewidth=1.5 * s, zorder=4)
    head = plt.Circle((neck_x + 1.5 * s * flip, cy + 5.5 * s),
                       1.2 * s, facecolor="none", edgecolor=color,
                       linewidth=1.2 * s, zorder=4)
    ax.add_patch(head)

    # Horn (the defining feature — long curved scimitar)
    horn_base_x = neck_x + 1.5 * s * flip
    horn_base_y = cy + 6.5 * s
    ts = np.linspace(0, 1, 20)
    horn_x = horn_base_x - flip * 8 * s * ts ** 0.8
    horn_y = horn_base_y + 6 * s * ts - 2 * s * ts ** 2
    ax.plot(horn_x, horn_y, color=color, linewidth=2.0 * s, zorder=4)

    # Tail (short upward flick)
    tail_x = cx - 6 * s * flip
    ax.plot([tail_x, tail_x - 1.5 * s * flip],
            [cy + 1 * s, cy + 3 * s],
            color=color, linewidth=1.0 * s, zorder=4)


def draw_markhor_silhouette(ax, cx, cy, scale=1.0, color="#3A2A1A",
                             facing_left=True):
    """Draw a stylised markhor — distinguished by spiral horns."""
    s = scale
    flip = -1 if facing_left else 1

    # Body
    body = mpatches.Ellipse((cx, cy), 11 * s, 5 * s,
                             facecolor="none", edgecolor=color,
                             linewidth=1.5 * s, zorder=4)
    ax.add_patch(body)

    # Legs
    for dx in [-3.5, -1.5, 1.5, 3.5]:
        ax.plot([cx + dx * s * flip, cx + dx * s * flip],
                [cy - 2.5 * s, cy - 6 * s],
                color=color, linewidth=1.2 * s, zorder=4)

    # Neck + head
    neck_x = cx + 5 * s * flip
    ax.plot([neck_x, neck_x + 1 * s * flip],
            [cy + 1 * s, cy + 5 * s],
            color=color, linewidth=1.5 * s, zorder=4)
    head = plt.Circle((neck_x + 1 * s * flip, cy + 5.5 * s),
                       1.2 * s, facecolor="none", edgecolor=color,
                       linewidth=1.2 * s, zorder=4)
    ax.add_patch(head)

    # Spiral horns (corkscrew — the defining feature)
    horn_base_x = neck_x + 1 * s * flip
    horn_base_y = cy + 6.5 * s
    ts = np.linspace(0, 3 * math.pi, 40)
    horn_x = horn_base_x + flip * 1.5 * s * np.sin(ts) * (1 - ts / (3 * math.pi) * 0.3)
    horn_y = horn_base_y + ts / (3 * math.pi) * 10 * s
    ax.plot(horn_x, horn_y, color=color, linewidth=1.8 * s, zorder=4)

    # Beard
    ax.plot([neck_x + 1 * s * flip, neck_x + 0.5 * s * flip],
            [cy + 4.5 * s, cy + 2.5 * s],
            color=color, linewidth=1.0 * s, zorder=4)


def draw_snow_leopard_silhouette(ax, cx, cy, scale=1.0, color="#3A2A1A",
                                  facing_left=True):
    """Draw a stylised snow leopard — long tail, low body.
    Rendered as outline only (negative) since the leopard is absent
    from the petroglyphs."""
    s = scale
    flip = -1 if facing_left else 1

    # Body (lower, longer than goats)
    body = mpatches.Ellipse((cx, cy), 14 * s, 4 * s,
                             facecolor="none", edgecolor=color,
                             linewidth=1.2 * s, linestyle="--",
                             zorder=4)
    ax.add_patch(body)

    # Legs (shorter, crouched)
    for dx in [-5, -2, 2, 5]:
        ax.plot([cx + dx * s * flip, cx + dx * s * flip],
                [cy - 2 * s, cy - 4.5 * s],
                color=color, linewidth=1.0 * s, linestyle="--", zorder=4)

    # Head (smaller, rounder)
    head_x = cx + 7 * s * flip
    head = plt.Circle((head_x, cy + 1 * s), 1.5 * s,
                       facecolor="none", edgecolor=color,
                       linewidth=1.0 * s, linestyle="--", zorder=4)
    ax.add_patch(head)

    # Long tail (the signature — as long as body)
    tail_base = cx - 7 * s * flip
    ts = np.linspace(0, 1, 20)
    tail_x = tail_base - flip * 12 * s * ts
    tail_y = cy + 2 * s * np.sin(ts * math.pi) + 1 * s * ts
    ax.plot(tail_x, tail_y, color=color, linewidth=1.2 * s,
            linestyle="--", zorder=4)


def draw_lammergeier_silhouette(ax, cx, cy, scale=1.0, color="#3A2A1A"):
    """Draw a bearded vulture in flight — petroglyph style, wings spread."""
    s = scale

    # Wings (broad V-shape, slightly angled)
    wing_span = 18 * s
    ts = np.linspace(-1, 1, 40)
    # Wing shape: broad, slightly swept back
    wing_x = cx + wing_span * ts
    wing_y = cy + 2 * s * np.abs(ts) ** 0.8 - 1 * s * ts ** 2
    ax.plot(wing_x, wing_y, color=color, linewidth=2.0 * s, zorder=4)

    # Body (diamond shape)
    body_pts = np.array([
        [cx, cy + 2 * s],      # head
        [cx + 1.5 * s, cy],    # right
        [cx, cy - 6 * s],      # tail
        [cx - 1.5 * s, cy],    # left
        [cx, cy + 2 * s],      # close
    ])
    ax.plot(body_pts[:, 0], body_pts[:, 1], color=color,
            linewidth=1.5 * s, zorder=4)

    # Tail (wedge-shaped, longer than most raptors)
    tail_pts = np.array([
        [cx - 1 * s, cy - 4 * s],
        [cx, cy - 8 * s],
        [cx + 1 * s, cy - 4 * s],
    ])
    ax.plot(tail_pts[:, 0], tail_pts[:, 1], color=color,
            linewidth=1.2 * s, zorder=4)

    # Beard (the diagnostic feature)
    ax.plot([cx, cx - 0.5 * s], [cy + 2 * s, cy + 3.5 * s],
            color=color, linewidth=1.0 * s, zorder=4)
    ax.plot([cx, cx + 0.5 * s], [cy + 2 * s, cy + 3.5 * s],
            color=color, linewidth=1.0 * s, zorder=4)
