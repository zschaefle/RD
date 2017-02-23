import random
import pygame
from pygame.locals import *
import math

#look for:   #VISUALS   to find where HTML visuals were removed

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
Cbacking = (170,170,170)

pygame.init()
size = (995, 259)
font = pygame.font.SysFont('couriernew', 13)
fontComp = pygame.font.SysFont('couriernew', 16, True)
smallfont = pygame.font.SysFont('couriernew', 12)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
debug = True

#two sets of coord pairs
def hitDetect(p1, p2, p3, p4 = None):
	if p4 == None:
		p4 = p3
	if p2[0] > p3[0] and p1[0] < p4[0] and p2[1] > p3[1] and p1[1] < p4[1]:
		return True

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

def cbrt(num):
	return num ** (1.0/3.0)
	

class DispObj(object):
	def refresh(self):
		if not self.simple:
			final = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
			for i in self.img:
				final.blit(i.img, i.coords)
			self.img = final
	#coords, img is blitable object or list of DispObj. simple is wether or not is list. size is needed if not simple.
	def __init__(self, img, coords = (0, 0), simple = True, size = (0, 0)):
		self.coords = coords
		self.img = img
		self.simple = simple
		self.refresh()
	
#takes single string, max width, font used, and color of text. returns list of dispObj
def wraptext(text, fullline, Font, render = False, color = (0,0,17)):  #need way to force indent in string
	Denting = True
	max = fullline
	size = Font.size(text)
	outtext = []
	while Denting:
		if Font.size(text)[0] > max:
			#Search for ammount of charachters that can fit in set fullline size
			thistext = ""
			for i in range(len(text)):
				if Font.size(thistext + text[i])[0] > max:
					count = len(thistext)
					break
				else:
					thistext += text[i]
			thistext = text[:count]
			#is it indentable
			if " " in thistext:
				for i in range(len(thistext)):
					#find first space from end
					if thistext[len(thistext)-(i+1)] == " ":
						#split text, add indent, update count
						outtext.append(thistext[:len(thistext)-(i+1)])
						text = text[len(thistext)-(i):]
						max = fullline
						break
			#unindentable, skip to next
			else:
				max += fullline
		else:
			#exit denting, add remaining to outtext, return
			Denting = False
			outtext.append(text)
			
	if render:
		text = []
		for i in range(len(outtext)):
			rand = outtext[i]
			text.append(DispObj(Font.render(rand, True, color),  (0, (i*size[1]))))
		outtext = text
	return outtext
	
#DispObj([
#DispObj()
#], ())



class ItemDisp(object):
	def refresh(self):
		global smallfont
		global font
		self.norm = DispObj([DispObj(self.mini, (2, 2)), DispObj(font.render(self.item.Name, True, (0, 0, 0)), (54, 2)), DispObj(wraptext(self.item.desc, 311, smallfont, True), (54, 2))])
		
	def __init__(self, item):
		self.id = item.Name
		self.item = item
		#different displays
		self.mini = pygame.transform.scale(item.img, (50, 50)) #just the item, resized
		self.norm =  self.mini #for use in inven, with name + desc
		self.press = self.mini #for inven, when clicked on.
		self.side = self.mini #for inven, large display
		self.refresh()
#pygame.transform.scale()

#all text objects initialized
TM1 = DispObj(wraptext("", 900, font, True), (10, 10), False, (900, 120)) #main room desc
TM2 = DispObj(wraptext("", 900, font, True), (10, 130), False, (900, 119)) #room responses
#TB1
#TB2
#TB3
TI1 = None

		
#Rooms for the dongeon
rooms = []
class Room():
	def __init__(self, plant, manmade, water, dark, animal, light, items, north, east, south, west, sane, message, exitA, exitB, exitFail, normal = True):
		self.plant = plant
		self.manmade = manmade
		self.water = water
		self.dark = dark
		self.animal = animal
		self.light = light
		self.items = items
		self.north = north
		self.east = east
		self.south = south
		self.west = west
		self.message = message
		self.exitA = exitA
		self.exitB = exitB
		self.exitFail = exitFail
		self.sanity = sane
		if normal:
			global rooms
			rooms.append(self)
		
		if (self.exitA == "" or self.exitA == " " or self.exitB == "" or self.exitB == " "):
			self.exitA = "You go "
			self.exitB = "."

room1 = Room(0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, -4 ,"Your eyes burn as you look into the lit black.  Green lines stretch to a vanishing point, showing you a door, a wall and a cliff.  Your eyesight blurs, reduced to craggy blocks.", "Your legs jitter as you walk on thin green lines, forming an exit to what you believe to be ", ".", "You feel like taking any extra steps in may be fatal.")
room2 = Room(1, 0, 0, 1, 1, 1, 1, rand(2)-1, 1, 2, rand(2)-1, 1, "This room is overrun by nature. There are twisted, moist vines covering the walls and most likely any exits.", "You carefully make your way to the ", ", occasionally tripping.", "You trip on your way over to the wall, only finding no exit.")
room3 = Room(0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, "You\'re in a linoleum cube, bare and featureless.   A circular opening appears behind you, and an open pit is just ahead.   A featureless voice speaks to you through static speakers.   You can\'t understand a single word.", "As you walk toward the ", ", the circular door smoothly opens in the wall ahead of you.", "The voice seems to be insulting you as you stumble about, slightly confused.")
room4 = Room(1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, "You find yourself in a lonely forest.  The snow on the ground mists in the sun, slowly turning into slush.  You take a moment to mourn the death of winter. Global warming man.  That\'s what it does.", "There's a small door in one of the trees to the ", ". You pull it open and and fall through.", "")
room5 = Room(0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, -2, "You stand on clouds, up to your ankles in condensation.  You see birds flying nearby.  You could swear that you see a large animal lurching its way towards you on lopsided legs.", " ", " ", " ")
room6 = Room(0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, -1, "You are in a room, a large centrepiece of machinery whirring to life, bursts of energy coming from within. There are voices yelling urgently at you from a viewport in the wall above.", "You manage to dodge the now falling rubble and make it through the ", "ern sliding doors.", "A zap of lightning from the core of the room leaps through the viewport, and you hear a scream of pain.")
room7 = Room(0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, "The walls cave inwards, rough rock with red striped sedimentary motif. The floor is loose packed sand, soft against your feet.  You look ahead, where the walls become lower and the ground gets rough.  You\'ll need to crawl.", "You crawl to the ", " exit, scraping your elbow.", "You realize that this is not an Indiana Jones movie, and that this wall will not open with enough force.")
room8 = Room(0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 4, "You see a single shelf, packed full of books, reaching upwards like a ladder into the darkness. ", "You grip the ", "ern shelves, pulling yourself up past musty tomes.", "You become distracted by the books, taking a moment to flip through one.")
room9 = Room(0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, -1, "There are huge wooden beams stretching across an empty cavern.  Coals smoulder in campfires across the expanse, lighting the room with grey dusk.  Rotting homes half-formed out of clay fill the room with a musty stench.", "You walk past small encampments and crusty artefacts to a hole in the ", "ern wall.", "You glance into one of the rooms. You spot a skeleton and an old vase. No exits here.")
room10 = Room(0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, -1, "The sun shines in your eyes.  You feel water underneath you.  Shielding your eyes from the glare, you see the boat you\'re standing on, a small and splintery craft.  The way it bobs under your weight alarms you.  A curl of rope under your feet obscures the bottom of the boat.", "you take hold of the paddles, paddling the boat to the ", ".", "Paddle as you may, the swirling currents quickly rush  you back into place.")
room11 = Room(0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, "You are on a cold, stormy beach. Litter is strewn across the sand, and a man with a prosthetic arm is purposefully cleaning it up, glancing around as if expecting someone, or some<i>thing</i>.", "As you meander your way to the ", ", the man shouts at you angrily, something about litter.", "You wade about in the ocean, unsure as to whether you are looking for something, or mourning.")
room12 = Room(0, 1, 0, 0, 1, 1, 1, rand(2)-1, rand(2)-1, 0, 1, rand(2), "You are in a room, full of red books with no titles, no markings at all. They fill the room, but you can hear a sort of carnal snore from somewhere in the room. You decide that would be best to keep away from whatever is producing the noise.", "You manage to sneak your way through to the ", ", cringing at the occasional shifting book.", "You wander throughout the room, surprisingly small for the quantity of books it holds.")
room13 = Room(rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, 1, 1, 1, 1, -7, "You find yourself in a room filled with bright darkness. Things seem to appear and disappear as if they were both there, and not there. You feel very dull all of a sudden, as if you have realized the futility of life.", "You walk slowly to what you think is a door, tripping over invisible things along the way to the ", ".", "You feel it would be best to leave as soon as possible.")
room14 = Room(1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, -3, "You find yourself in what at first appears to be a dog park, but upon closer inspection of the large black walls surrounding the area as well as the absence of any dogs and the presence of many hooded figures, you realize that this is not a dog park. Not a dog park at all.","After searching the "," side of the dog park, you don't find an exit, yet.....","The hooded figures are staring, and coming closer.....")
room15 = Room(0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, -1, "You stand before the barrier,your quest finally over, you are filled with DETERMINATION. That is until you realize that this was not the end off your quest and you must continue. Go on.","You walk through the "," side of the barrier","You bump into the barrier, and you realize that it lives up to it's name")
room16 = Room(0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, -3, "You find yourself in a room full of mirrors. Seeing yourself repeated thousands of times causes you to realize the monster you have become. How many creatures have you killed since you came here? You realize that you are a murderer.","You step into the "," mirror.","You bump into yourself.")
room17 = Room(1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 5, "You are momentarily blinded, when the light fades you look around. You seem to be in a tranquil cavern. There is a pond in the center, where lights dance peacefully on it's surface. You sit to rest for a time.", "You get up, though you wish to stay, but a hole to the ", " beckons you. You wave goodbye to the lights, they dance a farewell.", "A cavern wall seems to be where you are thinking of going, so you stay where you are..")
room18 = Room(1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 3, "You find yourself standing in a river, with a waterfall nearby. You take some time to rest in the lush greenery that surrounds you. You feel at peace.","You explore the forest to the ", ".","You walk straight into the waterfall.")
room19 = Room(rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, 1, rand(2)-1, rand(2)-1, -10, "you Are forced to ponDer your doings, finding that you aRe in fact <i>perfectly</i> sane. buT that is what they all say\;", "northnorthwesteastsouth", "westeastnorthsouth", "eastnorthwestsouthsoutheastsouthnorthupwest")
room20 = Room(0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, -2,"You find yourself in the very confined space that is the interior of an elevator. There is a corpse on the floor here, foaming at the mouth. A camera in one of the corners is watching you. A sound like fingernails on a chalkboard echoes throughout the room", "You leave through the elevator door on the ", " side.", "You bump into the wall.")
room21 = Room(0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, -6, "You step somewhere, you can't tell where, because there is literally nothing.", "You will yourself out, towards the... ", ", yeah, the east, that's right, you always wanted to go south.", "The nothingness seems to extend to that direction, and moving that way is fruitless.")
room22 = Room(0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, -5, "You step somewhere, you can't tell where, because there is literally nothing except a overwhelmingly bright light.", "You will yourself out, towards the...", ", yeah, the west, that's right, you always wanted to go south.", "The nothingness seems to extend to that direction, and moving that way is fruitless.")
room23 = Room(1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 10, "You step into a wondrous room filled with peaceful plants and animals. Waterfalls and large lush trees fill the landscape. It seems as if you have found a utopia.", "You must use all of your willpower to leave this peaceful utopia to the ",".", "You find yourself sliping deeper into this peace.")
room24 = Room(0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, -8, "As soon as you enter this room, you know you should not have. Various instruments of torture are strewn about the room. The room is filled with the wailing of the not yet dead corpses and the torture machines at work. The smell is indescribable.", "You quickly leave to the ",".", "You find yourself lost among the horrors of this room." )
room25 = Room(0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, -7, "It is dark. Creepily dark. You can hear a faint whispering.", "You somehow find the light in the ", ".", "The whispering is getting louder.")
room26 = Room(0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 5, "You are in your bedroom. It is clean and tidy in here. there is a doorway that leads to the main room.", "You walk to the ", ", out of your bedroom and into the main room.", "You decide against the act of heading that direction, maybe later.")
room27 = Room(0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, -2, "You are in your bedroom. It is messy and looks slightly looted. there is a doorway that leads to the main room.", "You walk to the ", ", out of your bedroom and into the main room.", "You decide against the act of heading north, maybe later.")
room28 = Room(1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 2, "You are in a peaceful courtyard with a bird fountain in the center, surrounded by walls and a tower made of quartz and marble.", "You walk to the ", ", through an intricately carved doorway.", "There is a wall here, you decide it would be too much trouble to climb it.")
room29 = Room(0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, "Your feet burn as you stand in the hot sand. You survey the endless expanse of desert around you, and realize that the in the years you have spent trekking through this wasteland have been useless.", "You continue your fruitless trek to the ", ".", "You become quite dizzy, probably an effect of dehydration.")
room30 = Room(0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, "You stand on top of a factory, the clanging of machinery behind you. Smoke pollutes the sky and obscures the sun. The occasional sizzle of laser cutters quietly supports the clanging.", "You walk through the factory, carefully avoiding the dangerous machines. You exit to the ", ".", "You breath in some of the smoke. It burns in the back of your throat, making it hard to breath.")
room31 = Room(0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, -2, "You are in a large warehouse, through the grimy windows you can see it is dusk. The occasional object is stored here, but everything is covered in spiderwebs.", "You open a large door in the ", "ern wall, someone helping from the other side.", "As you move, the strands of web begin catching.")
room32 = Room(1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, -9, "Everything is blurry. You blink and try to focus, realizing the world around you is out of focus, not your eyes.", "You squint on your way ", ", if but only to reduce visual exposure.", "You chuckle to yourself, thinking about how this place needs glasses.")
room33 = Room(0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, "You feel a knotting feeling in your gut, and lose sense of location. Glancing up, you find yourself in a room with other people, you try to get their attention, but they don't look up from their computers. At a loss, you sit down at a terminal, and begin browsing for anything to help you (and some cat pictures along the way).", "As you look through the files on your screen, you see one simply titled '", ".exe', clicking it, you feel the same knot, and the scenery changes.", "You can't leave. Goddamnit Zakiah")
room34 = Room(0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, -5, "You feel the walls watching you. You look closer, seeing that these are no ordinary walls, not walls at all, but millions of creepy bald guys.", "You sprint in a ", "ernly direction, Eager to escape their watching eyes.", "You hear your blood rushing, Everything going out of focus, knowing they are all watching only making it worse.")
room35 = Room(1, 0, rand(2)-1, rand(2)-1, 1, 0, 1, 0, 0, 0, 1, 2, "You stumble on a root that wasn't there a second ago, and glance around. You are now in a grove of many trees. Every one of the trees is thin, tall, and either willow or cottonwood. It is rather peaceful, and you take a moment to rest your weary legs", "You trek off to the ", ", knowing that it is the right thing to do.", "Valiently, you make an effort to leave. Though after some time walking, you find yourself back in the grove.")#room35.light = (room35.dark - 1) * (room35.dark - 1)
room36 = Room(1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 6, "You stand on a hill, on a path surrounded by flowers of many different colors. You decide to search for a specific flower, yet not knowing what it looks like.", "Turning ", ", you know your search has come to an end as you spot a fower adorned terrace.", "You stop and smell the flowers.")
room37 = Room(1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, -7, "yesssssssssssssss", "You exit through the ", ", stumbling over vines.", " \"I don't know...\" you mutter to yourself")
room38 = Room(0, 1, 0, 1, 0, 1, rand(1), 0, 1, 0, 1, 6, "You are in a large overhang, light from outside illuminating a massive array of small, intricately detailed clay soldiers.", "You clamber towards the ", "ern light, holding your hands above your eyes to block the light", "You stumble over the remains of the small clay soldiers, cracking them even further.")
room39 = Room(0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 3, "You are in a room, quite bland. You feel like it is a blank canvas, and you can do anything with it.", "You stroll to the ", ".", "Looks like you cannot, in fact, do anything with this room.")

bossroom = Room(0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, -2, "You find yourself in a wide open room. The ceiling is high and dark. An ominous feeling of doom hangs over you.", "Exhausted, you leave through the ", " door.", "You somehow walk into a nonexistent wall.", False)
roomBoss2 = Room(0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, -2, "You are in a small stone cavern, many twisting passageways leading through a winding cave system. You feel a drop of water plop on your head.", "You climb out through a ", "ern cave.", "You climb through a tunnel, only to find yourself in a room similar to the one you came from.", False)
roomBoss3 = Room(1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, "Suddenly you are in a forest. A crossroads leading in all directions, yet you feel leaving will not be that easy. Searching for why you feel that way, you notice a few houses around you, well made, and decide to lean on one to rest for a moment. Part of it chips off. You glance around hurriedly, hoping no one saw what you did. The house probably wasn't as sturdy as you expected.", "Free to leave now, you choose to go to the ", ", hoping it will lead to better fortunes and maybe even happiness.", "You somehow can't leave even with exits everywhere. You blame Zakiah.", False)
roomBoss4 = Room(0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 3, "You find yourself in a room, walls covered in mechanical and mystical constructs alike. Trees are visible through the sparsely placed windows.", "You find a button hidden on the ", "ern wall, pressing it against your better judgement.", "You become distracted by the intricacies of this room.", False)
#plant, manmade, water, dark, animal, light, items, north, east, south, west, sane, message, exitA, exitB, exitFail, normal = True

'''class item(object): #bland old items.
	def __init__(self, offence, defence, agility, sanity, score, name, divname, desc):
		self.atk = offence
		self.dfn = defence
		self.agil = agility
		self.score = score
		self.sane = sanity
		self.Name = name
		self.div = getImg("items/"+divname)
		self.desc = desc
		self.quant = 0
		self.findable = 0

hatandboots = item(5, 50, 8, 0, 10, "Hat and Boots", "hatandboots", "Can't Bump your head anymore, and probably won't stub your toes.")
zaroltrophy = item(0, 0, 0, 20, 50, "Zarol Trophy", "zaroltrophy", "Thinking back, Seriously. How the hell did you do that?")
fishingrod = item(5, 4, 2, 0, 10, "Fishing Rod", "fishingrod", "Hook, Line, and Sink.")
drawingpad = item(1, 3, 7, 12, 10, "Drawing Pad", "drawingpad", "Using this, you can stay positive. Because everything else is in here.")
pencil = item(7, 2, -1, -5, 10, "The Pencil", "pencil", "Quite oversized, you use it as a blunt weapon. But you feel there is more to it.")
jimsword = item(25, 5, -5, 0, 10, "Jim's Sword", "jimsword", "")
jimarmor = item(0, 35, -20, 0, 10, "Enchanted Armor", "jimarmor", "Glimmering metallic armor, Material flowing smoothly within it to fill the gaps in its structure.")
inactivecube = item(25, 7, 20, 0, 10, "Inactive Cube", "inactivecube", "")
card = item(2, 25, 25, 0, 20, "00000111", "card", "")
device = item(40, 0, 6, 0, 20, "Electrical device", "device", "You have no idea how it works, but it looks far beyond any tech you have seen.")
	'''
#New items, with the better system
#single chunk of armor calculation
class dfnChunk(object):
	def __init__(self, agil, protection = True, passive = False, durable = False, piercable = True, enchs = {}):
		#added to agil when active
		self.agil = agil
		#protection - True tanks all incoming damage into durability damage, number is max damage tanked
		self.dfn = protection
		#Passive - True always applies, False only applies when defending
		self.all = passive
		#durable - True doesn't effect durability, False does
		self.dur = durable
		self.piercable = piercable
		#list of Enchantments, all dealt with seperately.
		#Reflecting: multiplier of damage sent back to attacker; Thorns: False, or atkChunk
		#Destructive: direct durability damage to attacking weapon; Layered: value1 is chance for damage to be put through again, to max of value 2
		self.ench = {"reflecting":0, "thorns":False, "destructive":0, "trueProtection":False, "layered":[0, 0]}
		self.ench.update(enchs)

#single chunk of damage calculation. when putting into list, be sure to put in order: [projectile chunks, melee chunk, eternal chunks]. any other order will make some unused by attack()
class atkChunk(object):
	def __init__(self, dmg, agil, defend = True, eternal = False, piercing = 0, proj = False, enchs = {}):
		self.dmg = dmg
		#added to agil when damaging w/ chunk
		self.agil = agil
		#whether or not this chunk cancels defend
		self.dfn = defend
		#if these stats are added to attack chunk even if not used (needs to be equiped)
		self.etrn = eternal
		#projectiles. False, or the ammount of ammo required to use this chunk
		self.proj = proj
		#list of Enchantments, all dealt with seperately
		self.ench = {"destructive":0, "piercing":0, "heavy":0, "sweeping":0, "returning":[0, 0]}
		self.ench.update(enchs)
		#piercing level. 0 counts all armor chunks, 1 doesn't count piercable chunks, 2 skips all chunks (aside from special enchants). 3 skips everything.
		self.pierce = piercing + self.ench["piercing"]
		
allitems = []
class Item(object):
	#old: 				offence, defence, agility, sanity, score, name, divname, desc
	def __init__(self, offence, defence, durability, sanity, score, name, desc, img, lvl, destructable = True, ammo = False, regenammo = [], enchs = {}):
		self.atkChunks = offence
		self.dfnChunks = defence
		self.durability = durability
		self.broken = False
		self.maxdur = durability
		self.sane = sanity
		self.score = score
		self.Name = name
		self.desc = desc
		self.img = getImg("items/"+img)
		self.destructable = destructable #if true, this item is removed when durability reaches 0.
		self.ammo = ammo
		self.maxammo = ammo
		self.regenammo = regenammo
		#Regen: ticks before regen, ammount regenerated; Bound is times the item will NOT be destroyed by thing that remove all items. ie: Zarol, Monoliths
		self.ench = {"mending":[-1, 0], "bound":0}
		self.ench.update(enchs)
		self.mendTick = -1
		if self.ench["mending"][0] != -1:
			self.mendTick = 0
		self.lvl = lvl
		if self.lvl == -1:
			self.findable = 0
		else:
			self.findable = 1
		self.divname = ItemDisp(self)
		
		global allitems
		allitems.append(self)


nothing = Item([], [], 1, 0, 0, "", "", "no_thing", False)
allitems.remove(nothing)
acorncap = Item([], [dfnChunk(1, 1, True)], 15, 4, 9, "Acorn Cap", "If you were really tiny, like, smaller than a squirrel, this would be the perfect armor. You place it over your heart  You call it a kiss", "acorncap", 1)
boardgame = Item([], [dfnChunk(0, 1, True), dfnChunk(-1, 1)], 32, 2, 2, "Board Game", "The cardboard is battered  from years of wear, but you can see the winding  path your piece would take if you were a winner.   You're not a winner.", "boardgame", 1)
bobbypin = Item([atkChunk(1, 1)], [], 35, 1, 1, "Bobby Pin", "Ow... it's sharp.", "bobbypin", 1)
safetypin = Item([atkChunk(3, 4)], [], 40, 1, 1, "Safety pin", "Not actually very safe at all.<br/>Actually quite dangerous.", "safetypin", 1)
woodstick = Item([atkChunk(1, 0)], [dfnChunk(-1, 2)], 10, 3, 1, "Wooden Stick", "It might not be the best sword, but hey, it's worth a try.", "woodstick", 1)


#--BOSS ITEMS--
heroshield = Item([], [dfnChunk(-5, 6, False, False, False), dfnChunk(-2, 4, True)], 200, 1, 10, "Heroes Shield", "You feel a bit bad, killing someone with origins probably alike yours.", "heroshield", -1, False)
herosword = Item([atkChunk(6, 2)], [dfnChunk(0, 2, False, True)], 100, 1, 10, "Heroes Sword", "A fitting weapon for a hero. But are <i>you<i> a hero?", "herosword", -1, False)
#ALPHA
alphaxe = Item([atkChunk(20, -2, True, False, 0, False, {"sweeping":2, "heavy":1})], [dfnChunk(-2, -2, True, True), dfnChunk(-10, 12)], 400, 0, 10, "Alpha's Axe", "A large heavy axe, with surprisingly powerful hits.", "alphaxe", -1, False)
sivgoggles = Item([atkChunk(4, 15, False, True, 1, False, {"sweeping":1})], [dfnChunk(10, 2, True), dfnChunk(25, 2, False, True, True, {"trueProtection":True})], 30, -15, 10, "Alpha's Glasses", "Gazing through them, You can see things. Where they are, and where they are going.", "sivgoggles", -1, False, False, [], {"bound":4, "mending":[3, 1]})
hair = Item([atkChunk(1, 1, False, True, 0, False, {"destructive":30})], [], 10, -100, 10, "Alpha's Hair", "You stole this from a boss. Well, stole isn't the right word. More of Generated through Desire.", "hair", -1, False, False, [], {"bound":10})
shurikenbag = Item([atkChunk(35, 25, False, False, 1, 5, {"sweeping":5}), atkChunk(15, 20, True, False, 0, 1, {"returning":[2, 80], "destructive":10})], [dfnChunk(5, 4, True)], 100, -35, 10, "Shuriken Pouch", "A small, blood filled pouch, when you reach your hand into it, you always pull out a shuriken.", "shurikenbag", -1, False, 10, [1, 1], {"bound":1, "mending":[5, 2]})
#COOSOME
spoon = Item([atkChunk(50, 7, False, False, 2, 30), atkChunk(35, 6, False, False, 1, 1, {"returning":[2, 100]}), atkChunk(15, 3, True, True)], [dfnChunk(1, 1)], 100, -8, 10, "the Spoon", "It's just a spoon. But something feels powerful about it...", "spoon", -1, False, 30, [10, 1], {"mending":[500, 1], "bound":2})
lapis = Item([atkChunk(5000, 5000, False, False, 3, False, {"sweeping":1000})], [dfnChunk(0, True, False, True, False, {"trueProtection":True, "thorns":atkChunk(5000, 5000, False, False, 3)})], 1000, 0, 0, "Lapis", "The gem of the gods. Or at least the god of 7.", "lapis", -1, False, False, [], {"bound":100, "mending":[50, 1000]})


invenItems = []
score = 0
turn = 0
class Player(object):
	def __init__(self):
		self.name = "player"
		self.hp = 100
		self.dmg = 8
		self.atk = []
		self.basedef = 0
		self.dfn = 0
		self.passdfn = []
		self.ddev = 10
		self.healval = 1
		self.maxhp = 100
		self.hdev = 3
		self.baseagil = [18, 100]
		self.agil = [15, 100]
		self.lvl = 1
		self.sane = 8
		self.sanity = 8
		self.trueSane = 0
		self.minions = []
		self.id = 0
		self.minionTree = []
		self.atkmod = 1
		self.defmod = 1
		self.agilmod = 1
		self.defending = False
		self.equipped = [nothing]
	
	def refresh(self):
		#set self.sanity
		#set two attack chunks
		#for i in 
		global TI1
		TI1 = DispObj([DispObj(smallfont.render("Health: "+str(self.hp), True, (0, 0, 0))), DispObj(smallfont.render("Base Dmg: "+str(self.dmg), True, (0, 0, 0)), (0, 17)), DispObj(smallfont.render("Base Dfn: "+str(self.dfn), True, (0, 0, 0)), (0, 34)), DispObj(smallfont.render("Score: "+str(score), True, (0, 0, 0)), (0, 51)), DispObj(smallfont.render("Level: "+str(self.lvl), True, (0, 0, 0)), (0, 68)), DispObj(smallfont.render("Room: "+str(turn), True, (0, 0, 0)), (0, 85))], (10, 126), False, (195, 120)) #inventory stats
		
pla = Player()
pla.refresh()

class Enemy(object):
	def __init__(self, atk, de, name, pic, maxhp, ddev, agil, sane, message, cry, lvl, rundown, heal, interval, equip = [nothing]):
		self.hp = maxhp
		self.dmg = atk
		self.atk = []
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
		self.equipped = equip

creepybaldguy = Enemy(5, 10, "Creepy Bald Guy", "creep", 18, 2, [1,100], -1, "You know you are being watched. Always... ", "you feel it staring through your eyes, Into your Soul.", 1, ["Even though it seems nearly dead, it continues its steady gaze deep into your eyes.", "it seems to have lost some hair in this fight. You blink, realizing it was already bald.", "it seems to be observing, only attacking to see how you react.", "it is sitting there, staring at you. Waiting and observing your every move."], [2,3,4], 200)

bosses = []
class Boss(object):
	def __init__(self, hp, atk, de, name, img, maxhp, ddev, agil, heal, sane, loot, loot2, turn, message, cry, rundown, room, interval, equip = [nothing]):
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
		self.atkInt = math.ceil(interval)
		self.atkIntBase = math.ceil(interval)
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
		self.equipped = equip
		
		global bosses
		bosses.append(self)

adventurer = Boss(190, 20, 0, "Adventurer", "adventurer", 190, 5, [5,100], [100,50,30], -7, herosword, heroshield, 10, "You hear the footsteps of someone else.", "It is an Adventurer, Readying his stance for Battle!", ["He seems oddly unaware of the massive amounts of damage you have dealt him. Much like you are.", "", "", "", "He seems more confident of himself, more sure of his strides.",""],bossroom,100, [herosword, heroshield]);

bosses = []
class Enm(object):
	def __init__(self, hp, maxhp, atk, ddev, dfn, agil, heal, sane, name, img, message, cry, rundown, interval, equip = [nothing], Boss = False, room = None, turn = -1):
		self.hp = hp #initial
		self.maxhp = maxhp #max
		self.atk = atk #damage += atk (if melee)
		self.ddev = ddev #damage +- ddev
		self.dfn = dfn #damage -= dfn
		self.agil = agil #touple, #/# chance to dodge
		self.heal = heal[2]
		self.healchance = [heal[0], heal[1]] #kys
		self.sane = sane #Added to sanity when killed
		self.name = name
		self.img = getImg("entities/"+img) #blitable image
		self.message = message #added to roommessage when in room
		self.cry = cry #start of battle message
		self.rundown = rundown #list of messages displayed in battle, might be removed *le sad*
		self.atkInt = math.ceil(interval)
		self.atkIntBase = math.ceil(interval)
		self.equipped = equip
		self.boss = Boss
		if self.boss:
			self.room = room
			self.turn = turn
			global bosses
			bosses.append(self)
		
		self.defending = False
		self.minions = []
		self.minionTree = []


alpha = Enm(350, 500, 14, 6, 0, [68, 100], [5,4,10], -3, "Alpha", "alpha", "You hear sudden quick footsteps from behind you.", "you turn to see someone dashing at you, Swinging a large axe!", ["", "", "", "", "", ""], 120, [alphaxe, sivgoggles], True, roomBoss3, 20)


#minions go here, not needed yet

finalsanity = 0
ablerooms = []
lootitems = []
#based on player level, changes aspects of game such as tiers of items, and rooms.
def gentables():
	global lootitems
	global pla
	global ablerooms
	global allitems
	global rooms
	global finalsanity
	
	lootitems = []
	for i in allitems:
		if i.findable == 1 and pla.lvl >= i.lvl:
			lootitems.append(i)
				

	#Get ablerooms
	ablerooms = []
	for i in rooms:
		if (pla.sanity < 2):
			if (i.sanity >= math.floor(cbrt(pla.sanity) - pla.lvl) and i.sanity <= math.floor(cbrt(pla.sanity) + (pla.lvl * 1.5))):
				ablerooms.append(i)
		elif (pla.sanity >= 2):
			if (i.sanity <= math.floor(cbrt(pla.sanity) + pla.lvl) and i.sanity >= math.floor(cbrt(pla.sanity) - (pla.lvl * 1.5))):
				ablerooms.append(i)
	
	
	if (len(ablerooms) == 0 and pla.trueSane == 0):
		prints("Ablerooms empty. Sanity: "+ pla.sanity + " pla.sane: " + pla.sane)
		if (pla.sanity < 0):
			ablerooms = [room19]
			finalsanity = -1
		if (pla.sanity > 0):
			ablerooms = [room23]
			finalsanity = 1
	#when reached true sanities
	if pla.trueSane != 0:
		lootitems = []
		for i in allitems:
			if (i.sane <= 0 and pla.trueSane < 0) or (i.sane >= 0 and pla.trueSane > 0):
				lootitems.append(i)
		for i in rooms:
			if (i.sanity <= 0 and pla.trueSane < 0) or (i.sanity >= 0 and pla.trueSane > 0):
				ablerooms.append(i)

equippeditems = [nothing, nothing]
runs = 1
room = room3
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
	global finalsanity
	global room
	global lootable
	
	prints("Generating room.")
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
		 room = ablerooms[rand(len(ablerooms))-1]
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
		roommessage += chestmessages[rand(len(chestmessages)-1)]
	else:
		lootable = False

	ableminions = []
	'''for i in minions:
		if (i.lvl <= pla.lvl):
			ableminions.append(i)'''
	
	if (rand(8) == 1 and len(ableminions) > 0):
		minion = ableminions[rand(len(ableminions))-1]
		roommessage += minion.message
		getMinion(pla, minion)

	for i in bosses:
		if (i.turn == turn):
			roommessage += prepbattle(i)
			
	#Prepbattle not done yet
	'''if (room == room38):
		roommessage += prepbattle(terracotta)
		search = False'''

	'''
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
				roommessage += prepbattle(creepybaldguy)'''
	global TM1
	TM1.img = wraptext(roommessage, 900, font, True)
	TM1.refresh()
	
battleprep = -1
lastmove = 1


def move(direction):
	global roommessage
	global battleprep
	global room
	roommessage = ""
	if (battleprep == -1):
		success = False
		#north
		if(direction == 1):
			if (room.north == 1):
				success = True
				roommessage = room.exitA + "north" + room.exitB
		#east
		if(direction == 2):
			if (room.east == 1):
				success = True
				roommessage = room.exitA + "east" + room.exitB
		#south
		if (direction == 3):
			if (room.south == 1):
				success = True
				roommessage = room.exitA + "south" + room.exitB
		#west
		if (direction == 4):
			if (room.west == 1):
				success = True
				roommessage = room.exitA + "west" + room.exitB
			
		if success:
			#roommessage VISUALS figure out how to get a new line in here
			global TM2
			TM2.img = font.render("", True, (0, 0, 0))
			genRoom()
			global lastmove
			lastmove = direction
		else:
			global TM2
			TM2.img = wraptext(room.exitFail, 900, font, True)
			TM2.refresh()
			prints("move failed.")
	
def getitem(item):
	#AAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHH
	
	global invenItems
	invenItems.append(item) #need to change to a special item, probably a custom object
	
	global score
	global TM2
	score += item.score
	TM2.img = wraptext("You found "+item.Name + ".<br/>you place the newfound loot in your backpack.", 900, font, True)
	TM2.refresh()

def RDloot():
	global lootable
	global lootitems
	if lootable:
		gentables()
		itemget = lootitems[random.randint(0, len(lootitems)-1)]
		'''if (itemget == rock)
			Unlock(heatrock);
		}'''
		
		getitem(itemget)
		lootable = False
	else:
		global TM2
		TM2.img = wraptext("There is nothing to loot here.", 900, font, True)
		TM2.refresh()
	
def removeitem(item): #must take valid item
	global invenItems
	if item in invenItems:
		if item.ench["bound"] > 0:
			item.ench["bound"] = item.ench["bound"] -1
			prints("Bound item: "+item.Name)
			if item.durability <= 0:
				item.broken = True
		else:
			invenItems.remove(item)
			prints("Removed: "+item.Name)
	else:
		prints(item.Name+" not found in inventory!")

#refresh an entity's stats. probably unneeded at this point
def Refresh(ent):
	#ent.atk = []
	
	#Rebuild entity's defence chunks
	
	#ent.dfn, ent.passdfn = []
	agilmod = 0
	for i in ent.equipped:
		for x in i.dfnChunks:
			if x.passive or ent.defending:
				agilmod += x.agil
	
	ent.agil[0] = ent.baseagil[0] + agilmod
			
#does not include: minions, dodging, calculation of boosting items
def Damage(source, weapon, atk, target):
	enchValues = [0, 0] #local values needed for enchantments: layered, heavy
	initdmg = atk.dmg + source.dmg + random.randint(0, source.ddev * 2)- source.ddev
	prevdmg = initdmg
	dmg = initdmg #differentiated for enchants
	print initdmg
	for k in range(len(target.equipped)): #loop through equipped items, counts because enchantments can do stuff
		i = target.equipped[k]
		enchValues[0] = 0 #reset for layered
		for j in range(len(i.dfnChunks)): #loop through each item's defence chunks, counts because enchantments
			x = i.dfnChunks[j]
			tanked = 0
			if ((x.ench["trueProtection"] or atk.pierce < 2) and not (atk.pierce == 1 and x.piercable == True)) and ((target.defending and not x.all) or x.all) and i.durability > 0: #if you actually count the defence
				#print "Armored! defence:"
				#Damage reduction
				if x.dfn == True: #all damage goes to armor
					tanked = dmg
				else: #some damage goes to armor
					tanked = x.dfn
				
				#Damage calculation
				#print tanked
				dmg -= tanked
				if target.defending:
					if dmg < 0:
						dmg = 0
				else:
					if dmg < 1:
						dmg = 1
				
				#print "newdmg:", dmg
				#Durability reduction
				weapon.durability -= x.ench["destructive"]
				if not x.dur: #if durability is taken into account
					i.durability -= tanked + atk.ench["destructive"]
					if i.durability < 0: #if armor is destroyed, only tank as much as it can
						dmg -= i.durability
						#if dmg > prevdmg:  #only do this if rebounding is back
						#	dmg = prevdmg
				
				if x.ench["thorns"] != False: #if it has thorns
					if (x.ench["thorns"].proj != False) or (atk.proj == False): #if thorns applies #NEED AN EXCEPTION TO PREVENT THORNS LOOPING. THAT WOULD BE VERY BAD
						Damage(target, i, x.ench["thorns"], source)
				if x.ench["reflecting"] != 0:
					Damage (source, i, atkChunk(dmg*x.ench["reflecting"], atk.agil-10, False, False, atk.pierce-1), source) #NEED AN EXCEPTION TO PREVENT THORNS LOOPING
			if enchValues[0] < x.ench["layered"][1]: #test layered max
				if (random.randint(0, 100) < x.ench["layered"][0]):
					j -= 1
					enchValues[0] += 1
			prevdmg = dmg
			if enchValues[1] < atk.ench["heavy"]:
				enchValues[1] += 1
				dmg = initdmg
	
	dmg -= target.dfn
	message = source.name+" deals <strong>"+str(dmg)+"<strong> damage to "+ target.name
	target.hp -= dmg
	return message
	#check(target)

#takes in source, weapon used, and target.		[how many hits allowed, previous target, sweeping]
def attack(source, weapon, target, enchValues = [1, None, None]):
	messages = []
	#Sweeping
	enchValues[1] = target #can't hit the same person twice in a row
	if enchValues[2] == None: #figure out if weapon has sweeping
		for i in weapon.atkChunks:
			if i.ench["sweeping"] > 0:
				enchValues[2] = i
				break
	
	for x in range(enchValues[0]):#Sweeping, or hitting multiple times in any way
		attacking = True #more of "notHitMinion" or "attackingTarget"
		for i in target.minions:
			if (rand(100) <= i.dist and attacking) and (enchValues[1] != i):
				message, enchValues = attack(source, weapon, i, enchValues)
				messages.append(message)
				if (i.hp <= 0):
					target.minions.remove(i)
					#VISUALS 'source.name+"'s "+ minion.name+ " is dead."'
					target.minionTree = getMinionTree(target, 1)
				attacking = False

		if (attacking):
			atk = atkChunk(source.atk, source.agil[0]) #give a base value in case weapon has no valid atkChunks
			#Make the atkChunk to use in this attack
			for i in weapon.atkChunks:
				if i.proj == False:
					atk = atkChunk(source.atk + i.dmg, source.agil[0] + i.agil, i.dfn, i.etrn, i.pierce, i.proj, i.ench)
					
					break
				else:
					if weapon.ammo >= i.proj: #see if enough ammo to use proj chunk
						atk = atkChunk(i.dmg, source.agil[0] + i.agil, i.dfn, i.etrn, i.pierce, i.proj, i.ench)
						weapon.ammo -= i.proj
						break
			
			for i in source.equipped: #add boosts from other items
				for x in i.atkChunks:
					if x.etrn:
						atk.dmg += x.dmg
						atk.agil += x.agil
						#Add the enchants together, use the higher value
			
			if atk.ench["sweeping"] > 0:
				enchValues[0] = 1+atk.ench["sweeping"]
			
			if atk.proj != False and i.ench["returning"][0] != 0:
				if i.ench["returning"][0] > random.randint(0, 100):
					weapon.ammo += i.ench["returning"][1]
			
			#add agil mod of used chunk
			newagil = [((target.agil[0]*(source.agil[1]+atk.agil))-(((source.agil[0]+atk.agil)*target.agil[1])/2)), (target.agil[1]*(source.agil[1]+atk.agil))]
			#prints(newagil)
			if (rand(newagil[1]) <= newagil[0]):
				messages.append(target.name + " dodged "+ source.name +"'s attack")
				
			else:
				messages.append(Damage(source, weapon, atk, target))
			attacking = False
			return messages, enchValues


#MINIONS
def getMinionTree(entity, type):
	if type == 2:
		if (len(entity.minions) > 0):
			for i in range(len(entity.minions)):
				minionTree.append(entity.minions[i])
				if (len(entity.minions[i].minions) > 0):
					minionTree += getMinionTree(entity.minions[i], 2)
			return minionTree
	if type == 1:
		minionTree = []
		minionTree += getMinionTree(entity, 2)
		return minionTree
		

#Getting visuals for screens
Smain = getImg("screens/screenmain")
Sgrave = getImg("screens/gravestone")
Scompass = getImg("screens/compass")
Sinsane = getImg("screens/screenlastinsanity")
Szarol = getImg("screens/screenzarol")
looot = font.render("Loot", True, (0, 0, 0))
inveen = font.render("Inventory", True, (0, 0, 0))
baack = font.render("Back", True, (0, 0, 0))

running = True
Screen = 1
mouse_down = False
genRoom()

#main loop
while running:
	for event in pygame.event.get(): #key input
		if event.type == pygame.QUIT: 
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_down = True
		elif event.type == pygame.MOUSEBUTTONUP:
			mouse_down = False
		elif event.type == pygame.KEYDOWN and debug:
			if event.key == K_1:
				prints("boop")
				
	mouse_pos = pygame.mouse.get_pos()

	if Screen == 1: #main screen
		screen.fill(Cbacking)
		screen.blit(Smain, (0, 0))
		
		screen.blit(TM1.img, TM1.coords)
		screen.blit(TM2.img, TM2.coords)
		#buttons on side
		pygame.draw.rect(screen, Cbacking, [910, 10 , 75, 24])
		screen.blit(inveen, (910, 10))
		pygame.draw.rect(screen, Cbacking, [910, 37 , 75, 24])
		screen.blit(looot, (910, 37))
		screen.blit(Scompass, (910, 174))
		
		
		if mouse_down:
			if hitDetect((935, 174), (960, 199), mouse_pos): #north
				mouse_down = False
				move(1)
			if hitDetect((960, 199), (985, 224), mouse_pos): #east
				mouse_down = False
				move(2)
			if hitDetect((935, 224), (960, 249), mouse_pos): #south
				mouse_down = False
				move(3)
			if hitDetect((910, 199), (935, 224), mouse_pos): #west
				mouse_down = False
				move(4)

			if hitDetect((910, 10), (985, 32), mouse_pos): #invetory, button size: 75 x 24 px
				Screen = 2
				mouse_down = False
			if hitDetect((910, 37), (985, 61), mouse_pos): #loot

				mouse_down = False
				RDloot()
	
	if Screen == 2: #inven screen
		screen.fill(Cbacking)
		screen.blit(Smain, (0, 0))
		
		#buttons and stuff
		screen.blit(TI1.img, TI1.coords)
		pygame.draw.rect(screen, Cbacking, [10, 225 , 75, 24])
		screen.blit(baack, (10, 225))
		
		if mouse_down:
			if hitDetect((10, 225), (85, 249), mouse_pos):
				Screen = 1
	
	if Screen == 3: #battle
		screen.fill(Cbacking)

		
	if Screen == 4: #Grave, limbo 1
		screen.fill(BLACK)
		
		
	if Screen == 5: #Monoliths, limbo 2
		screen.fill(BLACK)
	
	
	#little stuff all the time
	for i in invenItems:
		if i.mendTick != -1:
			i.mendTick += 1
			if i.mendTick >= i.ench["mending"][0] and not i.broken: #mending
				i.mendTick = 0
				i.durability += i.ench["mending"][1]
				if i.durability > i.maxdur:
					i.durability = i.maxdur
				if i.durability <= 0 and i.destructable:
					removeitem(i)
			elif i.mendTick >= (i.ench["mending"][0]+100)*2 and i.broken and i.ench["mending"][1] > 0: #take long time to repair from broken. and don't keep breaking it
				i.mendTick = 0
				i.durability += 1 #and it only fixes a little bit
				if i.durability > 0:
					i.broken = False
				
	
	pygame.display.update()
	clock.tick(50)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	