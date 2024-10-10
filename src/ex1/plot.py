from matplotlib import pyplot as plt
import numpy
from matplotlib import colors
import types
from enum import Enum, auto


class quantity(Enum):
    
    L = auto()
    C = auto()


def linear(
    y:  list[float], y_errs: float,
    x:  list[float],
    f: types.FunctionType,
    q: quantity,
):
    y_errs = list(map(lambda x: x*5000000, y_errs))
    y = list(map(lambda x: 1000000*x, y))
    
    err_bar = plt.errorbar(x= x, y= y, yerr= y_errs, fmt= ".")
    err_bar.set_label("Dati empirici")
    
    axes = plt.gca()
    axes.grid(visible= True, which= "both")
      
    
    xaxis = numpy.linspace( max(x), min(x), 100 )
    yaxis = list(map(lambda x: 1000000*x, map(f, xaxis)))
    
    fit_curve = plt.plot(xaxis, yaxis, marker = "")[0]
    fit_curve.set_label("Curva del fit")

    plt.axhline(linewidth = .8, color = "k")
    plt.axvline(linewidth = .8, color = "k")
    
    legend = plt.legend()
    
    legend.set_label("Legenda")
    legend.set_loc("lower right")
    
    # plt.rcParams['text.usetex'] = True
    
    y_label: str
    title_txt: str
    
    if q == quantity.C:
        y_label     = "Capacità del cavo [F]"
        title_txt   = "a Capacità"
        
    elif q == quantity.L:
        y_label     = r"Induttanza del cavo [$\mu$H]"
        title_txt   = r"' Induttanza"
        
        
    else:
        raise "bro"
    
    axes.set_xlabel("Lunghezza del cavo [m]")
    axes.set_ylabel( y_label )
    
    # axes.set_xticks()
    
    title = plt.title("Fit per l" + title_txt, size = 16, weight = "roman")
    
    plt.show()

    