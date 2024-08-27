import sys
import math
import numpy as np
import heapq
import copy

def selection(array):
    sum = 0
    sum_p = 0
    saver = []
    for each in array:
        saver.append(float(each[0]))
        each[0] = (1 - float(each[0])) + 3000 # mijenjamo MSE sa dobrotom, sto je veci MSE manja je dobrota
        sum += each[0]
    
    for each in array:
        each[0] = each[0] / sum

    random_float = np.random.rand()
    for each in array:
        sum_p += each[0]
        if random_float < sum_p:
            for i in range(0, len(saver), 1):
                array[i][0] = saver[i]
            return each

def MSE(output):
    sum = 0
    for each in output:
        sum += (float(each[0])- float(each[1]))**2
    
    return (1/len(output))*sum

def sig(x):
 return 1/(1 + np.exp(-x))

def init_NN(nn_arh, header):

    head = header[0]  

    neureal_net = []

    for i in range(len(nn_arh)+2): # kreiranje polja neuronske mreze
        neureal_net.append([])

    for i in range(len(head)-1): # populiranje ulaza
        neureal_net[0].append([1])
    
    for i in range(1, len(neureal_net)-1, 1): # populiranje skrivenih slojeva tezinama
        
        for j in range(int(nn_arh[i-1])):
            neuron = []
            for k in range(len(neureal_net[i-1])): # populiranje neurona u skrivenim slojevima
                random_number = np.random.normal(loc=0.0, scale=0.01)
                neuron.append(random_number)
            random_number = np.random.normal(loc=0.0, scale=0.01)
            neuron.append(random_number)
            neureal_net[i].append(neuron)

    neuron = []
    for i in range(len(neureal_net[-2])): # populiranje izlaza
        random_number = np.random.normal(loc=0.0, scale=0.01)
        neuron.append(random_number)
    random_number = np.random.normal(loc=0.0, scale=0.01) # bias
    neuron.append(random_number)
    neureal_net[-1].append(neuron)

    return neureal_net

def forward_pass(nn):
    # [
    # [['ulazni podatci']], 
    # [[0.010580864246980718, 0.004350172338296049], [0.0008724495058931615, -0.010718842946196185]], 
    # [[0.00973539285181121, 0.011313062098989421, -0.020513544717604755], [-0.007063608610423087, 0.0035698864069266295, -0.0009253445930731259]], 
    # [[0.009172185190405309, -0.024516682523052356, -0.0014070111860754882]]
    # ]

    weight_matrix = []
    input_matrix = []
    bias_matrix = []

    for i in range(0, len(nn)-1, 1):
        weight_matrix = []
        bias_matrix = []

        if i == 0:
            for each in nn[i]:
                input_matrix.append([float(each[0])])
        for weight in nn[i+1]:
            w = []
            for j in range(0, len(nn[i]), 1):
                w.append(weight[j])
            
            weight_matrix.append(w)
            bias_matrix.append([weight[-1]])
        
        y_matrix = np.matmul(weight_matrix, input_matrix)
        y_matrix = np.add(y_matrix, bias_matrix)

        if i != len(nn)-2:
            y_matrix = sig(y_matrix)

        input_matrix = y_matrix

    return input_matrix

# python solution.py --train sine_train.txt --test sine_test.txt --nn 5s5s --popsize 10 --elitism 1 --p 0.1 --K 0.1 --iter 10000

train_dataset = sys.argv[2]
test_dataset = sys.argv[4]
nn_arh = (sys.argv[6]).split("s")
for each in nn_arh:
    if len(each) == 0:
        nn_arh.remove(each)
pop_size = int(sys.argv[8])
elitism = int(sys.argv[10])
p_m = float(sys.argv[12]) # probability of mutation
mutation_scale = float(sys.argv[14])
num_iter = int(sys.argv[16]) # number of iterations


'''train_dataset = "sine_train.txt"
test_dataset = "sine_test.txt"
nn_arh = "5s".split("s")
for each in nn_arh:
    if len(each) == 0:
        nn_arh.remove(each)
pop_size = 10
elitism = 1
p_m = 0.1 # probability of mutation
mutation_scale = 0.1
num_iter = 500 # number of iterations'''

nn = [] # neural network array
nn_array = []
header = []
output_array = []
MSE_array = [] # tu se nalaze [neuronska mreza sa svojim tezina, MSE koji dobijemo nakon unaprijednog prolaza]
current_iter = 0 # trenutna iteracija koja se provodi
population = [] # populacija djece koja se kasnije dodaju u populaciju

file_train = open(train_dataset, "r")
file_test = open(test_dataset, "r")
train_dataset = []
test_dataset = []
for each in file_train:
    each = each.replace("\n", "")
    each = each.split(",")
    train_dataset.append(each)

header.append(train_dataset[0])
train_dataset.remove(header[0])

for each in file_test:
    each = each.replace("\n", "")
    each = each.split(",")
    test_dataset.append(each)
test_dataset.remove(header[0])

#print(train_dataset)
for i in range(pop_size): # stvaramo zadanu populaciju neuronskih mreza
    nn = init_NN(nn_arh, header)
    nn_array.append(nn)
#print(nn) # [[[1], [1]], [[0.019020325913811635, -0.009211466749174883, -0.00824653618839752], [0.011996154069377736, 0.008276157778191353, 0.002809319983197675]], [[-0.018016881767382385, 0.0030192651688784157, -0.002217628008972591], [0.003287748456362126, -0.0048588362972636, -0.005512252454367698]], [[0.013593191550105677, -0.004943188075791018, -0.01181510363723056]]

for neural in nn_array:
    for each in train_dataset:
        for i in range(0, len(each)-1,1):
            neural[0][i] = [each[i]]
        forward_pass_output = forward_pass(neural)
        output_array.append([forward_pass_output[0][0], each[-1]]) # [[predicted value, ground truth]]
    MSE_value = MSE(output_array)
    MSE_array.append([MSE_value, neural])
    output_array = []

heapq.heapify(MSE_array)
'''for each in MSE_array:
    print(each[0])'''

while current_iter < num_iter:
    population = []
    for i in range(0, int(elitism), 1): # ovdje primjenjujemo elitizam, dakle cuvamo x najbolje djece
        best_kid = MSE_array[0]
        MSE_array.remove(best_kid) # nakon sto smo izabrali najbolje dijete izbacujemo ga kako ga nebi opet uzeli
        population.append(best_kid[1])
        heapq.heapify(MSE_array)
    while len(population) < pop_size:
        
        parents = []
        for j in range(2):
            #arr = copy.deepcopy(MSE_array)
            parent = selection(MSE_array) #napisat selekciju dvoje djece
            parents.append(parent)
            heapq.heapify(MSE_array)

        for j in range(1, len(parents[0][1]),1): # krecemo od 1 da skippamo ulaznu vrijednost
            for k in range(0, len(parents[0][1][j]), 1):
                for l in range(0, len(parents[0][1][j][k]), 1): # ovdje krizamo i mutiramo tezinu s vjerojatnosti 0.1
                    mutation = np.random.uniform(-(mutation_scale), mutation_scale)
                    mutate = ["yes", "no"]
                    probability = [float(p_m), 1-float(p_m)]
                    chose = np.random.choice(mutate, p=probability)
                    if chose == "yes":
                        parents[0][1][j][k][l] = ((float(parents[0][1][j][k][l]) + float(parents[1][1][j][k][l])) / 2) + mutation
                    elif chose == "no":
                        parents[0][1][j][k][l] = (float(parents[0][1][j][k][l]) + float(parents[1][1][j][k][l])) / 2
        # parents[0] je novo dijete dobiveno krizanjem 

        # dodaj novo dijete u populaciju
        population.append(parents[0][1])
    #MSE_array = []
    for neural in population:
        for each in train_dataset:
            for i in range(0, len(each)-1,1):
                neural[0][i] = [each[i]]
            forward_pass_output = forward_pass(neural)
            output_array.append([forward_pass_output[0][0], each[-1]]) # [[predicted value, ground truth]]
        MSE_value = MSE(output_array)
        MSE_array.append([MSE_value, neural])
        output_array = []
    heapq.heapify(MSE_array)
    current_iter += 1
    if (current_iter % 2000) == 0:
        print("[Train error @",current_iter,"]: ", MSE_array[0][0])

best_neural = MSE_array[0][1]
MSE_array = []
for each in test_dataset:
    for i in range(0, len(each)-1,1):
        best_neural[0][i] = [each[i]]
        forward_pass_output = forward_pass(best_neural)
        output_array.append([forward_pass_output[0][0], each[-1]]) # [[predicted value, ground truth]]
MSE_value = MSE(output_array)
MSE_array.append([MSE_value, best_neural])
output_array = []
print("[Test error]: ", MSE_array[0][0])



