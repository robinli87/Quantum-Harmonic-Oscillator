#Robin Li 19/1/2023
#Euler's approximation method - compute an approximation of the solutions just as a comparison to the other algorithms'
#inputs: delta, n , E, x0, xf
#outputs: the calculated solutions of x and psi


import math
from tkinter import *
import auxiliaries


class solve:

	def __init__(self, entries):
		#first extract our parameters and then define variables
		self.delta = float(entries[0].get())
		
		self.n = int(entries[2].get())
		self.E = 2 * self.n + 1#float(entries[1].get())
		self.x0 = float(entries[3].get())
		self.xf = float(entries[4].get())

		self.j = int(round(abs(self.xf - self.x0) / self.delta, 0))

		self.psi = []

		#Generate a list of x values to match the numerical version
		self.x = []
		for i in range(0, self.j):
			self.x.append(self.x0 + i * self.delta) #inside the bracket is the position of x in terms of i, the number of iterations done and the value of delta


		self.velocity = []  # first derivative
		self.acceleration = [] #second derivative
		#call the actual looping compute function

		
		self.compute()

	def compute(self):
		#now we need to enter the initial conditions
		#now we can start with the main calculation. First determine the parity of n
		parity = auxiliaries.parityCheck(self.n)

		#choose starting values based on parity:
		if parity == "even":
			self.psi.append(1) #psi(0)=1, psi'(0)=0. this appends psi(0)
			self.velocity.append(0)
			this_acceleration = self.psi[0] * (self.x[0] ** 2 - self.E)
			self.acceleration.append(this_acceleration)

		elif parity == "odd":
			self.psi.append(0)
			self.velocity.append(1)
			this_acceleration = self.psi[0] * (self.x[0] ** 2 - self.E)
			self.acceleration.append(this_acceleration)

		for i in range(0, self.j):
			#euler integration
			next_velocity = self.velocity[i] + self.acceleration[i] * self.delta #get the next psi'

			#use a verlet integration to get a more accurate value of the next psi, by averaging the velocities before and after
			next_psi = self.psi[i] + self.delta * (self.velocity[i] + next_velocity)/2 + self.acceleration[i] * self.delta ** 2 / 2

			#calculate the next acceleration (psi'') by plugging the new value of psi back into the differential equation
			next_acceleration = self.psi[i] * ((self.x[i] ** 2) - self.E)

			#append results to arrays
			self.velocity.append(next_velocity)
			self.psi.append(next_psi)
			self.acceleration.append(next_acceleration)


	def Return(self):
		return(self.x, self.psi)

