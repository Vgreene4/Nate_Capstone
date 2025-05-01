import numpy as np

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

    points_array = np.column_stack((x_sampled, y_sampled, np.zeros(count)))
    points = [points_array[p] for p in range(count)]

    return points

def exampleData():
    return sampleCirc((2, 0), 1.25, .2, 25) + sampleCirc((-2,0), 2.5, .2, 25)




if __name__ == "__main__":
    print(exampleData())