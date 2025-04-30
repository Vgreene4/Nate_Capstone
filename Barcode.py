import numpy as np
from ripser import ripser
from persim import plot_diagrams
from sklearn import datasets
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=67)

def sampleCirc(center: tuple, rad: float, var: float, count:int) -> list:
    """circulally sample points with noise

    Args:
        center (tuple): x,y coordinat of the center of the circle
        rad (float): radius
        var (float): standard deviation 
        count (int): number of points

    Returns:
        list: list of points, each as an array
    """
    t_sampled = 2*np.pi*rng.random(count)
    x_sampled = rad * np.cos(t_sampled) + rng.normal(scale=var, size=count) + center[0]
    y_sampled = rad * np.sin(t_sampled) + rng.normal(scale=var, size=count) + center[1]

    points_array = np.column_stack((x_sampled, y_sampled))
    points = [points_array[p] for p in range(count)]

    return points

def exampleData():
    return sampleCirc((2, 0), 1.25, .2, 25) + sampleCirc((-2,0), 2.5, .2, 25)

points = exampleData()
#print(points[0][0])
#print(points[1][0])


def check_points(points):
    x_points = [point[0] for point in points]
    print(x_points)
    y_points = [point[1] for point in points]

    plt.scatter(x_points, y_points)
    plt.show()

check_points(points)

dgms = ripser(np.array(points), coeff = 2)['dgms']

H_0 = dgms[0]
H_1 = dgms[1]

def plot_barcode(barcodes, dim):
    for i, bar in enumerate(barcodes):
        y = [i] #where the bar will be drawn

        left = bar[0] #where the bar is born
        width = [bar[1] - bar[0]] #width of the bar

        plt.barh(y, width, left = left, height = .5, color = "black")

    plt.title("Persistence Barcodes" + " " + dim)
    plt.xlim(0)
    plt.xlabel("Filtration")
    plt.ylabel("Features")
    plt.yticks([])
    plt.tight_layout()
    plt.show()

plot_barcode(H_1, "in H_1")