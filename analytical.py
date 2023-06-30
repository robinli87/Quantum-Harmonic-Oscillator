#analytical.py
#18/1/2023 Robin Li
#Computes an analytical solution based on given inputs
#inputs: inputs from the main program stored as a package
#outputs: the analytical solution, but computed at each corresponding x value. 

#as usual we start by importing the necessary modules

from tkinter import *
import math



class solve_analytically: 

	def __init__(self, entries):

		#first extract our parameters and then define variables
		self.delta = float(entries[0].get())
		
		self.n = int(entries[2].get())
		self.E = 2 * self.n + 1#float(entries[1].get())
		self.x0 = float(entries[3].get())
		self.xf = float(entries[4].get())

		self.j = int(round(abs(self.xf - self.x0) / self.delta, 0)) #calculate the number of intervals

		self.psi = []

		#Generate a list of x values to match the numerical version
		self.x = []
		for i in range(0, self.j):
			self.x.append(self.x0 + i * self.delta) #inside the bracket is the position of x in terms of i, the number of iterations done and the value of delta

		#call the actual looping compute function
		self.loop()

	def loop(self):

		#Now iterate through the list and compute. 
		for xn in self.x:
			psi_n = self.wavefunction(xn) #use the wavefunction function to calculate the value of psi at this point
			self.psi.append(psi_n)

		#print(self.psi)

	def Return(self):
		return(self.x, self.psi) #at the end of the loop we have the full list of solutions so we may return them back to the main program

	def wavefunction(self, xn):
		# psi = H(x) * exp(x^2/2), so it's easier to break up the hermite polynomial generation and the Gaussian'
		H = self.Hermite(xn) #call the hermite polynomial generation algorithm
		psi = H * math.e ** (-xn ** 2 / 2) #multiply the hermite by the Gaussian
		return(psi)

	def Hermite(self, xn):
		h = [1, 2 * xn] #the first 2  of the hermite polynomials are known
		i = 1 #a counter
		while i <= self.n: #we need to keep calculating until we reach the order we want
			next_h = 2 * xn * h[i] - 2 * i * h[i-1] #the recurrance formula for hermite polynomials
			h.append(next_h) #append to the list of known hermite polynomials values
			i += 1
		return(h[self.n])







