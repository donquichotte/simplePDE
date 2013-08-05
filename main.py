import sys, pygame
import math
import copy

class App:
	def __init__(self, cellsize, cellnum):
		print "Initializing App."
		self._running = True
		self._display = None
		self.fps = 24

		# constants for heat eqn
		self.k = 1
		self.deltax = 1
		self.deltat = 0.1

		# constant for wave eqn
		self.c = 0.7

		# equation type ("HEAT", "WAVE", ...)
		self.eqnType = "WAVE"

		# display parameters
		self.size = self.width, self.height = cellsize*cellnum, cellsize * cellnum
		self.cellsize = cellsize
		self.cellnum = cellnum

		# cell parameters. self.cells will be diplayed. self.oldcells is self.cells at (t-1). self.disturbance is a mouse-activated disturbance
		self.cells = []
		for i in range(0,self.cellnum):
			new = []
			for j in range(0,self.cellnum):
				new.append(0)
			self.cells.append(list(new))

		
		self.oldcells = copy.deepcopy(self.cells) 
		self.disturbance = copy.deepcopy(self.cells)
		self.zeros = copy.deepcopy(self.cells)

		# self.clock to set fps
		self.clock = pygame.time.Clock()
		self.black = 0, 0, 0

	def init(self):
		print "Executing init()."
		pygame.init()
		self._display = pygame.display.set_mode(self.size, pygame.HWSURFACE)
		self._running = True

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False

	def loop(self):

		oldcells = copy.deepcopy(self.cells)
		for i in range(0,self.cellnum):
			for j in range(0,self.cellnum):

				if ((i in [0, (self.cellnum-1)]) or (j in [0, (self.cellnum-1)])): # boundary
					self.cells[i][j] = 0
				else:
					north = oldcells[i][j-1]
					east = oldcells[i+1][j]
					south = oldcells[i][j+1]
					west = oldcells[i-1][j]

					center = oldcells[i][j]
					center_old = self.oldcells[i][j]

					disturbance = self.disturbance[i][j]					

					
					
					
					if self.eqnType == "HEAT":
						# heat equation
						factor = self.k * self.deltat / self.deltax / self.deltax
						self.cells[i][j] = center + factor*(north + south + east + west - 4 * center + disturbance) 
					elif self.eqnType == "WAVE":
						# wave equation
						c = self.c
						self.cells[i][j] = c * c * (north + east + south + west - 4 * center) - center_old + 2 * center + disturbance	
					else:
						self.cells[i][j] = disturbance


								


		self.oldcells = copy.deepcopy(oldcells)
		self.disturbance = copy.deepcopy(self.zeros)

		# mouse-activated disturbance: click & hold to disturb the fuck out of this membrane!
		buttons = pygame.mouse.get_pressed()
		if buttons[0]:
			pos = pygame.mouse.get_pos()
			activecell_x = int(math.floor(pos[0]/self.cellsize))
			activecell_y = int(math.floor(pos[1]/self.cellsize))
			if ((activecell_x in [0, (self.cellnum-1)]) or (activecell_y in [0, (self.cellnum-1)])):
				pass
			else:
				self.disturbance[activecell_x][activecell_y] = 0.8

		self.clock.tick(self.fps) # setting fps


	def render(self):
		self._display.fill(self.black)		

		for i in range(0,self.cellnum):
			for j in range(0,self.cellnum):
				color = self.colorize(self.cells[i][j])
				pygame.draw.rect(self._display, (color, color,0), (self.cellsize*i, self.cellsize*j, self.cellsize, self.cellsize),0)
			
		pygame.display.flip()



	def cleanup(self):
		print "Cleaning up."
		pygame.quit()
		sys.exit()

	def execute(self):
		self.init()
		while( self._running ):
			for event in pygame.event.get():
				self.on_event(event)
			self.loop()
			self.render()
		self.cleanup()

	def bound(self, value, bound):
		# expects a value, bounds it to [-bound, bound]
		result = min(value, bound)
		result = max(value, -bound)
		return result

	def colorize(self, color):
		# expects values between -1 and 1, converts them to integer between 0 and 255
		result = int(color * 128 + 127)
		result = max(result, 0)
		result = min(result, 255)
		return result





if __name__ == "__main__":


	leApp = App(30, 40) # cells are 10x10 pixels. Display consists of 90x90 cells.
	leApp.execute()