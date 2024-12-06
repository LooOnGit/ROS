import numpy as np

################################################################################### Code mã hóa của nhóm

# def encode(p):
#     val = []
#     for obj in p:
#         for gen in obj:
#             val.append(ord(str(gen)))
#     return val

################################################################################### Code giải mã của nhóm

# def decode(p, ngene):
#     matrix = np.zeros((1,ngene))
#     decode_val = []
#     for val in p:
#         decode_val.append(chr(val))
#     i = 0
#     for x in range(1):
#         for y in range(ngene):
#             matrix[x, y] = decode_val[i]
#             i+=1
#     return matrix

################################################################################### Code chọn lọc của nhóm

def selection(pop, fitness, ngene):
    AddNew = False
    result = []
    temp = []
    dup = []
    x = 0
    for i in fitness:
        for _ in range(i):
            temp.append(pop[x])
        x += 1
    for i in range(ngene):
        count = 0
        ran_num = np.random.randint(0, len(temp))
        value = temp[ran_num]
        for index, array_2d in enumerate(dup):
            if np.array_equal(value, array_2d):
                while True:
                    AddNew = False
                    break_val = 1
                    if count >= 10:
                        for gen in pop:
                            break_val = 1
                            for x in range(len(dup)):
                                if np.array_equal(dup[x], gen):
                                    break_val = 0
                                    break
                            if break_val == 1:
                                value = gen
                                AddNew = True
                                break 
                    else:
                        ran_num = np.random.randint(0, len(temp))
                        value = temp[ran_num]
                        for index, array_2d in enumerate(dup):
                            if np.array_equal(value, array_2d):
                                break_val = 0
                    if break_val == 1:
                        break
                    count += 1
                if AddNew == True:
                    break
        result.append(value)
        dup = np.array(result)
    return np.array(result)

################################################################################### Code lai ghép của nhóm

def crossover(pop, pop_size, input_size, ngene):
    result = []
    for i in range(ngene):
        if i %2 == 0:
            p1 = pop[i]
            p2 = pop[i+1]
            f1 = []
            f2 = []
            for _ in range(input_size):
                crossing_point = np.random.randint(1, pop_size-1)
                f1.append(np.concatenate((p1[_][:crossing_point], p2[_][crossing_point:])))
                f2.append(np.concatenate((p2[_][:crossing_point], p1[_][crossing_point:])))
            f1 = np.array(f1)
            result.append(f1)
            f2 = np.array(f2)
            result.append(f2)
    return np.array(result)

################################################################################### Code đột biến của nhóm

def mutation(pop, mutation_rate, pop_size, ngene):
    result = []
    for p in pop:
        matrix = np.random.rand(ngene, pop_size)
        changes = np.where(matrix < mutation_rate)
        p[changes] = np.random.uniform(0,2, size=len(changes[0]))
        result.append(p)
    return np.array(result)

################################################################################### Tổng hợp

def ga(pop, fitness, ngene, input_size, hidden_size):
    pop_after_selection = selection(pop, fitness, ngene)
    pop_after_crossover = crossover(pop_after_selection, hidden_size, input_size, ngene)
    pop_after_mutation = mutation(pop_after_crossover, mutation_rate = 0.1, pop_size=hidden_size, ngene=input_size)
    return pop_after_mutation