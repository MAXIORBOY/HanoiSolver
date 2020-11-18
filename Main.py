import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tempfile


class HanoiSolver:
    def __init__(self, number_of_discs):
        self.number_of_circles = number_of_discs
        self.containers = self.create_containers()
        self.animation_frames_raw_data = [[[el for el in row] for row in self.containers]]
        self.solve_hanoi_tower_problem()
        self.animation_frames_converted_data = self.convert_raw_animation_frames_data()

    def create_containers(self):
        return [list(np.linspace(1, self.number_of_circles, self.number_of_circles, dtype=int)), [], []]  # start, buffer, target

    @staticmethod
    def get_illegal_move(move):
        return [move[1], move[0], move[2]]

    def solve_hanoi_tower_problem(self):
        first_move = True
        memory = [-1, -1, -1]
        illegal_moves = []

        def pick_correct_move():
            correct_move = [0, 0, 0]  # from, to, what
            if first_move:
                if len(self.containers[0]) % 2 == 0:
                    correct_move = [0, 1, 1]
                else:
                    correct_move = [0, 2, 1]
            else:
                move_found = False
                for i in range(len(self.containers)):
                    if not move_found:
                        for j in range(len(self.containers)):
                            if i == j:
                                continue
                            elif len(self.containers[i]) == 0:
                                continue
                            elif self.containers[i][0] == memory[-1]:
                                continue
                            elif len(self.containers[j]) and self.containers[i][0] > self.containers[j][0]:
                                continue
                            elif [i, j, self.containers[i][0]] in illegal_moves:
                                continue
                            else:
                                correct_move = [i, j, self.containers[i][0]]
                                move_found = True
                                break
                    else:
                        break

            return correct_move

        while len(self.containers[0]) + len(self.containers[1]):
            move = pick_correct_move()
            memory = [move[i] for i in range(len(move))]
            self.register_move(move)
            self.animation_frames_raw_data.append([[el for el in row] for row in self.containers])
            illegal_move = self.get_illegal_move(move)

            if illegal_move not in illegal_moves:
                illegal_moves.append(illegal_move)

            if first_move:
                first_move = False

    def register_move(self, move):
        del self.containers[move[0]][0]
        self.containers[move[1]].insert(0, move[2])

    def convert_raw_animation_frames_data(self):
        animation_frames_converted_data = []
        for i in range(len(self.animation_frames_raw_data)):
            x, y, disc_size = [], [], []
            for j in range(3):
                x.extend([j] * len(self.animation_frames_raw_data[i][j]))
                max_len = len(self.animation_frames_raw_data[i][j])
                row = []
                for k in range(max_len):
                    row.append(max_len - k)
                y.extend(row)
                disc_size.extend(self.animation_frames_raw_data[i][j])

            animation_frames_converted_data.append([x, y, disc_size])

        return animation_frames_converted_data

    def build_plots_from_converted_data(self, tmpdirname):
        counter = 0
        container_names = ['Start ', 'Buffer ', 'Target ']
        for single_plot in self.animation_frames_converted_data:
            plt.figure()
            for i in range(len(single_plot[0])):
                plt.plot(single_plot[0][i], single_plot[1][i], 'co', markersize=20)
                plt.text(single_plot[0][i], single_plot[1][i], str(single_plot[2][i]), horizontalalignment='center', verticalalignment='center', fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'bold', 'size': 12})

            for i in range(len(container_names)):
                plt.text(i, 0, container_names[i], horizontalalignment='center', verticalalignment='center', fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'normal', 'size': 14})
            plt.xlim((-0.5, 2.5))
            plt.ylim((-0.5, len(single_plot[0]) + 0.5))

            plt.axis('off')
            if counter:
                plt.title(str(counter) + '/' + str(len(self.animation_frames_converted_data) - 1), fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'bold', 'size': 16})
            else:
                plt.title('Start', fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'bold', 'size': 16})

            plt.savefig(tmpdirname + '/' + str(counter + 1) + '.png', format='png')
            counter += 1
            plt.close()

    def start_animation(self, tmpdirname):
        plt.figure()
        for i in range(len(self.animation_frames_raw_data)):
            plt.axis('off')
            img = mpimg.imread(tmpdirname + '/' + str(i + 1) + '.png')
            plt.imshow(img)
            if i + 1 < len(self.animation_frames_raw_data):
                plt.show(block=False)
                plt.pause(0.5)
                plt.clf()
            else:
                plt.show()

        plt.close()

    def run(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.build_plots_from_converted_data(tmpdirname)
            self.start_animation(tmpdirname)
