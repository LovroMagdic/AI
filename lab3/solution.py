import csv
import math

def predict(header, row, tree, effects):
    arr = ["YES", "NO"]
    decision = str()
    root = tree["root"][0]
    print(root) # weather

    key = "root" + "_" + root # root_weather

    while decision not in arr:
        for value in tree[root]:
            if value in row:
                key = key + "_" + str(value) # root_weather_sunny
                root = key
                decision = (tree[key])[0]
                print(decision)

    print(decision)
    return 0


def transform_data(data,parent):
    new_data = []
    for each in data:
        if each[0] == parent:
            each.remove(each[0])
            new_data.append(each)
    return new_data

def get_yes_no(rows):
    length = len(rows[0]) -1
    yes , no = 0,0
    unkown = 0
    for each in rows:
        if each[length] == "yes":
            yes += 1
        elif each[length] == "no":
            no += 1
        else:
            unkown += 1
    return yes, no, unkown

def calc_entropy(yes, no):
    if yes == 0 or no == 0:
        return 0
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
            #print("ovo je za ", key)
            decision_parent = []
            for each in effects[key]:
                for row in data:
                    if each in row:
                        if "yes" in row:
                            yes += 1
                        elif "no" in row:
                            no += 1
                        else:
                            unkown += 1
                #print(each, "yes >", yes, " no >", no, "unkown >", unkown)
                if yes == 0 or no == 0:
                    if yes > no:
                        decision = "YES"
                    elif no > yes:
                        decision = "NO"
                decision_parent.append([each, decision])

                entropy = calc_entropy(yes, no)
                entropy_list.append(entropy)
                ig_small += float(entropy) * float((yes+no)/number)
                yes, no, unkown = 0, 0, 0
            #print(entropy_list) # lista svih izracuna entropija za cvorove
            yes, no, unkown = get_yes_no(data)
            ig_big = round(calc_entropy(yes, no) - (ig_small), 3)
        
        if max[1] < ig_big:
            max[3] = decision_parent
            max[2] = entropy_list
            max[1] = ig_big
            max[0] = key

        if max[0] == "":
            max[3] = decision_parent
            max[2] = [0,0]
        #print(ig_big)

        # reset za novi header
        ig_small = 0
        entropy_list = []
        yes, no, unkown = 0, 0, 0
        #print("*****")
    #print(max[3])
    if len(tree) == 0:
        tree["root"] = [max[0]]
        tree_node = "root" + "_" + str(max[0])
        #print(tree)
    elif len(tree) != 0:
        tree_node = tree_node + "_" + str(parent)
        tree[tree_node] = [max[0]]
        #print(tree)
    #ovdje je nastalo sranje jer treba skuzit kak spremat ak je grana gotova i kak spremit za kasniju predikciju
    # tj treba izgradit stablo nekak


    if (max[2] == [0,0] or max[2] == [0,0,0]) and max[0] != "":
        tree_node = tree_node + "_" + str(max[0])
        tree[tree_node] = [max[3]]
        for each in max[3]:
            tree_node = tree_node + "_" + str(each[0])
            tree[tree_node] = [each[1]]
        return 0
    #ovo je ako je odma odlucen yes ili no
    if max[0] == "":
        tmp = ((max[3])[0])[1]
        tree[tree_node] = [[tmp]]
        return 0
    
    #ovdje sam izabrao glavni cvor
    


    #print("najveci ig je >" ,max)
    #print()
    

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
        #print("pregledavam efeckt ", each)
        #print()
        ID3(each, trans_data, parent_data, new_header, number, tree_node)


#read csv file
file = open('volleyball.csv')
csvreader = csv.reader(file)
header = []
rows = []
header = next(csvreader)
header.remove(header[-1])
yes, no ,unkown = 0, 0, 0
for row in csvreader:
    rows.append(row)

effects = dict()
for i in range(len(header)):
    effects_list = set()
    for each in rows:
        effects_list.add(each[i])
    effects[header[i]] = effects_list



yes, no, unkown = get_yes_no(rows)
number = yes + no # number of actual data
entropy = calc_entropy(yes, no)

tree = dict()
tree_node = ""
ID3("NULL", rows, rows, header, number, tree_node)


file = open('volleyball.csv')
csvreader = csv.reader(file)
header = []
rows = []
header = next(csvreader)
header.remove(header[-1])
yes, no ,unkown = 0, 0, 0
for row in csvreader:
    rows.append(row)

for row in rows:
    print(row)
    predict(header, row, tree, effects)