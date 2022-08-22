import numpy as np
from PIL import Image
from cv2 import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot")

SIZE = 5
EPISODES = 25000
MOVE_PENALTY = 10
HIT_PENALTY = 100
LOSE_PENALTY = 1000
KILL_REWARD = 75
FOOD_REWARD = 50
epsilon = .8
EPS_DECAY = .09998
SHOW_EVERY = 2500
ENEMY_COUNT = 2

start_q_table = None

MOVING_ENEMIES = False
LEARNING_RATE = 0.1
DISCOUNT = 0.95

PLAYER_N = 1
ITEM_N = 2
ENEMY_N = 3

d = {1: (255, 175, 0), #color of blobs in BGR
	 2: (0, 255, 0),
	 3: (0, 0, 255)}

kills = 0


class Blob:
	ID = False
	can_move = True

	def __init__(self):
		self.x = np.random.randint(0, SIZE)
		self.y = np.random.randint(0, SIZE)
	def __str__(self):
		return f"{self.x}, {self.y}"
		
	def __sub__(self, other):
		print(f'other = {other}')
		print(f'got self, type: {type(self)}, and other, type: {type(other)}\n')
		return(self.x-other.x, self.y-other.y)

	def action(self, choice):
		if choice == 0:
			self.move(x=1,y=1)
		elif choice == 1:
			self.move(x=-1,y=-1)
		elif choice == 2:
			self.move(x=-1,y=1)
		elif choice == 3:
			self.move(x=1,y=-1)
		elif choice == 4:
			self.move(x=0,y=1)
		elif choice == 5:
			self.move(x=0,y=-1)
		elif choice == 6:
			self.move(x=-1,y=0)
		elif choice == 7:
			self.move(x=1,y=0)
		elif choice == 8:
			self.fire()
		elif choice == 9:
			self.fire()


		#elif choice == 9:
		#	self.shield()

	def move(self, x=False, y=False):
		if self.can_move:
			if not x:
				self.x += np.random.randint(-1,2)
			else:
				self.x += x
	
				if not y:
					self.y += np.random.randint(-1,2)
				else:
					self.y += y
	
	
				#check if in area 
				if self.x < 0:
					self.x = 0
				elif self.x > SIZE-1:
					self.x = SIZE-1
	
	
				if self.y < 0:
					self.y = 0
				elif self.y > SIZE-1:
					self.y = SIZE-1


	def fire(self, enemy, dir=False):
		#0:N 1:E 2:S 3:W 
		if dir == 0:
			if enemy.x == self.x and self.y - enemy.y >= -3 and self.y - enemy.y < 0:
				shoot(enemy.ID)     
		elif dir == 2:		
			if enemy.x == self.x and self.y - enemy.y <= 3 and self.y - enemy.y > 0:
				shoot(enemy.ID)     
		elif dir == 1:
			if enemy.y == self.y and self.x - enemy.x >= -3 and self.x - enemy.x < 0:
				shoot(enemy.ID)     
		elif dir == 3:
			if enemy.y == self.y and self.x - enemy.x <= 3 and self.x - enemy.x > 0:
				shoot(enemy.ID)

	def kill():
		can_move = False
		self.x = SIZE+10
		self.y = SIZE+10
		kill+=1


def shoot(target_id):
	enemy[target_id].kill()

def pClosest(points, K):
	points.sort(key = lambda K: K[0]**2 + K[1]**2)
	ans = points[:K]
	return ans


def findClosest(player, enemy = []):
	distances = []
	for i in range(len(enemy)):
		distances.append(np.sqrt((enemy[i].x-player.x)**2 + (enemy[i].y-player.y)**2))
	return(get_min_index(distances))

def get_min_index(inputlist):
	min_value = min(inputlist)

	min_index=inputlist.index(min_value)
	return(min_index)

if start_q_table is None:
	q_table = {}
	for x1 in range(-SIZE+1, SIZE):
		for y1 in range(-SIZE+1, SIZE):
			for x2 in range(-SIZE+1, SIZE):
				for y2 in range(-SIZE+1, SIZE):
					q_table[((x1, y1), (x2, y2))] = [np.random.uniform(-5, 0) for i in range(4)]
else:
	with open(start_q_table, "rb") as f:
		q_table = pickle.load(f)


episode_rewards = []
for episode in range(EPISODES):
	player = Blob()
	reward = Blob()
	enemy = []

	for i in range(ENEMY_COUNT):
		enemy.append(Blob())
		enemy[i].ID = i
		print(enemy[i])


	print(f"enemy 1 - enemy 2{enemy[0]-enemy[1]}\nplayer - enemy 1 {player-enemy[0]}")

	if episode % SHOW_EVERY == 0:
		 print(f"on # {episode}, epsilon: {epsilon}")
		 print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
		 show = True
	else:
		 show = False

	episode_reward = 0
	for i in range(200): #runs each move, 200 moves per episode max
		obs = (player-reward, player-enemy[findClosest(player, enemy)])
		print(f"obs: {player-reward, player-enemy[findClosest(player, enemy)]}")
		if np.random.random() > epsilon:
			action = np.argmax(q_table[obs])
		else:
			action = np.random.randint(0,4)

		player.action(action)

		if player.x == enemy[0].x and player.y == enemy[0].y:
			reward = -HIT_PENALTY
		elif player.x == reward.x and player.y == reward.y:
			reward = FOOD_REWARD
		else:
			reward = -MOVE_PENALTY



