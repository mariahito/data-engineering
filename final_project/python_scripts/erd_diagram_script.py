import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

def draw_table(ax, x, y, w, h, title, fields):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", edgecolor='black', facecolor='lightgrey')
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h - 5, title, ha='center', va='top', fontsize=10, weight='bold')
    for i, field in enumerate(fields):
        ax.text(x + 3, y + h - 15 - i * 7, field, ha='left', va='top', fontsize=8)

draw_table(ax, 10, 70, 30, 30, "states", ["state_id (PK)", "state_name", "fips_code"])
draw_table(ax, 60, 70, 30, 20, "time", ["time_id (PK)", "month_year"])
draw_table(ax, 10, 30, 40, 30, "weather", ["weather_id (PK)", "state_id (FK)", "time_id (FK)", "temp_max", "temp", "temp_min", "feels_like", "humidity", "precipitation", "precipitation_type", "conditions"])
draw_table(ax, 60, 30, 40, 40, "employment", ["employment_id (PK)", "state_id (FK)", "time_id (FK)", "civilian_population", "labor_force", "population_percent", "employment", "employment_percent", "unemployment", "unemployment_percent", "employment_to_population_ratio", "unemployment_rate"])

ax.annotate("", xy=(25, 70), xytext=(30, 60), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(75, 70), xytext=(70, 60), arrowprops=dict(arrowstyle="->"))

ax.annotate("", xy=(25, 30), xytext=(30, 25), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(75, 30), xytext=(70, 25), arrowprops=dict(arrowstyle="->"))

plt.savefig("erd_diagram.pdf", bbox_inches='tight')
print("ERD diagram saved as erd_diagram.pdf")
