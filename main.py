import tkinter as tk
import numpy as np
import matplotlib		# before 'from matplotlib import pyplot as plt' !!!
matplotlib.use("TkAgg")	# see above line !!
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib import pyplot as plt
from conv_eval import evaluate
import random

##########
# KERNEL #
##########
board = [[0 for j in range(15)] for i in range(15)]
board_ai_view = [[0 for j in range(15)] for i in range(15)]
value = [[0 for j in range(15)] for i in range(15)]
current = 1 # 1 for human player, -1 for AI

# Get the value gradient
def computeValue():
	for x in range(15):
		for y in range(15):
			if board[x][y] != 0:
				value[x][y] = -999999 # 
				continue
			value_a = evaluate(board_ai_view, x, y)
			value_b = evaluate(board, x, y)
			value[x][y] = (value_a+value_b)/2 + 2/(np.power((15/2 - x),2) + np.power((15/2 - y),2))

# Get the value gradient
def getBoardValue(BOARD):
	return evaluate(BOARD, -1, -1)

def choose():
	V = np.array(value)
	MAX = np.max(V)
	positions = []
	counter = 0
	for x in range(15):
		for y in range(15):
			if V[x][y] == MAX:
				positions.append(counter)
			counter+=1
	random.shuffle(positions)
	print(positions)
	return int(positions[0]/15), int(positions[0]%15)

# Make a move on the board
def move(x,y):
	global current
	if board[x][y] == 0:
		board[x][y] = current
		board_ai_view[x][y] = 0 - current
		current = 0 - current

# Reset everything!
def replay():
	global current
	current = 1
	board = [[0 for j in range(15)] for i in range(15)]
	board_ai_view = [[0 for j in range(15)] for i in range(15)]
	value = [[0 for j in range(15)] for i in range(15)]
	insight()
	# Create the board: x -> column; y -> row
	for y in range(15+1):
		for x in range(15+1):
			# Print "A B C D E F G ... M N O" in the first row
			if y == 0 and x != 0:
				col_label = tk.Label(master, text = str(chr(ord('A')+x-1)))
				col_label.grid(row = y, column = x)
			else:
				# Print the row number at the beginning of each row
				if x == 0 and y != 0:
					row_label = tk.Label(master, text = str(y))
					row_label.grid(row = y, column = x)	
				# The Buttons are grid intersections
				elif x!= 0 and y!= 0:	
					btn = tk.Canvas(master,bg='grey',width='20',height='20',bd='0')
					btn.grid(row = y, column = x)
					btn.bind('<Button-1>',moveHandler)


##########
## GUI ###
##########
def replayHandler(event):
	replay()

def exitHandler(event):
	exit()

def moveHandler(event):
	global current
	x = int(event.widget.grid_info().get('row'))-1
	y = int(event.widget.grid_info().get('column'))-1
	if board[x][y] == 0:
		if current == 1:
			#event.widget.configure(text='O')
			event.widget.configure(bg='black')
			move(x,y)
			# AI's Turn
			computeValue()
			insight()
			X,Y = choose()
			#master.grid_slaves(X+1, Y+1)[0].configure(text='X')
			master.grid_slaves(X+1, Y+1)[0].configure(bg='red')
			move(X,Y)



############################################
#把绘制的图形显示到tkinter窗口上 (insight window)
plot_root = tk.Tk()
plot_root.title('Insight')

# Create Figure
fig = plt.figure()

# Plot Value Gradient
ax = fig.add_subplot(111)

# Show the plot on plot window
canvas = FigureCanvasTkAgg(fig, master=plot_root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)




#############################
# Main window
master = tk.Tk()
master.title('Conv Gomoku')

#############################
# Control Panal window
panal = tk.Tk()
panal.title('Control Panal')
# Current value fields
yourField = tk.Label(panal, text='Your current value:')
aiField = tk.Label(panal, text='AI\'s current value:')
yourField.grid(row = 0, column = 0)
aiField.grid(row = 0, column = 2)
# Exit
exitBtn = tk.Button(panal, text='Exit')
exitBtn.grid(row = 1, column = 1)
exitBtn.bind('<Button-1>', exitHandler)


def insight():
	#ax1.clear()
	ax.clear()
	#plt.imshow(board)
	#computeValue()
	_V = np.array(value)
	for x in range(15):
		for y in range(15):
			if _V[x][y] == -999999:
				_V[x][y] = 0
	plt.imshow(_V)
	#print(value)
	canvas.draw()
	# Display the values of both human and AI players
	yourField.configure(text = 'Your current value:' + str(getBoardValue(board)-getBoardValue(board_ai_view)))


# Create the board: x -> column; y -> row
replay()

# Start GUI
master.mainloop()
panal.mainloop()
