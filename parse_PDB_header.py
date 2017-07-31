#!/usr/bin/env python3
__author__ = "Huan Wang"
__version__ = "1.1"


from decimal import Decimal, ROUND_HALF_UP
import numpy as np
import pandas as pd
import os, re, sys, time


items = ["Resolution", "GoodQ", "Median", "BadQ"]
grade = {"Resolution": [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6,
                        1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3,
                        2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0,
                        3.1, 3.2, 3.3, 3.4, 3.5, 4.0],
         "GoodQ":  [0.135, 0.145, 0.155, 0.162, 0.185, 0.190, 0.195,
                    0.200, 0.210, 0.215, 0.220, 0.228, 0.232, 0.238,
                    0.242, 0.245, 0.248, 0.250, 0.255, 0.257, 0.260,
                    0.265, 0.268, 0.270, 0.273, 0.275, 0.280],
         "Median": [0.150, 0.162, 0.175, 0.185, 0.200, 0.210, 0.215,
                    0.220, 0.228, 0.232, 0.240, 0.245, 0.250, 0.254,
                    0.258, 0.265, 0.268, 0.270, 0.273, 0.276, 0.280,
                    0.285, 0.290, 0.295, 0.300, 0.305, 0.310],
         "BadQ":   [0.165, 0.185, 0.195, 0.210, 0.220, 0.228, 0.232,
                    0.235, 0.245, 0.250, 0.260, 0.263, 0.266, 0.272,
                    0.275, 0.280, 0.285, 0.290, 0.293, 0.295, 0.297,
                    0.308, 0.310, 0.315, 0.320, 0.330, 0.350]}
rules = pd.DataFrame(grade, columns=items)


def find_PDB_files(path):
    suffix = ".pdb"
    return (f for f in os.listdir(path) if f.endswith(suffix))

    
def deal_round(number, n):
    ''' Rounded the input number (resolution) to n_th digit decimal. (here 0.1)
    For example：
    1.45 is rounded by the function of deal_round("1.45", 0.1),
    it will return 1.5.

    Pay attention, deal_round(1.45, 0.1) would give wrong result, 1.4!
    
    >>> Decimal(1.45)
    Decimal('1.4499999999999999555910790149937383830547332763671875')
    
    >>> Decimal("1.45")
    Decimal('1.45')
    '''
    # VERY IMPORTANT!
    # Here number is a string. It is better to use string type of number!
    # For example, Decimal instance is created from the string '1.45', 
    # and is converted straight to base-10.
    
    val = Decimal(number)  #### here, number is string type
    acc = str(n)  #### n = 0.1 or 0.01 or 0.001. Here, n = 0.1
    return float(Decimal(val.quantize(Decimal(acc), rounding=ROUND_HALF_UP)))


def calc_resolution_grade(resln):
    resln = float(resln)
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
    '''Note: here resln and R_free are strings '''
    
    if R_free.upper() == "NULL":
        return "NULL"
    
    elif 1.0 <= float(resln) <= 3.5:
        rounded = deal_round(resln, 0.1)

        array = rules[rules.Resolution.values == rounded]
        GoodQ  = array.GoodQ.values[0]
        Median = array.Median.values[0]
        BadQ   = array.BadQ.values[0]
        
        R_free = float(R_free)    
        if R_free <= (GoodQ - 0.02):
            return "MUCH BETTER THAN AVERAGE at this resolution"
    
        elif (GoodQ - 0.02) < R_free <= ((GoodQ + Median) / 2):
            return "BETTER THAN AVERAGE at this resolution"
    
        elif ((GoodQ + Median) / 2) < R_free <= ((Median + BadQ) / 2):
            return "AVERAGE at this resolution"
    
        elif ((Median + BadQ) / 2) < R_free <= (BadQ + 0.02):
            return "WORSE THAN AVERAGE at this resolution"
    
        elif R_free > (BadQ + 0.02):
            return "UNRELIABLE"
    
        else:
            return "Error!"
        
        
def parse_info(filename):
    R_free_list = []
    
    str_FREE_R = r"3\s+FREE R VALUE(\s+|\s+\(.+\)\s+):\s*(\d+\.\d+|NULL)"
    str_B_factor = r"3\s+MEAN B VALUE\s+\(.+:\s+([-+]?\d*\.\d+|NULL)"
    pattern_FREE_R = re.compile(str_FREE_R)
    pattern_B_factor = re.compile(str_B_factor)
    
    method = resln = resln_grade = R_free = R_free_grade = B_value = "NULL"

    with open(filename, 'r') as fo:
        for line in fo:
            #### extracting method information
            if line.startswith("EXPDTA"):
                method = line[8:].strip()
                print("Expt. Method:\t{:}".format(method))

            #### extracting the highest resolution
            if line.startswith("REMARK   2 RESOLUTION."):
                resln = float(re.search(r'[-+]?\d*\.\d+', line).group())
                print("Resolution:\t{:}".format(resln))
                resln_grade = calc_resolution_grade(resln)
                print("Resolution grade:\t{:}".format(resln_grade))
                
            #### dealing with the R_free value and the average B value    
            if line.startswith("REMARK   3"):
                                        
                #### extracting the R_free value
                match_R_free = re.search(pattern_FREE_R, line)
                if match_R_free:
                    value = match_R_free.group(2)
                    print("R_Free value:\t{:}".format(value))
                    
                    R_free_list.append(value)
                    if len(R_free_list) > 1:
                        print("=== The R_Free LIST ===:", R_free_list)
                    
                    R_free = min(R_free_list)

                    R_free_grade = calc_R_free_grade(resln, R_free, rules)
                    print("R_free_grade:\t{:}".format(R_free_grade))
                    
                #### extracting the average B value    
                match_B_val = re.search(pattern_B_factor, line)
                if match_B_val:
                    B_value = match_B_val.group(1)
                    print("Mean B_value:\t{:}".format(B_value))
            
            if line.startswith("ATOM"):
                break
    return (method, resln, resln_grade, R_free, R_free_grade, B_value)


def main():
    pathstr = '\nPlease type the directory contains PDB files: \n'
    path = input(pathstr)

    initial_time = time.time()
    pdbfiles = find_PDB_files(path)

    data          = {}
    PDB_ids       = []
    Expt_Methods  = []
    Resolutions   = []
    Resln_grades  = []
    R_free_values = []
    R_free_grades = []
    Mean_B_values = []
    title = ("PDB_id", "Method", "Resolution", "Resolution Grade",
             "R_free", "R_free Grade", "Mean B_value")

    for i, f in enumerate(pdbfiles):
        start_time = time.time()
        begin = ''.join(("\n", "-" * 50, "\n", "No. {:}, file {:}"))
        print(begin.format(i, f))
        
        Method, Resolution, Resolution_grade, \
        R_free, R_free_grade, B_value = parse_info(f)
        
        step_time = time.time() - start_time
        print("\nTime used in this file: {:.3f} Seconds".format(step_time))

        PDB_ids.append(os.path.splitext(f)[0].upper())
        Expt_Methods.append(Method)
        Resolutions.append(Resolution)
        Resln_grades.append(Resolution_grade)
        R_free_values.append(R_free)
        R_free_grades.append(R_free_grade)
        Mean_B_values.append(B_value)

    df = pd.DataFrame(np.column_stack((PDB_ids,
                                       Expt_Methods,
                                       Resolutions,
                                       Resln_grades,
                                       R_free_values,
                                       R_free_grades,
                                       Mean_B_values)),
                                       columns = title)

    print("The Final Table is \n", df)
    df.to_csv('database.csv', sep=',', index=False)
    
    total_time = time.time() - initial_time
    print("Work Completed. Used Time: {:.3f} Seconds".format(total_time))
    
    
if __name__ == "__main__":
    main()
