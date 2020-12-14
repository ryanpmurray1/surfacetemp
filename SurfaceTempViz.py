# Ryan Murray
# CS519 - Scientific Visualization
# Final Project

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import pylab
from matplotlib.widgets import CheckButtons
import plotly.express as px
import math
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

.mpld3-xaxis text
{
    
}
"""

#rawData = np.genfromtxt('GlobalTemperatures.csv', delimiter=",", skip_header=0, dtype=None, encoding=None)
avgTempData = pd.read_csv('GlobalTemperatures.csv', delimiter=",", header=0, usecols=[0,1,2])

avgTempData2 = pd.DataFrame(columns=('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), dtype=float)
#avgTempData2.set_index('Year')
#j = 0

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

minTemp = 100
maxTemp = -100

# Transpose the data for each entry into month columns
for i in range(avgTempData.shape[0]):
    #print(avgTempData.iloc[i, 0])
    year = int(avgTempData.iloc[i, 0][0:4])
    #print(year)
    #if avgTempData.iloc[i,0] not in avgTempData2:
    if year >= 1753:
        avgTempData2.append(pd.Series(name=year, dtype=float))
        for month in months:
            if month[0] in avgTempData.iloc[i, 0]:
                currTemp = avgTempData.iloc[i, 1].astype(float)
                avgTempData2.loc[year, month[1]] = currTemp
                if currTemp > maxTemp:
                    maxTemp = currTemp
                if currTemp < minTemp:
                    minTemp = currTemp


print(avgTempData2)
numYears = len(avgTempData2.index)

print("Max temp:", maxTemp)
print("Min temp:", minTemp)
print("Num years:", numYears)

maxTemp = math.ceil(maxTemp)
minTemp = math.floor(minTemp)

# Set the properties for the animated plot
fig, ax = plt.subplots(figsize=(12, 7))
plt.title('Average Temperature')
plt.xlabel('Year')
plt.xlim(1753, 2015)
plt.xticks(np.arange(1753, 2015, step=10), rotation=45, ha="right", rotation_mode="anchor")
plt.ylabel('Temperature (°C)')
plt.ylim(minTemp, maxTemp)
plt.yticks(np.arange(minTemp, maxTemp, step=2))
ax.yaxis.grid(color='lightgrey')
plt.subplots_adjust(left=0.1, bottom=0.2, top=0.9)

# Define the lines and trend lines
i = 0
lines = [None] * 12
trendLines = [None] * 12
for j in range(12):
    trendLines[j], = ax.plot(avgTempData2.index[:i], avgTempData2.iloc[:i, j],
                             visible=True, lw=2, color=months[j][2], label=months[j][1], alpha=1)
    lines[j], = ax.plot(avgTempData2.index[:i], avgTempData2.iloc[:i, j],
                        visible=True, lw=2, color=months[j][2], label=months[j][1], alpha=0.25)

# Define the legend
handles, labels = ax.get_legend_handles_labels()
labels = labels[::2]
handles = handles[::2]
ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))

# Make checkbuttons with all plotted lines with correct visibility
#rax = plt.axes([0.05, 0.4, 0.1, 0.15])
#labels = [str(line.get_label()) for line in lines]
#visibility = [line.get_visible() for line in lines]
#check = CheckButtons(rax, labels, visibility)

#lines = [0, 0, 0]

# Function to define the interactive labels
#def func(label):
#    index = labels.index(label)
#    lines[index].set_visible(not lines[index].get_visible())
#    #plt.draw()

def animate(i):
    #print(i)
    #avgTempData2.plot()

    #data = avgTempData2.iloc[:int(i+1)] #select data range
    #print("data.index:", data.index)
    #print("data:", data)
    #print("data['Jan']:", data['Jan'])

    for j in range(len(lines)):
        lines[j].set_data(avgTempData2.index[:i], avgTempData2.iloc[:i, j])
        if i > 20:
            z = np.polyfit(avgTempData2.index[:i].values, avgTempData2.iloc[:i, j].values, 4)
            p = np.poly1d(z)
            trendLines[j].set_data(avgTempData2.index[:i], p(avgTempData2.index[:i]))
        #else:
        #    trendLines[j].set_data(avgTempData2.index[:i], avgTempData2.iloc[:i, j])

    #plt.subplots_adjust(left=0.2)

    #lines = [l0, l1, l2]

# Add checkable legend on left side
#rax = plt.axes([0.05, 0.4, 0.1, 0.15])
#labels = [str(line.get_label()) for line in lines]
#visibility = [line.get_visible() for line in lines]
#check = CheckButtons(rax, labels, visibility)
#check.on_clicked(func)


animator = animation.FuncAnimation(fig, animate, frames=numYears, interval=20, repeat=False, fargs=None)

# Save the animation as an HTML page (instead of an MP4)
#with open("myvideo.html", "w") as f:
#    print(animator.to_html5_video(), file=f)

# Save the animation as an MP4 video file
writer = animation.FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
animator.save("SurfaceTempViz.mp4", writer=writer)
#animator.to_jshtml()
#animator.to_html5_video()
#plt.show()

#ax.get_legend().remove()

# Set the properties for the interactive plot
fig2, ax2 = plt.subplots(figsize=(12, 7))
plt.title('Average Temperature')
plt.xlabel('Year')
plt.xlim(1753, 2015)
plt.xticks(np.arange(1753, 2015, step=10), rotation=45, ha="right", rotation_mode="anchor")
plt.ylabel('Temperature (°C)')
plt.ylim(minTemp, maxTemp)
plt.yticks(np.arange(minTemp, maxTemp, step=2))
ax2.yaxis.grid(color='lightgrey')
plt.subplots_adjust(left=0.1, bottom=0.2, top=0.9)


lines2 = [None] * 12
trendLines2 = [None] * 12
lines2ToolTip = [None] * 12
trendLines2ToolTip = [None] * 12
for j in range(12):
    z = np.polyfit(avgTempData2.index[:numYears - 1].values, avgTempData2.iloc[:numYears-1, j].values, 4)
    p = np.poly1d(z)
    lines2[j], = ax2.plot(avgTempData2.index[:numYears-1], avgTempData2.iloc[:numYears-1, j],
                        visible=True, lw=2, color=months[j][2], label=months[j][1], alpha=0.2, marker='.')
    trendLines2[j], = ax2.plot(avgTempData2.index[:numYears-1], p(avgTempData2.index[:numYears-1]),
                        visible=True, lw=4, color=months[j][2], label=months[j][1], alpha=0.5, marker='.')
    yvals = avgTempData2.iloc[:numYears-1, j].to_numpy()
    xvals = avgTempData2.index[:numYears-1].to_numpy()
    trendvals = p(avgTempData2.index[:numYears-1])
    toolTipLabel = [None] * len(yvals)
    trendToolTipLabel = [None] * len(trendvals)
    for i in range(len(toolTipLabel)):
        toolTipLabel[i] = months[j][1] + " " + xvals[i].astype(str) + ": " + ("{:.2f}".format(yvals[i])) + " °C"
        trendToolTipLabel[i] = "Trend: " + months[j][1] + " " + xvals[i].astype(str) + ": " + ("{:.2f}".format(trendvals[i])) + " °C"

    #print(toolTipLabel)
    #lines2ToolTip[j] = plugins.PointLabelTooltip(lines2[j], labels=yvals, voffset=0, hoffset=10, location='mouse')
    lines2ToolTip[j] = plugins.PointHTMLTooltip(lines2[j], labels=toolTipLabel, voffset=10, hoffset=10, css=css)
    trendLines2ToolTip[j] = plugins.PointHTMLTooltip(trendLines2[j], labels=trendToolTipLabel, voffset=10, hoffset=10, css=css)

# Create the interactive legend
#handles, labels = ax2.get_legend_handles_labels()
line_collections = [None] * 12
for i in range(12):
    line_collections[i] = [lines2[i], trendLines2[i]]
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
interactive_legend = plugins.InteractiveLegendPlugin(line_collections, labels, alpha_unsel=0, alpha_over=1.5, start_visible=True)
plugins.connect(fig2, interactive_legend)
#mpld3.show()

#labels = ['point {0}'.format(i + 1) for i in range(numYears)]
#tooltip = plugins.PointLabelTooltip(trendLines2[0], "Label1", voffset=0, hoffset=10, location='mouse')
#print(tooltip)
#plugins.connect(fig2, tooltip)
plugins.connect(fig2,
                lines2ToolTip[0],
                lines2ToolTip[1],
                lines2ToolTip[2],
                lines2ToolTip[3],
                lines2ToolTip[4],
                lines2ToolTip[5],
                lines2ToolTip[6],
                lines2ToolTip[7],
                lines2ToolTip[9],
                lines2ToolTip[9],
                lines2ToolTip[10],
                lines2ToolTip[11],
                trendLines2ToolTip[0],
                trendLines2ToolTip[1],
                trendLines2ToolTip[2],
                trendLines2ToolTip[3],
                trendLines2ToolTip[4],
                trendLines2ToolTip[5],
                trendLines2ToolTip[6],
                trendLines2ToolTip[7],
                trendLines2ToolTip[9],
                trendLines2ToolTip[9],
                trendLines2ToolTip[10],
                trendLines2ToolTip[11])

# Generate the HTML page for the interactive plot
html_file = open("page2.html", "w")
html_file.write(mpld3.fig_to_html(fig2))
html_file.close()

#plt.show()