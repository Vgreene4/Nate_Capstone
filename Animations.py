from manim import *
import numpy as np
from itertools import combinations
from shapely.geometry import Point

rng = np.random.default_rng(seed=2)


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




class DrawPoints(Scene):
    def construct(self):
        points = sampleCirc((2, 0), 1.25, 0.2, 25) + sampleCirc((-2,0), 2.5, 0.5, 25)


        # --- Dots (0-simplices) ---
        dots = [Dot(p, color=BLUE) for p in points]
        self.add(*[dot for dot in dots])

class CechComplex(Scene):
    def construct(self):
        # --- Irregular, more spaced-out points ---
        # points = [
        #     np.array([-3.1, -1.8, 0]),
        #     np.array([1.2, 2.1, 0]),
        #     np.array([3.7, -2.3, 0]),
        #     np.array([-0.5, -3.2, 0]),
        #     np.array([-4.5, 2.5, 0]),
        #     np.array([-4.5, 2, 0])
        # ]

        points = sampleCirc((2, 0), 1.25, 0.2, 25) + sampleCirc((-2,0), 2.5, 0.5, 25)


       
        max_radius = 1.5
        radius_step = 0.05
        current_radius = 0.1

        # --- Dots (0-simplices) ---
        dots = [Dot(p, color=BLUE) for p in points]
        self.play(*[FadeIn(dot) for dot in dots])

        # --- Labels ---
        # labels = []
        # for i, p in enumerate(points):
        #     label = Text(chr(65 + i), font_size=24)
        #     label.next_to(p, UP, buff=0.2)
        #     labels.append(label)
        # self.play(*[Write(label) for label in labels])

        # --- Circles (balls) ---
        circles = [
            Circle(radius=current_radius)
            .move_to(p)
            .set_stroke(BLUE, opacity=0.3)
            for p in points
        ]
        self.play(*[Create(c) for c in circles])

        # --- Track drawn simplices ---
        created_edges = set()
        created_triangles = set()

        # --- Shapely geometry ---
        shapely_points = [Point(p[0], p[1]) for p in points]

        # --- Main loop ---
        while current_radius < max_radius:
            current_radius += radius_step

            # Grow circles visually
            self.play(*[
                c.animate.set(width=2 * current_radius)
                for c in circles
            ], run_time=0.1)

            # Update shapely circles
            shapely_circles = [p.buffer(current_radius) for p in shapely_points]

            new_simplices = []

            # --- 1-simplices (edges) ---
            for i, j in combinations(range(len(points)), 2):
                if (i, j) not in created_edges:
                    if shapely_circles[i].intersects(shapely_circles[j]):
                        edge = Line(points[i], points[j], color=ORANGE)
                        new_simplices.append(edge)
                        created_edges.add((i, j))
                        created_edges.add((j, i))

            # --- Detect new 1D hole (cycle of edges, no triangle yet) ---
            for i, j, k in combinations(range(len(points)), 3):
                edges_exist = all((a, b) in created_edges for a, b in [(i, j), (j, k), (k, i)])
                triangle_exists = (i, j, k) in created_triangles
                if edges_exist and not triangle_exists:
                    intersection = shapely_circles[i].intersection(shapely_circles[j]).intersection(shapely_circles[k])

            # --- 2-simplices (triangles) ---
            for i, j, k in combinations(range(len(points)), 3):
                if (i, j, k) not in created_triangles:
                    if (shapely_circles[i].intersects(shapely_circles[j]) and
                        shapely_circles[j].intersects(shapely_circles[k]) and
                        shapely_circles[k].intersects(shapely_circles[i])):

                        intersection = shapely_circles[i].intersection(shapely_circles[j]).intersection(shapely_circles[k])
                        if intersection.is_empty:
                            continue

                        pi, pj, pk = points[i], points[j], points[k]
                        triangle = Polygon(pi, pj, pk,
                                           fill_color=PURPLE,
                                           stroke_color=BLUE,
                                           fill_opacity=0.3,
                                           stroke_width=2)
                        new_simplices.append(triangle)

                        created_triangles.update({
                            (i, j, k), (i, k, j), (j, i, k),
                            (j, k, i), (k, i, j), (k, j, i)
                        })

            # Pause to show new simplex creation
            if new_simplices:
                self.wait(1/60)
                self.play(*[Create(s) for s in new_simplices], run_time=(1/60))
                # self.add(*[s for s in new_simplices])

        self.wait(1)



