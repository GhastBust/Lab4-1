from const import *
import extract_data
from my_file import myFile
from process_data import fit_for_tau, fit_for_c, fit_for_l
import math
import pprint


def ex1():

    data_files : list[myFile] = extract_data.extract()
    
    # print(data_files)
    
    # y1, y2 = data_files[0].ch1, data_files[0].ch2
    
    results: dict[str, list[tuple[int,float]]] = fit_for_tau(data_files)
    
    pprint.pprint(results)
    
    C_prime = fit_for_c(results["C"], 10_000)
    L_prime = fit_for_l(results["L"], 47)
    
    print(L_prime)
    print(C_prime)
    
    print(math.sqrt(1/L_prime/C_prime))
    
    



if __name__ == "__main__":
    
    ex1()