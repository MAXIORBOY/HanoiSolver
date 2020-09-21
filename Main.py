import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tempfile


def get_circles_number():
    return 5  # number of disks


def get_starting_matrix(n):
    return [list(np.linspace(1, n, n, dtype=int)), [], []]


def pick_correct_move(matrix, memory, illegal_moves, first_move):
    move = [0, 0, 0]

    if first_move:
        if len(matrix[0]) % 2 == 0:
            move = [0, 1, 1]
        else:
            move = [0, 2, 1]
    else:
        move_found = False
        for i in range(len(matrix)):
            if not move_found:
                for j in range(len(matrix)):
                    is_dest_array_empty = len(matrix[j]) == 0
                    if i == j:
                        continue
                    elif len(matrix[i]) == 0:
                        continue
                    elif matrix[i][0] == memory[-1][-1]:
                        continue
                    elif not is_dest_array_empty and matrix[i][0] > matrix[j][0]:
                        continue
                    elif [i, j, matrix[i][0]] in illegal_moves:
                        continue
                    else:
                        move = [i, j, matrix[i][0]]
                        move_found = True
                        break
            else:
                break

    return move


def register_move(matrix, move):
    del matrix[move[0]][0]
    matrix[move[1]].insert(0, move[2])

    return matrix


def correct_memory_array(memory):
    move_array = []
    for i in range(len(memory)):
        to_write = ''
        for j in range(len(memory[i])):
            if j < 2:
                if j == 1:
                    to_write += '->'

                to_write += change_index_to_letter(memory[i][j])

            else:
                to_write += ' | '
                to_write += str(memory[i][j])

        move_array.append(to_write)

    return move_array


def print_corrected_memory_array(corrected_memory):
    for i in range(len(corrected_memory)):
        print(str(i+1) + '. ' + corrected_memory[i])


def change_index_to_letter(index):
    if index == 0:
        return 'Start '
    elif index == 1:
        return 'Buffer'
    else:
        return 'Target'


def get_illegal_move(move):
    return [move[1], move[0], move[2]]


def copy_list(list_to_copy):
    new_list = []

    for i in range(len(list_to_copy)):
        row = []
        for j in range(len(list_to_copy[i])):
            row.append(list_to_copy[i][j])
        new_list.append(row)

    return new_list


def main(matrix, animate=True):
    first_move = True
    memory = []
    illegal_moves = []
    matrices = [copy_list(matrix)]

    while not(not len(matrix[0]) and not len(matrix[1])):
        move = pick_correct_move(matrix, memory, illegal_moves, first_move)
        matrix = register_move(matrix, move)
        memory.append(move)
        matrices.append(copy_list(matrix))
        illegal_move = get_illegal_move(move)

        if illegal_move not in illegal_moves:
            illegal_moves.append(illegal_move)

        if first_move:
            first_move = False

    print_corrected_memory_array(correct_memory_array(memory))
    if animate:
        with tempfile.TemporaryDirectory() as tmpdirname:
            create_plots(convert_to_plots(matrices), tmpdirname)
            start_animation(len(matrices), tmpdirname)


def convert_to_plots(matrices):
    plot_matrices = []
    for i in range(len(matrices)):
        x, y, size = [], [], []
        for j in range(3):
            x.extend([j] * len(matrices[i][j]))
            max_len = len(matrices[i][j])
            row = []
            for k in range(max_len):
                row.append(max_len - k)
            y.extend(row)
            size.extend(matrices[i][j])

        plot_matrices.append([x, y, size])

    return plot_matrices


def create_plots(converted_matrices, tmpdirname):
    counter = 0
    for single_plot in converted_matrices:
        plt.figure()
        for i in range(len(single_plot[0])):
            plt.plot(single_plot[0][i], single_plot[1][i], 'co', markersize=20)
            plt.text(single_plot[0][i], single_plot[1][i], str(single_plot[2][i]), horizontalalignment='center', verticalalignment='center', fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'bold', 'size': 12})

        plt.text(0, 0, 'Start ', horizontalalignment='center', verticalalignment='center', fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'normal', 'size': 14})
        plt.text(1, 0, 'Buffer ', horizontalalignment='center', verticalalignment='center', fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'normal', 'size': 14})
        plt.text(2, 0, 'Target ', horizontalalignment='center', verticalalignment='center', fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'normal', 'size': 14})
        plt.xlim((-0.5, 2.5))
        plt.ylim((-0.5, len(single_plot[0]) + 0.5))

        plt.axis('off')
        if counter:
            plt.title(str(counter) + '/' + str(len(converted_matrices) - 1), fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'bold', 'size': 16})
        else:
            plt.title('Start', fontdict={'family': 'DejaVu Sans', 'color': 'black', 'weight': 'bold', 'size': 16})

        plt.savefig(tmpdirname + '/' + str(counter + 1) + '.png', format='png')
        counter += 1
        plt.close()


def start_animation(n, tmpdirname):
    plt.figure()
    for i in range(n):
        plt.axis('off')
        img = mpimg.imread(tmpdirname + '/' + str(i+1) + '.png')
        plt.imshow(img)
        if i + 1 < n:
            plt.show(block=False)
            plt.pause(0.5)
            plt.clf()
        else:
            plt.show()

    plt.close()


main(get_starting_matrix(get_circles_number()))
