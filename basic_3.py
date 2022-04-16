import sys

# arg1 = sys.argv[1]
# arg2 = sys.argv[2]

# INPUT_FILE_PATH = arg1
# OUTPUT_FILE_PATH = arg2
f = open("../datapoints/in3.txt", "r")

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
    for i in range(1, len(meal) + 1):
        meal = meal[:raw[i] + 1] + meal + meal[raw[i] + 1:]

    return meal



class Seq_ali_basic: 
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
        self.alignment_cost_arr = [[-1 for i in range(len(self.y) + 1)] for j in range(len(self.x) + 1)]
        for i in range(len(self.x) + 1):
            self.alignment_cost_arr[i][0] = self.delta * i
        for j in range(len(self.y) + 1):
            self.alignment_cost_arr[0][j] = self.delta * j

    def calculate_alignment_cost_recursive(self, m, n):
        if self.alignment_cost_arr[len(m)][len(n)] != -1: 
            return self.alignment_cost_arr[len(m)][len(n)] 
        
        last_m = m[-1]
        last_n = n[-1]
        alpha = self.alpha_value_dict[(last_m, last_n)]
        self.alignment_cost_arr[len(m)][len(n)] = min(
            (alpha + self.calculate_alignment_cost_recursive(m[:-1], n[:-1])),
            (self.delta + self.calculate_alignment_cost_recursive(m[:-1], n)),
            (self.delta + self.calculate_alignment_cost_recursive(m, n[:-1]))
        )
        return self.alignment_cost_arr[len(m)][len(n)]

    def calculate_alignment_cost_loop(self, m, n): 
        for i in range(1, len(m) + 1):
            for j in range(1, len(n) + 1): 
                alpha = self.alpha_value_dict[(m[i-1:i], n[j-1:j])]
                self.alignment_cost_arr[i][j] = min(
                    (alpha + self.alignment_cost_arr[i - 1][j - 1]), 
                    (self.delta + self.alignment_cost_arr[i - 1][j]),
                    (self.delta + self.alignment_cost_arr[i][j - 1])
                )

    def find_alignment(self): 
        index_x = len(self.x)
        index_y = len(self.y)

        self.alignment_cost = self.alignment_cost_arr[index_x][index_y]
        while True:
            if index_x == 0 and index_y == 0: break
            if index_x == 0: 
                self.y_alignment = "_" + self.y_alignment
                index_y = index_y - 1
                continue
            if index_y == 0:
                self.x_alignment = "_" + self.x_alignment
                index_x = index_x - 1
                continue

            alignment_cost = self.alignment_cost_arr[index_x][index_y]
            x = self.x[index_x - 1: index_x]
            y = self.y[index_y - 1: index_y]
            alpha = self.alpha_value_dict[(x, y)]

            if alignment_cost == alpha + self.alignment_cost_arr[index_x - 1][index_y - 1]:
                self.x_alignment = x + self.x_alignment
                self.y_alignment = y + self.y_alignment
                index_x = index_x - 1
                index_y = index_y - 1
            elif alignment_cost == self.delta + self.alignment_cost_arr[index_x - 1][index_y]:
                self.x_alignment = "_" + self.x_alignment
                index_x = index_x - 1
            elif alignment_cost == self.delta + self.alignment_cost_arr[index_x][index_y - 1]:
                self.y_alignment = "_" + self.y_alignment
                index_y = index_y - 1
            else: 
                print("Error")
                break



if __name__ == "__main__":
    #x = "AA"
    x = CookingRaw(raw1)
    y = CookingRaw(raw2)
    #y = "C"

    print(f"====================================================================")
    basic = Seq_ali_basic(x, y)
    print(f"1_alignment_cost_arr_before: {basic.alignment_cost_arr}")
    basic.calculate_alignment_cost_recursive(x, y)
    print(f"1_alignment_cost_arr_after: {basic.alignment_cost_arr}")
    basic.find_alignment()
    print(f"alignment_cost: {basic.alignment_cost}")
    print(f"alignment_x: {basic.x_alignment}")
    print(f"alignment_y: {basic.y_alignment}")
    print(f"=======================================================")
    basic2 = Seq_ali_basic(x, y)
    print(f"2_alignment_cost_arr_before: {basic2.alignment_cost_arr}")
    basic2.calculate_alignment_cost_loop(x, y)
    print(f"2_alignment_cost_arr_after: {basic2.alignment_cost_arr}")
    basic2.find_alignment()
    print(f"alignment_cost: {basic2.alignment_cost}")
    print(f"alignment_x: {basic2.x_alignment}")
    print(f"alignment_y: {basic2.y_alignment}")