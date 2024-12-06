import numpy as np
import GA_Code as ga
import config as cf

pop_size = cf.pop_size
npar = cf.npar
ngene = cf.ngene
min_max = cf.min_max

################################################################################ Khởi tạo

pop = np.random.randint(0,10,size=(pop_size,npar,ngene))

############################################################################### Mã hóa

# print(pop[0])
# print("-----------------------------------")
# encode_val = ga.encode(pop[0])
# print(encode_val)

############################################################################### Giải mã

# print("-----------------------------------")
# decode_val = ga.decode(encode_val)
# print(decode_val)

################################################################################ Chọn lọc

print("----------------------------------- Bố mẹ")
print(pop)
fitness = [20,2,3,4,5,6,7,8,9,10]
pop_after_selection = ga.selection(pop, fitness)
print("----------------------------------- Chọn lọc")
print(pop_after_selection)

################################################################################ Lai ghép

print("----------------------------------- Lai ghép")
pop_after_crossover = ga.crossover(pop_after_selection)
print(pop_after_crossover)

################################################################################ Đột biến

print("----------------------------------- Đột biến")
print(ga.mutation(pop_after_crossover, 0.1))