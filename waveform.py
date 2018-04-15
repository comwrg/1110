import sys
import os

# analyse the argument input.
score_file = None
_character_ = "*"
total_addition = False
names = ['Total']  # save names
for a in sys.argv[1:]:
    if "--total" in a:
        total_addition = True
    elif "--character" in a:
        _character_ = a.split("=")[1][0]
    else:
        score_file = a

if not score_file:
    print("No score file specified.")
    quit()

# analyse score file input, to see if the file exists.
if not os.path.exists(score_file):
    print("Invalid path to score file.")
    quit()

# open the score file
with open(score_file, 'r') as score:
    score_dict = {}
    for line in score.read().splitlines():  # loop every line
        if not line:
            continue
        if line.startswith('|'):  # start with `|`
            replacing = [int(x) for x in line.replace("*", "1").replace("-", "0").replace("|", "")]
            score_dict[now_index].append(replacing)
        else:  # not start with `|`
            # why? for example, names=['Total', 'piano'], now need add `violin`, index of `violin` is len(names), is 2
            # then, add violin to names, names is ['Total', 'piano', 'violin']
            now_index = len(names)
            names.append(line)  # add name to names
            score_dict[now_index] = []
            if not os.path.exists("instruments/" + names[now_index]):  # check if the instrument file name exists.
                print("Unknown source.")
                exit()
# print('score_dict', score_dict)
# The part of converting score file is done.
##############################################################

# start to read instrument file
ins_dict = {}  # a map, key is filename, value is list of lists
for k in score_dict.keys():
    ins_dict[k] = []
    with open("instruments/" + names[k], 'r') as instrument:
        for line in instrument.read().splitlines():  # in the range of the instrument file
            n = line.split("\t")  # delete the tabs between the number and the wave.
            index = int(n[0])  # the number before the wave.
            wave = n[1]  # the wave
            wave_list = []
            for q in wave:
                if ' ' in q:  # append 0 when it comes to spaces
                    wave_list.append(0)
                else:  # append the index number when it comes to non-spaces
                    wave_list.append(index)
            ins_dict[k].append(wave_list)  # append it into a 2d list
# the next step is to add all the numbers in the total_list with the same index, to put them into a brand new list.


def add_colunm(d, t=False):
    """
    calculate sum same column
    :param d: dict
    :param t: total_addition
    :return:  calculated result
    """
    comb_dict = {}
    for k, v in d.items():
        max_size = max(map(len, v))  # get target list size
        # initialize target list to zeros - if nothing target is zero, then this will stay that way
        comb_dict[k] = [0] * max_size
        # add every element in `total_list` to `result`
        for sublist in v:
            for i, x in enumerate(sublist):
                comb_dict[k][i] += sublist[i]  # add element same column
    if t:  # if total_addition is True
        comb_dict[0] = []  # add index zero, why add zero, because variable names[0] is `Total`
        for k, v in comb_dict.items():
            if k is 0:  # if key is zero, continue
                continue
            comb_dict[0].append(v)  # add list to `Total`
        for k in range(1, len(names)):  # only keep comb_dict[0]
            comb_dict.pop(k)

        comb_dict = add_colunm(comb_dict)  # add_column comb_dict[0]
    return comb_dict


# changing the instrument file to numbers is done.
###################################################################

# add_column ins_dict
ins_dict = add_colunm(ins_dict)
# print('ins_dict', ins_dict)

# calculate result dict
result_dict = {}
for k, v in score_dict.items():  # loop score_dict
    result_dict[k] = []
    for p in v:
        index = 0
        result = []
        for s in p:
            if s is 1:
                if index >= len(ins_dict[k]):  # if beyond ins_dict max index, set index zero
                    index = 0
                result.append(ins_dict[k][index])
                index += 1
            elif s is 0:
                index = 0
                result.append(ins_dict[k][index])
        result_dict[k].append(result)

# add_column result_dict
result_dict = add_colunm(result_dict, total_addition)
# print(result_dict)

for k, v in result_dict.items(): # loop result_dict
    line_id = list(reversed(range(min(v), max(v) + 1)))  # to calculate line id, [min element, max element]
    result = {}
    for i in line_id:  # init result
        result[i] = [' '] * len(v)
    prev = v[0]  # init prev
    for i, x in enumerate(v):
        # prev = 1, x = 2, (1, 2]
        # range(prev+1, x+1)
        # prev = 4, x = 1, [1, 4)
        # range(x, prev)
        # to calculate point whether insert or not
        if abs(x - prev) < 2:  # like when x=1, prev=2, not insert point
            p = [x]
        elif prev < x:
            p = range(prev + 1, x + 1)  # if when x=4, prev=1, need insert 2,3,4, so is range(prev+1, x+1)
        elif prev > x:
            p = reversed(range(x, prev))  # if when x=1, prev=4, need insert 1,2,3, so is range(x, prev)

        for j in p:  # loop points
            result[j][i] = _character_  # insert
        prev = x  # to record prev line number
    print(names[k] + ':')  # print name
    for i in line_id:
        print('{: >2d}:\t'.format(i), end='')  # print line id, width is two, so need fill space before number
        print(''.join(result[i]))  # print each line
