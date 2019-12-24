from random import randint

import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction import image
from sklearn.utils.graph_shortest_path import graph_shortest_path


from intcode import IntcodeComputer


class Crawler:
    def __init__(self, fname='input.txt'):
        self.ic = IntcodeComputer(fname, allow_pausing=True)

        self.history = {(0, 0): 1}
        self.dir_tried = {(0, 0): [0, 0, 0, 0]}  # N, E, S, W
        self.junction_path_dirs = {(0,0): []}
        self.output = -1
        self.itercount = 0
        self.direction = 'N'
        self.position = np.array([0, 0])
        self.pos_visited = {(0,0): False}
        self.dir_dict = {'N': 1,
                         'S': 2,
                         'W': 3,
                         'E': 4}
        self.backtrack_dict = {1:2, 2:1, 3:4, 4:3}  # keep track of the reverse direction
        self.rev_dir_dict = {1: 'N',
                             2: 'S',
                             3: 'W',
                             4: 'E'}
        self.try_dir_dict = {'N': 0,
                             'E': 1,
                             'S': 2,
                             'W': 3}
        self.rev_try_dir_dict = {0: 'N',
                                 1: 'E',
                                 2: 'S',
                                 3: 'W'}
        self.add_dict = {'N': np.array([0, 1]),
                         'S': np.array([0, -1]),
                         'W': np.array([-1, 0]),
                         'E': np.array([1, 0])}

        self.maze = np.zeros((201, 201)) - 1
        self.xmin = -100
        self.ymin = -100
        self.junctions_list = []
        self.prev_dir = -1

    def plot(self, next_pos, output):
        try:
            x, y = next_pos
            self.maze[x - self.xmin, y - self.ymin] = output
            plt.imshow(self.maze.T)
            plt.pause(.05)
        except KeyboardInterrupt:
            self.output = 2


    def run(self):
        while self.output is not 2:
            # print("iteration", self.itercount)  #DELME
            # Run next step
            # print('-'*20)  #DELME
            next_input = self.strategy()
            if self.itercount == 0:
                self.ic.resume(next_input)
            else:
                self.ic.resume(next_input)
            self.output = self.ic.output[-1]
            # print("new_output = ", self.output)  #DELME


            next_pos = self.position + self.add_dict[self.direction]
            # print("next_pos = ", next_pos)  #DELME
            self.history[tuple(next_pos)] = self.output
            self.update_dir_tried()

            if self.output == 1 or self.output == 2:
                self.position = next_pos
            # print("new position = ", self.position)  #DELME
            self.itercount += 1
            # self.plot(next_pos, self.output)  #DELME?
            if self.itercount % 1000 == 0:
                plot_maze(self.history)  #DELME
            if self.itercount == 200000:  #DELME
                self.output = 2   #DELME


    def update_dir_tried(self):
        reverse_direction = {0: 2,
                             1: 3,
                             2: 0,
                             3: 1}
        next_pos = self.position + self.add_dict[self.direction]
        dir_index = self.try_dir_dict[self.direction]
        self.dir_tried[tuple(self.position)][dir_index] = 1
        if self.output == 1 or self.output == 2:
            if tuple(next_pos) not in self.dir_tried:
                self.dir_tried[tuple(next_pos)] = [0, 0, 0, 0]
            reverse_index = reverse_direction[dir_index]
            self.dir_tried[tuple(next_pos)][reverse_index] = 1



    def strategy(self):
        tried_list = self.dir_tried[tuple(self.position)]
        try:
            next_dir = tried_list.index(0)
        except ValueError:
            next_dir = randint(0, 3)
        self.direction = self.rev_try_dir_dict[next_dir]
        next_input = self.dir_dict[self.direction]

        # print("Iteration:", self.itercount)  #DELME
        # print("Position:", self.position)  #DELME
        # print("tried_list = ", tried_list)  #DELME
        # print("next_input = {0} ({1})".format(next_input, self.direction))  #DELME
        # print("old_output = ", self.output)  #DELME
        return next_input

        # transition = {'N': 'E',
        #               'E': 'S',
        #               'S': 'W',
        #               'W': 'N'}
        # if self.output == 0:
        #   self.direction = transition[self.direction]
        # next_input = self.dir_dict[self.direction]
        # tried_list = self.dir_tried[tuple(self.position)]
        # if tried_list[next_input]:
        #   try:
        #       tried_list.index

        # return 

    def breadth_first_search(self):
        while (len(self.junctions_list)>0                           # all junctions need to be exhausted
               or not self.pos_visited[tuple(self.position)]            # all search directions need to be checked for each position
               or len(self.junction_path_dirs[tuple(self.position)])>0):    # if a position has a junction forward position, we take it and pop it out
            if not self.pos_visited[tuple(self.position)]:
                self.generate_junction_path_dirs()
            if len(self.junction_path_dirs[tuple(self.position)]) > 0:
                self.move_from_junction()
            else:
                self.backtrack_to_last_junction()

    def backtrack_to_last_junction(self):
        """Go back son"""
        # Pop out most recent junction
        backtrack_list = self.junctions_list.pop(-1)
        # print("backtrack_list = ", backtrack_list)  #DELME
        # input("================Pause at Backtracking=================")  #DELME
        # for i in range(len(self.junctions_list)):
        #   junction_list = self.junctions_list[i]
        #   new_junction_list = junction_list[:-len(backtrack_list)]
        #   self.junctions_list[i] = new_junction_list
        # Remove backtracking elements from other junctions lists
        for junction_list in self.junctions_list:
            del junction_list[-len(backtrack_list):]
        # Backtrack to last junction
        for move_dir in backtrack_list[::-1]:
            self.ic.resume(move_dir) 
            self.direction = self.rev_dir_dict[move_dir]
            self.position = self.position + self.add_dict[self.direction]

    def move_from_junction(self):
        self.itercount += 1  #DELME
        # print('-'*20)  #DELME
        # print("Iteration", self.itercount)  #DELME
        # Pick a direction from valid ones
        junction_path_dirs = self.junction_path_dirs[tuple(self.position)]
        selection_index = randint(0, len(junction_path_dirs)-1)
        next_move_dir = junction_path_dirs[selection_index]
        junction_path_dirs.pop(selection_index)
        # if there were other directions we could've gone, we need to backtrack to here
        cur_reverse_dir = self.backtrack_dict[next_move_dir]
        for junction_list in self.junctions_list:
            junction_list.append(cur_reverse_dir)
        if len(junction_path_dirs) > 0:
            self.junctions_list.append([cur_reverse_dir])
        # Move to valid direction
        self.ic.resume(next_move_dir)
        # Update stuff that we need to keep track of
        self.direction = self.rev_dir_dict[next_move_dir]  # letter direction
        # print("Old position = ", self.position)  #DELME
        # print("Direction = ", self.direction)  #DELME
        self.position = self.position + self.add_dict[self.direction]
        # print("New position = ", self.position)  #DELME
        self.pos_visited[tuple(self.position)] = False
        self.prev_dir = self.backtrack_dict[next_move_dir]

    def generate_junction_path_dirs(self):
        """Try all 4 directions, only gets called when we're in a new position"""
        self.junction_path_dirs[tuple(self.position)] = []
        for dir_num in range(1,5):
            self.ic.resume(dir_num)
            self.output = self.ic.output[-1]
            direction = self.rev_dir_dict[dir_num]
            next_pos = self.position + self.add_dict[direction]
            self.history[tuple(next_pos)] = self.output
            # print("dir_num = ", dir_num)  #DELME
            # print("next_pos = ", next_pos)  #DELME
            # print("output = ", self.output)  #DELME
            if self.output == 1 or self.output == 2:
                # if self.output == 2:  #DELME
                #     input("===================FOUND TWO===============")  #DELME
                self.ic.resume(self.backtrack_dict[dir_num])
                if dir_num != self.prev_dir:
                    self.junction_path_dirs[tuple(self.position)].append(dir_num)
        self.pos_visited[tuple(self.position)] = True
        # print("junction_path_dirs = ", self.junction_path_dirs)  #DELME


def make_array_from_record(history):
    xs, ys = np.array(list(history.keys()), dtype='int').T
    xmin = xs.min()
    xmax = xs.max()
    ymin = ys.min()
    ymax = ys.max()
    dx = xmax - xmin + 1
    dy = ymax - ymin + 1

    maze = np.zeros((dx, dy)) - 1

    for (x, y), t in history.items():
        maze[x - xmin, y - ymin] = t
    return maze

def plot_maze(history):
    history[(0, 0)] = 3
    maze = make_array_from_record(history)
    plt.imshow(maze.T)
    plt.pause(.05)
    return maze

def condition_maze(maze):
    maze2 = maze + 0
    maze2[maze == -1] = 0
    maze2[maze == 2] = 1
    maze2[maze == 3] = 1
    return maze2

def ij_to_flat(i, j, shape):
    num_rows, num_cols = shape
    return i*num_cols + j

def flat_to_ij(flat, shape):
    num_rows, num_cols = shape
    i = flat // num_cols
    j = flat - i*num_cols
    return i, j

def graph_index_to_flat(img):
    return np.where(img.flatten() == 1)[0]

def graph_index_to_ij(img):
    graph_to_flat = graph_index_to_flat(img)
    return [flat_to_ij(x, img.shape) for x in graph_to_flat]

def ij_to_graph_index(img):
    graph_to_ij = graph_index_to_ij(img)
    toret = {}
    for i, pos in enumerate(graph_to_ij):
        toret[pos] = i
    return toret

crawler = Crawler()
try:
    crawler.breadth_first_search()
except IndexError:
    pass

maze = plot_maze(crawler.history)
maze2 = condition_maze(maze)

[x_oxy], [y_oxy] = np.where(maze == 2)
[x_start], [y_start] = np.where(maze == 3)

graph = image.grid_to_graph(*maze2.shape, mask=maze2, return_as=np.ndarray)
shortest_paths = graph_shortest_path(graph)

print("Time-to-oxygen = {} minutes".format(np.max(np.unique(shortest_paths))))

# ij_to_g = ij_to_graph_index(maze2)

# print("SHORTEST PATH ISSSSSSSS!")
# print(shortest_paths[ij_to_g[(x_start, y_start)], ij_to_g[(x_oxy, y_oxy)]])


# ic = IntcodeComputer(allow_pausing=True)
# ic.code[0] = 2
# ic.run(0)
# ic.resume(0)
# ic.resume(0)
# while ic.continue_flag:
#   ic.resume(next_input)
#   ic.resume(next_input)
#   ic.resume(next_input)
#   x, y, t = ic.output[-3:]
#   if x == -1:
#       score = t
#       print("score = ", score)
#       ax.imshow(canvas.T)
#       fig.canvas.draw()   
#       plt.pause(.01)
