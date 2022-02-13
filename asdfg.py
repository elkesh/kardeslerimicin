import numpy as np
import time
import random
from queue import PriorityQueue
class hepsi1:
	'''
	This is the random player used in the colab example.
	Edit this file properly to turn it into your submission or generate a similar file that has the same minimal class structure.
	You have to replace the name of the class (ME461Group) with one of the following (exactly as given below) to match your group name
		atlas
		backspacex
		ducati
		hepsi1
		mechrix
		meturoam
		nebula
		ohmygroup
		tulumba
	After you edit this class, save it as groupname.py where groupname again is exactly one of the above
	'''
	def __init__(self, userName, clrDictionary, maxStepSize, maxTime):
		self.name = userName # your object will be given a user name, i.e. your group name
		self.maxStep = maxStepSize # maximum length of the returned path from run()
		self.maxTime = maxTime # run() is supposed to return before maxTime
		colorz = {
			'black':((1,1,1), 0, 13),
			'clr100':((225, 1, 1), 100, 1),
			'clr50':((1, 255, 1), 50, 2), 
			'clr30':((1, 1, 255), 30, 2),
			'clr20':((200, 200, 1), 20, 2),
			'clr10':((255, 1, 255), 10, 2), 
			'clr9':((1, 255, 255), 9, 3),
			'clr8':((1,1,150), 8, 3),
			'clr7':((120,120,40), 7, 3),
			'clr6':((150,1,150), 6, 3),
			'clr5':((1,150,150), 5, 3),
			'clr4':((222,55,222), 4, 3),
			'clr3':((1, 99, 55), 3, 3),
			'clr2':((200, 100, 10),2, 3),
			'clr1':((100, 10, 200),1, 3)
		}
		self.clrDictionary = colorz
	initLocs = [(25, 175),(25, 375),(25, 575),(175, 25),(375, 25),(575, 25),(175, 725),(375, 725),(575, 725)]
	def run(self, img, info):
		myinfo = info[self.name]
		imS = img.shape[0] # assume square image and get size
		# get current location
		loc, game_point = info[self.name]
		(y,x) = loc # get current y,x coordinates

		def bestOption(loc,imag):
			whereami=loc

			def findNeighbor(loc,stepsize):
				(y,x) = loc
				neighArr = [(y+stepsize, x), (y-stepsize, x), (y, x-stepsize), (y,x+stepsize)] #calculate the 4-neighbors
				return neighArr

			pointdic = {} #initialize the dictionary to store the points
			centerpoints = [[675, 675], [675, 575], [675, 475], [675, 375], [675, 275], [675, 175], [675, 75], [575, 675], [575, 575], [575, 475], [575, 375], [575, 275], [575, 175], [575, 75], [475, 675], [475, 575], [475, 475], [475, 375], [475, 275], [475, 175], [475, 75], [375, 675], [375, 575], [375, 475], [375, 375], [375, 275], [375, 175], [375, 75], [275, 675], [275, 575], [275, 475], [275, 375], [275, 275], [275, 175], [275, 75], [175, 675], [175, 575], [175, 475], [175, 375], [175, 275], [175, 175], [175, 75], [75, 675], [75, 575], [75, 475], [75, 375], [75, 275], [75, 175], [75, 75]]
			pickme = PriorityQueue() #initialize the empty priority queue to sort the options
			for k,m in enumerate(centerpoints):
				for key in self.clrDictionary: #we should iterate each key of the dictionary to match colors of the maze with corresponding points
					if np.array_equal(imag[m[0],m[1],:],np.array(self.clrDictionary[key][0])): #check if the colors match
						pointdic[tuple(m)] = self.clrDictionary[key][1] #if the colors match, put the corresponding point from the key to the center dictionary
			if whereami in initLocs:
				neighAr=findNeighbor(whereami,50)
				for i,j in enumerate(neighAr):
					if j in pointdic:
						goal = j
			else:
				#adjust loc to center point later
				#egemennnn aklın bı sey geldi xd
				#0ın altına düşmemeliyiz !!
				neighAr1=findNeighbor(whereami,100)
				for a,b in enumerate(neighAr1):
					sum=0
					if b in pointdic:
						sum=0
						neighAr2=findNeighbor(b,100)
						sum= sum + 1.5*pointdic[b]
						for k,t in enumerate(neighAr2):
							if t in pointdic:
								sum=sum+ pointdic[t]
						pickme.put((-sum,b))
			goal = pickme.get()[1]
			return goal

		goal = bestOption(loc,img)

		#heuristic function h(current_state,goal_state)
		def h(current,goal):
			y1,x1 = current
			y2,x2 = goal
			return abs(x1-x2) + abs(y1-y2) #manhattan distance

		#uniform cost function g(current_state,initial_state)
		def g():
			return 1 #the cost will be uniform throughout the white and black (i.e. (255,255,255) and (1,1,1)) pixels)

		def neighbors(current): #function that calculates the neighbors of current cell
			#take care of the unpassable pixels (that are, other than white and black pixels)
			def isColorful(current):
				if (img[current[0],current[1]]==self.clrDictionary['black'][0]).all() or (img[current[0],current[1]]==(255,255,255)).all() or (img[current[0],current[1]]==(0,0,0)).all(): #change aGame.maze to the image we are given, if the 
					return True
				return False #other colors will return false
			(x,y) = current
			neighArr = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] #calculate the 4-neighbors
			result = filter(isColorful,neighArr) #filter out the colorful neighbors, the path will not pass through them
			return result
		#main search function
		def aSearch(initial,goal):
			initial=tuple(initial)
			goal = tuple(goal)
			open = PriorityQueue() #construct the priority queue
			open.put(((h(initial,goal)+0),0,initial)) #put the initial state in the queue
			#print(open.queue)
			came_from = {} #initialize an empty dictionary to record the parent nodes. keys are children and values are parents
			g_cost_so_far = {} #another empty dictionary to store the g-costs
			came_from[initial] = None #initial state has no parents
			g_cost_so_far[initial] = 0 #we start with zero cost. 
			while not open.empty(): #iterate until there is nothing left in the queue. If it is empty, it means no solution can be found.
				current = open.get()[2] #get the least cost cell coordinates from the queue
				if current == goal: #if we reach the goal, no more need for iteration
					break
				for candid in neighbors(current): #go over the neighbors of the current cell
					new_cost = g_cost_so_far[current] + g() #the cost is updated according to the neighbor candidate
					if candid not in g_cost_so_far or new_cost < g_cost_so_far[candid]: #if the neighbor is not visited before or cost from the start to it
                                                                          #is less than the time it is visited before
						g_cost_so_far[candid] = new_cost #associate its g-cost with the calculated cost
						f = new_cost + h(candid, goal)   #find the f cost
						open.put((f,g_cost_so_far[candid],candid)) #add the elements to the open set
						came_from[candid] = current #add the current state to the path (closed list) as the parent of candid
			return came_from

		came_from = aSearch(loc,goal) #these are hard coded on purpose, change them to your initial and goal state
		def onMyWay(came_from,initial,goal): #return the path. make sure N <= 100 and the x y coordinates are in a suitable order (pixels or image array are notated by y,x
			current = tuple(goal)
			initial = tuple(initial)
			path = []
			while current != initial: # note: this will fail if no path found. loop until the initial state which has no parents
				path.append(current) #append the current state to the path
				current = came_from[current] #update the current state with the parent of the current state. 
    				#The loop will construct the path backward (child to parent, goal to initial)
 	 	#path.append(start) # do not add this because Buğra Hoca does not want the initial state in the path
			path.reverse() # convert the backward path to forward
			return path
		path = list(onMyWay(came_from,loc,goal))
		return path
