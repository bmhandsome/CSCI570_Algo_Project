import sys
from resource import *
import time
import psutil

arg1 = sys.argv[1]
arg2 = sys.argv[2]

INPUT_FILE_PATH = arg1
OUTPUT_FILE_PATH = arg2

f = open(INPUT_FILE_PATH, "r")
#f = open("../SampleTestCases/input1.txt", "r")

raw1 = []
raw2 = []
i = 0

for x in f:
    if i==0:
        raw1.append(x.strip())
        i+=1
    elif i==1:
        try:
            raw1.append(int(x.strip()))
        except:
            raw2.append(x.strip())
            i+=1
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
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper(x, y):
    start_time = time.time()
    alignment_cost, x_alignment, y_alignment = call_algorithm(x, y)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    return time_taken, alignment_cost, x_alignment, y_alignment

def call_algorithm(x, y):

    efficient = Seq_ali_eff(x, y)
    alignment_cost, x_alignment, y_alignment = efficient.divide_and_conquer(x, y, 0)
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

    def divide_and_conquer(self, x, y, count):
        if (len(x) == 0 and len(y) == 0): return 0, "", ""
        if (len(x) == 0 and not len(y) == 0): return len(y) * self.delta, "_" * len(y), y
        if (not len(x) == 0 and len(y) == 0): return len(x) * self.delta, x, "_" * len(x)

        if (len(x) == 1 and len(y) == 1):
            alpha = self.alpha_value_dict[(x, y)]
            if alpha <= self.delta * 2:
                return alpha, x, y
            else:
                return self.delta * 2, "_" + x, y + "_"

        divide_index_x = int(len(x) / 2)
        x_left = x[:divide_index_x]
        x_right = x[divide_index_x:]
        x_right_reverse = x_right[::-1]
        y_reverse = y[::-1]

        alignment_cost_arr_left = [[0 for i in range(len(y) + 1)] for j in range(2)]
        for i in range(2):
            alignment_cost_arr_left[i][0] = 0
        for j in range(len(y) + 1):
            alignment_cost_arr_left[0][j] = self.delta * j

        #finding alignment cost of x_left and y
        index_x_left = 1
        while index_x_left <= len(x_left):
            alignment_cost_arr_left[1][0] = alignment_cost_arr_left[0][0] + self.delta
            for j in range(1, len(y) + 1):
                alpha = self.alpha_value_dict[(x_left[index_x_left-1],y[j-1])]

                alignment_cost_arr_left[1][j] = min(
                    (alpha + alignment_cost_arr_left[0][j - 1]),
                    (self.delta + alignment_cost_arr_left[0][j]),
                    (self.delta + alignment_cost_arr_left[1][j - 1])
                )

            index_x_left = index_x_left + 1
            alignment_cost_arr_left[0] = list(alignment_cost_arr_left[1])

        alignment_cost_arr_right = [[0 for i in range(len(y_reverse) + 1)] for j in range(2)]
        for i in range(2): 
            alignment_cost_arr_right[i][0] = 0
        for j in range(len(y_reverse) + 1):
            alignment_cost_arr_right[0][j] = self.delta * j

        #finding alignment cost of x_right_reverse and y_reverse
        index_x_right_reverse = 1
        while index_x_right_reverse <= len(x_right):
            alignment_cost_arr_right[1][0] = alignment_cost_arr_right[0][0] + self.delta
            for j in range(1, len(y_reverse) + 1):
                alpha = self.alpha_value_dict[(x_right_reverse[index_x_right_reverse-1],y_reverse[j-1])]
                alignment_cost_arr_right[1][j] = min(
                    (alpha + alignment_cost_arr_right[0][j -1]),
                    (self.delta + alignment_cost_arr_right[0][j]),
                    (self.delta + alignment_cost_arr_right[1][j - 1])
                )

            index_x_right_reverse = index_x_right_reverse + 1
            alignment_cost_arr_right[0] = list(alignment_cost_arr_right[1])

        alignment_cost_arr_sum = [0 for i in range(len(y) + 1)]

        for i in range(len(alignment_cost_arr_sum)):
            alignment_cost_arr_sum[i] = alignment_cost_arr_left[1][i] + alignment_cost_arr_right[1][len(y_reverse) - i]

        min_alignment_cost = min(alignment_cost_arr_sum)
        index_min = alignment_cost_arr_sum.index(min_alignment_cost)

        if divide_index_x == 0 and index_min == 0:
                return self.delta * (len(y) - len(x)), x + "_", y

        y_left = y[:index_min]
        y_right = y[index_min:]

        result_left = self.divide_and_conquer(x_left, y_left, count + 1)
        result_right = self.divide_and_conquer(x_right, y_right, count + 1)

        return min_alignment_cost, result_left[1] + result_right[1], result_left[2] + result_right[2]

if __name__ == "__main__":
    x = CookingRaw(raw1)
    y = CookingRaw(raw2)
    # x = "TC"
    # y = "CT"

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