import pickle

def pickle_save(filename,element):
    with open(filename+'.pkl', 'wb') as file:
       pickle.dump(element, file)

def pickle_load(filename):
    pickle_off = open(filename+".pkl", "rb")
    return pickle.load(pickle_off)

def remove_brac(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret

    


