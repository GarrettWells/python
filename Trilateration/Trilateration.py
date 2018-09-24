from abc import ABC
import time

import math

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rand
from shapely.geometry.point import Point


class Trilateration(ABC):
    """ABC for the Trilateration algorithms"""
    MAX_X = 1200  # set the size of the canvas
    MAX_Y = 800
    error_in_distance = math.sqrt(MAX_X ** 2 + MAX_Y ** 2) / 32  # maximum error due to noise in distance readings

    def __init__(self):
        self.fixed_points = np.array(((0, 0), (0, self.MAX_Y), (self.MAX_X, self.MAX_Y / 2)))  # create a 3x2 matrix of fixed positions
        self.position = (rand.randint(0, self.MAX_X), rand.randint(0, self.MAX_Y))  # generate the actual (x,y) position
        self.distances = rand.normal(0, self.error_in_distance, len(self.fixed_points))  # generate some random noise
        for i in range(len(self.fixed_points)):
            self.distances[i] += self.distance(self.fixed_points[i], self.position)  # add the actual distance to the noise

    @staticmethod
    def display_graph(plot_of_distances):
        """display the estimated distance visually using matplotlib"""
        # # matplotlib stuff
        # if isinstance(plot_of_distances, LinearRing):
        #     plot_of_distances = list(plot_of_distances.coords)  # get a list of (x, y) tuples
        #     x, y = zip(*plot_of_distances)
        #     plt.plot(x, y)
        #     plt.show
        # else:
        fig, ax = plt.subplots()
        cmap = plt.cm.get_cmap("viridis")
        im = ax.imshow(plot_of_distances, cmap=cmap)
        ax.set_xticks(np.arange(0, len(plot_of_distances[0]), len(plot_of_distances[0]) / 10))
        ax.set_yticks(np.arange(0, len(plot_of_distances), len(plot_of_distances) / 10))
        plt.xlabel('x')
        plt.ylabel('y')
        fig.tight_layout()
        plt.show()

    @staticmethod
    def start_time():
        """start a timer"""
        return time.time()

    @staticmethod
    def end_time(start_time):
        """end the timer"""
        print("\n--- %s seconds ---" % (time.time() - start_time))

    def print_coords(self):
        """print the real (x, y) coordinates"""
        print('\nreal x:%s\treal y:%s' % (self.position[0], self.position[1]))

    @staticmethod
    def distance(coord1, coord2):
        """calculated the distance between two (x, y) coordinates"""
        x1, y1 = coord1
        x2, y2 = coord2
        return math.hypot(x2 - x1, y2 - y1)  # returns the distance from (0, 0) to (x2 - x1, y2 - y1)

    def get_error_in_distance(self, coord):
        """
        used as a value function that converts an (x, y) position to a single float value


        First computes the distance from (i, j) and one of the fixed points, let this number be 'x'
        Then computes the difference between 'x', and the actual distance read by the rover and squares this difference
        Repeat the previous two steps for the other fixed points and sum the squares
        Take the square root
        Finally invert
        """
        i, j = coord
        temp = 0
        for k in range(len(self.fixed_points)):
            temp += (self.distance((i, j), self.fixed_points[k]) - self.distances[k]) ** 2
        try:
            return 1 / math.sqrt(temp)
        except ZeroDivisionError:  # if there was no error in the measurements
            return np.inf

    def calculate_buffer(self):
        """calculate the margin of error used for the circles centered at the fixed points"""
        error = 0
        for _ in range(len(self.fixed_points)):
            error += (1.5*(self.error_in_distance+1))**2
        return int(math.sqrt(error))


class TrilaterationNaive(Trilateration):
    """Naive approach which calculates the distance for every point on the screen"""
    def __init__(self):
        super().__init__()
        start = self.start_time()
        plot_of_distances = np.zeros((self.MAX_Y, self.MAX_X))
        for i in range(self.MAX_X):
            for j in range(self.MAX_Y):
                plot_of_distances[j, i] = self.get_error_in_distance((i, j))
        self.end_time(start)
        self.print_coords()
        self.display_graph(plot_of_distances)


class TrilaterationBetter(Trilateration):
    """
    Better than the naive approach.

    This approach looks at the reported distance away from each point, adds a buffer to these distances,
    finds the overlap of the circles centered at each fixed point with a radius of (reported distance + buffer),
    draws a rectangle around the circle, then calculates the value function for each point in that rectangle.
    """
    def __init__(self):
        super().__init__()
        start = self.start_time()
        plot_of_distances = np.zeros((self.MAX_Y, self.MAX_X))
        buffer = self.calculate_buffer()
        circles = []
        for k in range(len(self.fixed_points)):
            circles.append(Point(self.fixed_points[k][0], self.fixed_points[k][1]).buffer(self.distances[k] + buffer))
        overlap = circles[0]
        for i in range(1, len(circles)):
            overlap = overlap.intersection(circles[i])
        bounds = list(overlap.bounds)
        for x in range(int(bounds[0]), int(bounds[2])):
            if 0 <= x < self.MAX_X:
                for y in range(int(bounds[1]), int(bounds[3])):
                    if 0 <= y < self.MAX_Y:
                        temp = self.get_error_in_distance((x, y))
                        plot_of_distances[y, x] = temp
        self.end_time(start)
        self.print_coords()
        self.display_graph(plot_of_distances)


class TrilaterationBest(Trilateration):
    """
    This is the Fastest approach

    This approach looks at the reported distance away from each point, adds a buffer to these distances,
    finds the overlap of the circles centered at each fixed point with a radius of (reported distance + buffer),
    finds the geometric centroid of the overlap of the circles then draws a square around the geometric centroid with
    a side length of the buffer that was used before, then calculates the value function for each point in that square.
    """
    def __init__(self):
        super().__init__()
        start = self.start_time()
        plot_of_distances = np.zeros((self.MAX_Y, self.MAX_X))
        buffer = self.calculate_buffer()
        circles = []
        for k in range(len(self.fixed_points)):
            circles.append(Point(self.fixed_points[k][0], self.fixed_points[k][1]).buffer(self.distances[k] + buffer))
        overlap = circles[0]
        for i in range(1, len(circles)):
            overlap = overlap.intersection(circles[i])
        center = overlap.centroid
        center_x, center_y = int(center.x), int(center.y)
        # for theta in np.linspace(0, 360, 360, endpoint=False):  # check in a circle pattern
        #     for r in range(buffer):
        #         x = int(r*math.cos(theta))+center_x  # polar coordinates to cartesian coordinates
        #         y = int(r*math.sin(theta))+center_y
        #         if 0 <= x < self.MAX_X and 0 <= y < self.MAX_Y:
        #             plot_of_distances[y, x] = self.get_error_in_distance((x, y))
        for x in range(center_x-buffer, center_x+buffer):
            if 0 <= x < self.MAX_X:
                for y in range(center_y-buffer, center_y+buffer):
                    if 0 <= y < self.MAX_Y:
                        plot_of_distances[y, x] = self.get_error_in_distance((x, y))
        self.end_time(start)
        self.print_coords()
        self.display_graph(plot_of_distances)



if __name__ == "__main__":
    input = input('enter 1 for the slower algorithm or 2 for the faster algorithm or 3 for the fastest algorithm\n')
    if input == '1':
        TrilaterationNaive()
    elif input == '2':
        TrilaterationBetter()
    elif input == '3':
        TrilaterationBest()
    else:
        raise Exception('unknown command')
