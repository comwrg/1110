import os
import sys


# merge row
def merge(data, total=False):
    merge_results = {}
    for k, v in data.items():
        merge_results[k] = [0] * max(map(len, v))
        for item in v:
            for i in range(len(item)):
                merge_results[k][i] += item[i]
    # handle total, if total is True, merge all
    if total:
        total_result = []
        for v in merge_results.values():
            total_result.append(v)
        merge_results = merge({0: total_result})
    return merge_results


file = None
total_flag = False
flag = "*"

# handle input args
if len(sys.argv) < 2:
    print("No score file specified.")
    exit()
for a in sys.argv[1:]:
    if "--character=" in a:
        flag = a.split("=")[-1]
    elif "--total" in a:
        total_flag = True
    else:
        file = a
if file is None:
    print("No score file specified.")
    exit()
if not os.path.exists(file):
    print("Invalid path to score file.")
    exit()
"""
we define name first
piano                   # ins_file_name
|*************---|      # noise
"""
# define a list to save instruments filename appear in input file
ins_files_names = ['Total']
noises = {}
# analysis input file
with open(file, "r") as open_file:
    read_lines = open_file.read().splitlines()
for b in read_lines:
    if "|" not in b:
        index = len(ins_files_names)
        ins_files_names.append(b)
        noises[index] = []
        if not os.path.exists("instruments/" + b):
            print("Unknown source.")
            exit()
    else:
        ins_replace = [int(flag) for flag in b.replace("|", "").replace("*", "1").replace("-", "0")]
        noises[index].append(ins_replace)

# analysis instruments files
waves = {}
for k in noises.keys():
    waves[k] = []
    for c in open("instruments/" + ins_files_names[k], 'r').read().splitlines():
        replace_list = []
        n = c.split("\t")
        for q in n[1]:
            if " " in q:
                replace_list.append(0)
            else:
                replace_list.append(int(n[0]))
        waves[k].append(replace_list)

# merge row
waves = merge(waves)

# conversion, reference docs
results = {}
for k, v in noises.items():
    results[k] = []
    for item in v:
        index = 0
        r = []
        for p in item:
            if p is 0:
                index = 0
                r.append(waves[k][index])
            else:
                if index >= len(waves[k]):
                    index = 0
                r.append(waves[k][index])
                index += 1
        results[k].append(r)

# mark point and print answer
for k, v in merge(results, total_flag).items():
    # handle line number
    line_number_list = list(reversed(range(min(v), max(v)+1)))
    outputs = {}
    for i in line_number_list:
        outputs[i] = [" "] * len(v)
    prev = v[0]
    # mark point
    for i, p in enumerate(v):
        if abs(p - prev) < 2:
            outputs[p][i] = flag
        elif prev < p:
            for j in range(prev+1, p+1):
                outputs[j][i] = flag
        elif prev > p:
            for j in range(p, prev):
                outputs[j][i] = flag
        prev = p
    # print answer
    print(ins_files_names[k] + ":")
    for i in line_number_list:
        print("{: >2d}:\t".format(i), end="")
        print("".join(outputs[i]))




