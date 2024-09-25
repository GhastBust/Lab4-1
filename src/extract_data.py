from const import *
import csv
import os
from my_file import myFile


def extract() -> list[myFile] :
    
    listdir = os.listdir(DATA_PATH)
    
    files: list[myFile] = []
    
    for file in listdir:
        
        with open(os.path.join(DATA_PATH, file)) as csvfile :
            
            reader = csv.reader(csvfile)
            
            i = 0
            more_than_one_row  = False
            more_than_two_rows = False
            t0      : float = 0
            delta_t : float = 0
            ch1 = []
            ch2 = []
            
            for row in reader:

                i += 1
                
                if i <= 2:
                    continue
                
                if more_than_one_row == False:
                    more_than_one_row = True
                    t0 = float(row[0])
                    
                elif more_than_two_rows == False:
                    more_than_two_rows = True
                    delta_t = float(row[0]) - t0                      

                try:
                    ch1.append(float(row[1]))
                    ch2.append(float(row[2]))
                    
                except ValueError:
                    continue
                
            pass # close file.row    
        pass # close file
                
        name = file.split(sep = ".")[0]
        
        name_comp = name.split(sep = "_")
        
        quantity = name_comp[0]
        meters = int(name_comp[1].removesuffix("m"))
             
        files.append(myFile(file, meters, quantity, delta_t, ch1, ch2))
    pass # close loop in dir
    
    return files 
# extraxt()
    

def test() -> None : 

    files = extract()

    for file in files:
        
        file.print()
        print()
        
    return 
# test()


if __name__ == "__main__":
    test()