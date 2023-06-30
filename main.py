#Robin Li 18/01/2023
#Main,py - creates and maintains the main window:  fetching user inputs, displaying graphs, calling calculation modules. 
#inputs are the user's entry in the entry fields, outputs the graph and any other responses
#so far just for this one calculation type. The graphing function may be re-used generally.

#first import tkinter module for the GUI
from tkinter import *
import analytical
import numerov
import euler


class GUI:

	def __init__(self, master):
		self.master = master #the self.master now stands for the window and is globalised within this class

		#now we can apply our GUI design, first draw the frames

		self.master.title("Quantum Harmonic Oscillator")
		self.master.geometry("1920x1080") #set window size. Most UK people's computer screens have resolution 1920x1080 (FHD) in early 2023

		self.interaction_frame = Frame(self.master, width=840, height=1080) #left side frame to contain input fields and buttons
		self.interaction_frame.pack(side=LEFT)

		self.canvas = Canvas(self.master, width=1080, height=1080) #where the graph will be sketched
		self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

		self.input_panel = Frame(self.interaction_frame, width=840, height=380, bg="pink") #input panel
		self.input_panel.pack(fill=BOTH, expand=1)
		self.control_panel = Frame(self.interaction_frame, width=840, height=450, bg="cyan") #output panel
		self.control_panel.pack(fill=BOTH, expand=1)
		self.console = Frame(self.interaction_frame, width=840, height=250, bg="yellow") #console window to display program outputs
		self.console.pack(fill=BOTH, expand=1)

		#now widgets inside the frames
		self.entries1 = []  #stores actual physics and maths parameters
		self.entries2 = []  #stores zoom and offset
		self.labels = []

		#0 delta
		new = Entry(self.input_panel) #create an entry 
		new.grid(row = 1, column=1, padx=5, pady=5) #position it within input panel
		new.insert(0, "0.05") #insert in a default value to save effort when testing
		self.entries1.append(new) #add this to the list of entries to keep track
		new = Label(self.input_panel, text="Delta:") #put a label next to the left of the entry to guide the user
		new.grid(row = 1, column=0, padx=5, pady=5)
		self.labels.append(new) #append this to label list to keep track 

		#1. E
		new = Entry(self.input_panel)
		new.grid(row = 2, column=1, padx=5, pady=5)
		new.insert(0, "0.95")
		self.entries1.append(new)
		new = Label(self.input_panel, text="E:")
		new.grid(row =2 , column=0, padx=5, pady=5)
		self.labels.append(new) 

		#2 n
		new = Entry(self.input_panel)
		new.grid(row = 3, column=1, padx=5, pady=5)
		new.insert(0, "0")
		self.entries1.append(new)
		new = Label(self.input_panel, text="n:")
		new.grid(row = 3, column=0, padx=5, pady=5)
		self.labels.append(new) 

		#3 x0 
		new = Entry(self.input_panel)
		new.grid(row = 4, column=1, padx=5, pady=5)
		new.insert(0, "0")
		self.entries1.append(new)
		new = Label(self.input_panel, text="x0 (start of x interval)")
		new.grid(row = 4, column=0, padx=5, pady=5)
		self.labels.append(new) 

		#4 xf
		new = Entry(self.input_panel)
		new.grid(row = 5, column=1, padx=5, pady=5)
		new.insert(0, "5")
		self.entries1.append(new)
		new = Label(self.input_panel, text="End of x interval, xf")
		new.grid(row = 5, column=0, padx=5, pady=5)
		self.labels.append(new)

		#5 tolerance
		new = Entry(self.input_panel)
		new.grid(row = 6, column=1, padx=5, pady=5)
		new.insert(0, "0.01")
		self.entries1.append(new)
		new = Label(self.input_panel, text="Accuracy of Eigenvalue")
		new.grid(row = 6, column=0, padx=5, pady=5)
		self.labels.append(new)


		#now the zoom and offset factors inside the control panel 

		#0 xzoom
		new = Entry(self.control_panel)
		new.grid(row = 4, column=1, padx=5, pady=5)
		new.insert(0, "100")
		self.entries2.append(new)
		new = Label(self.control_panel, text="X axis ppu")
		new.grid(row = 4, column=0, padx=5, pady=5)
		self.labels.append(new) 

		#1 yzoom
		new = Entry(self.control_panel)
		new.grid(row = 5, column=1, padx=5, pady=5)
		new.insert(0, "100")
		self.entries2.append(new)
		new = Label(self.control_panel, text="Y axis ppu")
		new.grid(row = 5, column=0, padx=5, pady=5)
		self.labels.append(new) 

		#2 xoffset
		new = Entry(self.control_panel)
		new.grid(row = 6, column=1, padx=5, pady=5)
		new.insert(0, "0")
		self.entries2.append(new)
		new = Label(self.control_panel, text="X offset from origin")
		new.grid(row = 6, column=0, padx=5, pady=5)
		self.labels.append(new) 

		#3. yoffset
		new = Entry(self.control_panel)
		new.grid(row = 7, column=1, padx=5, pady=5)
		new.insert(0, "0")
		self.entries2.append(new)
		new = Label(self.control_panel, text="Y axis zoom")
		new.grid(row = 7, column=0, padx=5, pady=5)
		self.labels.append(new) 

		#now add buttons
		self.buttons = []
		new = Button(self.control_panel, text="Calculate", command=self.calculate)#0
		new.grid(row = 0, column=0, padx=5, pady=5) #tells the program to do maths
		self.buttons.append(new)
		new = Button(self.control_panel, text="Plot Numerov solution", command=self.plot_numerical)#1
		new.grid(row = 1, column=0, padx=5, pady=5) #displays the plot on the canvas
		self.buttons.append(new)
		new = Button(self.control_panel, text="Plot analytical solution", command=self.plot_analytical)#2
		new.grid(row = 1, column=1, padx=5, pady=5)
		self.buttons.append(new)
		new = Button(self.control_panel, text="Clear all", command=self.clear)#3
		new.grid(row = 0, column=2, padx=5, pady=5) #3clears the canvas
		self.buttons.append(new)
		new = Button(self.control_panel, text="Plot Euler approximation", command=self.plot_euler)#4
		new.grid(row=1, column=2, padx=5, pady=5)
		self.buttons.append(new)
		new = Button(self.control_panel, text="Apply Scaling", command=self.apply_scaling)#5
		new.grid(row=2, column=1, padx=5, pady=5)
		self.buttons.append(new)
		new = Button(self.control_panel, text="Show coordinate grid", command=self.coordinate_grid)#6
		new.grid(row=0, column=1, padx=5, pady=5)
		self.buttons.append(new)
		new = Button(self.control_panel, text="Find eigenvalue", command=self.Eigenvalue)
		new.grid(row=2, column=0, padx=5, pady=5)
		self.buttons.append(new)

		#now add labels in the console to display certain parameters:
		self.output_labels = []
		new = Label(self.console, text="Please press <calculate>") #0 Calculation done?
		new.grid(row=0, column=0, padx=5, pady=5)
		self.output_labels.append(new)
		new = Label(self.console, text="Scaling Factor: 1") #1 scaling
		new.grid(row=1, column=0, padx=5, pady=5)
		self.output_labels.append(new)
		new = Label(self.console, text="Eigenvalue E")
		new.grid(row=2, column=0, padx=5, pady=5)
		self.output_labels.append(new)
		new = Label(self.console, text="")
		new.grid(row=3, column=0, padx=5, pady=5)
		self.output_labels.append(new)

		#now draw the axis and their labels on the canvas
		x_axis = self.canvas.create_line(40, 540, 1040, 540)
		y_axis = self.canvas.create_line(540, 40, 540, 1040)
		x_label = self.canvas.create_text(1040, 560, text="x")
		y_label = self.canvas.create_text(420, 20, text="Psi (probability amplitude)")

		self.x = [] #will store future solutions
		self.analytical_psi = []#store 3 different versions of soolutions
		self.numerov_psi = []
		self.euler_psi = []

		self.trash = [] #stores all objects on canvas (except axis) so that they can be deleted.

		self.grid_flag = False  #for showing / clearing coordinate grids
		self.coordinate_grid_elements = []


	def calculate(self):
		#directly call the calculation modules, namely numerov.py and analytical.py
		#Then store the solutions fields in main.py  	

		A = analytical.solve_analytically(self.entries1) #turn the analytical class into an object called A
		self.x, self.analytical_psi = A.Return() #call the return method of object A to extract the solutions

		self.B = numerov.solve_numerov(self.entries1)
		self.x, self.numerov_psi = self.B.Return()

		C = euler.solve(self.entries1)
		self.x, self.euler_psi = C.Return()

		#update the user interface
		self.output_labels[0].configure(text="Solutions have been calculated, ready to plot")
		self.buttons[0].configure(text="Re-Calculate")

		self.master.update()

	def coordinate_grid(self):
		#triggered when the show / hide coordinate grid button is pressed
		#first check whether we should display the coordinate grid. By default, it's yes'
		if self.grid_flag == False:
			#change the flag to True so that the next time we press the button it will hide the grid
			self.grid_flag = True

			#extract the offsets and scaling factors
			xzoom = float(self.entries2[0].get())
			yzoom = float(self.entries2[1].get())
			xoffset = float(self.entries2[2].get())
			yoffset = float(self.entries2[3].get())

			#draw the grid lines at spacing 100 pixels
			for i in range(-6, 6):

				#x labels
				x_coord = i * 100 / xzoom + xoffset * 100 / xzoom
				e = self.canvas.create_text(540 + i * 100, 540, text=str(round(x_coord, 2)))
				self.coordinate_grid_elements.append(e)
				#x axis gridlines (vertical)
				e =  self.canvas.create_line(540 + i * 100, 40, 540 + i * 100, 1040, fill="grey")
				self.coordinate_grid_elements.append(e)
				#y labels
				y_coord = (i + yoffset) * 100 / yzoom
				e = self.canvas.create_text(540, 540 - i * 100, text=str(round(y_coord, 2)))
				self.coordinate_grid_elements.append(e)
				#y vertical lines
				e = self.canvas.create_line(40, 540 - i *100, 1040, 540-i*100, fill="grey")
				self.coordinate_grid_elements.append(e)
			
			self.buttons[6].configure(text="Hide coordinate grid") #change the text on the button so that the next time we press, we hide it
			self.master.update()

		else:
			#the coordinate grid is being displayed and we need to clear it
			#first we want to reset the flag
			self.grid_flag = False
			#delete every coordinate-grid-related item on canvas
			for item in self.coordinate_grid_elements:
				self.canvas.delete(item)
			self.master.update()
			#Update the button
			self.buttons[6].configure(text="Show coordinate grid")
			self.master.update()
			
			#finally clear the list
			self.coordinate_grid_elements = []

	def apply_scaling(self):

		scaling_factor = 1   #set default to 1, assuming they are the same

		#use a try except just in case there is division by 0

		try: 
			#consider the second elements, because the first pair might be 0 and we get a ZeroDivisionError
			scaling_factor = self.analytical_psi[1] / self.numerov_psi[1]  #calculate the scaling
			print("Scaling Factor = ", scaling_factor) #print it out 
			self.output_labels[1].configure(text="Scaling Factor = " + str(scaling_factor))#print it out in the window

			for i in range(0, len(self.numerov_psi)):
				self.numerov_psi[i] = self.numerov_psi[i] * scaling_factor  #multiply each numerical result by the scaling

		except: 
			 #if we get division by 0 again then let's give it up...
			# try:
			#  	scaling_factor = self.analytical_psi[1] / self.numerov_psi[1]  #calculate the scaling
			# 	print("Scaling Factor = ", scaling_factor) #print it out 
			# 	self.output_labels[1].configure(text="Scaling Factor = " + scaling_factor)

			# 	for i in range(0, len(self.numerov_psi)):
			# 		self.numerov_psi[i] = self.numerov_psi[i] * scaling_factor  #multiply each numerical result by the scaling
			# except:
			# 	print("Math error again, please check initial conditions")
				
			pass

			# for i in range(0, len(self.numerov_psi)):
			# 	print(round(self.analytical_psi[i] / self.numerov_psi[i], 2))

		self.master.update()


	def plot_numerical(self):
		#the solution fields will be passed onto a mapping module where a real world value will be mapped onto a pixel on the screen. 
		#Draw lines to connect all of the pixel dots. THis will not be a perfect curve but to human eyes it will look close enough. 

		x, y = self.map(self.x, self.numerov_psi) #mapping function

		N = len(x) #finding the total number of line segments needed for the graph

		for i in range(0, N-1):
			segment = self.canvas.create_line(x[i], y[i], x[i+1], y[i+1], fill = "red")#draw the line segments connecting current point and next point
			self.trash.append(segment) #put this segment into the trash list so that it can be deleted in the future.

		self.master.update()	#update the window to display new content

	def plot_analytical(self):
		#almost identical to numerical version, but this is not triggered automatically.
		x, y = self.map(self.x, self.analytical_psi) #mapping function

		N = len(x) #finding the total number of line segments needed for the graph

		for i in range(0, N-1):
			segment = self.canvas.create_line(x[i], y[i], x[i+1], y[i+1], fill = "blue")#draw the line segments connecting current point and next point
			self.trash.append(segment) #put this segment into the trash list so that it can be deleted in the future.

		self.master.update()	#update the window to display new content

	def plot_euler(self):
		x, y = self.map(self.x, self.euler_psi) #mapping function

		N = len(x) #finding the total number of line segments needed for the graph

		for i in range(0, N-1):
			segment = self.canvas.create_line(x[i], y[i], x[i+1], y[i+1], fill = "green")#draw the line segments connecting current point and next point
			self.trash.append(segment) #put this segment into the trash list so that it can be deleted in the future.

		self.master.update()	#update the window to display new content

	def map(self, x, y):
		#first extract parameters
		xzoom = float(self.entries2[0].get())
		yzoom = float(self.entries2[1].get())
		xoffset = float(self.entries2[2].get())
		yoffset = float(self.entries2[3].get())

		#mapped coordinates
		xprime = []
		yprime = []

		#do the mapping calculation
		for i in x:
			mapped = 540 + (i + xoffset) * xzoom  #x direction
			xprime.append(mapped)

		for i in y:
			mapped = 540 - (i + yoffset) * yzoom  #y direction
			yprime.append(mapped)

		return(xprime, yprime)
		

	def clear(self):
		for item in self.trash:
			self.canvas.delete(item)#clear object from canvas
		self.master.update()#update to see the clean canvas 
		self.trash = []#empty the bin

	def Eigenvalue(self):
		eigenvalue = self.B.find_eigenvalue(self.master, self.entries1) #call the find_eigenvalue method of object B
		self.output_labels[2].configure(text = "Eigenvalue of E = " + str(eigenvalue)) #update  output labels
		self.master.update()




#open a blank tkinter window 
root = Tk()
GUI(root) #parse it into the class as the master parameter
root.mainloop() #hold the window there to prevent self destruction
