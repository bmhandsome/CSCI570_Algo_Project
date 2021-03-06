import sys
from resource import *
import time
import psutil

arg1 = sys.argv[1]
arg2 = sys.argv[2]

INPUT_FILE_PATH = arg1
OUTPUT_FILE_PATH = arg2

f = open(INPUT_FILE_PATH, "r")
# f = open("../SampleTestCases/input4.txt", "r")

raw1 = []
raw2 = []
i = 0

for x in f:
    if i == 0:
        raw1.append(x.strip())
        i += 1
    elif i == 1:
        try:
            raw1.append(int(x.strip()))
        except:
            raw2.append(x.strip())
            i += 1
    else:
        raw2.append(int(x.strip()))


def CookingRaw(raw):
    meal = raw[0]
    for i in range(1, len(raw)):
        meal = meal[:raw[i] + 1] + meal + meal[raw[i] + 1:]

    return meal


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def time_wrapper(x, y):
    start_time = time.time()
    alignment_cost, x_alignment, y_alignment = call_algorithm(x, y)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return time_taken, alignment_cost, x_alignment, y_alignment


def call_algorithm(x, y):
    efficient = Seq_ali_eff(x, y)
    alignment_cost, x_alignment, y_alignment = efficient.divide_and_conquer(x, y)
    # alignment_cost, x_alignment, y_alignment, cost_list = efficient.divide_and_conquer(x, y)
    return alignment_cost, x_alignment, y_alignment


class Seq_ali_eff:
    def __init__(self, X, Y):
        self.alpha_value_dict = {
            ("A", "A"): 0, ("A", "C"): 110, ("A", "G"): 48, ("A", "T"): 94,
            ("C", "A"): 110, ("C", "C"): 0, ("C", "G"): 118, ("C", "T"): 48,
            ("G", "A"): 48, ("G", "C"): 118, ("G", "G"): 0, ("G", "T"): 110,
            ("T", "A"): 94, ("T", "C"): 48, ("T", "G"): 110, ("T", "T"): 0
        }
        self.delta = 30
        self.x = X
        self.y = Y
        self.x_alignment = ""
        self.y_alignment = ""
        self.alignment_cost = 0

    def divide_and_conquer(self, x, y):
        if (len(x) == 0 and len(y) == 0): return 0, "", ""
        if (len(x) == 0 and len(y) != 0): return len(y) * self.delta, "_" * len(y), y
        if (not len(x) == 0 and len(y) == 0): return len(x) * self.delta, x, "_" * len(x)

        if (len(x) == 1 and len(y) == 1):
            alpha = self.alpha_value_dict[(x, y)]
            if alpha <= self.delta * 2:
                return alpha, x, y
            else:
                return self.delta * 2, "_" + x, y + "_"

        if (len(x) == 2 and len(y) == 1):
            if x[0] == y:
                return self.delta, x, y + "_"
            elif x[1] == y:
                return self.delta, x, "_" + y
            elif self.alpha_value_dict[(x[0], y)] < self.delta * 2:
                return self.delta + self.alpha_value_dict[(x[0], y)], x, y + "_"
            elif self.alpha_value_dict[(x[1], y)] < self.delta * 2:
                return self.delta + self.alpha_value_dict[(x[1], y)], x, "_" + y
            else:
                return 3 * self.delta, "_" + x, y + "__"

        if (len(x) == 1 and len(y) == 2):
            if y[0] == x:
                return self.delta, x + "_", y
            elif y[1] == x:
                return self.delta, "_" + x, y
            elif self.alpha_value_dict[(y[0], x)] < self.delta * 2:
                return self.delta + self.alpha_value_dict[(y[0], x)], x + "_", y
            elif self.alpha_value_dict[(y[1], x)] < self.delta * 2:
                return self.delta + self.alpha_value_dict[(y[1], x)], "_" + x, y
            else:
                return 3 * self.delta, "__" + x, y + "_"

        if (len(x) == 1 and len(y) > 2):
            j = 0
            while j < len(y):
                if x == y[j]:
                    return (len(y) - 1) * self.delta, '_' * j + x + '_' * (len(y) - j - 1), y
                else:
                    j += 1
            j = 0
            while j < len(y):
                if self.alpha_value_dict[(x, y[j])] < self.delta * 2:
                    return (len(y) - 1) * self.delta + self.alpha_value_dict[(x, y[j])], '_' * j + x + '_' * (
                                len(y) - j - 1), y
                else:
                    j += 1

        divide_index_x = int(len(x) / 2)
        x_left = x[:divide_index_x]
        x_right = x[divide_index_x:]
        x_right_reverse = x_right[::-1]
        y_reverse = y[::-1]

        #####################################################################################

        alignment_cost_arr_left = [[-1 for j in range(len(y) + 1)] for i in range(2)]
        for i in range(2):
            alignment_cost_arr_left[i][0] = self.delta * i
        for j in range(len(y) + 1):
            alignment_cost_arr_left[0][j] = self.delta * j

        for i in range(1, divide_index_x + 1):
            for j in range(1, len(y) + 1):
                alpha = self.alpha_value_dict[(x_left[i - 1], y[j - 1])]
                alignment_cost_arr_left[1][j] = min(
                    (alpha + alignment_cost_arr_left[0][j - 1]),
                    (self.delta + alignment_cost_arr_left[0][j]),
                    (self.delta + alignment_cost_arr_left[1][j - 1])
                )
            if i != divide_index_x:
                alignment_cost_arr_left[0] = list(alignment_cost_arr_left[1])
                alignment_cost_arr_left[1][0] = alignment_cost_arr_left[0][0] + self.delta

        #####################################################################################

        alignment_cost_arr_right = [[-1 for j in range(len(y_reverse) + 1)] for i in range(2)]
        for i in range(2):
            alignment_cost_arr_right[i][0] = self.delta * i
        for j in range(len(y_reverse) + 1):
            alignment_cost_arr_right[0][j] = self.delta * j

        for i in range(1, len(x) - divide_index_x + 1):
            for j in range(1, len(y_reverse) + 1):
                alpha = self.alpha_value_dict[(x_right_reverse[i - 1], y_reverse[j - 1])]
                alignment_cost_arr_right[1][j] = min(
                    (alpha + alignment_cost_arr_right[0][j - 1]),
                    (self.delta + alignment_cost_arr_right[0][j]),
                    (self.delta + alignment_cost_arr_right[1][j - 1])
                )
            if i != len(x) - divide_index_x:
                alignment_cost_arr_right[0] = list(alignment_cost_arr_right[1])
                alignment_cost_arr_right[1][0] = alignment_cost_arr_right[0][0] + self.delta

        #####################################################################################

        alignment_cost_arr_sum = [-1 for j in range(len(y) + 1)]

        for i in range(len(y) + 1):
            alignment_cost_arr_sum[i] = alignment_cost_arr_left[1][i] + alignment_cost_arr_right[1][len(y) - i]

        min_alignment_cost = min(alignment_cost_arr_sum)
        index_min = alignment_cost_arr_sum.index(min_alignment_cost)

        #####################################################################################

        y_left = y[:index_min]
        y_right = y[index_min:]

        result_left = self.divide_and_conquer(x_left, y_left)
        result_right = self.divide_and_conquer(x_right, y_right)

        return min_alignment_cost, result_left[1] + result_right[1], result_left[2] + result_right[2]
        # return min_alignment_cost, result_left[1] + result_right[1], result_left[2] + result_right[2], y_left

if __name__ == "__main__":
    x = CookingRaw(raw1)
    y = CookingRaw(raw2)
    # x = "C"
    # y = "CG"

    time_taken, alignment_cost, x_alignment, y_alignment = time_wrapper(x, y)
    memory = process_memory()
    with open(OUTPUT_FILE_PATH, "wt") as f:
        f.write(f"{alignment_cost}\n")
        f.write(f"{x_alignment}\n")
        f.write(f"{y_alignment}\n")
        f.write(f"{time_taken}\n")
        f.write(f"{memory}")

    # efficient = Seq_ali_eff(x, y)
    # alignment_cost, x_alignment, y_alignment = efficient.divide_and_conquer(x, y, 0)
    # print(f"alignment_cost: {alignment_cost}")
    # print(f"x_alignment: {x_alignment}")
    # print(f"y_alignment: {y_alignment}")