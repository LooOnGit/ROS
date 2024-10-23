import numpy as np
# import ga

input_size = 10
hidden_size = 6
output_size = 2

# Hàm kích hoạt
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def neuron(sensor_input, w1, b1, w2, b2):
    # Tính toán đầu ra lớp ẩn
    hidden_layer_input = np.dot(sensor_input, w1) + b1
    hidden_layer_output = sigmoid(hidden_layer_input)
    
    # Tính toán đầu ra lớp ngõ ra
    output_layer_input = np.dot(hidden_layer_output, w2) + b2
    output_layer_output = sigmoid(output_layer_input)
    
    return output_layer_output

# # Khởi tạo input ngẫu nhiên cho GA
# pop_1 = np.random.randint(0,10,size=(hidden_size,1, input_size))
# fitness_1 = np.random.randint(0,10,size=(hidden_size))

# pop_2 = np.random.randint(0,10,size=(output_size,1, hidden_size))
# fitness_2 = np.random.randint(0,10,size=(output_size))

# # Từ GA tính toán trọng số cho lớp ẩn
# w1 = ga.ga(pop=pop_1, fitness=fitness_1, rate=0.1, pop_size=hidden_size, ngene=input_size)
# b1 = np.random.randn(hidden_size) 

# # Từ GA tính toán trọng số cho ngõ ra
# w2 = ga.ga(pop=pop_2, fitness=fitness_2, rate=0.1, pop_size=output_size, ngene=hidden_size)
# b2 = np.random.randn(output_size) 

# sensor_input = np.random.randn(input_size) 
# output = neuron(sensor_input,w1,b1,w2,b2)
# print("x = ", output[0])
# print("z = ", output[1])