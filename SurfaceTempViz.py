# Ryan Murray
# CS519 - Scientific Visualization
# Final Project

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#from matplotlib import pylab
#from matplotlib.widgets import CheckButtons
import mpld3
from mpld3 import plugins
from pylab import *

css = """
svg
{
    text-align:center;
    margin-left:auto; margin-right:auto; display:block;
}

.mpld3-tooltip
{
    font-family:Arial, Helvetica, sans-serif;
    border: 1px solid black;
    color: #000000;
    background-color: #ffffff;
}

.mpld3-text
{
    font-family:Arial, Helvetica, sans-serif;
    font-size: 15px;
    color: #000000;
    background-color: #ffffff;
}
"""
# ------------------------------------------------------------------------------------------------------------------
# Raw Data Parser - Using Python, import the raw data, parse it, and store in variables and/or data structures (20%)
# ------------------------------------------------------------------------------------------------------------------
raw_data = pd.read_csv('GlobalTemperatures.csv', delimiter=",", header=0, usecols=[0, 1, 2])
avg_temp_data = pd.DataFrame(columns=('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), dtype=float)

months = [["-01-", 'Jan', 'red'],
          ["-02-", 'Feb', 'green'],
          ["-03-", 'Mar', 'blue'],
          ["-04-", 'Apr', 'orange'],
          ["-05-", 'May', 'magenta'],
          ["-06-", 'Jun', 'darkseagreen'],
          ["-07-", 'Jul', 'pink'],
          ["-08-", 'Aug', 'deepskyblue'],
          ["-09-", 'Sep', 'peru'],
          ["-10-", 'Oct', 'navy'],
          ["-11-", 'Nov', 'gold'],
          ["-12-", 'Dec', 'indigo']]

min_temp = 100
max_temp = -100

# Transpose the data for each entry into month columns
for i in range(raw_data.shape[0]):
    year = int(raw_data.iloc[i, 0][0:4])
    if year >= 1753:
        avg_temp_data.append(pd.Series(name=year, dtype=float))
        for month in months:
            if month[0] in raw_data.iloc[i, 0]:
                currTemp = raw_data.iloc[i, 1].astype(float)
                avg_temp_data.loc[year, month[1]] = currTemp
                if currTemp > max_temp:
                    max_temp = currTemp
                if currTemp < min_temp:
                    min_temp = currTemp

# Calculate the total number of years, and max/min temperature values to plot
num_years = len(avg_temp_data.index)
max_temp = math.ceil(max_temp)
min_temp = math.floor(min_temp)

# Set the properties for the animated plot
fig_ani, ax_ani = plt.subplots(figsize=(12, 7))
plt.title('Average Temperature')
plt.xlabel('Year')
plt.xlim(1753, 2015)
plt.xticks(np.arange(1753, 2015, step=10), rotation=45, ha="right", rotation_mode="anchor")
plt.ylabel('Temperature (°C)')
plt.ylim(min_temp, max_temp)
plt.yticks(np.arange(min_temp, max_temp, step=2))
ax_ani.yaxis.grid(color='lightgrey')

# -------------------------------------------------------------
# Plot the Data - Generate a chart using Python libraries (35%)
# -------------------------------------------------------------
lines_ani = [None] * 12
trend_lines_ani = [None] * 12
for j in range(12):
    trend_lines_ani[j], = ax_ani.plot(avg_temp_data.index[:0], avg_temp_data.iloc[:0, j],
                                      visible=True, lw=2, color=months[j][2], label=months[j][1], alpha=1)
    lines_ani[j], = ax_ani.plot(avg_temp_data.index[:0], avg_temp_data.iloc[:0, j],
                                visible=True, lw=2, color=months[j][2], label=months[j][1], alpha=0.25)

# Define the legend
handles, labels = ax_ani.get_legend_handles_labels()
labels = labels[::2]
handles = handles[::2]
ax_ani.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()

# Function to perform the animation on the animation plot
def animate(i):
    for j in range(len(lines_ani)):
        lines_ani[j].set_data(avg_temp_data.index[:i], avg_temp_data.iloc[:i, j])
        if i > 20:
            z = np.polyfit(avg_temp_data.index[:i].values, avg_temp_data.iloc[:i, j].values, 4)
            p = np.poly1d(z)
            trend_lines_ani[j].set_data(avg_temp_data.index[:i], p(avg_temp_data.index[:i]))

# --------------------------------------------------------
# Animate - Add animation to the chart with controls (15%)
# --------------------------------------------------------
animator = animation.FuncAnimation(fig_ani, animate, frames=num_years, interval=20, repeat=False, fargs=None)

# Save the animation as an MP4 video file
writer = animation.FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
animator.save("SurfaceTempViz.mp4", writer=writer)

# Set the properties for the interactive plot
fig_int, ax_int = plt.subplots(figsize=(12, 7))
plt.title('Average Temperature')
plt.xlabel('Year')
plt.xlim(1753, 2015)
plt.xticks(np.arange(1753, 2015, step=10), rotation=45, ha="right", rotation_mode="anchor")
plt.ylabel('Temperature (°C)')
plt.ylim(min_temp, max_temp)
plt.yticks(np.arange(min_temp, max_temp, step=2))
ax_int.yaxis.grid(color='lightgrey')
plt.tight_layout()
plt.subplots_adjust(left=0.1, right=0.9)

# -------------------------------------------------------------
# Plot the Data - Generate a chart using Python libraries (35%)
# -------------------------------------------------------------
lines_int = [None] * 12
trend_lines_int = [None] * 12
lines_tooltip = [None] * 12
trend_lines_tooltip = [None] * 12
for j in range(12):
    z = np.polyfit(avg_temp_data.index[:num_years].values, avg_temp_data.iloc[:num_years, j].values, 4)
    p = np.poly1d(z)
    lines_int[j], = ax_int.plot(avg_temp_data.index[:num_years], avg_temp_data.iloc[:num_years, j],
                                visible=True, lw=2, color=months[j][2], label=months[j][1], alpha=0.2, marker='.')
    trend_lines_int[j], = ax_int.plot(avg_temp_data.index[:num_years], p(avg_temp_data.index[:num_years]),
                                      visible=True, lw=4, color=months[j][2], label=months[j][1], alpha=0.5, marker='.')
    y_vals = avg_temp_data.iloc[:num_years, j].to_numpy()
    x_vals = avg_temp_data.index[:num_years].to_numpy()
    trend_vals = p(avg_temp_data.index[:num_years])
    tooltip_label = [None] * len(y_vals)
    trend_tooltip_label = [None] * len(trend_vals)
    for i in range(len(tooltip_label)):
        tooltip_label[i] = months[j][1] + " " + x_vals[i].astype(str) + ": " + ("{:.2f}".format(y_vals[i])) + " °C"
        trend_tooltip_label[i] = "Trend: " + months[j][1] + " " + x_vals[i].astype(str) + ": " + ("{:.2f}".format(trend_vals[i])) + " °C"

    lines_tooltip[j] = plugins.PointHTMLTooltip(lines_int[j], labels=tooltip_label, voffset=10, hoffset=10, css=css)
    trend_lines_tooltip[j] = plugins.PointHTMLTooltip(trend_lines_int[j], labels=trend_tooltip_label, voffset=10, hoffset=10, css=css)

# ----------------------------------------------------------------------------------
# Interactive Features - Add interactive features to the chart (e.g., filters) (15%)
# ----------------------------------------------------------------------------------
# Create the interactive legend
line_collections = [None] * 12
for i in range(12):
    line_collections[i] = [lines_int[i], trend_lines_int[i]]
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
interactive_legend = plugins.InteractiveLegendPlugin(line_collections, labels, alpha_unsel=0, alpha_over=1.5, start_visible=True)
plugins.connect(fig_int, interactive_legend)

plugins.connect(fig_int,
                lines_tooltip[0],
                lines_tooltip[1],
                lines_tooltip[2],
                lines_tooltip[3],
                lines_tooltip[4],
                lines_tooltip[5],
                lines_tooltip[6],
                lines_tooltip[7],
                lines_tooltip[8],
                lines_tooltip[9],
                lines_tooltip[10],
                lines_tooltip[11],
                trend_lines_tooltip[0],
                trend_lines_tooltip[1],
                trend_lines_tooltip[2],
                trend_lines_tooltip[3],
                trend_lines_tooltip[4],
                trend_lines_tooltip[5],
                trend_lines_tooltip[6],
                trend_lines_tooltip[7],
                trend_lines_tooltip[8],
                trend_lines_tooltip[9],
                trend_lines_tooltip[10],
                trend_lines_tooltip[11])

# ----------------------------------------------------------------------------------------------------------
# Publish Online - Publish the resulting interactive charts to a website, adding some descriptive text (15%)
# ----------------------------------------------------------------------------------------------------------
# Generate the HTML page for the interactive plot
html_file = open("page2_figure_only.html", "w")
html_file.write(mpld3.fig_to_html(fig_int))
html_file.close()

#plt.show()