import sys
import time

# [['water'], ['heater'], ['coffee_powder'], ['~water', '~heater', 'hot_water'], ['~coffee_powder', '~hot_water', 'coffee']]

# [['~coffee', '~lovro']]  

def main(clause, premise):
    for pre in premise: # ['~coffee', '~lovro']
        if ["NIL"] in premise:
            return 0
        new_knowledge = [] # ovo polje sadrzi novo znanje koje smo dobili
        negative_premise = negative(pre) # ['coffee', 'lovro']
        
        for cla in clause: # ['~coffee_powder', '~hot_water', 'coffee']
            helper = [] # ovo polje koristim da skupim sve zajedno premise i klauzule u jedno polje i onda dajem u funkciju resolve koja vraca rjesenje
            helper.append(pre) # dodajem premise
            if negative_premise in cla:
                for each in cla:
                    helper.append(each) # dodajem klauzule

                if helper != pre: # ako je drugaciji znaci da sadrze nesto zajednicko
                    print("ovo je premisa", pre)
                    print("ovo je formula", helper) # ['~coffee', '~lovro', '~coffee_powder', '~hot_water', 'coffee'] ovo dajemo u resolve funkciju, ocekujemo da nam vrati ['~lovro', '~coffee_powder', '~hot_water']
                                # takoder ocekujemo ako imamo [~lovro, ~ime, kava, lovro, ime] da vrati [kava] odnosno da ponisti sve kaj moze
                    new_knowledge = resolve(helper)
                    if new_knowledge == ["NIL"]:
                        print("Dosli smo do NIL!")
                    print("ovo je rjesenje formule", new_knowledge) # ['~coffee_powder', '~hot_water']
                    print("******************")

                    if new_knowledge not in clause and new_knowledge not in premise:
                        premise.append(new_knowledge)
                
def resolve(formula):
    temp = formula
    for each in formula:
        also_remove = each # također treba maknut i ~coffee i coffee, a ne samo coffee
        if "~" in each:
            each = each.replace("~", "")
        elif "~" not in each:
            each = str("~" + each)
        
        if each in formula:
            temp.remove(each)
            temp.remove(also_remove)
            #print(each, temp) # ovo odkomentiraj ako zelis vidjet kako je rjesio

    
    temp = list(dict.fromkeys(temp))

    if len(temp) == 0:
        temp = ["NIL"]
    return temp

def negative(arr):
    tmp = []
    for each in arr:
        if "~" in each:
            each = each.replace("~", "")
            tmp.append(each)
        elif "~" not in each:
            each = str("~" + each)
            tmp.append(each)
    return tmp



















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

def resolve1(list1, list2, resolvent):
    rem = []
    duplicate = []
    l = []
    counter = 0
    flag = True
    res = negate(list1)
    '''
    for each in res:
        if each in list2:
            counter += 1
    if counter == len(res):
        flag = True
    else:
        flag = False

    if flag == False:
        for each in list2:
            if each in list1:
                counter += 1
        if counter == len(list2):
            flag = True
        else:
            flag = False
    '''

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
        '''
        for each in list1:
            if "~" in each:
                each = each.replace("~", "")
            else:
                each = "~" + each
            l.append(each)
        for each in list2:
            if each in l:
                duplicate.append(each)
                l.remove(each)
            else:
                l.append(each)
        '''
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
            #print(clause)
            #print("NIL za ", tmp)
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
                    #print("rjesavamo za",c[i])
                    #print(c)
                    #print(p)
                    flag, result = resolve(c, p, c[i])
                    #print(result)
                    #print(flag)
                    #print("*************")
                    if flag:
                        if (result not in clause) and (result not in premise):
                            clause.append(result)
                            premise.append(result)
                            key = " v ".join(result)
                            line[key] = [c] + [p]
                    #print(line)
                end = checkNIL(clause)
                if end:
                    break
            final = " V ".join(destination)
            if end:
                if '' not in line:
                    line['']= [c] + [p]
                #print(line)
                reverse(line)
                print("[CONCLUSION]:",final,"is true")
                return 0
    print("[CONCLUSION]:",final,"is unknown")
    return 0

'''
if sys.argv[1] == "resolution1":
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
    #print(goal)
    #print(goal)
    #g = " v ".join(goal)
    #goal = []
    #goal.append(g)

    premise = []
    clause = []

    for each in f:   
        each = each.split(" v ")
        premise.append(each)
    for each in goal:  
        each = each.split(" v ")
        clause.append(each)
    #print(clause)

    all(clause, premise)
    ''''''
        line = dict()
        result = []
        flag = True
        cnt = 0
        for c in clause:
            for i in range(len(c)):
                tmp = negate_clause(c[i])
                for p in premise:
                    if tmp[0] in p:
                        #print("rjesavamo za",c[i])
                        #print(c)
                        #print(p)
                        flag, result = resolve(c, p, c[i])
                        #print(result)
                        #print(flag)
                        #print("*************")
                        if flag:
                            if (result not in clause) and (result not in premise):
                                clause.append(result)
                                premise.append(result)
                                key = " v ".join(result)
                                line[key] = [c] + [p]
                        #print(line)
                    end = checkNIL(clause)
                    if end:
                        break
                final = " V ".join(destination)
                if end:
                    if '' not in line:
                        line['']= [c] + [p]
                    #print(line)
                    #reverse(line)
                    print("[CONCLUSION]:",final,"is true")
                    exit()
        print("[CONCLUSION]:",final,"is unknown")'''
'''
elif sys.argv[1] == "cooking":

    start = time.time()
    end = time.time()
    print(end - start)
    #file_recept = open(sys.argv[2],"r", encoding='utf-8').readlines()
    #file_input = open(sys.argv[3],"r", encoding='utf-8').readlines()

    file_recept = open("cooking_chicken_alfredo.txt", "r").readlines()
    file_input = open("cooking_chicken_alfredo_input.txt", "r").readlines()

    file_recept = [x.strip() for x in file_recept]
    f_recept = []

    for each in file_recept:
        each = each.lower()
        if "#" not in each:
            f_recept.append(each)

    file_input = [x.strip() for x in file_input]
    f_input = []

    for each in file_input:
        each = each.lower()
        if "#" not in each:
            f_input.append(each)

    #print(f_recept) # polje sa svime kaj imam i receptima
    #print(f_input)  #polje sa novim naredbama
    #print("*************")
    i = 0
    for inp in f_input:
        start = time.time()
        
        i+=1
        if "?" in inp:
            
            inp = inp.replace(" ?", "")
            goal = inp.split(" v ")
            destination = goal
            goal = negate(goal)
            #print(goal)
            #print(goal)
            #g = " v ".join(goal)
            #goal = []
            #goal.append(g)

            premise = []
            clause = []

            for each in f_recept:   
                each = each.split(" v ")
                premise.append(each)
            for each in goal:  
                each = each.split(" v ")
                clause.append(each)

            #print(premise)

            #print(clause)
            #print("solving for > ", goal)
            all(clause, premise)
            #print("****************************")
            end = time.time()
            print(end - start)
        elif " -" in inp:
            #zelimo izbaciti kaj god user zeli direkt iz recepta ne iz premisa jer premise se ucitavaju ispocetka sza svaki upit
            #print("izbacujemo >", inp)
            #print(f_recept)
            inp = inp.replace(" -", "").lower()

            f_recept.remove(inp) # iz recepta izbacujemo 'heater'

            #print(f_recept)
            #print("****************************")
        elif " +" in inp:
            #zelimo dodati kaj god user zeli direkt iz recepta ne iz premisa jer premise se ucitavaju ispocetka za svaki upit
            #print("dodajemo >", inp)
            #print(f_recept)
            inp = inp.replace(" +", "").lower()

            f_recept.append(inp) # iz recepta dodajemo 'heater'

            #print(f_recept)
            #print("****************************")
'''
start = 1
#if sys.argv[1] == "resolution":
if start:
    #file_recept = open(sys.argv[2],"r", encoding='utf-8').readlines()
    
    file_recept = open("resolution_coffee_or_tea.txt", "r").readlines()

    file_recept = [x.strip() for x in file_recept]
    f_recept = []

    for each in file_recept:
        each = each.lower()
        if "#" not in each:
            f_recept.append(each)

    premise = [] # polje premisa sadrzi recept odnosno svo znanje koje imamo zadano
    clause = [] # u polju klauza je cilj ono sto zelimo dokazati i tu bi trebali dodavati svo novo znanje koje pronademo a koje nije u premisama

    goal = f_recept.pop().split(" v ") # ako ciljno stanje cini vise atoma treba ih rastavit
    goal_print = (" v ".join(goal))
    goal = negative(goal) # ciljno stanje negiramo i dodajemo u premise polje
    for each in goal:
        premise.append(each)

    for each in f_recept:
        clause.append(each.split(" v ")) # recept dodajemo u klauzule u obliku [sastojak], [sastojak1, sastojak2]
    
    #print(clause) # [['water'], ['heater'], ['coffee_powder'], ['~water', '~heater', 'hot_water'], ['~coffee_powder', '~hot_water', 'coffee']]
    #print()
    #print(premise) # [['~coffee']]
    state = main(clause, premise)

    if state == 0:
        print("[CONCLUSION]:",goal_print, "is true.")
    else:
        print("[CONCLUSION]:",goal_print, "is not true.")



















#python solution.py cooking cooking_chicken_alfredo.txt cooking_chicken_alfredo_input.txt

#python solution.py resolution resolution_coffee_or_tea.txt