import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import math

points = []
coords = [[], []]
bg_lines = []
dist = 5
rotation = int(input("rotation (in degrees): "))

def genCircle(n):
    step = 360/n
    for i in range(n):
        point = int(round((step / 2) + (step * i), 0))
        points.append(point)
        #print(point)

def genPoints():
    for i in range(len(points)):
        angle = math.radians(points[i] + 90 + rotation)
        point = [round(-1 * dist * math.cos(angle), 5), round(dist * math.sin(angle), 5)]
        #print(f'Point {points[i]:3d} at x = {point[0]}, {point[1]}')
        points[i] = point

def showCirc():
    fig, ax = plt.subplots()
    circ = Circle((0, 0), radius=dist+.5, edgecolor='black', facecolor='white')
    circ2 = Circle((0, 0), radius=dist+.25, edgecolor='black', facecolor='white')
    
    circ3 = Circle((points[1][0], points[1][1]), radius=.25, edgecolor='black', facecolor='white')
    
    ax.add_patch(circ)
    ax.add_patch(circ2)
    ax.add_patch(circ3)
    ax.set_aspect('equal')
    plt.grid(False)
    ax.set_axis_off()
    for start in points:
        for end in points:
            bg_lines.append([[start[0], end[0]], [start[1], end[1]]])
    for line in bg_lines:
        plt.plot(line[0], line[1], lw=.5, c=(0.5, 0.5, 0.5, 0.3))
    for point in points:
        coords[0].append(point[0])
        coords[1].append(point[1])
    x = np.array(coords[0])
    y = np.array(coords[1])
    plt.scatter(x, y)
    plt.show()


size = int(input("Number of points: ")) # change to higher than 9 for larger alphabet
genCircle(size)
genPoints()

showCirc()
