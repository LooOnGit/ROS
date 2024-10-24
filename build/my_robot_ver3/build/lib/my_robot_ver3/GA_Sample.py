import numpy as np
import config as cf

pop_size = cf.pop_size
npar = cf.npar
ngene = cf.ngene
min_max = cf.min_max

################################################################################## Code giải mã của thầy Kiên

def decode(p):# Truyền vào pop[0]
    val = np.zeros((npar,1))
    for i in range(npar):
        for j in range(ngene):
            val[i] = val[i]*10 + p[i,j]
    val = min_max[0] + val/(10**ngene-1)*(min_max[1]-min_max[0]) # val = -2 + val/99999 * 4 = nếu val = 0 thì val_new = -2
    return val

################################################################################## Code mã hóa của thầy Kiên

def encode(p):# Truyền vào decode(pop[0])
    val = np.zeros((npar, 1))
    my_list = np.zeros((npar, ngene), dtype=int)
    for i in range(npar):
        val[i] =  np.round((p[i] - min_max[0]) / (min_max[1] - min_max[0]) * (10**ngene - 1)) #Thêm round để tránh làm tròn khiến cho kết quả bị chênh lệch giá trị so với ban đầu
        my_string = str(int(val[i][0]))
        my_string = my_string.zfill(ngene)
        my_list[i] = [int(char) for char in my_string]
    return my_list

################################################################################## Code chọn lọc của thầy Kiên

def selection(pop, fitness, c): # Truyền vào (pop, fitness, 0.5)
    sort_index = np.argsort(fitness)
    p = pop[sort_index,:,:]
    n = len(fitness)
    pk = [1]
    for _ in range(n-1):
        next_element = pk[-1]*c
        pk.append(next_element)
    pk=pk/np.sum(pk)
    # print(pk)
    p1=np.random.choice(range(int(n)), size=int(n), p=pk, replace=True)
    p = p[p1,:,:]
    return p

################################################################################## Code lai ghép của thầy Kiên

def crossover(p): # truyền vào pop
    k = int(len(p)/2)
    crossing_point =np.random.randint(1, ngene-1)
    p1 = p[0::2,:,:]
    p2 = p[1::2,:,:]
    c1 = np.dstack((p1[:,:,0:crossing_point],p2[:,:,crossing_point:]))
    c2 = np.dstack((p2[:,:,0:crossing_point],p1[:,:,crossing_point:]))
    c = np.vstack((c1,c2))
    return c

################################################################################## Code đột biến của thầy Kiên

def mutation(p,mutation_rate): # truyền vào pop và tỉ lệ đột biến
    pp = p
    for k in range(pop_size):
        for i in range(npar):
            if np.random.rand() < mutation_rate:
                indices_to_change = np.random.choice(ngene, size=1, replace=False)
                for idx in indices_to_change:
                    pp[k,i,idx] = np.random.randint(0,10)
    return pp


# Tính toán hàm mục tiêu để robot đi từ A đến B
# lưu trọng số GA vào exel
# mạng nơ ron đầu vào là vị trí hiện tại và giá trị 10 cảm biến
# đầu vào mạng nơ ron là sai số của x và y. Ví dụ robot đang ở vị trí 0 0, nếu sai số x với y là 2 0 thì thành công