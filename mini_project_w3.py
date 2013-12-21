# Stopwatch - the game

# import statements
import simpleguitk as simplegui

# global variables
counter=0
stops = 0
wins = 0

# helper functions
def format(t):
	""" Formats a time value expressed in tenths of a second
	The returned format is MM:SS.ss where
	M = minutes
	S = seconds
	s = tenths of seconds

	"""

	tenths = t % 10
	minutes = (t / 10) / 60
	seconds = (t / 10) % 60 
	
	min_str = add_leading(minutes)
	sec_str = add_leading(seconds)
	ten_str = add_leading(tenths)

	return min_str + ":" + sec_str + "." + ten_str

def add_leading(number):
	"""	Adds a leading 0 to a number if this number has only one digit

	"""
	num_str = str(number)
	if (number < 10):
		num_str = "0" + num_str

	return num_str

# handler functions for UI and timer

def tick():
	""" The handler for the timer just increments the counter

	"""
	global counter
	counter += 1

def draw_handler(canvas):
	""" The draw handler which handles the UI work

	"""
	canvas.draw_text(format(counter),(100,100),24,"#FFFFFF")
	win_str = str(wins) + "/" + str(stops)
	canvas.draw_text(win_str,(260, 40), 17, "#FF2222")

def start_button_handler():
	timer.start()

def stop_button_handler():
	""" Stops the timer.
	Also computes the stops / winning stops 

	"""
	global stops, wins
	
	if (timer.is_running()):
		stops += 1
		if (counter % 10) == 0:
			wins += 1
		timer.stop()

def reset_button_handler():
	""" Resets the timer, stops and winning stops

	"""
	global counter, wins, stops
	counter = 0
	wins = 0
	stops = 0


# The main code of the app
frame = simplegui.create_frame("Stopwatch", 320, 240)
frame.set_draw_handler(draw_handler)
button_start = frame.add_button("Start", start_button_handler)
button_stop = frame.add_button("Stop",stop_button_handler)
button_reset = frame.add_button("Reset", reset_button_handler)

timer = simplegui.create_timer(100,tick)

frame.start()