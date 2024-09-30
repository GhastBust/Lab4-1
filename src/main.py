from const import *
import extract_data
from my_file import myFile
from process_data import fit_for_tau, fit_for_c, fit_for_l, get_v_in_medium
import math
import pprint
import myutils


def ex1():

    data_files : list[myFile] = extract_data.extract()
    
    # for file in data_files:
    #     file.print()
    
    # data_files[0].print()
    
    # print(data_files)
    
    # y1, y2 = data_files[0].ch1, data_files[0].ch2
    
    results: dict[str, list[tuple[int, float, float]]] = fit_for_tau(data_files)
    
    # pprint.pprint(results)
    
    C_prime, C_err = fit_for_c(results["C"], 10_000)
    L_prime, L_err = fit_for_l(results["L"], 47)
    
    # print(C_err/C_prime)
    # print(L_err/L_prime)
    
    display_C = myutils.sci_err(C_prime, C_err)
    display_L = myutils.sci_err(L_prime, L_err)
    
    print( "C' =", display_C )
    print( "L' =", display_L )
    
    v, v_err = get_v_in_medium(C_prime, C_err, L_prime, L_err)
    display_v = myutils.sci_err(v, v_err)
    
    print( "v  =", display_v )
    
    
    
    
    
def ex2() :
    pass
    


if __name__ == "__main__":
    
    ex1()
    # ex2()