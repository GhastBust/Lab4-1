import numpy
import scipy
import scipy.optimize
from myutils import phypot, bsci_err
from matplotlib import lines
import matplotlib.pyplot as plt
import itertools


L =    [ 10,    20,	    30,	    40  ]
t1 =   [ 3.40,  3.40,	3.50,	3.50]
t2 =   [ 104.80,206,    309,	409 ] # ns -> us -> ms -> m
t_err =[ 0.10,	0.20,	0.50,	1   ]
V1 =   [ 2.38,	2.38,	2.38,	2.38]
V2 =   [ 2.08,	1.82,	1.60,	1.40]


R_gen = 50
R = [0,	10,	20,	30,	40,	50,	60,	70,	80,	90,	100, 110.10, 140, 170, 187.30]
V_rifl = numpy.array([-1.98, -1.32, -0.95, -0.48, -0.28, 0.01, 0.12, 0.26, 0.41, 0.52, 0.62, 0.71, 0.93, 1.06, 1.14])
V_gen = numpy.ones_like(V_rifl) * 2.38
V_err = numpy.ones_like(V_rifl) * 0.01


def frac_simm_err( a: float, b: float, sigma: float) -> float:
    
    return sigma * phypot( 1/b, a/b**2 )


def prod_err( a: float, sigma_a: float, b: float, sigma_b: float ) -> float :
    
    return phypot( a * sigma_b, b * sigma_a )



def extract() : 
    
    delta_t = numpy.array(t2) - numpy.array(t1) # in ns
    delta_t /= 1_000_000_000
    sigma = numpy.array(t_err) / numpy.sqrt(12) / 1_000_000_000
    
    lenght = lambda dt, v: v * dt
    
    v2, v_err2 = scipy.optimize.curve_fit( 
        lenght,
        xdata= delta_t,
        ydata= L,
        sigma= sigma,
        p0= 200_000_000
    )
    
    v       = v2 * 2
    v_err   = numpy.sqrt(v_err2) * 2

    lenghtt= lambda dt : lenght(dt, v)
    
    display = bsci_err(float(v), float(v_err))
    print("v nel medio =", display)
    
    # --------------------------------------------------------------------------
    
    C_norm, C_norm_err = get_normalization_contant(V1, V2)
    
    gamma_from_V, gamma_from_V_err = get_gamma_from_V(
        V_rifl, V_gen, V_err,
        C_norm, C_norm_err
    )
    
    
    gamma_f = lambda z_L, z : (z_L - z) / (z_L + z)
    
    z_fit, z_fit_err = scipy.optimize.curve_fit(
        gamma_f,
        xdata= R,
        ydata= gamma_from_V,
        sigma= gamma_from_V_err,
        p0= 50
    )
    
    gamma_ff = lambda z_L: gamma_f(z_L, z_fit)
    
    graph(gamma_from_V, gamma_from_V_err, R, gamma_ff )
    
    
    display = bsci_err( float(z_fit), float(numpy.sqrt(z_fit_err)) )
    print("Z =", display)
    
    

def graph(y: list[float], y_err: float, x: list[float], lenght) :
    
    y_err = list(map(lambda x: x*20, y_err))
    
    err_bar = plt.errorbar(x= x, y= y, yerr= y_err, fmt= ".")
    err_bar.set_label("Dati empirici")
    
    axes = plt.gca()
    axes.grid(visible= True, which= "both")
    
    xlim = list(axes.get_xlim())
    
    ylim = list(axes.get_ylim())
    
    # xaxis = lines.Line2D(xdata= )    
    
    xaxis = numpy.linspace( max(x), min(x), 100 )
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


def graph_points(y, y_err, x) :
    pass


def graph_line() :
    pass


def get_gamma_from_V(V_rifl, V_gen, V_err, C_norm, C_norm_err):
    
    gamma_from_V = V_rifl / V_gen / C_norm
    gamma_from_V_err = []
    
    for Vg, Vr, Ve in zip(V_gen, V_rifl, V_err) :
        temp = Vr / Vg
        temp_err = frac_simm_err(Vr, Vg, Ve / numpy.sqrt(12))
        
        err = prod_err( temp, temp_err, C_norm, C_norm_err )
        
        gamma_from_V_err.append(err)
        
    return gamma_from_V,gamma_from_V_err


def get_normalization_contant(V1, V2):
    
    C_norm  = V2[0] / V1[0]
    C_norm_err = frac_simm_err(V2[0], V1[0], 0.02 / numpy.sqrt(12))
    
    return C_norm, C_norm_err