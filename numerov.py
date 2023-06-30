#numerov.py
#Robin Li 18/1/2023
#Does the maths
#Inputs: the initial conditions and parameters. Receiving them as a package the extract the details out
#Outputs: the solution field

from tkinter import *
import math
import auxiliaries
import analytical

class solve_numerov:

	def __init__(self, entries):

		#first extract inputs
		self.delta = float(entries[0].get())
		self.E = float(entries[1].get())
		self.n = int(entries[2].get())
		self.x0 = float(entries[3].get())
		self.xf = float(entries[4].get())

		#define global variables and constants
		self.j = int(round(abs(self.xf - self.x0) / self.delta, 0))
		self.psi = [] #empty list of psi
		self.x = [] #linspace of x
		for i in range(0, self.j):
			self.x.append(self.x0 + i * self.delta) #inside the bracket is the position of x in terms of i, the number of iterations done and the value of delta

		self.compute()

	def compute(self):
		#we need to separate the compute section from the init so that it can be called separately without triggering the init, or within the class.
		self.psi = []

		#now we can start with the main calculation. First determine the parity of n
		parity = auxiliaries.parityCheck(self.n)

		#define f, which is the function being integrated (also the potential function - E)
		def f(x):
			y = (x ** 2) - self.E
			return(y)

		#choose starting values based on parity:
		if parity == "even":
			self.psi.append(1) #psi(0)=1, psi'(0)=0. this appends psi(0)

			psi_1 = 1 - self.delta**2 * self.E /2 + self.delta ** 4 * self.E ** 2 / 24
			self.psi.append(psi_1)

		elif parity == "odd":
			self.psi.append(0)
			psi_1 = self.delta - self.delta ** 3 * self.E / 6
			self.psi.append(psi_1)

		#The actual calculations that determine the next term from known terms
		for i in range(1, self.j-1):
			#break up the complicated recurrence equation into parts so that it's easy to debug. Decomposition - computational thinking
			A = 2 + 5 * self.delta ** 2 * f(self.x[i]) / 6
			B = 1 - f(self.x[i-1]) * self.delta ** 2 / 12
			C = 1 - self.delta ** 2 * f(self.x[i+1]) / 12

			next_psi = (A * self.psi[i] - B * self.psi[i-1]) / C
			self.psi.append(next_psi) #add this next term to the list of psi

	def Return(self):
		#for external scripts to query the data being stored in this class.
		return(self.x, self.psi)


	def checkRepeats(self, checkdigit, array):
		counter = 0
		#go through every element in the array and see if we can spot the item we are looking for
		for item in array:
			if item == checkdigit:
				#we found it! add 1 to the counter
				counter += 1

		return(counter)


	def find_eigenvalue(self, master, entries):

		#first compute a set of results
		self.compute()
		x, psi_analytical = analytical.solve_analytically(entries).Return()  #computes the analytical value and keeps it

		epsilon = float(entries[5].get()) #some small change to our guess
		guesses = [] #stores the list of gueses that  we have tried
		sign = 1 #by default we add

		#first compute the original difference
		guesses.append(self.E) #put this guess into the list of guesses
		this_diff = abs(psi_analytical[-1] - self.psi[-1]) #find the error of our first crude guess

		print("Difference: ", this_diff)

		#insert a new guess of E into the input field and retry:
		#we first need to get a new E
		self.E = self.E + sign * epsilon
		guesses.append(self.E)

		#then we insert the new E into the entry to notify the user
		entries[1].delete(0, END)
		entries[1].insert(0, str(self.E))
		master.update()

		while self.checkRepeats(self.E, guesses) < 5:
			#if the same guess has been used 5 times or more then we are most likely circling around 2 values - the correct Eigenvalue is somewhere in between.
			print(self.checkRepeats(self.E, guesses)) #print out the number of repeats found

			#now we need to see how well our new guess is doing:
			self.compute()
			#Finding the error of our new guess
			next_diff = abs(psi_analytical[-1] - self.psi[-1])

			#compare our new guess to the previous guess
			if next_diff < this_diff:
				#this new guess is better, we are heading in the right direction, so let's keep doing what we were doing.
				print("Eigenvalue: ", self.E, "Difference: ", next_diff)


			else:
				#this new guess is worse, we are heading in the wrong direction reverse the direction of addition
				sign = -1 * sign
				print("Eigenvalue: ", self.E, "Difference: ", next_diff)

			this_diff = next_diff #update the difference to prepare for next loop

			self.E = self.E + sign * epsilon #generate next guess

			guesses.append(self.E)#add our new guess to the list of guesses

			entries[1].delete(0, END)
			entries[1].insert(0, str(round(self.E, len(str(epsilon))-2)))#display new value, rounding it to the same decimal place as the user's tolerance
			master.update()#update the window

		return(self.E)







