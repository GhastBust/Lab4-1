from my_file import myFile
from scipy.optimize import curve_fit
import math
import numpy
from matplotlib import pyplot as plt


def V( 
    t,
    tau,
    A,
    y0 
) -> float :
    
    return A * numpy.exp( t  / tau ) + y0


def rescale( vec: list[float], factor: float) -> list[float] :
    
    for i in range(len(vec)) :
        vec[i] *= factor
        
    return vec


def fit_for_tau( data_files: list[myFile] ) -> dict[str, list[tuple[int, float]]] :
    
    results: dict[str, list] = {"L": [], "C": []}
        
    last_tau = 0.1
    
    A_test = 5
    
    for file in data_files:
        
        if file.quantity == "inductance":
            A_test = -2.25
        
        llim, rlim = detect_downward_curve(file.ch1)
        
        discharge = file.ch2[ llim : rlim ]
        
        time = rescale( list(range(len(discharge))), file.delta_t )
        # print(len(time), len(discharge))
        # print(type(time), type(discharge))
        
        (tau, A, y0), a = curve_fit(
            V,
            numpy.array(time),
            numpy.array(discharge),
            p0 = (last_tau, A_test, 0)
        )
        
        if file.quantity == "capacity":
            results["C"].append((file.meters, tau))
            
        elif file.quantity == "inductance":
            results["L"].append((file.meters, tau))
            
        else :
            raise "boh"
        
                                             
        # print(tau, A, y0)
        last_tau = tau
        
        
    return results

        
    
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

    
    
def fit_for_c( results: list[tuple[int, float]], factor: float ) -> float :

    ls = []
    Cs = []
    
    for l, t in results:
        
        ls.append(l)
        Cs.append(t / factor)
        
    (m, q), a = curve_fit( lambda l, C_prime, C0: l * C_prime + C0, ls, Cs )
    
    return m
    
def fit_for_l(results: list[tuple[int, float]], factor: float ) -> float :
    
    return fit_for_c(results, 1/(factor+50))
    
    