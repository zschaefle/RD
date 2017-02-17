import random
import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREY = (100,100,100)

pygame.init()
font = pygame.font.SysFont('Calibri', 15, True, False)
size = (995, 259)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
debug = True

def getImg(name):
	full = "Assets/img/"+name+".png"
	print "Loading: "+full
	try:
		return pygame.image.load(full)
	except pygame.error:
		print "--File not found. Substituting"
		return pygame.image.load("Assets/img/wip.png")
		
def prints(stuff):
	global debug
	if debug:
		print stuff
		
def rand(num):
	return random.randint(1, num)
#
class Player(object):
	def __init__(self):
		self.name = "player"
		self.hp = 100
		self.baseatk = 8
		self.atk = 8
		self.basedef = 0
		self.dfn = 0
		self.ddev = 10
		self.healval = 1
		self.maxhp = 100
		self.hdev = 3
		self.baseagil = [18, 100]
		self.agil = [15, 100]
		self.lvl = 1
		self.sane = 8
		self.trueSane = 0
		self.minions = []
		self.id = 0
		self.minionTree = []
		self.atkmod = 1
		self.defmod = 1
		self.agilmod = 1
		self.defending = False
pla = Player()

class Enemy(object):
	def __init__(self, atk, de, name, pic, maxhp, ddev, agil, sane, message, cry, lvl, rundown, heal, interval):
		self.hp = maxhp
		self.atk = atk
		self.dfn = de
		self.name = name
		self.img = getImg(pic)
		self.ddev = ddev
		self.maxhp = maxhp
		self.agil = agil
		self.message = message
		self.cry = cry
		self.turn = lvl
		self.heal = heal[2]
		self.rundown = rundown
		self.healchance = [heal[0], heal[1]]
		self.boss = False
		self.atkInt = interval
		self.atkIntBase = interval
		self.sane = sane
		self.minions = []
		self.minionTree = []
		self.atkmod = 1
		self.defmod = 1
		self.agilmod = 1
		self.defending = False

creepybaldguy = Enemy(5, 10, "Creepy Bald Guy", "creep", 18, 2, [1,100], -1, "You know you are being watched. Always... ", "you feel it staring through your eyes, Into your Soul.", 1, ["Even though it seems nearly dead, it continues its steady gaze deep into your eyes.", "it seems to have lost some hair in this fight. You blink, realizing it was already bald.", "it seems to be observing, only attacking to see how you react.", "it is sitting there, staring at you. Waiting and observing your every move."], [2,3,4], 200)

#items go here, not ready yet

class Boss(object):
	def __init__(self, hp, atk, de, name, img, maxhp, ddev, agil, heal, sane, loot, loot2, turn, message, cry, rundown, room, interval):
		self.hp = hp
		self.rehp = hp
		self.atk = atk
		self.dfn = de
		self.name = name
		self.img = getImg(img)
		self.ddev = ddev
		self.maxhp = maxhp
		self.agil = agil
		self.message = message
		self.cry = cry
		self.lvl = turn
		self.heal = heal[2]
		self.rundown = rundown
		self.healchance = [heal[0], heal[1]]
		self.boss = True
		self.atkInt = Math.ceil(interval)
		self.atkIntBase = Math.ceil(interval)
		self.turn = turn
		self.loot = loot
		self.loot2 = loot2
		self.sane = sane
		self.minions = []
		self.room = room
		self.minionTree = []
		self.atkmod = 1
		self.defmod = 1
		self.agilmod = 1
		self.defending = False

adventurer = Boss(190, 20, 0, "Adventurer", "adventurer", 190, 5, [5,100], [100,50,30], -7, herosword, heroshield, 10, "You hear the footsteps of someone else.", "It is an Adventurer, Readying his stance for Battle!", ["He seems oddly unaware of the massive amounts of damage you have dealt him. Much like you are.", "", "", "", "He seems more confident of himself, more sure of his strides.",""],bossroom,100);
bosses = [adventurer]


#minions go here, not needed yet


ablerooms = []
lootitems = []
finalsanity = 0
#based on player level, changes aspects of game such as tiers of items, and rooms.
def gentables():
	global lootitems
	global pla
	global ablerooms
	global allitems
	global finalsanity
	global rooms
	
	lootitems = []
	for i in allitems:
		item = allitems[i]
		if item.findable == 0:
			if (pla.lvl == 1 and (item.atk + item.def + (item.agil / 3) + (item.sane / 3)) <= 5):
				lootitems.append(item)
			if (pla.lvl == 2 and (item.atk + item.def + (item.agil / 2) + (item.sane / 2)) <= 10):
				lootitems.append(item)
			if (pla.lvl == 3 and (item.atk + item.def + item.agil + item.sane) <= 15):
				lootitems.append(item)
			if pla.lvl >= 4:
				lootitems.append(item)

	#Get ablerooms
	ablerooms = []
	for i in rooms:
		localrand = rooms[i]
		if (sanity < 2):
			if (localrand.sanity >= Math.floor(Math.cbrt(sanity) - pla.lvl) and localrand.sanity <= Math.floor(Math.cbrt(sanity) + (pla.lvl * 1.5))):
			ablerooms.append(rooms[i])
		else if (sanity >= 2):
			if (localrand.sanity <= Math.floor(Math.cbrt(sanity) + pla.lvl) and localrand.sanity >= Math.floor(Math.cbrt(sanity) - (pla.lvl * 1.5))):
			ablerooms.append(rooms[i])
	
	if (ablerooms.length == 0 and pla.trueSane == 0):
		prints("Ablerooms empty. Sanity: "+ sanity + " pla.sane: " + pla.sane)
		if (sanity < 0):
			ablerooms = [room19]
			finalsanity = -1
		if (sanity > 0):
			ablerooms = [room23]
			finalsanity = 1
	#when reached true sanities
	if pla.trueSane != 0:
		lootitems = []
		for i in allitems:
			if (i.sane <= 0 and pla.trueSane < 0):
				lootitems.append(i)
			if (i.sane >= 0 and pla.trueSane > 0):
				lootitems.append(i)
		for i in rooms:
			if (i.sanity <= 0 and pla.trueSane < 0):
				ablerooms.append(i)
			if (i.sanity >= 0 and pla.trueSane > 0):
				ablerooms.append(i)



equippeditems = [nothing, nothing]
runs = 1
turn = 0
room = ""
lootable = False
chestmessages = ["There is a small chest about the size of your fist lurking in the corner. ", "A golden chest sits with elegant details and pure beauty.", "There\'s a lumpy sack over there", "You hear the wheeze of a chest.  \"Open me\" it calls, with the music of its collapsing wood.", "In a rotting monster carcass, you glimpse something... interesting.", "There\'s a lump in the ground. Like a squirrel buried a tasty rock and then ran off and died.", "Something calls your attention. It sucks you in. You imagine riches.", "You smell something.  It smells like goods.", "You glimpse a confection of wood and nails, almost big enough to hold something.", "There is a small door that seems to have something sticking out, perhaps something useful."]
runmessages = ["Run", "Dodge", "Sprint", "Jump", "Duck", "Roll", "Slide", "Feint", "Fake", "Switch", "Distract", "Twist", "Lurch", "Insult", "Shout"]
#unlockmessages = ["You hear the sound of something unlocking from far away.", "You feel the dongeon blink, and you have a moment of deja vu.", "A feeling of release washes over you, the feeling of access.", "You feel something click, almost like a realization."]
score = 0
healable = True
noKillEpic = True
roommessage = ""
search = True

#The meat of the game, Generates the room randomly
def genRoom():
	global healable
	global score
	global pla
	global roommessage
	global turn
	global search
	
	prints("Generating room.")
	RDrefresh()
	gentables()
	turn += 1
	healable = True
	#leveling up
	if (score >= 30 and pla.lvl == 1):
		pla.lvl = 2
		roommessage += "You can sence something.. Change, or Alter, in the dongeons around you.."
	if (score >= 75 and pla.lvl == 2):
		pla.lvl = 3
		roommessage += "You hear the calls of things, Unknown Creatures, from close by.."
	if (score >= 220 and pla.lvl == 3):
		pla.lvl = 4
		roommessage += "You feel attention has shifted to you, knowing this is not a good thing."
	if (score >= 400 and pla.lvl == 4):
		pla.lvl = 5
		roommessage += "You can feel the Anger, the Hatred in the dongeon, Radiating from the surfaces, Aimed at you..."
	if (score >= 800 and pla.lvl == 5):
		pla.lvl = 6
		roommessage += "The hairs rise on the back of your neck. You have reached your top potential, and know it is only downhill from here."
	
	search = True
	if (turn == 1):
		search = False
		
	global bosses
	for i in bosses:
		if (i.turn == turn):
			search = False
			room = i.room
	if turn == 35:
		search = False

	if (search or turn == 1):
		 room = ablerooms[rand(ablerooms.length)-1]
	roommessage += room.message
	
	
	avent = random.randint(1, 30)
	
	if (avent == 1):
		roommessage += " Your feet are suddenly covered in water, with more rising from an unseen source."
		room.water = 1
	if (avent == 2):
		roommessage += " Vines lazily wind their way towards you."
		room.plant = 1
	if (avent == 3):
		roommessage += " You feel a gust of wind from the south."
		room.south = 1
	if (avent == 4):
		roommessage += " The very air around you seems to emit a warm glow."
		room.dark, room.light = 0, 1
	if (avent == 5):
		roommessage += " The air muffles and dilutes not sound, but light."
		room.dark, room.light = 1, 0
	if (avent == 6):
		roommessage += " You can hear the clicking and whirring  of unseen machinery."
		room.manmade = 1
	if (avent == 7):
		roommessage += " A large crowd of flies is hovering in a corner, seemingly growling at you."
		room.animal = 1
	if (avent == 8):
		roommessage += " You become lost in a cloud of dark light."
		room.dark, room.light = 1, 1
	if (avent == 9):
		roommessage += " There seems to be a lot of gold here. You must resist the urge to loot it all."
		room.items = 1
	if (avent == 10):
		roommessage += " Everything around you seems smoother, or Curvier"
		room.manmade = 1
	if (avent == 11):
		roommessage += " You have a moment of dizziness, a thought of doubt."
		pla.sane -= 1
	if (avent == 12):
		roommessage += " You hear whispering. You turn quickly, but nothing is there."
		pla.sane -= 3
	if (avent == 13):
		roommessage += " You feel a tap on your shoulder, and turn around to find that there is nothing there."
		pla.sane -= 5
	if (avent == 14):
		roommessage += " No matter to the circumstances, you are tired. You take a moment to rest."
		pla.sane += 5
	if (avent == 15):
		roommessage += " You feel a sense of refreshment, of redefining who you are."
		pla.sane += 3
	if (avent == 16):
		roommessage += " You blink. Something seems off."
		localrand = room.north
		room.north = room.east
		room.east = room.south
		room.south = room.west
		room.west = localrand
	'''if (avent == 17):
		room = specroom1
		roommessage = room.message
		search = False
		room.items = 0
	}
	if (avent == 18){
		room = specroom2;
		roommessage = room.message;
		search = False;
		room.items = 0;
	}'''
	pla.sane += room.sanity
	pla.sane += (equippeditems[0].sane)/5
	pla.sane += (equippeditems[1].sane)/5
	for i in pla.minions:
		pla.sane += (pla.minions[i].sane / 5)
	
	
	#Determining lootable
	if (rand(2) == 1 and room.items == 1):
		lootable = True
		roommessage += chestmessages[rand(chestmessages.length-1)]
	else:
		lootable = False

	ableminions = []
	for i in minions:
		if (i.lvl <= pla.lvl):
			ableminions.append(i)
	
	if (rand(8) == 1 and ableminions.length > 0):
		minion = ableminions[rand(ableminions.length)-1]
		roommessage += minion.message
		getMinion(pla, minion)

	for i in bosses:
		if (i.turn == turn):
			roommessage += prepbattle(i)
			
	'''if (room == room38):
		roommessage += prepbattle(terracotta)
		search = False'''

	
	if search:
		if (noKillEpic and turn == 35):
			if (pla.atk >= pla.dfn and pla.atk >= pla.agil[0]):
				roommessage = epicalpha.room
				roommessage += prepbattle(epicalpha)
			elif (pla.dfn >= pla.atk and pla.dfn >= pla.agil[0]):
				roommessage = epiccoo.room
				roommessage += prepbattle(epiccoo)
			elif (pla.agil[0] >= pla.atk and pla.agil[0] >= pla.dfn):
				roommessage = epicjim.room
				roommessage += prepbattle(epicjim)
			else:
				if (pla.sane <= 0):
					finalsanity = -1
				if (pla.sane > 0):
					finalsanity = 1
		
		if (finalsanity == 1 and turn > 20 and pla.TrueSane == 0):
			roommessage += prepbattle(lastinsanity)
			finalsanity = 0
		
		if (finalsanity == -1 and turn > 20 and pla.TrueSane == 0):
			roommessage += prepbattle(lastsanity)
			finalsanity = 0
		
		
		if (pla.lvl >= 5 and search):
			enemyspawn = rand(5)
			if (enemyspawn == 3):
				roommessage += prepbattle(creep4)
		
		if (pla.lvl >= 4 and search):
			enemyspawn = rand(5)
			if (enemyspawn == 1 and room.plant == 0 and room.animal == 0):
				roommessage += prepbattle(rockgolum)
			if (enemyspawn == 2 and room.water == 1):
				roommessage += prepbattle(koi)
			if (enemyspawn == 3):
				roommessage += prepbattle(creep3)
				
		if (pla.lvl >= 3 and search):
			enemyspawn = rand(5)
			if (enemyspawn == 4 and room.plant == 1 and room.animal == 1):
				roommessage += prepbattle(dog)
			if (enemyspawn == 5):
				roommessage += prepbattle(slime)
			if (enemyspawn <= 2 and room.water == 0 and room.dark == 1 and room.animal == 1 and room.light == 0):
				roommessage += prepbattle(catwatcher)
			if (enemyspawn == 3 and room.animal == 1 and room.light == 1):
				roommessage += prepbattle(nerveball)
		
		if (pla.lvl >= 2 and search):
			enemyspawn = rand(5)
			if (enemyspawn == 1 and room.manmade == 1 and room.water == 0):
				roommessage += prepbattle(bookofdeath)
			if (enemyspawn == 2 and room.manmade == 1):
				roommessage += prepbattle(clone)
			if (enemyspawn == 3 and room.light == 1):
				roommessage += prepbattle(lightorb)
			if (enemyspawn == 4 and room.items == 0):
				roommessage += prepbattle(mimic)
				lootable = True
			if (enemyspawn == 5):
				roommessage += prepbattle(creep2)
			
		if (pla.lvl >= 1 and search):
			enemyspawn = rand(6)
			if (enemyspawn == 1 and room.water == 1 and room.animal == 1):
				roommessage += prepbattle(anenemy)
			if (enemyspawn == 2 and room.plant == 1 and room.water == 0):
				roommessage += prepbattle(axeurlegs)
			if (enemyspawn == 3):
				roommessage += prepbattle(muffin)
			if (enemyspawn >= 5):
				roommessage += prepbattle(creepybaldguy)
	return roommessage







print genRoom()
raw_input(":")



