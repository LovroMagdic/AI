import csv
import math

def predict(header, row, tree, result_1,result_2,result_3 ):
    tmp = []
    typ1 = type(tmp)
    arr = [result_1, result_2, result_3]
    decision = "“"
    root = tree["root"][0]
    #print(root) # weather

    key = "root" + "_" + root # root_weather

    while decision not in arr:
        for value in tree[key]:
            typ = type(value)
            if typ == typ1:
                for each in value:
                    tmp.append(each[0])
                for value in tmp:
                    if value in row:
                        key = key + "_" + str(value) # root_weather_sunny
                        root = key
                        decision = (tree[key])[0]
                        #print(decision)
                    elif value in header:
                        key = key + "_" + str(value) # root_weather_sunny
                        root = key
                        decision = (tree[key])[0]
                        #print(decision)
            elif value in row:
                key = key + "_" + str(value) # root_weather_sunny
                root = key
                decision = (tree[key])[0]
                #print(decision)
            elif value in header:
                key = key + "_" + str(value) # root_weather_sunny
                root = key
                decision = (tree[key])[0]
                #print(decision)

    #print(decision)
    return decision


def transform_data(data,parent):
    #print("ovo je trans_data za ",parent)
    new_data = []
    for each in data:
        if parent in each:
            each.remove(parent)
            new_data.append(each)
    return new_data

def get_yes_no(rows, result_1, result_2, result_3):
    length = len(rows[0]) -1
    yes , no, unkown = 0, 0, 0
    for each in rows:
        if each[length] == result_1:
            yes += 1
        elif each[length] == result_2:
            no += 1
        elif each[length] == result_3:
            unkown += 1
    return yes, no, unkown

def calc_entropy(yes, no, unkown, result_3):
    if (yes == 0 or no == 0 or unkown == 0) and result_3 != "":
        return 0
    elif yes == 0 or no == 0:
        return 0
    if result_3 != "":
        result = ((-yes/(yes+no+unkown))*math.log2(yes/(yes+no+unkown)) + (-no/(yes+no+unkown))*math.log2(no/(yes+no+unkown)) + (-unkown/(yes+no+unkown))*math.log2(unkown/(yes+no+unkown)))
    else:
        result = ((-yes/(yes+no))*math.log2(yes/(yes+no)) + (-no/(yes+no))*math.log2(no/(yes+no)))
    result = round(result, 3)
    return result

def ID3(parent, data, parent_data, header, number, tree_node):
    decision_parent = []
    
    max = ["", 0, [], []] # koristimo za odredivanje maksimalnog IG
    entropy_list = [] # lista entropija izracunatih za neki header
    ig_small = 0 # zbor entropija jednog headera jednog headera
    ig_big = 0 # konacna informacijska dobit headera
    entropy = 0 # izracunata entropija za jedan header
    decision = str()

    yes, no , unkown = 0, 0, 0
    for key in effects:
        if key in header:
            print("ovo je za ", key)
            decision_parent = []
            for each in effects[key]:
                for row in data:
                    if each in row:
                        if result_1 in row:
                            yes += 1
                        elif result_2 in row:
                            no += 1
                        elif result_3 in row:
                            unkown += 1
                print(each, "yes >", yes, " no >", no, "unkown >", unkown)
                if (yes == 0 or no == 0 or unkown == 0) and result_3 != "":
                    if yes > no and yes > unkown:
                        decision = result_1
                    elif no > yes and no > unkown:
                        decision = result_2
                    elif unkown > no and unkown > yes:
                        decision  = result_3

                elif (yes == 0 or no == 0) and result_3 == "":
                    if yes > no and yes > unkown:
                        decision = result_1
                    elif no > yes and no > unkown:
                        decision = result_2
                decision_parent.append([each, decision])

                entropy = calc_entropy(yes, no, unkown, result_3)
                entropy_list.append(entropy)
                ig_small += float(entropy) * float((yes+no+unkown)/number)
                yes, no, unkown = 0, 0, 0
            print(entropy_list) # lista svih izracuna entropija za cvorove
            yes, no, unkown = get_yes_no(data, result_1, result_2, result_3)
            ig_big = round(calc_entropy(yes, no, unkown, result_3) - (ig_small), 3)
        
        if max[1] < ig_big:
            max[3] = decision_parent
            max[2] = entropy_list
            max[1] = ig_big
            max[0] = key

        if max[0] == "":
            max[3] = decision_parent
            max[2] = [0,0]
        print(ig_big)

        # reset za novi header
        ig_small = 0
        entropy_list = []
        yes, no, unkown = 0, 0, 0
        print("*****")
    #print(max[3])
    if len(tree) == 0:
        tree["root"] = [max[0]]
        tree_node = "root" + "_" + str(max[0])
        print(tree)
    elif len(tree) != 0:
        tree_node = tree_node + "_" + str(parent)
        tree[tree_node] = [max[0]]
        print(tree)
    

    if (max[2] == [0,0] or max[2] == [0,0,0]) and max[0] != "" and parent != "NULL":
        tree_node = tree_node + "_" + str(max[0])
        tree[tree_node] = [max[3]]
        
        for each in max[3]:
            #print("tu sam dodao nes")
            tree_node_tmp = tree_node + "_" + str(each[0])
            tree[tree_node_tmp] = [each[1]]
        #print(tree)
        return 0
    #ovo je ako je odma odlucen yes ili no
    if max[0] == "":
        tmp = ((max[3])[0])[1]
        tree[tree_node] = [tmp]
        return 0

    #ovdje sam izabrao glavni cvo
    print("najveci ig je >" ,max)
    print()
    tree[tree_node] = list(effects[max[0]])
    #print(tree)
    for each in effects[max[0]]:
        new_header = []
        #za svaki sunny rainy cloudy pozvat ID3 i racunat sa manjim dataset, valjda
        trans_data = transform_data(data, each)
        #print(trans_data)
        for head in header:
            if head != max[0]:
                new_header.append(head)
        #print()
        print("pregledavam efekt ", each)
        #print(trans_data)
        #print()
        ID3(each, trans_data, parent_data, new_header, number, tree_node)




#ovo je MAIN PROGRAM
#read csv file
file = open('logic_small.csv')
csvreader = csv.reader(file)
header = []
rows = []
header = next(csvreader)
#header.remove(header[-1])
yes, no ,unkown = 0, 0, 0
for row in csvreader:
    rows.append(row)

effects = dict()
for i in range(len(header)):
    effects_list = set()
    for each in rows:
        effects_list.add(each[i])
    effects[header[i]] = effects_list

result_1 = list(effects[header[-1]])[0]
result_2 = list(effects[header[-1]])[1]
result_3 = ""
if len(effects[header[-1]]) > 2:
    result_3 = list(effects[header[-1]])[2]


trash = header[-1]
del effects[trash]


yes, no, unkown = get_yes_no(rows, result_1, result_2, result_3)
number = yes + no + unkown # number of actual data
entropy = calc_entropy(yes, no, unkown, result_3)

tree = dict()
tree_node = ""
ID3("NULL", rows, rows, header, number, tree_node)
print(tree)

# here starts prediction method
file = open('logic_small_test.csv')
csvreader = csv.reader(file)
header = []
rows = []
header = next(csvreader)
header.remove(header[-1])
yes, no ,unkown = 0, 0, 0
for row in csvreader:
    rows.append(row)
prediction_list = []

for row in rows:
    prediction = predict(header, row, tree, result_1, result_2, result_3)
    prediction_list.append(prediction.lower())

print(prediction_list)
