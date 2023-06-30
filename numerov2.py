#numerov2.py
#Robin Li 22/01/2023
#Second version of numerov numerical algorithm without classes, with eigenvalue calculator.

import math
import auxiliaries
import analytical

#first extract inputs
def solve_numerov(delta, E, n, x0, xf):

    #define global variables and constants
    j = int(round(abs(xf - x0) / delta, 0))
    psi = [] #empty list of psi
    x = [] #linspace of x
    for i in range(0, j):
        x.append(x0 + i * delta) #inside the bracket is the position of x in terms of i, the number of iterations done and the value of delta

    #now we can start with the main calculation. First determine the parity of n
    parity = auxiliaries.parityCheck(n)

    #define f, which is the function being integrated.
    def f(x):
        y = x ** 2 - E
        return(y)

    #choose starting values based on parity:
    if parity == "even":
        psi.append(1) #psi(0)=1, psi'(0)=0. this appends psi(0)

        psi_1 = 1 - delta**2 * E /2 + delta ** 4 * E ** 2 / 24
        psi.append(psi_1)

    elif parity == "odd":
        psi.append(0)
        psi_1 = delta - delta ** 3 * E / 6
        psi.append(psi_1)

    for i in range(1, j-1):
        A = 2 + 5 * delta ** 2 * f(x[i]) / 6
        B = 1 - f(x[i-1]) * delta ** 2 / 12
        C = 1 - delta ** 2 * f(x[i+1]) / 12

        next_psi = (A * psi[i] - B * psi[i-1]) / C
        psi.append(next_psi)

    return(x, psi)
