import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LogNorm
from scipy.interpolate import griddata

file_path = 'D:/SLU/excel Files/For Python.csv'
df = pd.read_csv(file_path)

name = np.array(df.iloc[:, 0])  
x = np.array(df.iloc[:, 4])     
y = np.array(df.iloc[:, 5])     
root = np.array(df.iloc[:, 1])  
stem = np.array(df.iloc[:, 2])  
soil = np.array(df.iloc[:, 3])  
xr1 = np.array(df.iloc[:, 6])   
yr1 = np.array(df.iloc[:, 7])   
xr21 = np.array(df.iloc[:, 8])  
yr21 = np.array(df.iloc[:, 9])  
xr22 = np.array(df.iloc[:, 10]) 
yr22 = np.array(df.iloc[:, 11]) 
xr3 = np.array(df.iloc[:, 12])  
yr3 = np.array(df.iloc[:, 13])  
xr4 = np.array(df.iloc[:, 14])  
yr4 = np.array(df.iloc[:, 15])

tree_x = [1.46, 2.02, 1.89]
tree_y = [1.23, 1.24, 1.59]

def circumcircle(x1, y1, x2, y2, x3, y3):
    A = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2
    B = (x1**2 + y1**2) * (y3 - y2) + (x2**2 + y2**2) * (y1 - y3) + (x3**2 + y3**2) * (y2 - y1)
    C = (x1**2 + y1**2) * (x2 - x3) + (x2**2 + y2**2) * (x3 - x1) + (x3**2 + y3**2) * (x1 - x2)

    # Circumcenter
    cx = -B / (2 * A)
    cy = -C / (2 * A)

    # Radius
    radius = np.sqrt((cx - x1) ** 2 + (cy - y1) ** 2)
    
    return cx, cy, radius

cx, cy, radius = circumcircle(tree_x[0], tree_y[0], tree_x[1], tree_y[1], tree_x[2], tree_y[2])

resistivity_data = [
    (root, 'Resistance (Ω)', '#1-Electrode in Root'),
    (stem, 'Resistance (Ω)', '#1-Electrode in Stem'),
    (soil, 'Resistance (Ω)', '#1-Electrode in Soil')
]

extra_points_x = [1.27, 1.48, 1.21]
extra_points_y = [1.47, 1.405, 1.56]

vmin_value = 1e1
vmax_value = 1e2 

fig, axs = plt.subplots(1, 3, figsize=(35, 10))

for i, (resistivity_values, label, title) in enumerate(resistivity_data):
    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    X, Y = np.meshgrid(xi, yi)
    
    Z = griddata((x, y), resistivity_values, (X, Y), method='nearest')

    ax = axs[i]
    
    heatmap = ax.imshow(Z, extent=(min(x), max(x), min(y), max(y)), origin='lower',
                        aspect='auto', cmap='plasma', norm=LogNorm(vmin=vmin_value, vmax=vmax_value))
    

    cbar = fig.colorbar(heatmap, ax=ax, orientation='horizontal', pad=0.15)
    cbar.set_label(label, size=15)  
    cbar.ax.tick_params(labelsize=15)
    
    ax.set_xlabel('X values (m)', size=20)
    ax.set_ylabel('Y values (m)', size=20)
    ax.set_title(title, size=20)

    ax.tick_params(axis='x', labelsize=15)  
    ax.tick_params(axis='y', labelsize=15)
    
 
    ax.plot(xr1, yr1, color='black', marker='o', markersize=10, markerfacecolor='none')
    ax.plot(xr21, yr21, color='black', marker='o', markersize=10, markerfacecolor='none')
    ax.plot(xr22, yr22, color='black', marker='o', markersize=10, markerfacecolor='none')
    ax.plot(xr3, yr3, color='black', marker='o', markersize=10, markerfacecolor='none')
    ax.plot(xr4, yr4, color='black', marker='o', markersize=10, markerfacecolor='none')

    ax.scatter(x, y, color='black', marker='o', s=50)
    

    ax.scatter(extra_points_x[i], extra_points_y[i], color='blue', marker='x', s=300, label='Extra Electrode')
    ax.text(extra_points_x[i], extra_points_y[i], f'#1-{i+1}', fontsize=15, color='blue')
    
    circle = plt.Circle((cx, cy), radius, color='red', fill=False, linestyle='--', linewidth=2)
    ax.add_artist(circle)

    ax.plot(tree_x, tree_y, 'ro', markersize=10, label='Tree Geometry')
    ax.grid(False)

axs[-1].legend(['Root 1', 'Root 2', 'Root 3', 'Root 4', 'Electrodes Position', 'Tree Geometry', 'Extra Electrode'], 
               loc='lower left', bbox_to_anchor=(1.05, 0.5), fontsize=15)


plt.tight_layout()
plt.show()

