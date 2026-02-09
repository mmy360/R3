import matplotlib.pyplot as plt
import numpy as np

# ===========================================================
# Matplotlib global settings
# ===========================================================
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ===========================================================
# Data
# ===========================================================
batch_sizes = [100, 200]

# Total Step Time (seconds)
step_100 = [197.6238, 237.2]    # R3 fast, R3 official
step_200 = [272.15, 346.46]     # R3 fast, R3 official

# ===========================================================
# Figure
# ===========================================================
fig, ax = plt.subplots(figsize=(10, 7))

# --- softer academic colors ---
color_fast = '#4C72B0'      # muted blue
color_official = '#DD8452'  # muted orange

x = np.arange(len(batch_sizes))
width = 0.10  # <- 柱子更窄

# Bars
bars_fast = ax.bar(
    x - width / 2,
    [step_100[0], step_200[0]],
    width,
    label='R3 fast (Ours)',
    color=color_fast,
    edgecolor='black',
    linewidth=1.2
)

bars_official = ax.bar(
    x + width / 2,
    [step_100[1], step_200[1]],
    width,
    label='R3 official',
    color=color_official,
    edgecolor='black',
    linewidth=1.2
)

# ===========================================================
# Labels & layout
# ===========================================================
ax.set_xlabel('Batch Size', fontsize=16, fontweight='bold')
ax.set_ylabel('Total Step Time (s)', fontsize=16, fontweight='bold')
ax.set_title('Total Step Time Comparison', fontsize=18, fontweight='bold', pad=18)

ax.set_xticks(x)
ax.set_xticklabels(batch_sizes, fontsize=12)

ax.legend(fontsize=13, loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.3)

# Lower is better annotation -> 左上角但稍往下避开 legend
ax.text(
    0.35, 0.85,
    'Lower is better ↓',
    transform=ax.transAxes,
    ha='left',
    va='top',
    fontsize=16,
    fontweight='bold',
    color='dimgray'
)

# ===========================================================
# Bar value labels
# ===========================================================
for bars in [bars_fast, bars_official]:
    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h,
            f'{h:.1f}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

# ===========================================================
# Helper: add gap annotation (long dashed line to official bar)
# ===========================================================
def add_gap_annotation(ax, x_center, y_low, y_high, text):
    arrow_offset = 0.22          # arrow整体左移
    x_arrow = x_center - arrow_offset

    # right edge of official bar (for connection)
    x_right_bar = x_center + width / 2

    # dashed horizontal caps (connect to official bar)
    ax.plot(
        [x_arrow, x_right_bar],
        [y_low, y_low],
        linestyle='--',
        color='black',
        linewidth=1.2
    )
    ax.plot(
        [x_arrow, x_right_bar],
        [y_high, y_high],
        linestyle='--',
        color='black',
        linewidth=1.2
    )

    # vertical double arrow
    ax.annotate(
        '',
        xy=(x_arrow, y_high),
        xytext=(x_arrow, y_low),
        arrowprops=dict(arrowstyle='<->', linewidth=1.4)
    )

    # text
    ax.text(
        x_arrow + 0.20,
        y_high,
        text,
        ha='right',
        va='center',
        fontsize=13,
        fontweight='bold',
        bbox=dict(facecolor='white', edgecolor='none', pad=1.0)
    )

# ===========================================================
# Add comparisons
# ===========================================================
# Batch 100
gap_100 = step_100[1] - step_100[0]
improvement_100 = gap_100 / step_100[1] * 100
add_gap_annotation(
    ax,
    x_center=0,
    y_low=step_100[0],
    y_high=step_100[1],
    text=f'Δ {gap_100:.1f}s\n↓ {improvement_100:.1f}%'
)

# Batch 200
gap_200 = step_200[1] - step_200[0]
improvement_200 = gap_200 / step_200[1] * 100
add_gap_annotation(
    ax,
    x_center=1,
    y_low=step_200[0],
    y_high=step_200[1],
    text=f'Δ {gap_200:.1f}s\n↓ {improvement_200:.1f}%'
)

# ===========================================================
# Save & show
# ===========================================================
plt.tight_layout()
plt.savefig('r3_step_time_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# ===========================================================
# Console analysis
# ===========================================================
print("=" * 60)
print("R3 Total Step Time Analysis")
print("=" * 60)

print("\nBatch Size 100:")
print(f"  R3 fast:     {step_100[0]:.2f}s")
print(f"  R3 official: {step_100[1]:.2f}s")
print(f"  Gap:         {gap_100:.2f}s")
print(f"  Improvement: {improvement_100:.1f}%")

print("\nBatch Size 200:")
print(f"  R3 fast:     {step_200[0]:.2f}s")
print(f"  R3 official: {step_200[1]:.2f}s")
print(f"  Gap:         {gap_200:.2f}s")
print(f"  Improvement: {improvement_200:.1f}%")

fast_growth = (step_200[0] / step_100[0] - 1) * 100
official_growth = (step_200[1] / step_100[1] - 1) * 100

print("\nScalability (BS100 → BS200):")
print(f"  R3 fast:     +{fast_growth:.1f}%")
print(f"  R3 official: +{official_growth:.1f}%")
print("  → R3 fast scales better")
print("=" * 60)
