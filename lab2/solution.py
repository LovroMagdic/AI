import sys

def redundant(premise, result):
    remove = []
    add = True

    for literal in result:
        if len(result) == 1:
            for each in premise:
                if literal in each:
                    remove.append(each)
            for each in remove:
                premise.remove(each)
            return premise, add
        elif len(result) > 1:
            for each in premise:
                if literal in each and len(each) == 1:
                    add = False
                    return premise, add
    return premise, add

def revert():
    file = open(sys.argv[2],"r", encoding='utf-8').readlines()
    #file = open("cooking_coffee.txt", "r").readlines()

    file = [x.strip() for x in file]
    f = []
    for each in file:
        each = each.lower()
        f.append(each)
    for each in f:
        if each.startswith("#"):
            f.remove(each)
    premise = []
    for each in f:   
        each = each.split(" v ")
        premise.append(each)
    return premise

def cook():
    return 0

def reverse(line):
    wait = []
    path = []

    path.append(["NIL"])
    for each in line.get(''):
        wait.append(each)
    path.append(line.get(''))
    
    while wait:
        key = wait[0]
        key = " v ".join(key)
        ap = line.get(key)
        
        if ap != None:
            for each in ap:
                wait.append(each)
            path.append(ap)
        wait.remove(wait[0])

    path = path[::-1]

    for group in path:
        if group != ["NIL"]:
            str1 = " V ".join(group[0])
            str2 = " V ".join(group[1])
            print(str1, " ", str2)
        else:
            print(group[0])
    return path

def negate(goal):
    res = []
    for each in goal:
        if "~" not in each:
            each = str("~" + each)
        elif "~" in each:
            each = each.replace("~", "")
        res.append(each)
    return res

def negate_clause(string):
    res = []
    if "~" in string:
        tmp = string.replace("~", "")
    else:
        tmp = "~" + string
    res.append(tmp)
    return res

def resolve(list1, list2, resolvent):
    rem = []
    duplicate = []
    l = []
    counter = 0
    flag = True
    res = negate(list1)

    if flag:

        for each in list1:
            if each == resolvent:
                if "~" in each:
                    red = each.replace("~", "")
                    each = each.replace("~", "")
                else:
                    red = "~" + each
                    each = "~" + each
            l.append(each)
        for each in list2:
            if each in l and each == red:
                l.remove(each)
            else:
                l.append(each)

        l = list(dict.fromkeys(l))
        #tautology
        for each in l:
            if "~" in each:
                neg = each.replace("~", "")
                if neg in l:
                    rem.append(each)
            elif "~" not in each:
                neg = "~" + each
                if neg in l:
                    rem.append(each)
        if rem:
            return False, rem
        else:
           return True, l
    else:
        return False, rem

def checkNIL(clause):

    for each in clause:
        tmp = negate(each)
        if tmp in clause:
            return True
    return False

def all(clause, premise):
    line = dict()
    result = []
    flag = True
    cnt = 0
    for c in clause:
        for i in range(len(c)):
            tmp = negate_clause(c[i])
            for p in premise:
                if tmp[0] in p:
                    flag, result = resolve(c, p, c[i])
                    if flag:
                        if (result not in clause) and (result not in premise):
                            premise, add = redundant(premise, result)
                            if add:
                                clause.append(result)
                                premise.append(result)
                                key = " v ".join(result)
                                line[key] = [c] + [p]

                end = checkNIL(clause)
                if end:
                    break
            final = " V ".join(destination)
            if end:
                if '' not in line:
                    line['']= [c] + [p]
                reverse(line)
                print("[CONCLUSION]:",final,"is true")
                return 0
    print("[CONCLUSION]:",final,"is unknown")
    return 0

if sys.argv[1] == "resolution":
    file = open(sys.argv[2],"r", encoding='utf-8').readlines()
    #file = open("resolution_coffee.txt", "r").readlines()
    file = [x.strip() for x in file]
    f = []

    for each in file:
        each = each.lower()
        f.append(each)

    for each in f:
        if each.startswith("#"):
            f.remove(each)

    goal = f.pop().split(" v ")
    destination = goal
    goal = negate(goal)

    premise = []
    clause = []

    for each in f:   
        each = each.split(" v ")
        premise.append(each)
    for each in goal:  
        each = each.split(" v ")
        clause.append(each)

    all(clause, premise)

elif sys.argv[1] == "cooking1":
    file = open(sys.argv[2],"r", encoding='utf-8').readlines()
    input = open(sys.argv[3],"r", encoding='utf-8').readlines()

    #file = open("cooking_coffee.txt", "r").readlines()
    #input = open("cooking_coffee_input.txt", "r").readlines()

    file = [x.strip() for x in file]
    f = []
    for each in file:
        each = each.lower()
        f.append(each)
    for each in f:
        if each.startswith("#"):
            f.remove(each)
    premise = []
    for each in f:   
        each = each.split(" v ")
        premise.append(each)

    dont = revert()

    
    input = [x.strip() for x in input]
    user = []
    for each in input:
        each = each.lower()
        user.append(each)

    #user = ['water ?', 'hot_water ?', 'coffee ?', 'Heater -', 'Heater +']

    for each in user:
        clause = []
        if "?" in each:
            each = each.replace(" ?", "")
            each = each.split(" V ")
            destination = each
            each = negate(each)
            clause.append(each)
            
            premise = []
            for each in dont:
                premise.append(each)
            all(clause, premise)
        elif "-" in each:
            each = each.replace(" -", "")
            each = each.lower()
            each = each.split(" V ")

            dont.remove(each)
            print("user removed > ", each[0])
        elif "+" in each:
            each = each.replace(" +", "")
            each = each.lower()
            each = each.split(" V ")

            dont.append(each)
            print("user added > ", each[0])

elif sys.argv[1] == "cooking":
    cook()

