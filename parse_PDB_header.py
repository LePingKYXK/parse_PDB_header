#!/usr/bin/env python3
__author__ = "Huan Wang"
__version__ = "1.0.0"

import pandas as pd
import os, re, sys, time


items = ["Resolution", "GoodQ", "Median", "BadQ"]
grade = {"Resolution": [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
		     "GoodQ":[0.135, 0.145, 0.155, 0.162, 0.185, 0.19, 0.195, 0.2, 0.21, 0.215, 0.22],
		     "Median":[0.15, 0.162, 0.175, 0.185, 0.2 , 0.21, 0.215, 0.22, 0.228, 0.232, 0.24],
		     "BadQ":[0.165, 0.185, 0.195, 0.21, 0.22, 0.228, 0.232, 0.235, 0.245, 0.25, 0.26]}
rule = pd.DataFrame(grade, columns=items)


def find_PDB_files(path):
    suffix = ".pdb"
    files = np.asarray([f for f in os.listdir(path) if f.endswith(suffix)])
    return np.sort(files)
    
    
def calc_resolution_grade(resln):
    if resln < 1.6:
        return "EXCELLENT"
    elif 1.6 <= resln <= 1.79:
        return "EXCELLENT/VERY GOOD"
    elif 1.8 <= resln <= 1.99:
        return "VERY GOOD"
    elif 2.0 <= resln <= 2.29:
        return "VERY GOOD/GOOD"
    elif 2.3 <= resln <= 2.59:
        return "GOOD"
    elif 2.6 <= resln <= 2.89:
        return "GOOD/FAIR"
    elif 2.9 <= resln <= 3.19:
        return "FAIR"
    elif 3.2 <= resln <= 3.49:
        return "FAIR/POOR"
    elif resln >= 3.5:
        return "POOR"
        
        
def calc_R_free_grade(resln, R_free, rules):
    resln = round(resln, 1)
    R_free = float(R_free)
    print("Resolution Decimal", resln)
    array = rules[rules.Resolution.values == resln]
    print("Current Line in rules", array)
    print("R_free", R_free, type(R_free))
    GoodQ  = array.GoodQ.values[0]
    print("Type of GoodQ:", type(GoodQ))
    Median = array.Median.values[0]
    BadQ   = array.BadQ.values[0]
    
    if R_free <= (GoodQ - 0.02):
        return "MUCH BETTER THAN AVERAGE at this resolution"
    elif GoodQ < R_free <= ((GoodQ + Median) / 2):
        return "BETTER THAN AVERAGE at this resolution"
    elif R_free <= ((GoodQ + BadQ) / 2):
        return "AVERAGE at this resolution"
    elif R_free <= (BadQ + 0.02):
        return "WORSE THAN AVERAGE at this resolution"
    elif R_free > (BadQ + 0.02):
        return "UNRELIABLE"
    else:
        return None
        
        
def parse_info(filename):
    with open(filename, 'r') as fo:
        
        for line in fo:
            #### extracting method information
            if line.startswith("EXPDTA"):
                method = line[8:].strip()

            #### extracting the highest resolution
            if line.startswith("REMARK   2 RESOLUTION.") and method[:5] == "X-RAY":
                resln = float(re.search(r'[-+]?\d*\.\d+'.strip(), line).group())
                print("Resolution", resln)
                resln_grade = Resolution_grade(round(float(resln), 2))
                print(resln_grade)
                
            if line.startswith("REMARK   3"):
                #### extracting the R_free value
                if re.search(r'.3\s+FREE R VALUE\s+:', line):
                    R_free = re.search(r'[-+]?\d*\.\d+|NULL', line).group()
                    print("R_free:", R_free, type(R_free))
                    grade = R_free_grade(resln, R_free, rules)
                    print(grade)
                    
                #### extracting the average B value    
                if re.search(r'MEAN B VALUE\s+\(.+', line):
                    B_value = re.search(r'[-+]?\d*\.\d+|NULL', line).group()
                    print("Mean B_value:", B_value)
    return (method, resln, R_free, B_value)


def main():
    pathstr = '\nPlease type the directory contains PDB files: \n'

    initial_time = time.time()
    path = input(pathstr)
    pdbfiles = find_PDB_files(path)
    print(pdbfiles, '\n')

    PDB_ids       = []
    Expt_Methods  = []
    Resolutions   = []
    R_free_values = []
    Mean_B_values = []
    title = ["PDB_id", "Method", "Resolution", "B_value", "R_free"]

    for i, f in enumerate(pdbfiles):
        start_time = time.time()
        begin = ''.join(("\n", "-" * 50, "\n", "No. {:}, file {:}"))
        print(begin.format(i, f))
        Method, Resolution, R_free, B_value = parse_info(f)

        PDB_ids.append(f)
        Expt_Methods.append(Method)
        Resolutions.append(Resolution)
        Mean_B_values.append(B_value)
        R_free_values.append(R_free)

    data = np.array((PDB_ids,
                     Expt_Methods,
                     Resolutions,
                     Mean_B_values,
                     R_free_values,)).T

    df = pd.DataFrame(data, columns = title)
    df.replace("NULL", np.nan, inplace=True)
    print("DataFrame:\n",df, df.dropna())
    
    
    
    
if __name__ == "__main__":
    main()
