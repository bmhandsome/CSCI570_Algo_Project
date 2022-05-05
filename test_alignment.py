import sys

from numpy import char
INPUT_FILE_1 = sys.argv[1]
INPUT_FILE_2 = sys.argv[2]

cost_from_file_1 = 0
cost_from_file_2 = 0
string_1_x = ""
string_1_y = ""
string_2_x = ""
string_2_y = ""

with open(INPUT_FILE_1, "r") as f1:
    cost_from_file_1 = int(f1.readline())
    string_1_x = f1.readline()
    string_1_y = f1.readline()

with open(INPUT_FILE_2, "r") as f2:
    cost_from_file_2 = int(f2.readline())
    string_2_x = f2.readline()
    string_2_y = f2.readline()

print(f'cost 1: {cost_from_file_1} | cost 2: {cost_from_file_2} | read from file')
assert cost_from_file_1 == cost_from_file_2

print(f'lenght string1_x: {len(string_1_x)} | lenght string1_y: {len(string_1_y)}')
assert len(string_1_x) == len(string_1_y)

print(f'lenght string2_x: {len(string_2_x)} | lenght string2_y: {len(string_2_y)}')
assert len(string_2_x) == len(string_2_y)

print(f'lenght string1: {len(string_1_x)} | lenght string2: {len(string_2_x)}')
assert len(string_1_x) == len(string_2_x)


def calculate_alignment_cost(x, y):
    delta = 30
    alpha_value_dict = {
        ("A", "A"): 0, ("A", "C"): 110, ("A", "G"): 48, ("A", "T"): 94,
        ("C", "A"): 110, ("C", "C"): 0, ("C", "G"): 118, ("C", "T"): 48,
        ("G", "A"): 48, ("G", "C"): 118, ("G", "G"): 0, ("G", "T"): 110,
        ("T", "A"): 94, ("T", "C"): 48, ("T", "G"): 110, ("T", "T"): 0
    }

    alignment_cost = 0
    for i in range(len(x) - 1):
        char_x = x[i]
        char_y = y[i]
        
        if char_x == '_' or char_y == '_':
            alignment_cost += delta
        else:
            alignment_cost += alpha_value_dict[(char_x, char_y)]
    
    return alignment_cost
alignment_cost_1 = calculate_alignment_cost(string_1_x, string_1_y)
alignment_cost_2 = calculate_alignment_cost(string_2_x, string_2_y)

print(f'alignment_cost_from_file_basic: {cost_from_file_1} | alignment_cost_from_cal_basic: {alignment_cost_1}')
assert cost_from_file_1 == alignment_cost_1
print(f'alignment_cost_from_file_efficient: {cost_from_file_2} | alignment_cost_from_cal_efficient: {alignment_cost_2}')
assert cost_from_file_2 == alignment_cost_2
print(f'alignment_cost_1: {alignment_cost_1} | alignment_cost_2: {alignment_cost_2} | calculate')
assert alignment_cost_1 == alignment_cost_2