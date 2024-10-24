import numpy as np

input_size = 10
hidden_size = 6
output_size = 2
ngene = 10

# Hàm kích hoạt
def sigmoid(x):
    return 1/(1 + np.exp(-x))

def neuron(sensor_input, w1, w2):
    result = []
    for i in range(len(w1)):
        # Tính toán đầu ra lớp ẩn
        hidden_layer_input = np.dot(w1[i].T,sensor_input)
        hidden_layer_output = sigmoid(hidden_layer_input)
        # Tính toán đầu ra lớp ngõ ra
        output_layer_input = np.dot(w2[i].T, hidden_layer_output)
        output_layer_output = sigmoid(output_layer_input)
        result.append(output_layer_output)
    
    return result

input_size = 16 # số lượng ngõ vào
hidden_size = 10 # số neuron lớp ẩn
output_size = 2 # số ngõ ra mong muốn
ngene = 10 # số lượng cá thể

sensor_input = np.random.uniform(0,10, size=(input_size))
w1 = np.random.uniform(0,2,size=(ngene, input_size, hidden_size))
w2 = np.random.uniform(0,2,size=(ngene, hidden_size, output_size))
print(neuron(sensor_input, w1, w2))