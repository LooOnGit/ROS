import numpy as np
import random
import config as cf

pop_size = cf.pop_size
npar = cf.npar
ngene = cf.ngene
min_max = cf.min_max

################################################################################### Code mã hóa của nhóm

def encode(p):
    val = []
    for obj in p:
        for gen in obj:
            val.append(ord(str(gen)))
    return val

################################################################################### Code giải mã của nhóm

def decode(p):
    matrix = np.zeros((npar,ngene))
    decode_val = []
    for val in p:
        decode_val.append(chr(val))
    i = 0
    for x in range(npar):
        for y in range(ngene):
            matrix[x, y] = decode_val[i]
            i+=1
    return matrix

################################################################################### Code chọn lọc của nhóm

def selection(pop, fitness):
    i = 0
    temp = []
    p = []
    for val in fitness:
        for _ in range(val):
            temp.append(pop[i])
        i+=1
    temp = np.array(temp)
    ran_num = random.sample(range(0, len(temp)), pop_size)
    for i in range(len(fitness)):
        p.append(temp[ran_num[i]])
    return np.array(p)

################################################################################### Code lai ghép của nhóm

def crossover(p):
    result = []
    for i in range(pop_size):
        if i%2 == 0:
            crossing_point = np.random.randint(1, ngene-1)
            value = []
            for x in range(npar):  
                value.append(np.concatenate((p[i][x][:crossing_point], p[i+1][x][crossing_point:])))
            value = np.array(value)
            result.append(value)

            value = []
            for x in range(npar):  
                value.append(np.concatenate((p[i+1][x][:crossing_point], p[i][x][crossing_point:])))
            value = np.array(value)
            result.append(value)
    return np.array(result)

################################################################################### Code đột biến của nhóm

def mutation(p, mutation_rate):
    matrix = np.random.rand(pop_size,npar,ngene)
    changes = np.where(matrix < mutation_rate)
    print(changes)
    print("-----------------------------------")
    p[changes] = np.random.randint(0, 10, size=len(changes[0]))
    return p