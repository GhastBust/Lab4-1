from matplotlib import pyplot as plt
import numpy
from matplotlib import colors
import types


def gamma_vs_V(
    gamma:  list[float], gamma_err: float,
    volt:   list[float],
    lenght: types.FunctionType
):
    
    gamma_err = list(map(lambda x: x*20, gamma_err))
    
    err_bar = plt.errorbar(x= volt, y= gamma, yerr= gamma_err, fmt= ".")
    err_bar.set_label("Dati empirici")
    
    axes = plt.gca()
    axes.grid(visible= True, which= "both")
    
    xlim = list(axes.get_xlim())
    
    ylim = list(axes.get_ylim())
    
    # xaxis = lines.Line2D(xdata= )    
    
    xaxis = numpy.linspace( max(volt), min(volt), 100 )
    yaxis = list(map(lenght, xaxis))
    
    fit_curve = plt.plot(xaxis, yaxis, marker = "")[0]
    fit_curve.set_label("Curva del fit")

    plt.axhline(linewidth = .8, color = "k")
    plt.axvline(linewidth = .8, color = "k")
    
    legend = plt.legend()
    
    legend.set_label("Legenda")
    legend.set_loc("lower right")
    
    plt.rcParams['text.usetex'] = True
    
    axes.set_xlabel(r"Resistenza di carico [$\bf\Omega$]", )
    axes.set_ylabel("Coefficiente di rifrazione")
    
    title = plt.title("Fit per la rifrazione", size = 16, weight = "roman")
    
    plt.show()
    