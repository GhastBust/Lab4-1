from const import *
import csv
import os    
from tabulate import tabulate
from decimal import Decimal
from color import green, azure
# from dataclasses import dataclass

def transpose( vec1: list, vec2: list, end: int = -1 ) -> list[list] : 
    
    if end == -1:
        end = len(vec1)
        
    accumulator : list[list] = []
    
    for i in range(end) :
        accumulator.append( [vec1[i], vec2[i]] )
        
    return accumulator
# transpose( vec1, vec2, end )


class myFile:
    
    name: str
    
    meters: int
    quantity: str
    
    delta_t: float
    
    ch1: list[float] = []
    ch2: list[float] = []
    
    def __init__ (
        self,
        name:       str,
        meters:     int,
        quantity:   str,
        delta_t:    float,
        ch1:    list[float],
        ch2:    list[float]
    ) -> None :
        
        self.name = name
        self.meters = meters
        self.quantity = quantity
        self.delta_t = delta_t
        self.ch1 = ch1
        self.ch2 = ch2
        
        return 
    # __init__()
    
    def print( self, lenght: int = 5 ) -> None :
        
        print(
            "name:", azure( self.quantity ), 
            "for", self.meters, "\bm")
        
        # '\x1b[6;30;42m' + 'Success!' + '\x1b[0m'
        # '\x1b[93m' + self.quantity +  '\x1b[93m'
        displ_delta_t = '%.3E' % Decimal(self.delta_t)
        print("delta t:", green(displ_delta_t) )
        
        # print(self.ch1)
          
        print(tabulate(
            transpose(self.ch1, self.ch2, end = lenght), 
            headers=["ch1", "ch2"]
        ))
        
        return 
    # print( lenght ) 
# class myFile


def extract():
    
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