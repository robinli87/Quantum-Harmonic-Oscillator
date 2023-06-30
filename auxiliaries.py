#auxiliaries.py
#19/01/2023  Robin Li
#Subroutines that are useful for calculations and the program in general.

def map(x, y, entries):
	xzoom = float(entries[0].get())
	yzoom = float(entries[1].get())
	xoffset = float(entries[2].get())
	yoffset = float(entries[3].get())

	xprime = []
	yprime = []

	for i in x:
		mapped = 540 + (i - xoffset) * xzoom
		xprime.append(mapped)

	for i in y:
		mapped = 540 - (i - yoffset) * yzoom
		yprime.append(mapped)

	return(xprime, yprime)

def parityCheck(n):
	ans = round(n / 2, 1) #need to remove numerical noise; we only look at the first decimal place
	ans = str(ans) #convert to string for analysis

	if ans[-1] == "5": #division result is something point 5 -> odd
		return("odd")

	elif ans[-1] == "0": #if we get an integer
		return("even")

