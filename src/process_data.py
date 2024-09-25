from my_file import myFile

def processs( data_files: list[myFile] ) -> None :
    
    for file in data_files:
        
        detect_downward_curve(file.ch1)
        
        ...
    
    ...
    
    
def detect_downward_curve( data: list[float] ) -> tuple[int, int] :
    
    accumulate = 0
    stdacc = 0
    llim: int = 0
    rlim: int = 0
    
    for i, datum in enumerate(data):
        
        relative_index = i - llim
        
        # salta l'elemento 0, non posso dividere per zero
        if relative_index == 0:
            continue
        
        # non entro il 10% della media parziale
        if abs(accumulate/relative_index - datum) <= stdacc * 3 / relative_index:
            pass
        
        elif llim == 0 and i > 10:
            accumulate = abs(datum)
            stdacc = abs(datum/10)
            llim = i
            continue
        
        elif rlim == 0 and relative_index > 100:
            rlim = i -1
            break
        
            
        stdacc += abs(accumulate / relative_index - datum)
        accumulate += abs(datum)
    
    return llim, rlim

    
def fit_curve( xs: list[float], ys: list[float], yerrs: float ) :
    
    return (0, 0), (0, 0), (0, 0)
    ...
    
