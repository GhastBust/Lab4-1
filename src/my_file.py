from tabulate import tabulate
from decimal import Decimal
from color import green, azure, red


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
    err: float = []
    
    def __init__ (
        self,
        name:       str,
        meters:     int,
        quantity:   str,
        delta_t:    float,
        ch1:    list[float],
        ch2:    list[float],
        err:        float
    ) -> None :
        
        self.name = name
        self.meters = meters
        self.quantity = quantity
        self.delta_t = delta_t
        self.ch1 = ch1
        self.ch2 = ch2
        self.err = err
        
        return 
    # __init__()
    
    def print( self, lenght: int = 5 ) -> None :
        
        print(
            "name:", azure( self.quantity ), 
            "for", self.meters, "\bm")
        
        # '\x1b[6;30;42m' + 'Success!' + '\x1b[0m'
        # '\x1b[93m' + self.quantity +  '\x1b[93m'
        displ_delta_t   = '%.3E' % Decimal(self.delta_t)
        displ_err       = '%.1E' % Decimal(self.err)
        
          
        print(
            "delta t:", green(displ_delta_t),
            "with err:", red("±" + displ_err) 
        )
        print(tabulate(
            transpose(self.ch1, self.ch2, end = lenght), 
            headers=["ch1", "ch2"]
        ))
        
        return 
    # print( lenght ) 
# class myFile
