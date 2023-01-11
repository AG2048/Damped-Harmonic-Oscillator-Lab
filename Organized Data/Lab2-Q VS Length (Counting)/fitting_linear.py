# -*- coding: utf-8 -*-
"""
This program imports data from the file specified by the string filename.
The first line of the file is ignored (assuming it's the name of the variables).
After that the data file needs to be formatted: 
number space number space number space number newline
Do NOT put commas in your data file!! You can use tabs instead of spaces.
The data file should be in the same directory as this python file.
The data should be in the order:
x_data y_data x_uncertainty y_uncertainty

Then this program tries to fit a function to the data points.
It plots the data as dots with errorbars and the best fit line.
It then prints the best fit information.
After that, it plots the "residuals": ydata - fittedfunction(xdata)
That is it subtracts your fitted ideal values from your actual data to see 
what is "left over" from the fit.
Ideally your residuals graph should look like noise, otherwise there is more
information you could extract from your data (or you used the wrong fitting
function).

If you want to change the file name, that's the next line below this comment.
"""

filename = "Q vs length.txt"
""" 
Change this if your filename is different.

Note: you might need to type in the entire path to your file, in which case
you need to use double slashes (in Windows) to get this to work. For example

filename="C:\\Users\\Brian\\PHY224\\mydata.txt"
"""

import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
from pylab import loadtxt


def damped_sinusoid(t, a, tau, T, phi):
    return a * np.exp(-t / tau) * np.cos(2 * np.pi * t / T + phi)


def exponential(t, a, tau):
    return a * np.exp(-t / tau)


def linear(t, m, b):
    return m * t + b


def quadratic(t, a, b, c):
    return a * t ** 2 + b * t + c


def powerlaw(t, a, b):
    return a * t ** b

def powerseries(t, a, b, c):
    return a*(1 + t*b + t*c**2)

def power_series_6(t, a, b, c, d, e, f, g):
    return a + b*t + c*t**2 + d*t**3 + e*t**4 + f*t**5 + g*t**6

def power_series_3(t, a, b, c, d):
    return a + b*t + c*t**2 + d*t**3

def square_root(L, K, n):
    return K * L**n

def sine(L, A, w, d, phi):
    return A*np.sin(w*L + phi)+d

"""
The above five functions should be all you need for PHY180
The first line in main() is where you choose which function you want to use
Note that the different functions have different numbers of parameters. This
is crucial. Look below for what you have to change based on this, which is
highlighted by comments that look like:
########### HERE!!! ##############
"""


def main():
    my_func = linear
    # Change to whichever of the 5 functions you want to fit

    plt.rcParams.update({'font.size': 15})
    plt.rcParams['figure.figsize'] = 10, 9
    # Change the fontsize of the graphs to make it easier to read.
    # Also change the picture size, useful for the save-to-file option.

    data = loadtxt(filename, usecols=(0, 1, 2, 3), skiprows=1, unpack=True)
    # Load file, take columns 0 & 1 & 2 & 3, skip 1 row, unpack means
    # the data points are line by line instead of line 2 being all x values
    # and line 3 being all the y values, etc.

    xdata = data[0] / 100  # lengths were in cm
    ydata = data[1]  # in here a period of 1s will break the code, so
    # I changed it to 1.00001s (so log1.00001 != 0)
    xerror = data[2] / 100  # length in cm
    yerror = data[3]
    # Finished importing data, naming it sensibly.

    ########### HERE!!! ##############

    init_guess = (1, 1)
    # Your initial guess of (a, tau, T, phi)
    # For sinusoidal functions, guessing T correctly is critically important
    # Note: your initial guess must have the same number of parameters as
    # you are fitting

    popt, pcov = optimize.curve_fit(my_func, xdata, ydata, sigma=yerror, p0=init_guess, maxfev=10000)
    # The best fit values are popt[], while pcov[] tells us the uncertainties.

    ########### HERE!!! ##############

    m = popt[0]
    b = popt[1]
    # best fit values are named nicely
    u_m = pcov[0, 0] ** (0.5)
    u_b = pcov[1, 1] ** (0.5)
    # uncertainties of fit are named nicely

    start = min(xdata)
    stop = max(xdata)
    xs = np.arange(start, stop, (stop - start) / 10000)
    curve = my_func(xs, *popt)
    # (x,y) = (xs,curve) is the line of best fit for the data in (xdata,ydata).
    # It has 1000 points to make it look smooth.
    # Note: the "*" tells Python to send all the popt values in a readable way.

    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})
    # Make 2 graphs above/below each other: ax1 is top, ax2 is bottom.
    # The gridspec_kw argument makes the top plot 2 times taller than the bottom plot.
    # You can adjust the relative heights by, say, changing [2, 1] to [3, 1].

    ax1.errorbar(xdata, ydata, yerr=yerror, xerr=xerror, fmt=".", label="Q Factors", color="blue")
    # Plot the data with error bars, fmt makes it data points not a line, label is
    # a string which will be printed in the legend, you should edit this string.

    ax1.plot(xs, curve, label="Linear Best Fit", color="black")
    # Plot the best fit curve on top of the data points as a line.
    # NOTE: you may want to change the value of label to something better!!

    ax1.legend(loc='upper left')  # for this specifically, to not block data points
    # Prints a box using what's in the "label" strings in the previous two lines.
    # loc specifies the location

    ax1.set_xlabel("Length of Pendulum, L / m")
    ax1.set_ylabel("Q Factor, Q")
    ax1.set_title("Relationship Between Pendulum Length and Q Factor")
    # Here is where you change how your graph is labelled.

    # ax1.set_xscale('log')
    # ax1.set_yscale('log')
    # uncomment out the above two lines if you want to make it log-log scale

    ########### HERE!!! ##############

    print("m:", m, "+/-", u_m)
    print("b:", b, "+/-", u_b)
    # prints the various values with uncertainties
    # This is printed to your screen, not on the graph.
    # If you want to print it on the graph, use plt.text(), details at
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html

    residual = ydata - my_func(xdata, *popt)
    ax2.errorbar(xdata, residual, yerr=yerror, xerr=xerror, fmt=".", color="blue")
    # Plot the residuals with error bars.

    ax2.axhline(y=0, color="black")
    # Plot the y=0 line for context.

    ax2.set_xlabel("Length of Pendulum, L / m")
    ax2.set_ylabel("Residual of Q Factor, Q")
    ax2.set_title("Residuals of the Best Fit Curve")
    # Here is where you change how your graph is labelled.

    # ax2.set_xscale('log')
    # ax2.set_yscale('log')

    fig.tight_layout()
    # Does a decent cropping job of the two figures.
    # ax1.plot(0, 0)  # show origin
    # mng = plt.get_current_fig_manager()
    # mng.full_screen_toggle()
    plt.show()
    # Show the graph on your screen.

    fig.savefig("Graphs/Q vs L linear.png")
    # This saves the graph as a file, which will get overwritten
    # every time you run this program, so rename the file if you
    # want to keep multiple files!

    return None
    # End of main(). Note that it does not return anything.


main()
# Run the program.
