

import pygame
import random
import numpy as np
from time import sleep

class Cube(object):
	"""docstring for Cube"""
	def __init__(self, x, y, color):
		self.x=x
		self.y=y
		self.pos=(x,y)
		self.color=color

	def draw_cube(self, win, w ,r):
		t=w//r
		# print(self.color)
		pygame.draw.rect(win, self.color, (self.x*t+1,self.y*t+1,t-1,t-1))

	def draw_cube_head(self, win, w ,r):
		t=w//r
		pygame.draw.rect(win, self.color, (self.x*t+1,self.y*t+1,t-1,t-1))
		center=t//2
		rad=3
		cm=(self.x*t+center-rad,self.y*t+6)
		cm2=(self.x*t+t-rad*2,self.y*t+6)
		pygame.draw.circle(win, (0,0,0), cm, rad)
		pygame.draw.circle(win, (0,0,0), cm2, rad)



def random_snack(rows, snake, color):
	positons = snake.body
	# colors=[(255,0,0),(255,255,0),(0,255,0),(0,0,255),(0,255,255),(255,0,255)]
	colors=[tuple(np.random.choice(range(256), size=3)) for i in range(20)]
	while(1):
		x=random.randrange(rows)
		y=random.randrange(rows)

		if((len(list(filter(lambda z:z.pos==(x,y), positons)))) > 0):
			continue
		else:
			break
	c=3
	while(colors[c] == color):
		c=random.randrange(20)

	return Cube(x, y, colors[c])


class Snake(object):
	"""docstring for Snake"""
	def __init__(self, x , y, color):
		self.color=color
		self.head=Cube(x,y,color)
		self.val1= 1
		self.val2= 0
		self.length=1
		self.body=[]
		self.body.append(self.head)

	def draw(self, win, w, r):
		for i,c in enumerate(self.body):
			# print("hello")
			if(i==0):
				c.draw_cube_head(win,w,r)
			else:
				c.draw_cube(win,w,r)

	def move(self):
		keys = pygame.key.get_pressed()
		pygame.key.set_repeat(10,10)
		x=self.body[0].pos[0]+ self.val1
		y=self.body[0].pos[1]+ self.val2
		self.body.insert(0,Cube(x,y,self.color))
		self.body.pop()

		if(keys[pygame.K_LEFT]):
			self.val1=-1
			self.val2=0

		if(keys[pygame.K_RIGHT]):
			self.val1=1
			self.val2=0

		if(keys[pygame.K_UP]):
			self.val1=0
			self.val2=-1

		if(keys[pygame.K_DOWN]):
			self.val1=0
			self.val2=1

	def add_cube(self, khana):
		self.color=khana.color
		self.body.append(khana)


def check(snake):
	global width,rows
	head=snake.body[0].pos
	positons=snake.body[1:]
	if(head[0]<0 or head[0]>=rows-1 or head[1]<0 or head[1]>=rows-1):
		return True
	elif((len(list(filter(lambda z:z.pos==head, positons)))) > 0):
		return True

	return False


def reDrawWindow(win, snake, khana, level, player_name, f):
	global width,rows
	win.fill((0,0,0))
	#draw the grid
	t=width//rows
	x=0
	y=0
	for l in range(rows):
		x+=t
		y+=t
		pygame.draw.line(win, (255,255,255), (x,0) , (x,width))
		pygame.draw.line(win, (255,255,255), (0,y) , (width,y))

	khana.draw_cube(win, width, rows)
	snake.draw(win,width,rows)
	score=(len(snake.body)-1)*10
	level_label=f.render(f"Level: {level}",1,(255,255,0))
	score_label=f.render(f"Score: {score}",1 ,(255,255,0))
	p_label=f.render(f"Name: {player_name}",1 ,(0,255,0))
	win.blit(level_label,(10,(rows)*t+10))
	win.blit(p_label,((rows//2-3)*t,(rows)*t+10))
	win.blit(score_label,((rows-3)*t-10,(rows)*t+10))
	pygame.display.update()
	# sleep(0.3)

run=True
width=600
rows=20

print("---------------- Welcome to snake game ----------------")
player_name=input("Enter player name : ")
level=int(input("Enter level [ 1 - 10 ] : "))

win = pygame.display.set_mode((width,width+50))
pygame.display.set_caption("Snake Game")
pygame.init()
f=pygame.font.SysFont("comicsans",30)

while(run):
	clock = pygame.time.Clock()
	snake=Snake(0, 0, (255,255,0))
	khana=random_snack(rows, snake, snake.color)
	
	while(run):
		clock.tick(level+3)
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				run = False
				pygame.quit()

		

		if(snake.body[0].pos==khana.pos):
			snake.add_cube(khana)
			khana=random_snack(rows, snake, snake.color) 

		snake.move()
		reDrawWindow(win,snake,khana,level,player_name,f)


		if(check(snake)):
			run= False
			print(" [ Your Score is : ",(len(snake.body)-1)*10, " ]")
			print(" [ Game Over ]")
			pygame.quit()
