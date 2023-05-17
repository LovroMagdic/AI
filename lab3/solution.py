import csv
import math

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

def ID3(parent, data, parent_data, header, number):
    max = ["name", 0, []] # koristimo za odredivanje maksimalnog IG
    entropy_list = [] # lista entropija izracunatih za neki header
    ig_small = 0 # zbor entropija jednog headera jednog headera
    ig_big = 0 # konacna informacijska dobit headera
    entropy = 0 # izracunata entropija za jedan header

    yes, no , unkown = 0, 0, 0
    for key in effects:
        if key in header:
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
                entropy = calc_entropy(yes, no)
                entropy_list.append(entropy)
                ig_small += float(entropy) * float((yes+no)/number)
                yes, no, unkown = 0, 0, 0
            #print(entropy_list) # lista svih izracuna entropija za cvorove
            yes, no, unkown = get_yes_no(data)
            ig_big = round(calc_entropy(yes, no) - (ig_small), 3)
        if max[1] <= ig_big:
            max[2] = entropy_list
            max[1] = ig_big
            max[0] = key
        print(ig_big)

        # reset za novi header
        ig_small = 0
        entropy_list = []
        yes, no, unkown = 0, 0, 0
        print("*****")

    #ovdje je nastalo sranje jer treba skuzit kak spremat ak je grana gotova i kak spremit za kasniju predikciju
    # tj treba izgradit stablo nekak
    if max[2] == [0,0] or max[2] == [0,0,0]:
        print(max)
        return 0
    print("najveci ig je >" ,max)
    print()
    
    
    
    for each in effects[max[0]]:
        new_header = []
        #za svaki sunny rainy cloudy pozvat ID3 i racunat sa manjim dataset, valjda
        trans_data = transform_data(data, each)
        for head in header:
            if head != max[0]:
                new_header.append(head)
        print(each)
        ID3(each, trans_data, parent_data, new_header, number)


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

ID3("NULL", rows, rows, header, number)
