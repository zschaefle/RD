import random
import pygame
from pygame.locals import *
import math

#look for:   #VISUALS   to find where HTML visuals were removed
debug = True

#prevent crashes
nothing = None

BLACK = (0, 0, 0)
BLIMBO = (34, 34, 34)
WHITE = (255, 255, 255)
BLUE = (0, 0, 220)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LGREY = (153, 153, 153)
GREY = (100, 100, 100)
Cbacking = (170,170,170)

pygame.init()
size = (995, 259)
font = pygame.font.SysFont('couriernew', 18) #13
fontComp = pygame.font.SysFont('couriernew', 20, True) #16
smallfont = pygame.font.SysFont('couriernew', 12) #12
massive = pygame.font.SysFont('couriernew', 200, True)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

invenItems = []
scrollMod = 0
scrollMom = 0
netSize = 0
score = 0
turn = 0
finalsanity = 0
ablerooms = []
lootitems = []
runs = 1
room = None
lootable = False
chestmessages = ["There is a small chest about the size of your fist lurking in the corner. ", "A golden chest sits with elegant details and pure beauty.", "There\'s a lumpy sack over there", "You hear the wheeze of a chest.  \"Open me\" it calls, with the music of its collapsing wood.", "In a rotting monster carcass, you glimpse something... interesting.", "There\'s a lump in the ground. Like a squirrel buried a tasty rock and then ran off and died.", "Something calls your attention. It sucks you in. You imagine riches.", "You smell something.  It smells like goods.", "You glimpse a confection of wood and nails, almost big enough to hold something.", "There is a small door that seems to have something sticking out, perhaps something useful."]
runmessages = ["Run", "Dodge", "Sprint", "Jump", "Duck", "Roll", "Slide", "Feint", "Fake", "Switch", "Distract", "Twist", "Lurch", "Insult", "Shout"]
#unlockmessages = ["You hear the sound of something unlocking from far away.", "You feel the dongeon blink, and you have a moment of deja vu.", "A feeling of release washes over you, the feeling of access.", "You feel something click, almost like a realization."]
healable = True
noKillEpic = True
roommessage = ""
search = True
battleprep = -1
inbattle = False
checkpoint = 0
bossesbeat = 0
running = True
Screen = 1
mouse_down = False
#Boss stuff
plaTime = 0
plaatk1 = 0
plaatk2 = 0
pladfn = 0
plaheal = 0
plaTotal = 1
bossmisc = 0
finalbosses = ["zarol", "zarol", "zarol", "Coo", "North", "Blue", "Jim", "Siv"]
endboss = "zarol"
CIstage = 0
COstage = 0
Cmode = 0
SanPool = 0


def prints(stuff):
	global debug
	if debug:
		print stuff

#two sets of coord pairs
def hitdetect(p1, p2, p3, p4 = None):
	if p4 == None:
		p4 = p3
	if p2[0] > p3[0] and p1[0] < p4[0] and p2[1] > p3[1] and p1[1] < p4[1]:
		return True

#useful for mouse and buttons. if point p3 is in p1 with size p2
def hitDetect(p1, p2, p3):
	if p1[0] + p2[0] > p3[0] and p1[0] < p3[0] and p1[1] + p2[1] > p3[1] and p1[1] < p3[1]:
		return True

def getImg(name):
	full = "Assets/img/"+name+".png"
	prints("Loading: "+full)
	try:
		return pygame.image.load(full)
	except pygame.error:
		print "--File not found. Substituting"
		return pygame.image.load("Assets/img/wip.png")
		
actImg = getImg("special/active")
ac2Img = pygame.transform.scale(actImg, (50, 50)) #probably make special img
dfnImg = getImg("special/defensive")
melImg = getImg("special/melee")
me2Img = pygame.transform.scale(melImg, (50, 50)) #probably make special img
pasImg = getImg("special/passive")
prjImg = getImg("special/projectile")
#Screens
Smain = getImg("screens/screenmain")
Sgrave = getImg("screens/gravestone")
Scompass = getImg("screens/compass")
Sinsane = getImg("screens/screenlastinsanity")
Szarol = getImg("screens/screenzarol")
Scrafter = getImg("screens/Crafter")
Sbattle = Smain
		
def rand(num):
	return random.randint(1, num)

def cbrt(num):
	if num < 0:
		return -(math.fabs(num) ** (1.0/3.0))
	else:
		return num ** (1.0/3.0)
	
def addEnch(type, en1, en): #DO THORNS GOOD
	en2 = {"reflecting":0, "thorns":False, "destructive":0, "trueProtection":False, "layered":[0, 0], "piercing":0, "heavy":0, "sweeping":0, "returning":[0, 0], "mending":[-1, 0], "bound":0}
	en2.update(en)
	if type == 1: #defensive
		en3 = {"reflecting":0, "thorns":False, "destructive":0, "trueProtection":False, "layered":[0, 0]}
		en3["reflecting"] = en1["reflecting"]+en2["reflecting"]
		en3["destructive"] = en1["destructive"]+en2["destructive"]
		if en1["trueProtection"] or en2["trueProtection"]:
			en3["trueProtection"] = True
		en3["layered"][0] = max(en1["layered"][0], en2["layered"][0])
		en3["layered"][1] = max(en1["layered"][1], en2["layered"][1])
		en3["thorns"] = en2["thorns"]
		print en3
		return en3
		
	if type == 2: #offensive
		en3 = {"destructive":0, "piercing":0, "heavy":0, "sweeping":0, "returning":[0, 0]}
		en3["destructive"] = en1["destructive"]+en2["destructive"]
		en3["piercing"] = en1["piercing"]+en2["piercing"]
		en3["heavy"] = en1["heavy"]+en2["heavy"]
		en3["sweeping"] = en1["sweeping"]+en2["sweeping"]
		en3["returning"][0] = max(en1["returning"][0], en2["returning"][0])
		en3["returning"][1] = max(en1["returning"][1], en2["returning"][1])
		
		print en3
		return en3
		
	if type == 3: #full item
		en3 = {"mending":[-1, 0], "bound":0}
		en3["bound"] = en1["bound"]+en2["bound"]
		
		#en3["mending"][1] = max(en1["mending"][1], en2["mending"][1]) #gets highest
		en3["mending"][1] = math.floor((en1["mending"][1] + en2["mending"][1]) *0.75) #kida adds them

		n1 = en1["mending"][0]
		n2 = en2["mending"][0]
		n3 = min(n1, n2)
		if n3 == -1: # if either is -1, the other is the least or also -1; both >= -1
			n3 = max(n1, n2)
		en3["mending"][0] = n3

		'''if self.ench["mending"][0] != -1:
			self.mendTick = 0
		else:
			self.mendTick = -1
		if self.regenammo[0] != 0:
			self.regenTick = 0
		else:
			self.regenTick = -1'''
		print en3
		return en3
		
def Enchant(item, spec = 0):
	print "ENCHANTING:", item.Name

	atklen = len(item.atkChunks)
	dfnlen = len(item.dfnChunks)
	localrand = rand(atklen + dfnlen + 1) -1

	prints("Enchant number: " + str(localrand))

	if localrand > 0 and localrand <= atklen:
		num = localrand - 1
		if item.atkChunks[num].proj != None:
			num2 = rand(5)
			if num2 == 1:
				enchs = {"destructive":(rand(math.fabs(item.lvl)+1) * rand(4))}
			if num2 == 2:
				enchs = {"piercing":rand(2)}
			if num2 == 3:
				enchs = {"heavy":1}
			if num2 == 4:
				enchs = {"sweeping":1}
			if num2 == 5:
				enchs = {"returning":([int(rand(item.maxammo)/2)+1, 5*rand(8)])}
		else:
			num2 = rand(4)
			if num2 == 1:
				enchs = {"destructive":(rand(math.fabs(item.lvl)+1))*rand(5)}
			if num2 == 2:
				enchs = {"piercing":rand(2)}
			if num2 == 3:
				enchs = {"heavy":1}
			if num2 == 4:
				enchs = {"sweeping":rand(2)}
		item.atkChunks[num].ench = addEnch(2, item.atkChunks[num].ench, enchs)
	if localrand > atklen:
		#self.ench = {"reflecting":0, "thorns":False, "destructive":0, "trueProtection":False, "layered":[0, 0]}
		num = localrand - atklen - 1
		if item.dfnChunks[num].dfn == None: #DONT TRUE PROTEC
			num2 = rand(4)
			if num2 == 1:
				enchs = {"reflecting":(2*rand(4) + 2)/100.0}
			if num2 == 2:
				enchs = {"thorns":atkChunk(math.ceil(rand(math.fabs(item.lvl)+1)*0.3), 15*rand(6), random.choice([True, False]), False, rand(2)-1)}
			if num2 == 3:
				enchs = {"destructive":((rand(5)+1)*rand(10))}
			if num2 == 4:
				enchs = {"layered":[5*rand(15), rand(3)]}
		else:
			num2 = rand(5)
			if num2 == 1:
				enchs = {"reflecting":(2*rand(3) + 3)/100.0}
			if num2 == 2:
				enchs = {"thorns":atkChunk(math.ceil(rand(math.fabs(item.dfnChunks[num].dfn)+1)*0.2), 12*rand(6), random.choice([True, False]), False)}
			if num2 == 3:
				enchs = {"destructive":((rand(5)+1)*rand(10))}
			if num2 == 4:
				enchs = {"layered":[5*rand(15), rand(3)]}
			if num2 == 5: #maybe not if already trueprotec
				enchs = {"trueProtection":True}
		print num2
		item.dfnChunks[num].ench = addEnch(1, item.dfnChunks[num].ench, enchs)
	if localrand == 0:
		num2 = rand(2)
		if num2 == 1:
			enchs = {"mending":[(rand(20)+50)*(rand(20)+50), rand(math.floor(item.maxdur/15))]}
		if num2 == 2:
			enchs = {"bound":1}
		item.ench = addEnch(3, item.ench, enchs)
		#self.ench = {"mending":[-1, 0], "bound":0}
	return item
		
class DispObj(object):
	def refresh(self):
		if not self.simple:
			final = pygame.Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
			for i in self.all:
				final.blit(i.img, i.coords)
			self.img = final
	#coords, img is blitable object or list of DispObj. simple is wether or not is list. size is needed if not simple.
	def __init__(self, img, coords = (0, 0), simple = True, size = (0, 0)):
		self.coords = coords
		self.baseCoords = coords
		self.img = img
		self.all = img
		self.simple = simple
		self.size = size
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
			x = outtext[i]
			text.append(DispObj(Font.render(x, True, color),  (0, (i*size[1]))))
		outtext = text
	return outtext
	
TM1 = DispObj(wraptext("", 900, font, True), (10, 10), False, (900, 120)) #main room desc
TM2 = DispObj(wraptext("", 900, font, True), (10, 130), False, (900, 119)) #room responses
ItemsDisp = DispObj([], (115, 10), False, (370, 239)) #Inventory items display
TL1 = DispObj([DispObj(Sgrave), 
	DispObj(fontComp.render("RIP", False, (0, 0, 0)), (88, 30)), 
	DispObj(wraptext("You are dead. Not big surprise.", 150, font, True), (26, 48), False, (150, 200))
], (397, 9), False, (200, 250)) #gravestone
TL2 = DispObj(font.render("RUN DUDE, RUN!!", True, (250, 250, 250)), (428, 120)) #Dodge button
TL3 = DispObj(wraptext("", 975, font, True), (10, 10), False, (975, 200)) #cliff message

class ItemDisp(object):
	def refresh(self, type):
		global smallfont
		global font
		global nothing
		#NORMAL IMAGE, name and description with image
		if type == 1 and self.item != nothing:
			self.norm = DispObj([
				DispObj(self.mini, (2, 2)), 
				DispObj(font.render(self.item.Name, True, (0, 0, 0)), (54, 2)), 
				DispObj(wraptext(self.item.desc, 314, smallfont, True), (54, 18), False, (314, 200))
			], (0, 0), False, (370, 54)) #inven, name + desc + images
			
			if self.item.act:
				global actImg
				self.norm.all.append(DispObj(actImg, (350, 2)))
			if self.item.dfn:
				global dfnImg
				self.norm.all.append(DispObj(dfnImg, (350, 2)))
			if self.item.mel or self.item.prj:
				global melImg
				self.norm.all.append(DispObj(melImg, (350, 2)))
				
			self.norm.refresh()
			#self.press.refresh()
			
			#SIDE IMAGE, image, description, and full chunk display
			self.side = DispObj([
				DispObj(self.mini),
				DispObj(wraptext(self.item.desc, 446, smallfont, True), (52, 0), False, (446, 50)), #for wraptext size, use fullsize-50-2
			], (487, 10), False, (498, 239))
			
			allchunks, allsize, astring = [], 52, ""
			if self.item.ench["mending"][0] > -1: #item has mending
				astring += "-Mending "
			if self.item.ench["bound"] > 0:
				astring += "-Bound: "+str(self.item.ench["bound"])
			if astring != "":
				self.side.all.append(DispObj(font.render(astring, True, (0, 0, 0)), (2, 52)))
				allsize += 16
			
			
			proj = {"is":False, "dmg":[None, None], "ammo":None, "agil":0, "pierce":0, "enchs":{"destructive":0, "piercing":0, "heavy":0, "sweeping":0, "returning":[0, 0]}}
			for i in self.item.atkChunks: #build offence displays
				if i.proj != None: #if projectile
					proj["is"] = True
					#get lowest damage
					proj["dmg"][0] = i.dmg if (proj["dmg"][0] == None) else min(proj["dmg"][0], i.dmg)
					#get highest damage
					proj["dmg"][1] = i.dmg if (proj["dmg"][1] == None) else max(proj["dmg"][1], i.dmg)
					#get highest ammo cost
					proj["ammo"] = i.proj if (proj["ammo"] == None) else max(proj["ammo"], i.proj)
					#get highest agil
					proj["agil"] = max(i.agil, proj["agil"])
					#get the highest pierce
					proj["pierce"] = max(proj["pierce"], i.pierce)
					#add the enchantments
					proj["enchs"] = addEnch(2, proj["enchs"], i.ench)
					
				else:#normal melee
					localrand = DispObj([], (0, 0), False, (223, 200))
					
					if i.etrn:
						localrand.all.append(DispObj(pasImg, (0, 0)))
						if i.dmg < 0:
							localrand.all.append(DispObj(font.render("Passive "+str(i.dmg), True, (0, 0, 0)), (20, 0)))
						else:
							localrand.all.append(DispObj(font.render("Passive +"+str(i.dmg), True, (0, 0, 0)), (20, 0)))
					else:
						localrand.all.append(DispObj(font.render("Dmg: "+str(i.dmg), True, (0, 0, 0)), (20, 0)))
						if not i.dfn:
							localrand.all.append(DispObj((dfnImg), (0, 0)))
						localrand.all.append(DispObj((melImg), (0, 0)))
					
					#agildesc, piercing
					astring = ""
					if i.agil < -2:
						astring = "Cumbersome"
					if i.agil < -20:
						astring = "Hindering"
					if i.agil >= -2 and i.agil <= 2: # if -2 <= i.agil <= 2
						astring = "Unobtrusive"
					if i.agil > 2:
						astring = "Balanced"
					if i.agil > 20:
						astring = "Nimble"
					
					if i.pierce > 0:
						if i.pierce > 1:
							astring += " - Piercing+"
						else:
							astring += " - Piercing"
					
					localrand.all.append(DispObj(font.render(astring, True, (0, 0, 0)), (1, 19))) #the agil description
					thissize = 37
					
					#enchants hereish
					if i.ench["destructive"] > 0:
						localrand.all.append(DispObj(font.render("Destructive "+str(i.ench["destructive"]), True, (0, 0, 100)), (1, thissize)))
						thissize += 16
					if i.ench["piercing"] != 0:
						localrand.all.append(DispObj(font.render("Piercing +"+str(i.ench["piercing"]), True, (0, 0, 100)), (1, thissize)))
						thissize += 16
					if i.ench["heavy"] > 0:
						localrand.all.append(DispObj(font.render("Heavy "+str(i.ench["heavy"]), True, (0, 0, 100)), (1, thissize)))
						thissize += 16
					if i.ench["sweeping"] > 0:
						localrand.all.append(DispObj(font.render("Sweeping "+str(i.ench["sweeping"]), True, (0, 0, 100)), (1, thissize)))
						thissize += 16
					if i.ench["returning"][0] > 0:
						localrand.all.append(DispObj(font.render("Returning "+str(i.ench["returning"][0])+" ("+str(i.ench["returning"][1])+"% chance)", True, (0, 0, 100)), (1, thissize)))
						thissize += 16
					
					localrand.size = (223, thissize)
					localrand.refresh()
					allchunks.append(localrand)
				
				
			if proj["is"]: #it has proj chunks
				localrand = DispObj([], (0, 0), False, (223, 200))#unknown vertical size. enchants will modify
				localrand.all.append(DispObj(prjImg, (0, 0)))
				if proj["dmg"][0] == proj["dmg"][1]: #one damage
					localrand.all.append(DispObj(font.render("Dmg: "+str(proj["dmg"][0]), True, (0, 0, 0)), (20, 0)))
				else:
					localrand.all.append(DispObj(font.render("Dmg Range: "+str(proj["dmg"][0])+"-"+str(proj["dmg"][1]), True, (0, 0, 0)), (20, 0)))
				localrand.all.append(DispObj(font.render("Cost: "+str(proj["ammo"]), True, (0, 0, 0)), (155, 0)))
				
				#agildesc, piercing
				astring = ""
				if proj["agil"] < 0:
					astring = "Somewhat"
				if proj["agil"] < -50:
					astring = "Not"
				if proj["agil"] == 0:
					astring = "Normally"
				if proj["agil"] > 0:
					astring = "Very"
				if proj["agil"] > 50:
					astring = "Incredibly"
				astring += " accurate"
				
				if proj["pierce"] > 0:
					if proj["pierce"] > 1:
						astring += " - Piercing+"
					else:
						astring += " - Piercing"
				
				localrand.all.append(DispObj(font.render(astring, True, (0, 0, 0)), (1, 19))) #the agil description
				thissize = 37
				
				#enchants {"destructive":0, "piercing":0, "heavy":0, "sweeping":0, "returning":[0, 0]}
				if i.ench["destructive"] > 0:
					localrand.all.append(DispObj(font.render("Destructive "+str(i.ench["destructive"]), True, (0, 0, 100)), (1, thissize)))
					thissize += 16
				if i.ench["piercing"] != 0:
					localrand.all.append(DispObj(font.render("Piercing +"+str(i.ench["piercing"]), True, (0, 0, 100)), (1, thissize)))
					thissize += 16
				if i.ench["heavy"] > 0:
					localrand.all.append(DispObj(font.render("Heavy "+str(i.ench["heavy"]), True, (0, 0, 100)), (1, thissize)))
					thissize += 16
				if i.ench["sweeping"] > 0:
					localrand.all.append(DispObj(font.render("Sweeping "+str(i.ench["sweeping"]), True, (0, 0, 100)), (1, thissize)))
					thissize += 16
				if i.ench["returning"][0] > 0:
					localrand.all.append(DispObj(font.render("Returning "+str(i.ench["returning"][0])+" ("+str(i.ench["returning"][1])+"% chance)", True, (0, 0, 100)), (1, thissize)))
					thissize += 16
				
				localrand.size = (223, thissize)
				localrand.refresh()
				allchunks.insert(0, localrand)
			
			for i in self.item.dfnChunks: #dfn chunks
				localrand = DispObj([], (0, 0), False, (223, 200))
				
				astring = "Dfn: "
				if i.all:
					localrand.all.append(DispObj(dfnImg, (0, 0)))
					if i.dfn > 0 or i.dfn == None:
						astring = "Passive +"
					if i.dfn <= 0:
						astring = "Passive "
				else:
					localrand.all.append(DispObj(actImg, (0, 0)))
				if i.dfn == None:
					astring += "Full"
				elif i.dfn != 0:
					astring += str(i.dfn)
				if not i.piercable:
					astring += " Impervious" #not piercable
				localrand.all.append(DispObj(font.render(astring, True, (0, 0, 0)), (20, 0)))
					
				#agildesc, durable
				astring = ""
				if i.agil < -2:
					astring = "Cumbersome"
				elif i.agil < -20:
					astring = "Hindering"
				elif i.agil > 2:
					astring = "Nimble"
				elif i.agil > 20:
					astring = "Agile"
				else:
					astring = "Unobtrusive"
					
				if i.dur:
					astring += " - Durable"
				
				localrand.all.append(DispObj(font.render(astring, True, (0, 0, 0)), (1, 19))) #the agil description
				thissize = 37
				
				#enchants
				if i.ench["reflecting"] > 0:
					localrand.all.append(DispObj(font.render("Reflecting "+str(100*i.ench["reflecting"])+"%", True, (0, 0, 100)), (1, thissize)))
					thissize += 16
				if i.ench["thorns"] != False:
					localrand.all.append(DispObj(font.render("Thorns +"+str(i.ench["thorns"].dmg), True, (0, 0, 100)), (1, thissize)))
					thissize += 16
				if i.ench["destructive"] != 0:
					localrand.all.append(DispObj(font.render("Destructive "+str(i.ench["destructive"]), True, (0, 0, 100)), (1, thissize)))
					thissize += 16
				if i.ench["trueProtection"] > 0:
					localrand.all.append(DispObj(font.render("True Protection", True, (0, 0, 100)), (1, thissize)))
					thissize += 16
				if i.ench["layered"][1] > 0:
					localrand.all.append(DispObj(font.render("Layered "+str(i.ench["layered"][1])+" ("+str(i.ench["layered"][0])+"% chance)", True, (0, 0, 100)), (1, thissize)))
					thissize += 16
					
				
				localrand.size = (223, thissize)
				localrand.refresh()
				allchunks.append(localrand)
			
			bigsize = 0
			for i in range(len(allchunks)): #update coords using allsize
				if ((i+1) % 2 == 0):
					allchunks[i].coords = (225, allsize)
					if allchunks[i].size[1] > bigsize:
						bigsize = allchunks[i].size[1]
					allsize += bigsize #get largest size
				else:
					allchunks[i].coords = (0, allsize)
					bigsize = allchunks[i].size[1]
			
			
			self.side.all += allchunks
			self.side.refresh()
			
			self.fight = DispObj([DispObj(pygame.Surface((52, 52), pygame.SRCALPHA, 32).convert_alpha())], (10, 199), False, (52, 52))
			if self.item.ammo == None:
				self.fight.all.append(DispObj(self.mini, (1, 0)))
			else:
				self.fight.all.append(DispObj(self.mini))
			
		if type == 1 and self.item == nothing:
			self.side = DispObj([], (0, 0), False, (0, 0)) #very invisable
			self.fight = DispObj([DispObj(pygame.Surface((52, 52), pygame.SRCALPHA, 32).convert_alpha()), DispObj(self.mini)], (10, 199), False, (52, 52))
		
		#FIGHT display
		if type == 2:
			#global pla
			self.item.refresh()
			if self.item.ammo != None and self.item.maxammo != 0:
				pygame.draw.rect(self.fight.all[0].img, LGREY, (50, 0, 2, 52))
				pygame.draw.rect(self.fight.all[0].img, BLUE, (50, 52, 2, (self.item.ammo/self.item.maxammo)*(-52)))#ammo
				pygame.draw.rect(self.fight.all[0].img, LGREY, (0, 50, 50, 2))
				pygame.draw.rect(self.fight.all[0].img, GREEN, (0, 50, (self.item.dfratio)*50, 2))#dura
			else:
				pygame.draw.rect(self.fight.all[0].img, LGREY, (0, 50, 52, 2))
				pygame.draw.rect(self.fight.all[0].img, GREEN, (0, 50, (self.item.dfratio)*52, 2))#dura
			self.fight.refresh()
			
		if type == 3:
			global pla #don't know how to properly make modular
			global nothing
			if (self.item == pla.equipped[2]) or (pla.equipped[2] == nothing and pla.equipped[3] == self.item):
				self.fight.coords = (10, 199)
			else:
				self.fight.coords = (70, 199)


	def __init__(self, item):
		self.id = item.Name
		self.item = item
		#different displays
		self.mini = pygame.transform.scale(item.img, (50, 50)) #just the item, resized
		self.fight = DispObj(self.mini, (10, 199))
		self.norm =  self.mini #for use in inven, with name + desc
		self.press = self.mini #for inven, when clicked on.
		self.side = self.mini #for inven, large display
		self.refresh(1)
#pygame.transform.scale()

def refreshItems(type): #used for displaying of all items
	global ItemsDisp
	global scrollMod
	if type == 1: #run when adding a new item to invenItems
		ItemsDisp.all = []
		global invenItems
		global netSize
		netSize = 0
		for i in invenItems:
			i.div.norm.baseCoords = (0, netSize)
			netSize += i.div.norm.size[1] #add size to total size
			ItemsDisp.all.append(i.div.norm)
		if netSize <= 239:
			scrollMod = 0
		refreshItems(2)
			
	if type == 2: #update w/ scroll mod
		for i in ItemsDisp.all:
			i.coords = (i.coords[0], i.baseCoords[1]+scrollMod)
	
	ItemsDisp.refresh()
refreshItems(1)
		
#Rooms for the dongeon
rooms = []
class Room():
	def __init__(self, plant, manmade, water, dark, animal, light, items, north, east, south, west, sane, message, exitA, exitB, exitFail, reference = False, normal = True):
		#give a UID at some point
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
		self.isref = reference
		if normal:
			global rooms
			rooms.append(self)
		
		if (self.exitA == "" or self.exitA == " " or self.exitB == "" or self.exitB == " "):
			self.exitA = "You go "
			self.exitB = "."

#REF: Mono, Valve, YS
#TYPE: Trip, Daily, Lore, Split
			
room1 = Room(0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, -4 ,"Your eyes burn as you look into the lit black.  Green lines stretch to a vanishing point, showing you a door, a wall and a cliff.  Your eyesight blurs, reduced to craggy blocks.", "Your legs jitter as you walk on thin green lines, forming an exit to what you believe to be ", ".", "You feel like taking any extra steps in may be fatal.")
room2 = Room(1, 0, 0, 1, 1, 1, 1, rand(2)-1, 1, 2, rand(2)-1, 1, "This room is overrun by nature. There are twisted, moist vines covering the walls and most likely any exits.", "You carefully make your way to the ", ", occasionally tripping.", "You trip on your way over to the wall, only finding no exit.")
room3 = Room(0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, "You\'re in a linoleum cube, bare and featureless.   A circular opening appears behind you, and an open pit is just ahead.   A featureless voice speaks to you through static speakers.   You can\'t understand a single word.", "As you walk toward the ", ", the circular door smoothly opens in the wall ahead of you.", "The voice seems to be insulting you as you stumble about, slightly confused.", ["Valve"])
room4 = Room(1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, "You find yourself in a lonely forest.  The snow on the ground mists in the sun, slowly turning into slush.  You take a moment to mourn the death of winter. Global warming man.  That\'s what it does.", "There's a small door in one of the trees to the ", ". You pull it open and and fall through.", "")
room5 = Room(0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, -2, "You stand on clouds, up to your ankles in condensation.  You see birds flying nearby.  You could swear that you see a large animal lurching its way towards you on lopsided legs.", " ", " ", " ")
room6 = Room(0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, -1, "You are in a room, a large centrepiece of machinery whirring to life, bursts of energy coming from within. There are voices yelling urgently at you from a viewport in the wall above.", "You manage to dodge the now falling rubble and make it through the ", "ern sliding doors.", "A zap of lightning from the core of the room leaps through the viewport, and you hear a scream of pain.", ["Valve"])
room7 = Room(0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, "The walls cave inwards, rough rock with red striped sedimentary motif. The floor is loose packed sand, soft against your feet.  You look ahead, where the walls become lower and the ground gets rough.  You\'ll need to crawl.", "You crawl to the ", " exit, scraping your elbow.", "You realize that this is not an Indiana Jones movie, and that this wall will not open with enough force.")
room8 = Room(0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 4, "You see a single shelf, packed full of books, reaching upwards like a ladder into the darkness. ", "You grip the ", "ern shelves, pulling yourself up past musty tomes.", "You become distracted by the books, taking a moment to flip through one.")
room9 = Room(0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, -1, "There are huge wooden beams stretching across an empty cavern.  Coals smoulder in campfires across the expanse, lighting the room with grey dusk.  Rotting homes half-formed out of clay fill the room with a musty stench.", "You walk past small encampments and crusty artefacts to a hole in the ", "ern wall.", "You glance into one of the rooms. You spot a skeleton and an old vase. No exits here.")
room10 = Room(0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, -1, "The sun shines in your eyes.  You feel water underneath you.  Shielding your eyes from the glare, you see the boat you\'re standing on, a small and splintery craft.  The way it bobs under your weight alarms you.  A curl of rope under your feet obscures the bottom of the boat.", "you take hold of the paddles, paddling the boat to the ", ".", "Paddle as you may, the swirling currents quickly rush  you back into place.")
room11 = Room(0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, "You are on a cold, stormy beach. Litter is strewn across the sand, and a man with a prosthetic arm is purposefully cleaning it up, glancing around as if expecting someone, or some<i>thing</i>.", "As you meander your way to the ", ", the man shouts at you angrily, something about litter.", "You wade about in the ocean, unsure as to whether you are looking for something, or mourning.", ["Split"])
room12 = Room(0, 1, 0, 0, 1, 1, 1, rand(2)-1, rand(2)-1, 0, 1, rand(2), "You are in a room, full of red books with no titles, no markings at all. They fill the room, but you can hear a sort of carnal snore from somewhere in the room. You decide that would be best to keep away from whatever is producing the noise.", "You manage to sneak your way through to the ", ", cringing at the occasional shifting book.", "You wander throughout the room, surprisingly small for the quantity of books it holds.", ["Mono"])
room13 = Room(rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, 1, 1, 1, 1, -7, "You find yourself in a room filled with bright darkness. Things seem to appear and disappear as if they were both there, and not there. You feel very dull all of a sudden, as if you have realized the futility of life.", "You walk slowly to what you think is a door, tripping over invisible things along the way to the ", ".", "You feel it would be best to leave as soon as possible.")
room14 = Room(1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, -3, "You find yourself in what at first appears to be a dog park, but upon closer inspection of the large black walls surrounding the area as well as the absence of any dogs and the presence of many hooded figures, you realize that this is not a dog park. Not a dog park at all.","After searching the "," side of the dog park, you don't find an exit, yet.....","The hooded figures are staring, and coming closer.....", True)
room15 = Room(0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, -1, "You stand before the barrier,your quest finally over, you are filled with DETERMINATION. That is until you realize that this was not the end off your quest and you must continue. Go on.","You walk through the "," side of the barrier","You bump into the barrier, and you realize that it lives up to it's name", True)
room16 = Room(0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, -3, "You find yourself in a room full of mirrors. Seeing yourself repeated thousands of times causes you to realize the monster you have become. How many creatures have you killed since you came here? You realize that you are a murderer.","You step into the "," mirror.","You bump into yourself.")
room17 = Room(1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 5, "You are momentarily blinded, when the light fades you look around. You seem to be in a tranquil cavern. There is a pond in the center, where lights dance peacefully on it's surface. You sit to rest for a time.", "You get up, though you wish to stay, but a hole to the ", " beckons you. You wave goodbye to the lights, they dance a farewell.", "A cavern wall seems to be where you are thinking of going, so you stay where you are..", True)
room18 = Room(1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 3, "You find yourself standing in a river, with a waterfall nearby. You take some time to rest in the lush greenery that surrounds you. You feel at peace.","You explore the forest to the ", ".","You walk straight into the waterfall.")
room19 = Room(rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, 1, rand(2)-1, rand(2)-1, -10, "you Are forced to ponDer your doings, finding that you aRe in fact <i>perfectly</i> sane. buT that is what they all say\;", "northnorthwesteastsouth", "westeastnorthsouth", "eastnorthwestsouthsoutheastsouthnorthupwest")
room20 = Room(0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, -2,"You find yourself in the very confined space that is the interior of an elevator. There is a corpse on the floor here, foaming at the mouth. A camera in one of the corners is watching you. A sound like fingernails on a chalkboard echoes throughout the room", "You leave through the elevator door on the ", " side.", "You bump into the wall.")
room21 = Room(0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, -6, "You step somewhere, you can't tell where, because there is literally nothing.", "You will yourself out, towards the... ", ", yeah, the east, that's right, you always wanted to go south.", "The nothingness seems to extend to that direction, and moving that way is fruitless.")
room22 = Room(0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, -5, "You step somewhere, you can't tell where, because there is literally nothing except a overwhelmingly bright light.", "You will yourself out, towards the...", ", yeah, the west, that's right, you always wanted to go south.", "The nothingness seems to extend to that direction, and moving that way is fruitless.")
room23 = Room(1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 10, "You step into a wondrous room filled with peaceful plants and animals. Waterfalls and large lush trees fill the landscape. It seems as if you have found a utopia.", "You must use all of your willpower to leave this peaceful utopia to the ",".", "You find yourself sliping deeper into this peace.")
room24 = Room(0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, -8, "As soon as you enter this room, you know you should not have. Various instruments of torture are strewn about the room. The room is filled with the wailing of the not yet dead corpses and the torture machines at work. The smell is indescribable.", "You quickly leave to the ",".", "You find yourself lost among the horrors of this room." )
room25 = Room(0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, -7, "It is dark. Creepily dark. You can hear a faint whispering.", "You somehow find the light in the ", ".", "The whispering is getting louder.")
room26 = Room(0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 5, "You are in your bedroom. It is clean and tidy in here. there is a doorway that leads to the main room.", "You walk to the ", ", out of your bedroom and into the main room.", "You decide against the act of heading that direction, maybe later.", ["Lore"])
room27 = Room(0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, -2, "You are in your bedroom. It is messy and looks slightly looted. there is a doorway that leads to the main room.", "You walk to the ", ", out of your bedroom and into the main room.", "You decide against the act of heading north, maybe later.", ["Lore"])
room28 = Room(1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 2, "You are in a peaceful courtyard with a bird fountain in the center, surrounded by walls and a tower made of quartz and marble.", "You walk to the ", ", through an intricately carved doorway.", "There is a wall here, you decide it would be too much trouble to climb it.", ["Lore"])
room29 = Room(0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, "Your feet burn as you stand in the hot sand. You survey the endless expanse of desert around you, and realize that the in the years you have spent trekking through this wasteland have been useless.", "You continue your fruitless trek to the ", ".", "You become quite dizzy, probably an effect of dehydration.")
room30 = Room(0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, "You stand on top of a factory, the clanging of machinery behind you. Smoke pollutes the sky and obscures the sun. The occasional sizzle of laser cutters quietly supports the clanging.", "You walk through the factory, carefully avoiding the dangerous machines. You exit to the ", ".", "You breath in some of the smoke. It burns in the back of your throat, making it hard to breath.")#ben plz confirm
room31 = Room(0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, -2, "You are in a large warehouse, through the grimy windows you can see it is dusk. The occasional object is stored here, but everything is covered in spiderwebs.", "You open a large door in the ", "ern wall, someone helping from the other side.", "As you move, the strands of web begin catching.", ["Trip"])
room32 = Room(1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, -9, "Everything is blurry. You blink and try to focus, realizing the world around you is out of focus, not your eyes.", "You squint on your way ", ", if but only to reduce visual exposure.", "You chuckle to yourself, thinking about how this place needs glasses.", ["Trip"])
room33 = Room(0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, "You feel a knotting feeling in your gut, and lose sense of location. Glancing up, you find yourself in a room with other people, you try to get their attention, but they don't look up from their computers. At a loss, you sit down at a terminal, and begin browsing for anything to help you (and some cat pictures along the way).", "As you look through the files on your screen, you see one simply titled '", ".exe', clicking it, you feel the same knot, and the scenery changes.", "You can't leave. Goddamnit Zakiah", ["Lore"])
room34 = Room(0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, -5, "You feel the walls watching you. You look closer, seeing that these are no ordinary walls, not walls at all, but millions of creepy bald guys.", "You sprint in a ", "ernly direction, Eager to escape their watching eyes.", "You hear your blood rushing, Everything going out of focus, knowing they are all watching only making it worse.")
room35 = Room(1, 0, rand(2)-1, rand(2)-1, 1, 0, 1, 0, 0, 0, 1, 2, "You stumble on a root that wasn't there a second ago, and glance around. You are now in a grove of many trees. Every one of the trees is thin, tall, and either willow or cottonwood. It is rather peaceful, and you take a moment to rest your weary legs", "You trek off to the ", ", knowing that it is the right thing to do.", "Valiently, you make an effort to leave. Though after some time walking, you find yourself back in the grove.", True)#room35.light = (room35.dark - 1) * (room35.dark - 1)
room36 = Room(1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 6, "You stand on a hill, on a path surrounded by flowers of many different colors. You decide to search for a specific flower, yet not knowing what it looks like.", "Turning ", ", you know your search has come to an end as you spot a fower adorned terrace.", "You stop and smell the flowers.", ["Daily"])
room37 = Room(1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, -7, "yesssssssssssssss", "You exit through the ", ", stumbling over vines.", " \"I don't know...\" you mutter to yourself")
room38 = Room(0, 1, 0, 1, 0, 1, rand(1), 0, 1, 0, 1, 6, "You are in a large overhang, light from outside illuminating a massive array of small, intricately detailed clay soldiers.", "You clamber towards the ", "ern light, holding your hands above your eyes to block the light", "You stumble over the remains of the small clay soldiers, cracking them even further.", True)
room39 = Room(0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 3, "You are in a room, quite bland. You feel like it is a blank canvas, and you can do anything with it.", "You stroll to the ", ".", "Looks like you cannot, in fact, do anything with this room.")
room40 = Room(1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, rand(6) - 3, "Spikes jut up from the ground as the world molds into shape. The landscape begins to form itself, like concrete pouring into a mould. In fact, the landscape seems like one of nature, if all matter was concrete. In the far distance you see two figures, you feel it would be a bad idea to get their attention.", "Gaining your footing on the uneven ground, you stumble a few steps towards the ", ". just as you fully ready yourself to leave you hear a gleeful shout and the world reforms...", "The spiking cement grass impedes you, causing you to trip almost immediately.", ["Lore"])
room41 = Room(0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, "You can't stop blinking for a period... When you finally stop you see the world as it once was, pure and without pollution. It fills you with a tranquility, knowing there was something before humans ruined it... and maybe some echo of it here.", "", "", "")

bossroom = Room(0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, -2, "You find yourself in a wide open room. The ceiling is high and dark. An ominous feeling of doom hangs over you.", "Exhausted, you leave through the ", " door.", "You somehow walk into a nonexistent wall.", False, False)
roomBoss2 = Room(0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, -2, "You are in a small stone cavern, many twisting passageways leading through a winding cave system. You feel a drop of water plop on your head.", "You climb out through a ", "ern cave.", "You climb through a tunnel, only to find yourself in a room similar to the one you came from.", False, False)
roomBoss3 = Room(1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, "Suddenly you are in a forest. A crossroads leading in all directions, yet you feel leaving will not be that easy. Searching for why you feel that way, you notice a few houses around you, well made, and decide to lean on one to rest for a moment. Part of it chips off. You glance around hurriedly, hoping no one saw what you did. The house probably wasn't as sturdy as you expected.", "Free to leave now, you choose to go to the ", ", hoping it will lead to better fortunes and maybe even happiness.", "You somehow can't leave even with exits everywhere. You blame Zakiah.", ["Lore"], False)
roomBoss4 = Room(0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 3, "You find yourself in a room, walls covered in mechanical and mystical constructs alike. Trees are visible through the sparsely placed windows.", "You find a button hidden on the ", "ern wall, pressing it against your better judgement.", "You become distracted by the intricacies of this room.", True, False)
#plant, manmade, water, dark, animal, light, items, north, east, south, west, sane, message, exitA, exitB, exitFail, reference = False, normal = True


#New items, with the better system
#single chunk of armor calculation
class dfnChunk(object):
	def __init__(self, agil, protection = None, passive = False, durable = False, piercable = True, enchs = {}):
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
		self.ench = {"reflecting":0, "thorns":False, "destructive":0, "trueProtection":False, "layered":[0, 0]} #in conversion, change to single stuff
		self.ench.update(enchs)
	def rebuild(self):
		return dfnChunk(self.agil, self.dfn, self.all, self.dur, self.piercable, self.ench)

#single chunk of damage calculation. when putting into list, be sure to put in order: [projectile chunks, melee chunk, eternal chunks]. any other order will make some unused by attack()
class atkChunk(object):
	def __init__(self, dmg, agil, defend = True, eternal = False, piercing = 0, proj = None, enchs = {}):
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
		self.ench = {"destructive":0, "piercing":0, "heavy":0, "sweeping":0, "returning":[0, 0]} #in conversion, change to single stuff
		self.ench.update(enchs)
		#piercing level. 0 counts all armor chunks, 1 doesn't count piercable chunks, 2 skips all chunks (aside from special enchants). 3 skips everything.
		self.pierce = piercing + self.ench["piercing"]
	def rebuild(self):
		return atkChunk(self.dmg, self.agil, self.dfn, self.etrn, self.pierce - self.ench["piercing"], self.proj, self.ench)
		
allitems = []
class Item(object):
	def refresh(self):
		if self.durability <= 0 and self.maxdur > 0:
			removeitem(self)
		try:
			self.dfratio = float(self.durability)/self.maxdur
		except ZeroDivisionError:
			self.dfratio = 0
		
	#offence, defence, agility, sanity, score, name, divname, desc
	def __init__(self, offence, defence, durability, sanity, score, name, desc, img, lvl, ref = [], destructable = True, ammo = None, regenammo = [], enchs = {}, toappend = True):
		self.atkChunks = offence
		self.dfnChunks = defence
		self.durability = durability
		self.broken = False
		self.maxdur = durability
		self.sane = sanity
		self.score = score
		self.Name = name
		self.desc = desc
		self.ref = ref
		try:#Do something you can only do on objects. needed in case this is an item copy. In conversion, save both? or just the image from an image class
			self.img = pygame.transform.scale(img, (50, 50))
		except:
			self.img = getImg("items/"+img)
		self.destructable = destructable #if true, this item is removed when durability reaches 0.
		if ammo != None:
			ammo = float(ammo)
		self.ammo = ammo
		self.maxammo = ammo
		if regenammo == []:
			regenammo = [0, 0]
		self.regenammo = regenammo
		#Regen: ticks before regen, ammount regenerated; Bound is times the item will NOT be destroyed by thing that remove all items. ie: Zarol, Monoliths
		self.ench = {"mending":[-1, 0], "bound":0}
		self.ench.update(enchs)
		if self.ench["mending"][0] != -1:
			self.mendTick = 0
		else:
			self.mendTick = -1
		if self.regenammo[0] != 0:
			self.regenTick = 0
		else:
			self.regenTick = -1
			
		self.lvl = lvl
		if self.lvl == -1:
			self.findable = False
		else:
			self.findable = True
		
		self.dfratio = 0
		self.refresh()
		self.act = False #active defence
		self.dfn = False #passive defence
		self.pas = False #passive effects
		self.mel = False #has melee
		self.prj = False #has projectiles
		
		for i in self.atkChunks: #also use to build self.side
			if i.proj != None:
				self.prj = True
			else:
				if i.etrn:
					self.pas = True
				else:
					self.mel = True
		for i in self.dfnChunks:
			if i.all:
				self.dfn = True
			else:
				self.act = True
		
		self.div = ItemDisp(self)
		if toappend:
			global allitems
			allitems.append(self)
			
def newItem(item):
	prints("New Item Copy: "+item.Name+str(item))
	newAtk = []
	for x in item.atkChunks:
		newAtk.append(x.rebuild())
	newDef = []
	for x in item.dfnChunks:
		newDef.append(x.rebuild())

	#apparantly passing by reference here, so look out
	newit =  Item(newAtk, newDef, item.durability, item.sane, item.score, item.Name, item.desc, item.img, item.lvl, item.ref, item.destructable, item.ammo, item.regenammo, item.ench, False)
	return newit
	
#REF: Mono, Valve, YS, MN
#TYPE: Trip, Daily, Lore, Split
		
nothing = Item([], [], 0, 0, 0, "", "", "no_thing", -1, [], False, None, [], {}, False)
nothing.img = getImg("special/passive")
nothing.div = ItemDisp(nothing)
acorncap = Item([], [dfnChunk(1, 1, True)], 15, 4, 9, "Acorn Cap", "If you were really tiny, like, smaller than a squirrel, this would be the perfect armor. You place it over your heart  You call it a kiss", "acorncap", 1)
boardgame = Item([], [dfnChunk(0, 1, True), dfnChunk(-1, 1)], 32, 2, 2, "Board Game", "The cardboard is battered  from years of wear, but you can see the winding  path your piece would take if you were a winner.   You're not a winner.", "boardgame", 1)
bobbypin = Item([atkChunk(2, 1)], [], 35, 1, 1, "Bobby Pin", "Ow... it's sharp.", "bobbypin", 1)
safetypin = Item([atkChunk(3, 4)], [], 40, 1, 1, "Safety pin", "Not actually very safe at all. Actually quite dangerous.", "safetypin", 1)
woodstick = Item([atkChunk(1, 0)], [dfnChunk(-1, 2)], 10, 3, 1, "Wooden Stick", "It might not be the best sword, but hey, it's worth a try.", "woodstick", 1)
brokenglasses = Item([], [dfnChunk(3, 1, True), dfnChunk(-1, 0)], 10, -1, 2, "Broken Glasses", "The few shards of perfectly clear glass in these frames could have only been made by magic.", "brokenglasses", 1)
fakesword = Item([atkChunk(0, 2)], [dfnChunk(0, 1)], 10, 2, 1, "Fake Sword", "This is actually just an inflatable party favor", "fakesword", 1)
hoodie = Item([], [dfnChunk(-1, 3, True), dfnChunk(-1, 1)], 60, 5, 1, "Hoodie", "It has a flannel pattern on the inside", "hoodie", 1)
journal = Item([atkChunk(1, -1)], [dfnChunk(0, 1, True), dfnChunk(-1, 4)], 20, 4, 5, "Journal", "It's dusty and old", "journal", 1)
keyboard = Item([atkChunk(-1, 2)], [dfnChunk(-3, 5)], 80, 1, 6, "Keyboard", "Learn to type right and you won't ruin your wrists. Also use Dvorak.", "keyboard", 1)
lamp = Item([], [], 30, 2, 6, "Lamp", "Rub it hard enough and it'll be cleaner", "lamp", 1)
no_thing = Item([], [], 1, -2, -1, "Nothing", "You stare off into the distance.... You realize that you can't just get loot from nowhere.", "no_thing", 1)
#var reflectivevest = new item(0, 1, 1, 1, 1, "Reflective Vest", "reflectivevest","At least you won't get hit by a car");
#var sharktooth = new item(2, 0, 2, 1, 2, "Shark Tooth", "sharktooth","Maybe you can give it to the tooth fairy and get some money.");
#var steeltoedboots = new item(1, 5, -2, 1, 1, "Steel Boots", "steeltoedboots", "Your enemy might be able to kill you, but hey at least your toes will be fine.");
#var styrofoamchestplate = new item(0, 1, -1, 2, 2, "White Chestplate", "styrofoamchestplate","It's hefty with beautiful detailing that shines in even the blackest cavern.  You wish it was made out of something other than styrofoam.");
wandofwater = Item([atkChunk(3, 1, True, False, 1, 2), atkChunk(2, -1)], [], 20, -3, 3, "Wand of Water", "You'll never be thirsty again", "wandofwater", 1, [], True, 20, [30, 1])
wings = Item([], [dfnChunk(-5, 2, True, False, False)], 40, -2, 1, "Wings", "Now you can fly!  (No you can't)", "wings", 1)
#var organs = new item(1, 1, 3, -5, 5, "Organs", "organs", "A wet gooey mass that drips on your hand.  You can hear an almost musical wheeze.");
onepin = Item([atkChunk(5, 5, False)], [], 100, 2, 4, "One Pin", "The tip is dull from overuse.", "onepin", 1)
nerfgun = Item([atkChunk(2, 10, False, False, 0, 1)], [], 60, 3, 3, "Nerf Gun", "Sometimes Styrofoam bullets can hurt.", "nerfgun", 1, [], True, 6, [750, 6])

redbook = Item([atkChunk(1, -1)], [dfnChunk(0, 2)], 40, 2, 6, "Red Book", "There are no markings, but you feel as though there are many others much like it.", "redbook", 1, ["Mono"])
buttton = Item([], [dfnChunk(-3, 1, True)], 50, 3, 9, "Button", "Even though it is just a normal button, you feel as though it marks you for a death from an unknown source.", "buttton", 1, ["Trip"])

'''

var rotflesh = new item(3,2, 0, -7, 4,"Rotting Flesh","rotflesh","It's a rotting leg, snatched off a carcass that was probably dead.   Probably.");
var crate = new item(-1, 3, -3, 2, 3, "Crate", "crate","It cowers, trying to get away from you.  You can hear it whimper.  It knows what's coming.");
var fakebeard = new item(0,1,3,4,4,"Beard", "fakebeard", "It's a beard. You suddenly feel like you have been here for longer than you think you have.");
var gear = new item(3, 2, 2, 2, 1, "Gear", "gear", "A small gear. It looks like it fell out of some machine.");
var catears = new item(2, 2, 2, 2, 2, "Cat Ears", "catears", "nekomimi");
var bikeweel = new item(2, 1, -3, 2, 3, "Bike Wheel", "bikeweel", "It's part of your bike. Did you have a bike?");
var recording = new item(7, -2, 1, -2, 6, "Recording", "recording", "Nyan cat recording");
var potato = new item(2, 2, 1, 8, 6, "Potato", "potato", "Quite a normal potato.");
var otatop = new item(0, 7, -2, -2, 6, "Otatop", "otatop", "Quite a inverted potato.");
var squiglasses = new item(2, 1, 2, 4, 7, "Glasses", "squiglasses", "They are non-prescription, acting more as a mask, allowing you to be someone else.");
var map = new item(0, 1, 3, 1, 8, "Map", "map", "A roughly drawn map, you don't recognize any of the landmarks. You deem it useless.");
var cable = new item(2, 0, 1, 5, 3, "a Cable", "cable", "You are sure it charges something.<br/>Somewhere.");
var croptop = new item(0, 3, 2, 2, 3, "Crop Top", "croptop", "It is woven from corn stalks. You are amazed by the makers commitment as you laugh yourself to tears.");
var rock = new item(3, 2, 0, 2, 2, "Rock", "rock", "A small rock. It's tasty. Maybe a bit too much salt.");
var fourclover = new item(0, 1, 7, 15, 4, "Clover", "fourclover", "A four leaf clover. How lucky!");
var sevenclover = new item(0, 1, 15, 20, 4, "Clover", "sevenclover", "A seven leaf clover. Quite lucky?");
var stonekey = new item(1, 1, 3, 5, 5, "Stone Key", "stonekey", "A stone key. It looks like it fits into a door somewhere.")
var happyshirt = new item(0, 2, 3, 10, 3, "Happy Shirt", "happyshirt", "It makes you smile when clouds are gray.")

'''

#LEVEL 2
circularsaw = Item([atkChunk(15, 0, True, False, 1, None, {"destructive":5, "heavy":1})], [dfnChunk(-1, -5, True)], 120, -7, 8, "Circular Saw", "You feel as though only a psychopath would use this as a weapon. The stains of blood imply that it already has.", "circularsaw", 2, ["YS"])
bullet = Item([atkChunk(0, 1, False, True, 1, None, {"heavy":1, "destructive":2})], [], 180, 1, 9, "Bullet", "A massive bullet, it could probably take out a tank from the right gun.", "bullet", 2, ["Split"])
mirror0 = Item([], [dfnChunk(-15, 20, False, False, False, {"reflecting":0.2})], 10, 5, 3, "Grimy Mirror", "Covered with muck, seems to reflect things thrown upon it. But still only as durable as any old plate of glass.", "mirror0", 2)
brokenseashell = Item([atkChunk(-1, 4, False, True)], [dfnChunk(4, 2, True)], 20, 5, 8, "Broken seashell", "It appears recently broken, but you keep it for sentimental value. Towards what, even you cannot quite tell.", "brokenseashell", 2, ["Split"])
redball = Item([atkChunk(-1, 1, False, True)], [dfnChunk(8, 1, True)], 8, 10, 6, "Red Ball", "It is comforting, yet oddly unnerving. You keep it as an anchor to remind you of the 'real world.'", "redball", 2, ["MN"])
crowbar = Item([atkChunk(3, -2)], [dfnChunk(0, 3, False, True)], 300, 3, 3, "Crowbar", "A red crowbar. You feel as though the fact that it has three points is significant.", "crowbar", 1, ["Valve"])

#LEVEL 3
higgs = Item([atkChunk(1, 1, False, True, 1)], [], 5, -15, 4, "Higgs Boson", "You have no idea how you found this. And you know you probably shouldn't have been able to.", "higgs", 3, [], True, None, [], {"mending":[1000, -1]})
romace = Item([atkChunk(26, 5)], [dfnChunk(-3, 2, True), dfnChunk(-10, 18, False, False, True, {"thorns":atkChunk(5, -10)})], 500, 5, 5, "Romace", "It was love at first slice.", "mace", 3, ["Self"])#"mace of restoration, neverwinter game"
mirror1 = Item([], [dfnChunk(-20, None, False, False, False, {"reflecting":0.6})], 30, 6, 3, "Mirror", "Quite clear, seems to reflect anything thrown upon it. But still only as durable as any old plate of glass.", "mirror1", 3)

#LEVEL 4
mirror2 = Item([], [dfnChunk(-10, None, False, False, False, {"reflecting":1, "trueProtection":True})], 50, 7, 3, "Shiny Mirror", "Clean as new, seems to reflect anything thrown upon it perfectly. But still only as durable as any old plate of glass.", "mirror2", 4)

#LEVEL 5
mirror3 = Item([], [dfnChunk(-10, None, False, False, False, {"reflecting":1.4, "trueProtection":True})], 100, 2, 3, "Gleaming Mirror", "Shining like nothing before, Reflecting things tossed upon it with vigor to surpass your own.", "mirror1", 5)

#--BOSS ITEMS--
#HERO
heroshield = Item([], [dfnChunk(-5, 6, False, False, False), dfnChunk(-2, 4, True)], 600, 1, 10, "Heroes Shield", "You feel a bit bad, killing someone with origins probably alike yours.", "heroshield", -1, [], False)
herosword = Item([atkChunk(6, 2)], [dfnChunk(0, 2, False, True)], 200, 1, 10, "Heroes Sword", "A fitting weapon for a hero. But are <i>you<i> a hero?", "herosword", -1, [], False)

#COOSOME
fishingrod = Item([atkChunk(6, 10, True, False, 1, 1, {"destructive":5}), atkChunk(5, 0)], [dfnChunk(0, 3)], 150, 0, 10, "Fishing Rod", "Hook, Line, and Sink.", "fishingrod", -1, ["Self"], True, 1, [300, 1])
pencil = Item([atkChunk(8, -5, True, False, 0, None, {"heavy":1})], [dfnChunk(-5, 10), dfnChunk(-1, 2, True, True)], 300, -5, 10, "the Pencil", "Quite oversized, you use it as a blunt weapon. But you feel there is more to it.", "pencil", -1, ["Self"], False, None, [], {"mending":[50, 1]})
drawingpad = Item([atkChunk(2, 1, True, True, 1)], [dfnChunk(5, 2, True, True, False)], 50, 12, 10, "Drawing Pad", "Using this, you can stay positive. Because everything else is in here.", "drawingpad", -1, [], False, None, [], {"mending":[500, 10]})
spoon = Item([atkChunk(50, 7, False, False, 2, 30), atkChunk(35, 6, False, False, 1, 1, {"returning":[2, 100]}), atkChunk(15, 3, True, True)], [dfnChunk(1, 1)], 100, -8, 10, "the Spoon", "It's just a spoon. But something feels powerful about it...", "spoon", -1, ["Self", "Lore"], False, 30, [10, 1], {"mending":[500, 1], "bound":2})

#ALPHA
alphaxe = Item([atkChunk(20, -2, True, False, 0, None, {"sweeping":2, "heavy":1})], [dfnChunk(-2, -2, True, True), dfnChunk(-10, 12)], 250, 0, 10, "Alpha's Axe", "A large heavy axe, with surprisingly powerful hits.", "alphaxe", -1, ["Self", "Lore"], False)
sivgoggles = Item([atkChunk(4, 15, False, True, 1, None, {"sweeping":1})], [dfnChunk(10, 2, True), dfnChunk(25, 2, False, True, True, {"trueProtection":True})], 30, -15, 10, "Alpha's Glasses", "Gazing through them, You can see things. Where they are, and where they are going.", "sivgoggles", -1, ["Self", "Lore"], False, None, [], {"bound":4, "mending":[3, 1]})
hair = Item([atkChunk(1, 1, False, True, 0, None, {"destructive":30})], [], 10, -100, 10, "Alpha's Hair", "You stole this from a boss. Well, stole isn't the right word. More of Generated through Desire.", "hair", -1, ["Self"], False, None, [], {"bound":10})
shurikenbag = Item([atkChunk(35, 25, False, False, 1, 5, {"sweeping":5}), atkChunk(15, 20, True, False, 0, 1, {"returning":[2, 80], "destructive":10})], [dfnChunk(5, 4, True)], 100, -35, 10, "Shuriken Pouch", "A small, blood filled pouch, when you reach your hand into it, you always pull out a shuriken.", "shurikenbag", -1, ["Self", "Lore"], False, 10, [1, 1], {"bound":1, "mending":[5, 2]})
#rune = Item() #the god rune

#JIM GRIND
jimsword = Item([atkChunk(25, 20, True, False, 0, None, {"heavy":3})], [dfnChunk(-20, None), dfnChunk(-20, 4, True)], 1000, 0, 10, "Jim's Sword", "An incredibly heavy weapon, you can barely pick it up off the ground; you also wonder how that man could toss it around.", "jimsword", -1, ["Self"])
communism = Item([atkChunk(80, 100, True, False, 2, 1, {"heavy":2}), atkChunk(5, -10)], [], 100, 4, 10, "Crossbow", "An intricate, heavy crossbow with an ingraved name: 'Communism mk. II'", "communism", -1, ["Self"], True, 1, [500, 1])
jimarmor = Item([], [dfnChunk(-10, 5, False, True), dfnChunk(-20), dfnChunk(-5, 8, True, True, None, {"layered":[70, 2]}), dfnChunk(-5, 25, True, False, None, {"trueProtection":True, "thorns":atkChunk(5, 0, False)})], 500, -2, 10, "Enchanted Armor", "Glimmering metallic armor, Material flowing smoothly within it to fill the gaps in its structure.", "jimarmor", -1, ["Self"], False, None, [], {"mending":[5, 4]})
hatandboots = Item([], [dfnChunk(15, 10, False, True), dfnChunk(0, None, False, False, False, {"trueProtection":True}), dfnChunk(0, 15, True, True, False, {"layered":[80, 2]}), dfnChunk(20, 20, True, False, False, {"trueProtection":True})], 800, -2, 10, "Hat and Boots", "Can't Bump your head anymore, and probably won't stub your toes.", "hatandboots", -1, ["Self"], False, None, [], {"mending":[1, 1], "bound":2})
	
#CUBE
device = Item([atkChunk(30, 30, False, False, 2, None, {"sweeping":2}), atkChunk(10, 5, False, True)], [], 80, -6, 10, "Electrical Device", "You have no idea how it works, but it looks far beyond any tech you have ever seen.", "device", -1, ["Self", "Lore"], False, None, [], {"mending":[20, 1]})
inactivecube = Item([], [dfnChunk(0, 1)], 1, 0, 10, "Inactive Cube", "You bet you could find some way to use it.", "inactivecube", -1, ["Self", "Lore"], False)
#card = item(2, 25, 25, 0, 20, "00000111", "card", "")

#ZAROL
zaroltrophy = Item([], [], 1, 0, 30, "Zarol Trophy", "Thinking back, Seriously. How the hell did you do that?", "zaroltrophy", -1, ["Self"], True, None, [], {"bound":2})
zarolflesh = Item([], [dfnChunk(2, 15, True, True, False, {"destructive":5}), dfnChunk(-2, 2, False, True, False, {"layered":[60, 10], "thorns":atkChunk(5, 0, False, False, 0, None, {"destructive":1})})], 1000, -10, 10, "Zarol's Flesh", "A mysterious substance, unlike any of which you have ever seen before.", "zflesh", -1, ["Self"], True, None, [], {"mending":[5, -2]})
zarolmist = Item([atkChunk(25, 20, False, False, 2, 10, {"destructive":30, "sweeping":5}), atkChunk(10, 0, True, True, 1, None, {"destructive":20})], [], 20, -10, 10, "Zarol Mist", "How you can possess this eludes your mind.", "zmist", -1, ["Self"], False, 10, [20, 1], {"mending":[15, 1]})

lapis = Item([atkChunk(5000, 5000, False, False, 3, None, {"sweeping":1000})], [dfnChunk(0, None, False, True, False, {"trueProtection":True})], 1000, 0, 0, "Lapis", "The gem of the gods. Or at least the god of 7.", "lapis", -1, [], False, None, [], {"bound":100, "mending":[50, 1000]}, False)


class Player(object):
	def __init__(self):
		self.name = "player"
		self.hp = 100
		self.dmg = 8
		self.dfn = 0
		self.ddev = 3
		self.heal = 1
		self.maxhp = 100
		self.hdev = 3
		self.baseagil = [18, 100]
		self.agil = [15, 100]
		self.lvl = 1
		self.sane = 8 #PLAYER sanity
		self.sanity = 8 #WITH ITEMS sanity
		self.trueSane = 0
		self.minions = []
		self.id = 0
		self.minionTree = []
		self.defending = False
		self.equipped = [nothing, nothing, nothing, nothing]

		self.hpratio = 1.0
		self.dfratio = 0.0
	
	def reStats(self):
		prints("Recalculating stats for: "+self.name)
		self.dfratio = float(0)
		self.hpratio = float(1)
		dfTotal = 0
		for i in self.equipped:
			dfTotal += i.maxdur
			self.dfratio += i.durability
		
		try:
			self.dfratio = self.dfratio/dfTotal #Wait, why doesn't this crash all the time? is it because of the nothing item?
		except ZeroDivisionError:
			self.dfratio = 0
		
		ratio = (float(self.hp)/self.maxhp)
		if ratio < 0:
			ratio = 0

		self.hpratio = ratio

	def refresh(self):
		#set self.sanity
		localrand = self.sane
		localdfn = self.dfn
		localatk = self.dmg
		for i in self.equipped:
			localrand += i.sane
			for x in i.atkChunks:
				if x.etrn:
					localatk += x.dmg
			for x in i.dfnChunks:
				if x.all and x.dfn != None:
					localdfn += x.dfn
		global score
		if score < 0:
			localrand += score*2
		self.sanity = math.floor(localrand)
		global TI1
		TI1 = DispObj([DispObj(smallfont.render("Health: "+str(self.hp), True, (0, 0, 0))), DispObj(smallfont.render("Base Dmg: "+str(localatk), True, (0, 0, 0)), (0, 15)), DispObj(smallfont.render("Base Dfn: "+str(localdfn), True, (0, 0, 0)), (0, 30)), DispObj(smallfont.render("Score: "+str(score), True, (0, 0, 0)), (0, 45)), DispObj(smallfont.render("Level: "+str(self.lvl), True, (0, 0, 0)), (0, 60)), DispObj(smallfont.render("Room: "+str(turn), True, (0, 0, 0)), (0, 75))], (10, 126), False, (195, 120)) #inventory stats
		
pla = Player()
pla.refresh()
pla.reStats()
actions = [["atk1", 1]]
bosses = []


class Enm(object):
	#enemy base:	   atk, de, name, pic, maxhp, ddev, agil, sane, message, cry, lvl, rundown, heal, interval, equip = [nothing]
	#boss base:		hp, atk,   de,  name, img, maxhp, ddev, agil, heal, sane, loot, loot2, turn, message, cry, rundown, room, interval, equip = [nothing] #NEW INTERVALS NEED TO BE HALF ORIGONAL
					  #hp, maxhp, atk, ddev, de, agil, heal, sane, lvl, name, pic, message, desc, interval, distract
	def __init__(self, hp, maxhp, atk, ddev, dfn, agil, heal, sane, name, img, message, cry, rundown, interval, actions = [], equip = [nothing], Boss = False, room = None, turn = -1, toappend = True):
		self.hp = float(hp) #initial
		self.maxhp = maxhp #max
		self.hptop = hp #
		self.dmg = atk #damage += atk (if melee)
		self.ddev = ddev #damage +- ddev
		self.dfn = dfn #damage -= dfn
		self.baseagil = agil[:]
		self.agil = agil[:] #touple, #/# chance to dodge
		self.heal = heal
		self.sane = sane #Added to sanity when killed
		self.name = name
		self.img = getImg("entities/"+img)
		if self.name not in ["Zarol", "Last Remnants of Sanity", "Last Remnants of Insanity"]:
			self.img = pygame.transform.scale(self.img, (129, 129)) #Resize if not full screen boss
			self.mega = False
		else:
			self.mega = True
		self.message = message #added to roommessage when in room
		self.cry = cry #start of battle message
		self.rundown = rundown #list of messages displayed in battle, might be removed *le sad*
		self.atkInt = interval #remember to math.ciel() for rebuild adventurer
		self.atkIntBase = interval
		self.equipped = equip
		self.boss = Boss
		if self.boss:
			self.room = room
			self.turn = turn
			if toappend:
				global bosses
				bosses.append(self)
		
		self.actions = actions
		self.totalact = 0
		for i in self.actions:
			self.totalact += i[1]
		
		self.defending = False
		self.hpratio = 1.0
		self.dfratio = 0.0
		
		#Minions stuff
		self.minions = []
		self.minionTree = []
		self.dist = 0
		

	def Minionize(self, dist, lvl):
		thisminion = Enm(self.hp, self.maxhp, self.dmg, self.ddev, self.dfn, self.agil, self.heal, self.sane, self.name, "", self.message, self.cry, self.rundown, self.atkIntBase, self.actions, self.equipped, False, None, -1, False)
		thisminion.dist = dist
		thisminion.turn = lvl
		return thisminion
		
	def reStats(self):
		prints("Recalculating stats for ENM: "+self.name)
		self.dfratio = float(0)
		self.hpratio = float(1)
		dfTotal = 0
		for i in self.equipped:
			dfTotal += i.maxdur
			if i.durability <= 0 and i.destructable:
				prints("Item broken: "+i.Name)
				self.equipped.remove(i)
			else:
				self.dfratio += i.durability
		try:
			self.dfratio = self.dfratio/dfTotal #Wait, why doesn't this crash all the time? is it because of the nothing item?
		except ZeroDivisionError:
			self.dfratio = 0 #apparantly it does, because this ended up here
		
		ratio = (float(self.hp)/self.maxhp)
		if ratio < 0:
			ratio = 0

		self.hpratio = ratio


#MINIONS
def getMinionTree(entity, type):
	minionTree = []
	if type == 2:
		for i in entity.minions:
			minionTree.append(i)
			if len(i.minions) > 0:
				minionTree += getMinionTree(i, 2)
		return minionTree
	if type == 1:
		minionTree = []
		minionTree += getMinionTree(entity, 2)
		return minionTree

def getMinion(source, min):
	#if source is player, make div of minion with id=minion.div+minion.id.   new div is only hp
	thisMin = min.Minionize(min.dist, min.turn)
	source.minions.append(thisMin)
	if (source == pla):
		print "DISPLAY"
	source.minionTree = getMinionTree(source, 1)
	prints("Gave "+source.name+" "+thisMin.name)
		
def killMinion(source, minion):
	for i in source.minions:
		if (i == minion):
			if (source == pla):
				pass
			#printc(minion, source.name+"'s "+ minion.name+ " is dead.");
			#prints(source.name+"'s "+ minion.name+ " is dead.");
			source.minions.remove(i)
		
creepybaldguy = Enm(18, 18, 5, 2, 10, [1, 100], 4, -1, "Creepy Bald Guy", "creep", "You know you are being watched. Always... ", "you feel it staring through your eyes, Into your Soul.", ["Even though it seems nearly dead, it continues its steady gaze deep into your eyes.", "it seems to have lost some hair in this fight. You blink, realizing it was already bald.", "it seems to be observing, only attacking to see how you react.", "it is sitting there, staring at you. Waiting and observing your every move."], 100, [["atk1", 3]], [nothing])
creep2 = Enm(35, 35, 8, 3, 12, [1, 100], 8, -1, "Creepier Bald Guy", "creep2", "You know you are being watched. Always... ", "you feel it staring through your eyes, Into your Soul.", ["Even though it seems nearly dead, it continues its steady gaze deep into your eyes.", "it seems to have lost some hair in this fight. You blink, realizing it was already bald.", "it seems to be observing, only attacking to see how you react.", "it is sitting there, staring at you. Waiting and observing your every move."], 87, [["heal", 1], ["atk1", 19]], [nothing])
creep3 = Enm(120, 120, 12, 4, 15, [5, 100], 10, -2, "Creepier Balder Guy", "creep3", "You know you are being watched. Always... ", "you feel it staring through your eyes, Into your Soul.", ["Even though it seems nearly dead, it continues its steady gaze deep into your eyes.", "it seems to have lost some hair in this fight. You blink, realizing it was already bald.", "it seems to be observing, only attacking to see how you react.", "it is sitting there, staring at you. Waiting and observing your every move."], 60, [["heal", 1], ["atk1", 10]], [nothing])
creep4 = Enm(200, 200, 15, 5, 20, [10, 100], 12, -2, "Creepiest Bald Guy", "creep4", "You know you are being watched. Always... ", "you feel it staring through your eyes, Into your Soul.", ["Even though it seems nearly dead, it continues its steady gaze deep into your soul.", "it seems to have lost some hair in this fight. You blink, realizing it was already bald.", "it seems to be observing, only attacking to see how you react.", "it is sitting there, staring at you. Waiting and observing your every move."], 40, [["heal", 1], ["atk1", 10]], [nothing])
terracotta = Enm(5, 5, 0, 5, 12, [13, 100], 0, 0, "clay soldier", "terracotta", "Intricately carved hinges begin to move,", "Beginning its advance towards you.", ["It lays on the ground, cracks running through it.", "It wobbles, an arm and a leg missing.", "There are small cracks beginning to run through its body.", "it stands there, it's carefully carved tiny eyes staring at you."], 50, [["atk1", 2]], [nothing])
thug = Enm(100, 100, 7, 5, 0, [0, 100], 4, 0, "Thug", "thug", "A thug approaches you on the street. You prepare your fists, being much stronger than your lean appearance implies.", "'Hey, Idiot. Whose territory do you think you're Waltzing around in?'", ["", "", "", "He holds his hands up in front of his face, posture like that of a fake wrestler."], 150, [["heal", 1], ["atk1", 2]], [nothing])
bookofdeath = Enm(3, 3, 10, 1, 20, [5, 100], 4, -1, "Flailing Broken Binding", "bookofdeath", "A nearby book seems to stir..", "A book snaps into a row of paper teeth.....", ["It stops, all of its pages missing.", "It squeals, trying to flee.", "Pages are everywhere", "It flaps, words flying"], 37, [["heal", 3], ["atk1", 7]], [nothing])
catwatcher = Enm(65, 65, 15, 2, 5, [20, 100], 20, -1, "Watcher Catling", "catwatcher", "You feel as though something is watching you.....", "Some kind of cat person leaps at you!", ["", "", "", ""], 50, [["heal", 9], ["atk1", 11]], [nothing])
axeurlegs = Enm(10, 10, 2, 1, 0, [0, 100], 1, -2, "Axeurlegs", "axeurlegs", "One of the plants seems to be twitching.....", "Steel blades click into place as the plant spins into action!", ["", "", "", "Its spinning extremely quickly, blades hacking away at your legs inch by inch."], 4, [["atk1", 3]], [nothing])
anenemy = Enm(38, 38, 5, 10, 7, [10, 100], 8, 0, "Anenemy", "anenemy", "A sloshing sound alerts you to anenemy in the water......", "Anenemy attacks you!", ["Anenemy", "Anenemy", "Anenemy", "Anenemy"], 37, [["heal", 2], ["atk1", 8]], [nothing])
lightorb = Enm(5, 5, 12, 3, 20, [80, 100], 3, 0, "Light Orb", "lightorb", "A glowing orb floats gently towards you", "", ["It's light is so dim, you can almost make out the creature emitting it.", "it is no longer floating quite as high as before, and it's light is fading.", "It's light is getting duller, and it sways from side to side.", "It darts around in front of you, a streak of light across your vision."], 50, [["atk1", 2]], [nothing])
mimic = Enm(20, 20, 5, 5, 15, [1, 100], 3, -1, "Mimic", "mimic", "A golden chest sits with elegant details and pure beauty.", "The chest snaps open, revealing not loot,  But a row of Teeth!", ["Battered and bruised, it knows what is coming.", "You cut off its tounge. It continues to laugh.", "You have managed to knock one of its teeth out.", "It scoffs at you."], 37, [["atk1", 2]], [nothing])
nerveball = Enm(20, 20, 20, 8, 8, [10, 100], 3, -3, "the ball of nerves", "nerveball", "You see a swirling ball of... nerves?", "it turns towards you, screaming with silence   ...and electrical currents.", ["", "", "", ""], 25, [["atk1", 2]], [nothing])
clone = Enm(100, 100, 15, 5, 10, [5, 100], 10, -5, "Your clone", "clone", "You see a more menacing version of yourself in what you think is a mirror....", "", ["It's lost many of its limbs. It attempts to crawl away.", "It has realized it's mistake. It attempts to escape.", "It seems slightly startled, as if this was an accedent.", "It's you."], 37, [["heal", 1], ["atk1", 9]], [nothing])
koi = Enm(250, 250, 20, 3, -2, [1, 100], 50, 0, "Koi", "koi", "There is a very strange looking fish swimming in the water....", "It leaps at you, with it's blunt teeth!", ["", "", "", ""], 37, [["heal", 1], ["atk1", 9]], [nothing])
slime = Enm(150, 150, 3, 2, 15, [1, 100], 2, -3, "Slime", "slime", "a strange substance seems to be dripping from above you...", "You are consumed by a large blob of jelly!", ["You final stick your head out, the slime almost gone.", "You attempt to escape. This sort of works.", "The acid melts away your skin.", "You can't breath"], 13, [["heal", 1], ["atk1", 39]], [nothing])
dog = Enm(175, 175, 10, 20, 10, [4, 100], 0, 0, "Dog", "dog", "The sounds of a happy dog are getting louder....", "ARF ARF!", ["The dog is wimpering now. It's afraid.", "Tastes like gingerbread", "Smells like gingerbread.", "It runs up to you, ready to play."], 37, [["atk1", 100]], [nothing])
muffin = Enm(30, 30, 2, 2, 2, [80, 100], 20, 4, "Muffin", "muffin", "A bake sale is going on nearby", "An angry muffin attacks you with it's tiny fangs bared!", ["Only now, with its body crumbling, does it consider you might be stronger, and begins searching for an escape", "Though a few bit-sized chunks have fallen off, it maintains its combative stance.", "A few crumbs have fallen off, but it still stays committed.", "'I SHALL NOT BE DEFEATED' it shouts"], 25, [["heal", 4], ["atk1", 11]], [nothing])
rockgolum = Enm(200, 200, 10, 20, 35, [1, 100], 10, 0, "Rock Golum", "rockgolum", "You hear a thumping from nearby", "A golum bursts from the wall!", ["", "", "", ""], 75, [["heal", 1], ["atk1", 99]], [nothing])
enm = creepybaldguy


#Minions
trapfall = Enm(100, 100, 80, 10, 10, [500, 100], 0, -1, "Ceiling trap", "trapfall", "There are lines in the cieling.", "it's a tarp!", [], 500, [["atk1", 2]], [nothing])
trapfall = trapfall.Minionize(0, 7)
trapfire = Enm(5, 5, 1, 0, 1, [500, 100], 0, -1, "Fire Trap", "trapfire", "Fiiiirrrreeeee", "it's a tarp!", [], 7, [["atk1", 2]], [nothing])
trapfire = trapfire.Minionize(1, 7)
trapdart = Enm(1, 1, 10, 1, 0, [0, 100], 0, -1, "Dart Trap", "trapdart", "You stumble over a small box.", "it's a tarp!", [], 95, [["atk1", 2]], [nothing])
trapdart = trapdart.Minionize(2, 7)
trapsword = Enm(1, 1, 20, 3, 0, [0, 100], 0, -1, "Sword Trap", "trapsword", "You stumble over a small box.", "it's a tarp!", [], 600, [["atk1", 2]], [nothing])
trapsword = trapsword.Minionize(1, 7)
shield = Enm(400, 430, 20, 4, 4, [0, 100], 0, 3, "Shield", "shield", "You see a shield lying next to you. You decide to pick it up and take it with you.", "A shield", [], 200, [["atk1", 2]], [nothing])
shield = shield.Minionize(80, 5)
sheild = Enm(150, 170, 10, 4, 5, [0, 100], 0, 3, "Sheild", "sheild", "You see a sheild lying next to you. You decide to pick it up and take it with you.", "A sheild", [], 300, [["atk1", 2]], [nothing])
sheild = sheild.Minionize(78, 4)
enteddy = Enm(10, 12, 3, 1, 20, [3, 100], 4, 10, "Teddy Bear", "enteddy", "You find a Teddy bear lying on the ground. You decide to pick it up.", "It looks a little grimy and beat up, but you can't seem to brush it off. Must've been made that way.", [], 125, [["heal", 1], ["atk1", 5]], [nothing])
enteddy = enteddy.Minionize(1, 4)
fairy = Enm(10, 10, 1, 0, 1, [90, 100], 1, -2, "A fairy", "fairy", " You feel a presence nearby.", "When did this get here? All it seems to do is say watch out, and tell you to listen.", [], 85, [["heal", 1], ["atk1", 29]], [nothing])
fairy = fairy.Minionize(1, 4)
nyancat = Enm(30, 35, 7, 2, 1, [88, 100], 1, -15, "Nyan Cat", "nyancat", "You see a.. Cat? It jumps up, flying toward you, Rainbows trailing it.", "Nyaning", [], 8, [["heal", 19], ["atk1", 1]], [nothing])
nyancat = nyancat.Minionize(45, 5)
strikorb = Enm(35, 45, 17, 3, -5, [25, 100], 7, -3, "Red Orb", "strikorb", "There seems to be a floating red orb here.", "It's a reddish, transparent, sphere, floating next to you. It's presence sets your blood boiling, making you ready to pounce.", [], 35, [["heal", 1], ["atk1", 14]], [nothing])
strikorb = strikorb.Minionize(8, 5)
balorb = Enm(50, 50, 10, 1, 10, [20, 100], 6, 5, "White Orb", "balorb", "There seems to be a floating white orb here.", "It's a whitish, transparent, sphere, floating next to you. It's presence cools your blood, Balancing your thoughts.", [], 40, [["heal", 1], ["atk1", 3]], [nothing])
balorb = balorb.Minionize(10, 5)
tankorb = Enm(75, 100, 1, 1, 25, [2, 100], 10, -3, "Green Orb", "tankorb", "There seems to be a floating green orb here.", "It's a greenish, transparent, sphere, floating next to you. It's presence makes you feel as though your blood is of iron, Steeling against any attack.", [], 50, [["heal", 1], ["atk1", 1]], [nothing])
tankorb = tankorb.Minionize(25, 5)
miniminion = Enm(1, 1, 0, 0, 0, [7, 100], 0, 1, "Minion", "miniminion", "A single tiny sphere, hugely out of place. It approaches you hesitantly. ", "A single tiny sphere, hanging close by.", [], 90, [["atk1", 3]], [nothing])
miniminion = miniminion.Minionize(5, 4)
superminion = Enm(40, 40, 1, 1, 2, [2, 100], 4, -5, "The Group", "superminion", "uhh, minions follow you", "A huge grouping of small orbs, swarming around you like fruit flies around fruit.", [], 10, [["heal", 1], ["atk1", 49]], [nothing])
superminion = superminion.Minionize(4, 5)
cube = Enm(1, 1, 1, 1, 20, [10, 100], 0, -1, "Cube", "cube", "There is a cube here. It is small.", "A small cube. It hungers for it's friends.", [], 50, [["atk1", 11]], [nothing])
cube = cube.Minionize(75, 6)
chicken = Enm(46, 46, 1, 4, 1, [1, 100], 10, 6, "Chicken", "chicken", "There's a chicken here.", "Loot?", [], 75, [["heal", 1], ["atk1", 99]], [nothing])
chicken = chicken.Minionize(25, 4)


#bosses
adventurer = Enm(190, 190, 10, 5, 0, [5,100], 30, -7, "Adventurer", "adventurer", "You hear the footsteps of someone else.", "It is an Adventurer, Readying his stance for Battle!", ["He seems oddly unaware of the massive amounts of damage you have dealt him. Much like you are.", "", "", "", "He seems more confident of himself, more sure of his strides.", ""], 50, [["atk1", 4], ["heal", 1]], [herosword, heroshield], True, bossroom, 10)

coo33 = Enm(80, 120, -5, 75, 10, [19,100], 8, -2, "coo33", "coosome", "You hear something behind you.", "\'Here,  Fishy..   Fishy...\'", ["It's bloodied eyes dart across you, searching for ways to finish you off quickly.", "It looks angry, but seems to have survived worse.", "It is smiling, although panting. It seems as though it's malnourishedness is taking effect.", "He seems unfazed, a low growl and a chuckle murmured from within.", "It takes a deep breath, the type one might take after a good nights sleep.", "It seems to be toying with you, darting through the room."], 26, actions, [fishingrod, pencil], True, roomBoss2, 15)
coosome = Enm(140, 150, 25, 2, 14, [14,100], 20, -1, "Coosome", "coosome", "You see someone, just as they see you. He stares at you with deadpan eyes.", "", ["It's bloodied eyes dart across you, searching for ways to finish you off quickly.", "It looks angry, but seems to have survived worse.", "It is smiling, although panting. It seems as though it's malnourishedness is taking effect.", "He seems unfazed, a low growl and a chuckle murmured from within.", "It takes a deep breath, the type one might take after a good nights sleep.", "It seems to be toying with you, darting through the room."], 34, actions, [fishingrod, pencil], True, roomBoss2, 15, False)
colton = Enm(120, 140, 10, 8, 10, [28,90], 12, -1, "Colton", "coosome", "You see a person, just as he hears you. He jumps, making an odd noise.", "", ["It's bloodied eyes dart across you, searching for ways to finish you off quickly.", "It looks angry, but seems to have survived worse.", "It is smiling, although panting. It seems as though it's malnourishedness is taking effect.", "He seems unfazed, a low growl and a chuckle murmured from within.", "It takes a deep breath, the type one might take after a good nights sleep.", "It seems to be toying with you, darting through the room."], 41, actions, [drawingpad, pencil], True, roomBoss2, 15, False)

alpha = Enm(350, 500, 14, 6, 0, [45, 80], 10, -3, "Alpha", "alpha", "You hear sudden quick footsteps from behind you.", "you turn to see someone dashing at you, Swinging a large axe!", ["", "", "", "", "", ""], 60, [["atk1", 4], ["heal", 1]], [alphaxe, sivgoggles], True, roomBoss3, 20)
jimgrind = Enm(200, 200, 10, 2, 35, [3,120], 12, -2, "Jim Grind", "jimgrind", "Someone is in the room with you. You turn just fast enough to see him. He knows he has been spotted.", "A stern look on his face; A deadly look in his eyes.", ["", "You can see small gaps in his defence now, chinks in his armor.", "His breathing is heavy, and his swings are slower, yet just as powerful.", "He stands with a confident air about him, holding his sword firmly.", "His armor is beginning to glow, even the largest gaps in his armor closing as the armor reshapes into its original form.", "He seems unaware of your blows, simply tanking all damage you may deal to him."], 130, actions, [jimsword, jimarmor], True, roomBoss4, 25)
#strangecube = Enm(250, 350, -50, 2, -5, [10,100], 75, -3, "Strange Cube", "cube", "A strange cube is sitting on the ground in front or you.", "Sudden arcs of electricity jump across its surface as it rises into the air.", ["Although grounded, it still musters up powerful shocks upon you.", "It appears to have physical damage, and is barely able to keep itself aloft.", "It is wavering now, seeming to have less energy within it, focusing on attacks.", "It floats evenly in front of you, electricity visibly through internal circuits.", "electricity is visible streaking across its surface, arcing to nearby surfaces.", "It's magnetic fields are powerful, you can feel them pulling on your magnetic accessories."], 37, actions, [inactivecube, device], True, bossroom, 30)

#epicalpha = Enm(450, 450, 50, 12, 10, [65, 80], 20, -6, "Alpha 949", "alpha", "You find yourself in a familiar looking room. Looking around, you realize you have some unfinished business. You hear sudden quick footsteps from behind you.", "you turn to see a familiar figure dashing towards you, Swinging a large axe!", ["", "", "", "", "", ""], 45, actions, [sivgoggles, shurikenbag], True, roomBoss3, -100)
#epicjim = Enm(320, 360, 45, 2, 150, [0,110], 35, -2, "Jim Grind", "jimgrind", "You find yourself in a familiar looking room. Looking around, you realize you have some unfinished business. Someone is in the room with you. You turn to face him. You both know who won last time. ", "A stern look on his face; A deadly look in his eyes.", ["", "You can see small gaps in his defence now, chinks in his armor.", "His breathing is heavy, and his swings are slower, yet just as powerful.", "He stands with a confident air about him, holding his sword firmly.", "His armor is beginning to glow, even the largest chinks in his armor closing as the armor reshapes into its original form.", "He seems unaware of your blows, simply tanking all damage you may deal to him."], 95, actions, [jimarmor, hatandboots], True, roomBoss4, -100)
#epiccoo = Enm(400, 400, 40, 100, 15, [30,100], 22, -4, "The Coosome", "coosome", "You find yourself in a familiar looking room. Looking around, you realize you have some unfinished business. You hear a familiar chilling voice behind you.", "\'Here,  Fishy..   Fishy...\'", ["It's bloodied eyes dart across you, searching for ways to finish you off quickly.", "It looks angry, but seems to have survived worse.", "It is smiling, although panting. It seems as though it's malnourishedness is taking effect.", "He seems unfazed, a low growl and a chuckle murmured from within.", "It takes a deep breath, the type one might take after a good nights sleep.", "It seems to be toying with you, darting through the room."], 25, actions, [pencil, spoon], True, roomBoss2, -100)

lastsanity = Enm(500, 500, 18, 5, 16, [29,100], 100, -100, "Last Remnants of Sanity", "lastsanity", "You feel parts of your mind fighting back, with nonsense of '<i>Something is wrong</i>.'", "You realize you need to silence these nagging voices.", ["<i>You are destroying yourself...</i>", "<i>Do you even know the names of the people you killed?</i>", "<i></i>", "<i>Something is seriously wrong with you,</i>"], 60, actions, [], True, bossroom, -100)
lastinsanity = Enm(1000, 1000, 15, 90, 10, [2,100], 3, 100, "Last Remnants of Insanity", "lastinsanity", "You feel parts of your mind begin to come together.......", "You have come to a realization: the only way to obtain your goal is to wipe insanity from your mind.", ["but.. What is this place?", "How do you not return to what was already there?", "", ""], 25, actions, [], True, bossroom, -100)
#creepiestbaldest = Enm(400, 500, 40, 1, 5, [83, 100], 20, -20, "The Knowing Eye", "creepiestbaldest", "You see one blink. And with its eyes, another one is opening.", "You feel its knowing gaze, that it has nothing more to learn.", ["", "", "", "", "", ""], 55, [["atk1", ]], [map, shinedisk], True, room34, 52)


coompanion = coo33.Minionize(100, 15)


minions = [coompanion, cube, shield, sheild, nyancat, balorb, strikorb, tankorb, superminion, miniminion] #, mincreep2, mincreep3, mincreep4, enteddy, fairy, chicken, trapfall, trapfire];

class crafter(object):
	def __init__(self):
		self.Istage = 0
		self.Ostage = 0
		self.mode = 0
		self.working = False #doing something
		self.disabled = False #used up
		self.inroom = False #is it in the room?
		self.inputs = [nothing, nothing]
		self.output = nothing
		self.img = Scrafter
		self.Iimg = (getImg("special/I0"), getImg("special/I1"))
		self.Oimg = (getImg("special/O0"), getImg("special/O1"), getImg("special/O2"))
		self.Mimg = (getImg("special/M0"), getImg("special/M1"), getImg("special/M2"))
		
		
C = crafter()

zarol = None
def buildFinal():
	global score
	global runs
	global bossmisc
	global endboss
	
	if endboss == "zarol":
		global bossroom
		global zarolflesh
		global zarolmist
		global zaroltrophy
		enm = Enm(500+score, 10000+score*2, 5, 80, 18+runs*5, [5, 100], 1000+score, -10, "Zarol", "zarol", "You stand in the final room, reveling in your victory.  From just over your left shoulder, you hear heavy breathing.", "Your head slowly swivels, back poker straight, to look into three wide red eyes.", ["Everything you can see is unrecognizable, even the boss that has now dispersed to the point of surrounding you.", "It is infuriated by your damage, darkness billowing from its wounds, disintegrating all it touches.", "You seem to have gotten its attention, but it's cold glare assures you this is not a good.", "It seems almost to be ignoring you, focusing solely on destruction.", "You feel an aura of confidence, coming from it as it methodically destroys all that surrounds it.", "You feel a burst of energy from it, enveloping you with searing pain."], 75, actions, [zaroltrophy, zaroltrophy], True, bossroom, 45, False)
	
	if endboss == "Coo":
		global spoon
		global pencil
		print "COO BOSS SPAWN"
		
	if endboss == "North":
		print "NORTH BOSS SPAWN"
		
	if endboss == "Blue":
		print "BLUE BOSS SPAWN"
		
	if endboss == "Jim":
		global jimsword
		global communism
		global jimarmor
		global hatandboots
		print "JIM BOSS SPAWN"
		
	if endboss == "Siv":
		#global rune
		print "SIV BOSS SPAWN"
	
	return enm
#minions go here, not needed yet
#for i in bosses:
#	print i.name, i.turn

def Heal(entity):
	global pla
	global inbattle
	global healable
	if (entity == pla and pla.hp > 0):
		if inbattle:
			heal = pla.heal + random.randint(0, 2*pla.hdev)-pla.hdev
			if (pla.hp + heal > pla.maxhp):
				heal = pla.maxhp - pla.hp
			pla.hp = pla.hp+heal
			if pla.hp > pla.maxhp:
				heal -= pla.hp - pla.maxhp
				pla.hp = pla.maxhp
			pla.reStats()
			return "you heal "+str(heal)+" hp"
				
		else:
			if healable:
				heal = pla.heal*10 + random.randint(0, 3*pla.hdev)
				if (pla.hp + heal > pla.maxhp):
					heal = pla.maxhp - pla.hp
				pla.hp = pla.hp+heal
				if (pla.hp > pla.maxhp):
					heal -= pla.hp - pla.maxhp
					pla.hp = pla.maxhp
				healable = False
				if heal > 0:
					pla.reStats()
					return "You heal "+str(heal)+" hp!"
					pla.sane += 0.2 #soon REMOVE
				else:
					healable = True
					return "You are already at peak health."
			else:
				return "You feel as though you should move on."
	else:
		if (entity.hp + entity.heal > entity.maxhp):
			heal = entity.maxhp - entity.hp
		else:
			heal = entity.heal
		entity.hp = entity.hp+heal
		#printc(entity, entity.name + " heals <strong>"+ heal+ "</strong> hp") #VISUALS
		print entity.name+" Healed"
		entity.reStats()

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
		if i.findable and pla.lvl >= i.lvl:
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
			if ((i.sane <= 0 and pla.trueSane < 0) or (i.sane >= 0 and pla.trueSane > 0)) and i.findable:
				lootitems.append(i)
		for i in rooms:
			if ((i.sanity <= 0 and pla.trueSane < 0) or (i.sanity >= 0 and pla.trueSane > 0)) and i.findable:
				ablerooms.append(i)

def prepbattle(enemy):
	global search
	global enm
	global pla
	global battleprep
	global Sbattle
	global zarol
	global lastinsanity
	global SanPool
	search = False
	enm = enemy
	if enm.boss:
		pla.sane += SanPool
		SanPool = 0
	pla.defending = False
	'''localrand = rand(100) #Traps
	if (localrand == 1){
		enm.minions.push(alltraps[rand(alltraps.length-1)]);
	}'''
	if enm.name == "Zarol":
		global Szarol
		Sbattle = Szarol
	elif enm.name == lastinsanity.name:
		global Sinsane
		Sbattle = Sinsane
	else:
		global Smain
		Sbattle = Smain
	
	'''if (enm.name == zarol.name){
		zarol = buildZarol();
		enm = zarol
	}'''
	battleprep = 400
	#VISUALS Clear all battle message areas
	pla.minionTree = getMinionTree(pla, 1)
	enm.minionTree = getMinionTree(enm, 1)
	for i in enm.minionTree:
		i.atkInt = rand(i.atkIntBase)
	for i in pla.minionTree:
		i.atkInt = rand(i.atkIntBase)
	enm.reStats()
	return enm.message

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
	global endboss
	global C
	global SanPool
	
	pla.refresh()
	print pla.sane, pla.sanity
	
	prints("Generating room.")
	gentables()
	turn += 1
	healable = True

	#used for enemy stuff
	enmpool = []
	enmcount = 0
	
	
	if rand(5) <= 3:
		C.inroom = True
		C.disabled = False
		if C.working:
			C.output = Enchant(C.output)
		else:
			C.Istage = 0
			C.Ostage = 0
	else:
		C.inroom = False
	
	#leveling up
	if (score >= 35 and pla.lvl == 1):
		pla.lvl = 2
		roommessage += "You can sence something.. Change, or Alter, in the dongeons around you.."
	if (score >= 100 and pla.lvl == 2):
		pla.lvl = 3
		roommessage += "You hear the calls of things, Unknown Creatures, from close by.."
	if (score >= 250 and pla.lvl == 3):
		pla.lvl = 4
		roommessage += "You feel attention has shifted to you, knowing this is not a good thing."
	if (score >= 400 and pla.lvl == 4):
		pla.lvl = 5
		roommessage += "You can feel the Anger, the Hatred in the dongeon, Radiating from the surfaces, Aimed at you..."
	if (score >= 800 and pla.lvl == 5):
		pla.lvl = 6
		roommessage += "The hairs rise on the back of your neck. You have reached your top potential, and know it is only downhill from here."
	pla.refresh()
	
	search = True
	if (turn == 1):
		search = False
		
	global bosses
	for i in bosses: #bosses
		if (i.turn == turn):
			search = False
			room = i.room
	if turn == 35: #epics
		search = False
	
	if turn == 45: #final bosses
		search = False
		prepbattle(buildFinal())
		global enm
		room = enm.room
			

	if (search or turn == 1):
		room = ablerooms[rand(len(ablerooms))-1]
	roommessage += room.message
	if room.isref != False:
		prints("Room is a reference.")
	
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
		enmcount -= 1 #increase enm chance
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
		SanPool -= 1
	if (avent == 12):
		roommessage += " You hear whispering. You turn quickly, but nothing is there."
		SanPool -= 3
	if (avent == 13):
		roommessage += " You feel a tap on your shoulder, and turn around to find that there is nothing there."
		SanPool -= 5
		enmcount -= 1
	if (avent == 14):
		roommessage += " No matter to the circumstances, you are tired. You take a moment to rest."
		SanPool += 5
		enmcount += 2 #reduce chance to encounter an enemy
	if (avent == 15):
		roommessage += " You feel a sense of refreshment, of redefining who you are."
		SanPool += 3
	if (avent == 16):
		roommessage += " You blink. Something seems off."
		localrand = room.north
		room.north = room.east
		room.east = room.south
		room.south = room.west
		room.west = localrand
	if (avent == 17):
		roommessage += " You feel the hairs rise on your neck."
		enmcount -= 2 + pla.lvl
	if (avent == 18):
		roommessage += " It seems calm here; in its own special way."
		enmcount += 2 * pla.lvl
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
	
	if turn == 1:
		localrand = ""
		if endboss == "zarol":
			localrand = "You can feel the tremors of a great power from within the dongeon."
		if endboss == "Jim":
			localrand = "A powerful greed from deep below sends a shiver up your spine."
		if endboss == "North":
			localrand = "You feel as though luck may be a great asset to have."
		if endboss == "Blue":
			localrand = "You feel a sudden wave of apathy."
		if endboss == "Siv":
			localrand = "You feel a need to quicken your step."
		if endboss == "Coo":
			localrand = "You know you will need to be prepared."
		roommessage += localrand
	
	SanPool += room.sanity
	for i in pla.equipped:
		SanPool += (i.sane)/5
	for i in pla.minions:
		SanPool += (i.sane / 5)
	
	
	#Determining lootable
	if (rand(2) == 1 and room.items == 1):
		lootable = True
		roommessage += chestmessages[rand(len(chestmessages)-1)]
	else:
		lootable = False

	ableminions = []
	for i in minions:
		if (i.turn <= pla.lvl):
			ableminions.append(i)
	
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
		
		'''if (pla.lvl >= 5 and search):
			enemyspawn = rand(5)
			if (enemyspawn == 3):
				roommessage += prepbattle(creep4)
		
		#change to loot table type

		if (pla.lvl >= 4 and search):
			enemyspawn = rand(6)
			if (enemyspawn == 1 and room.plant == 0 and room.animal == 0):
				roommessage += prepbattle(rockgolum)
			if (enemyspawn == 2 and room.water == 1):
				roommessage += prepbattle(koi)
			if (enemyspawn == 3):
				roommessage += prepbattle(creep3)
			if (enemyspawn == 4 and room.manmade == 1):
				roommessage += prepbattle(clone)
				
		if (pla.lvl >= 3 and search):
			enemyspawn = rand(7)
			if (enemyspawn == 4 and room.plant == 1 and room.animal == 1):
				roommessage += prepbattle(dog)
			if (enemyspawn == 5):
				roommessage += prepbattle(slime)
			if (enemyspawn <= 2 and room.water == 0 and room.dark == 1 and room.animal == 1 and room.light == 0):
				roommessage += prepbattle(catwatcher)
			if (enemyspawn == 3 and room.animal == 1 and room.light == 1):
				roommessage += prepbattle(nerveball)
		
		if (pla.lvl >= 2 and search):
			enemyspawn = rand(8)
			if (enemyspawn == 1 and room.manmade == 1 and room.water == 0):
				roommessage += prepbattle(bookofdeath)
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
			#if (enemyspawn == 3):
				#roommessage += prepbattle(muffin)
			if (enemyspawn >= 5):
				roommessage += prepbattle(creepybaldguy)
				'''
		if search:

			#add enemies to the pool, and add test counts

			if (pla.lvl >= 5):
				enmcount += 1
				if room.water:
					enmpool.append(slime)
				enmpool.append(creep4)
			if pla.lvl >= 4:
				if not room.plant and not room.animal:
					enmpool.append(rockgolum)
					enmcount += 2
				if room.water:
					enmpool.append(koi)
					enmcount += 2
				if room.manmade:
					enmpool.append(clone)
					enmcount += 1
				enmpool.append(creep3)

			if pla.lvl >= 3:
				if room.animal:
					enmcount += 1
				if not room.water:
					enmcount += 1
				if room.plant and room.animal:
					enmpool.append(dog)
				if not room.water:
					enmpool.append(slime)
				if not room.water and room.dark and room.animal and not room.light:
					enmpool.append(catwatcher)
					enmcount += 2
				if room.animal and room.light:
					enmpool.append(nerveball)
				enmpool.append(creep2)
			if pla.lvl >= 2:
				enmcount += 2
				if room.manmade and not room.water:
					enmpool.append(bookofdeath)
				if room.light and not room.dark:
					enmpool.append(lightorb)
				if not room.items:
					enmpool.append(mimic)
				enmpool.append(creep2)
			if pla.lvl >= 1:
				enmcount += 3
				if room.plant and not room.water:
					enmpool.append(axeurlegs)
				if room.water and room.animal:
					enmpool.append(anenemy)
				enmpool.append(creepybaldguy)
			prints("length: " + str(len(enmpool)))
			prints("choices: " + str(enmcount))

			localrand = random.randint(0, enmcount)
			prints("selected: "+ str(localrand))
			if localrand < len(enmpool) and localrand >= 0:
				roommessage += prepbattle(enmpool[localrand])



	global TM1
	TM1.all = wraptext(roommessage, 900, font, True)
	TM1.refresh()

#Sets the final boss of that run and removes from list. run before genroom. 
def SetBoss():
	global endboss
	global finalbosses
	global runs
	if runs > 1:
		endboss = random.choice(finalbosses)
		finalbosses.remove(endboss)
	else:
		endboss = "zarol"
	
lastmove = 1

def move(direction):
	global roommessage
	global battleprep
	global inbattle
	global room
	global TM2
	roommessage = ""
	if (battleprep == -1) and not inbattle:
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
			TM2.img = font.render("", True, (0, 0, 0))
			genRoom()
			global lastmove
			lastmove = direction
		else:
			TM2.all = wraptext(room.exitFail, 900, font, True)
			TM2.refresh()
			prints("move failed.")
	else:
		if inbattle:
			TM2.all = wraptext("It is too dangerous to leave something behind you.", 900, font, True)
			TM2.refresh()
		else:
			TM2.all = wraptext("You feel this would be a bad idea.", 900, font, True)
			TM2.refresh()
	
	
def getitem(item): #AAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHH
	global invenItems
	global score
	global TM2
	newitem = newItem(item)
	invenItems.insert(0, newitem)
	score += item.score
	prints("Found: "+item.Name)
	TM2.all = wraptext("You found "+item.Name + ". You place the newfound loot in your backpack.", 900, font, True)
	TM2.refresh()
	refreshItems(1)
	
def equip(item):
	global pla
	global invenItems
	success = False
	if item.durability > 0:
		if pla.equipped[2] == nothing or pla.equipped[3] == nothing: #try to do weapons first
			if item.mel or item.prj: #is usable as weapon
				if pla.equipped[2] == nothing:
					pla.equipped[2] = item
				elif pla.equipped[3] == nothing:
					pla.equipped[3] = item
				invenItems.remove(item)
				success = True
		if (pla.equipped[0] == nothing or pla.equipped[1] == nothing) and not success: #try to equip as armor/support item
			if item.pas or item.dfn or item.act:
				if pla.equipped[0] == nothing:
					pla.equipped[0] = item
				elif pla.equipped[1] == nothing:
					pla.equipped[1] = item
				invenItems.remove(item)
				success = True
	if success:
		refreshItems(1)
		pla.refresh()
		for i in pla.equipped:
			i.div.refresh(3)
	
def unequip(slot):
	global pla
	global invenItems
	global nothing
	if pla.equipped[slot] != nothing:
		pla.equipped[slot].div.refresh(1)
		invenItems.insert(0, pla.equipped[slot])
		pla.equipped[slot] = nothing
		refreshItems(1)
	
		pla.equipped[2].div.refresh(2)
		pla.equipped[3].div.refresh(2)

def RDloot():
	global lootable
	global lootitems
	global TM2
	if lootable:
		itemget = lootitems[random.randint(0, len(lootitems)-1)]
		'''if (itemget == rock)
			Unlock(heatrock);
		}'''
		
		getitem(itemget)
		lootable = False
	else:
		TM2.all = wraptext("There is nothing to loot here.", 900, font, True)
		TM2.refresh()
	
def removeitem(item): #must take valid item. ignores indestructable, only cares about bound
	global invenItems
	global pla
	if item in invenItems:
		if item.ench["bound"] > 0:
			item.ench["bound"] = item.ench["bound"] -1
			prints("Bound item: "+item.Name)
			if item.durability <= 0:
				item.broken = True
		else:
			prints("Removed: "+item.Name)
			invenItems.remove(item)
	elif item in pla.equipped:
		if item.ench["bound"] > 0:
			item.ench["bound"] = item.ench["bound"] -1
			prints("Bound item: "+item.Name)
			if item.durability <= 0:
				item.broken = True
				unequip(pla.equipped.index(item))
		else:
			prints("Removed: "+item.Name)
			num = pla.equipped.index(item)
			global nothing
			pla.equipped[num] = nothing
		
	else:
		prints(item.Name+" not found in inventory!")
	item.div.refresh(1)
	refreshItems(1)

#refresh an entity's stats. (agil)
def Refresh(ent):
	agilmod = 0
	for i in ent.equipped:
		for x in i.dfnChunks:
			if x.all or ent.defending:
				agilmod += x.agil
	
	ent.agil[0] = ent.baseagil[0] + agilmod
	
def op(type):
	global pla
	if type == "allitems":
		global allitems
		for i in allitems:
			getitem(i)
		getitem(lapis)
	if type == "loot":
		global lootable
		lootable = True
		RDloot()
	if type == "revive":
		global enm
		pla.hp = pla.maxhp
		prints("Revived")
		enm.hp = 0
		plaFight(1)
	if type == "insane":
		pla.trueSane = -1
		pla.baseatk = 16
		pla.ddev = 12
		pla.maxhp = 110
		pla.baseagil = [10, 110]
		pla.dfn = -5
	if type == "sane":
		pla.trueSane = 1
		pla.maxhp = 110
		pla.dfn = 5
		pla.heal = 2
		pla.ddev = 3
		pla.baseagil = [10, 90]
	if type == "normal":
		pla.trueSane = 0
		pla.maxhp = 100
		pla.baseatk = 8
		pla.ddev = 6
		pla.baseagil = [8, 100]
		pla.dfn = 0
		pla.heal = 1
		
	if type == "Craft":
		C.inroom = True
		C.disabled = False
		if not C.working:
			C.Istage = 0
			C.Ostage = 0
			
	if type == "enchant":
		if len(invenItems) > 0:
			invenItems[0] = Enchant(invenItems[0])
		refreshItems(1)
	'''if type == "minions":
		for (var i = 0; i < 3; i++){
			getMinion(pla, miniminion);
		}
		for i in pla.minions:
			for (var i = 0; i < 3; i++){
				getMinion(pla.minions[i], miniminion)'''
	
dodging = False
dodged = 0
monolithTime = 1500
gravetime = 0
monolithOrig = monolithTime
limbostuff = [0, ""]
suffix = [["You were brutaly evicerated by ", "."], ["You were slain by ", ". It mocks your death"],["You where killed by ",". The gods did not favor you today."], ["Your futile exsistance was ended by ", "."],["You where kneecaped by ", ". The cats will miss you."], ["You are dead. "," mocks your death and thinks 'hey, that was easy'."], ["Sometimes, you are favored by the gods. ", " was favored this time."], ["Your entrails where removed by ", "."], ["Your face was torn off by ", "."], ["You were fast, but ", " was faster"], ["You have lost. ", " aplauds your failure."]]

def limbo(type, message):
	global TL1
	global suffix
	global gravetime
	global Screen
	global limbostuff
	global font
	global enm
	prefix = suffix[rand(len(suffix)-1)]
	TL1.all[2] = DispObj(wraptext(prefix[0] + enm.name + prefix[1], 150, font, True), (32, 48), False, (150, 200))
	TL1.refresh()
	gravetime = 300
	Screen = 4
	limbostuff = [type, message]

def limbob(type, message = ""):
	global roommessage
	global score
	global pla
	global enm
	global runs
	global turn
	global checkpoint
	global Screen
	global dodging
	global dodged
	global monolithTime
	global monolithOrig
	global SanPool
	roommessage = ""
	#normal death
	if type == 0:
		score -= 1
		SanPool -= 5
		pla.sane += SanPool
		SanPool = 0
		if (checkpoint < 0):
			checkpoint = 1
		
		turn = checkpoint
		if (turn < -2):
			turn = -2
		pla.hp = 80+rand(20)
		pla.refresh()
		pla.reStats()
		#var screen = document.getElementById("limbotext");
		#screen.innerHTML = message; #VISUALS
		TL3.all = wraptext(message, 975, font, True, (255, 255, 255))
		TL3.refresh()
		
		if (pla.sanity < 0):
			#if (rand(100) <= pla.sanity*-1):
				#monolith spawn.
				dodging = True
				dodged = 0
				monolithTime = 1500 + (pla.sanity * 1.5)
				#do a special animation here, because we can now. #VISUALS
				if (monolithTime <= 1):
					monolithTime = 5
				monolithOrig = monolithTime
				'''var screen = document.getElementById("RDmono")
				screen.style.backgroundImage = "url('img/monoAnimation/mono1.png')";'''
				Screen = 6
			
		else:
			Screen = 5
	#anything zarol
	if type == 1:
		if (enm.hp <= 0):
			runs += 1
			'''if (runs == 1):
				Unlock(oddplug)
			if (runs == 2):
				Unlock(cresentstone)
			'''
		
		score += 10
		turn = 0
		checkpoint = 0
        
		pla.sane = pla.sane / 1.1
		pla.hp = 100
		unequip(0)
		unequip(1)
		unequip(2)
		unequip(3)
		'''
		var screen = document.getElementById("limbotext");
		screen.innerHTML = message;'''
		global invenItems
		localrand = len(invenItems)
		for i in range(len(invenItems)):
			removeitem(invenItems[localrand-(i+1)])
		localrand = len(invenItems)
		for i in range(len(invenItems)):
			removeitem(invenItems[localrand-(i+1)])
			
		global coo33
		global coosome
		global colton
		global bosses
		coosomes = [coo33, coosome, colton]
		bosses[1] = coosomes[rand(3)-1]
		for i in bosses:
			i.hp = i.hptop
		global noKillEpic
		noKillEpic = True
		SetBoss()
		#for (i in pla.minions){killMinion(pla, pla.minions[0])}
		'''for i in range(28+(runs*2)):
			getMinion(strangecube, cube)
		
		localrand = pla.minions.length
		for (var i = 0; i < localrand; i ++){
			killMinion(pla, pla.minions[0]);
		}'''
		Screen = 5
	#you jumped (button)
	
	#monolith TOUCH


def check(entity):
	global enm
	global inbattle
	global score
	global pla
	global SanPool
	if (entity.hp <= 0):
		if (entity.name == enm.name and inbattle):
			inbattle = False
			message = "You Kill the enemy."
			entity.minions = []
			score += 1
			SanPool -= 1
			SanPool += entity.sane
			pla.refresh()
			if entity.boss:
				global bossesbeat
				global checkpoint
				if (entity.name == "Zarol"):
					limbo(1, "At the moment of your victory, a swirling vortex of malevolence forms. You attempt in vain to escape it, but you are not yet strong enough. You find yourself in a familiar place...");
				if not (entity.name == "True Insanity" or entity.name == "True Sanity" or entity.name == "Zarol" or entity.name == "epicalpha" or entity.name == "epiccoo" or entity.name == "epicjim"):
					checkpoint = entity.turn
					
				localrand = rand(3)
				if (localrand == 1):
					message += " You Claim your rare prize."
					getitem(entity.equipped[1])
				else:
					message += " You Claim your prize."
					getitem(entity.equipped[0])
				bossesbeat += 1
				if (entity.name == "Adventurer" or entity.name == "Yourself"):
					prints("Recreating Adventurer.")
					[pla.equipped[2], pla.equipped[3], pla.equipped[0], pla.equipped[1]]
					if (pla.equipped[2] == nothing):
						global herosword
						miscA = herosword
					else:
						miscA = pla.equipped[2]
					if (pla.equipped[3] == nothing):
						global herosword
						miscB = herosword
					else:
						miscB = pla.equipped[3]
					if (pla.equipped[0] == nothing):
						global heroshield
						miscC = heroshield
					else:
						miscC = pla.equipped[0]
					if (pla.equipped[1] == nothing):
						global heroshield
						miscD = heroshield
					else:
						miscD = pla.equipped[1]
					global bosses
					#bosses[0] = new Boss(pla.maxhp, pla.atk, pla.def, "Yourself", "adventurer", pla.maxhp, pla.ddev, pla.agil, [plaTotal, plaTotal-plaHeal+1, 4], sanity, miscA, miscB, 10, "You hear the footsteps of someone else.", "It is an Adventurer,  Readying his stance for Battle!", ["He seems oddly unaware of the massive ammounts of damage you have delt him. Much like you were.", "", "", "", "He seems more confident of himself, more sure of his strides.",""], bossroom, (Math.floor(plaTime/plaTotal)));
					bosses[0] = Enm(pla.maxhp, pla.maxhp, pla.dmg, pla.ddev, pla.dfn, pla.baseagil, pla.heal, -15, "Yourself", "adventurer", "You hear the footsteps of someone else.", "It is an Adventurer,  Readying his stance for Battle!", ["He seems oddly unaware of the massive ammounts of damage you have delt him. Much like you were.", "", "", "", "He seems more confident of himself, more sure of his strides.",""], math.floor(plaTime/plaTotal), [["defend", pladfn], ["heal", plaheal], ["atk1", plaatk1], ["atk2", plaatk2]], [miscA, miscB, miscC, miscD], True, bossroom, 10, False)
					bosses[0].minions = pla.minions
					
				if (entity.name == "Last Remnants of Sanity"):
					op("insane")
				if (entity.name == "Last Remnants of Insanity"):
					op("sane")
			
			global Screen
			global TM2
			if Screen == 3:
				Screen = 1
			#printb(message) #VISUALS
			TM2.all = wraptext(message, 900, font, True)
			TM2.refresh()
			
		if (entity.name == pla.name):
			#printc(pla, "The enemy Kills you.") #VISUALS
			inbattle = False
		   
			if (enm.name == "Zarol"):
				limbo(1, "At the moment of your death, a swirling vortex of malevolence forms. You attempt in vain to escape it, but you are not yet strong enough. You find yourself in a familiar place...")
				#screen = document.getElementById("RDfight")
				#screen.style.backgroundImage = "url('img/screenmain.png')"
				#WHAT DOES THAT DO #VISUALS
			else:
				limbo(0, "After experiencing a moment of extreme pain, you find yourself in a suprisingly calm dark space. The only landmarks are a large cliff dropping off into endlessness infront of you, and strange floating structures to high for you to reach. You realize that there is only one thing you can do....")
		if (entity in pla.minions):
			pla.minions.remove(entity)
			
#does not include: minions, dodging, calculation of boosting items
def Damage(source, weapon, atk, target):
	enchValues = [0, 0] #local values needed for enchantments: layered, heavy
	initdmg = atk.dmg + random.randint(0, 2*source.ddev) - source.ddev
	if initdmg < 0:
		initdmg = 0
	prevdmg = initdmg
	dmg = initdmg #differentiated for enchants
	prints("------")
	prints("Initial damage: "+source.name+" "+str(initdmg)+" on "+target.name)
	for k in range(len(target.equipped)): #loop through equipped items, counts because enchantments can do stuff
		i = target.equipped[k]
		enchValues[0] = 0 #reset for layered
		for j in range(len(i.dfnChunks)): #loop through each item's defence chunks, counts because enchantments
			x = i.dfnChunks[j]
			tanked = 0
			if ((x.ench["trueProtection"] or atk.pierce < 2) and not (atk.pierce == 1 and x.piercable == True)) and ((target.defending and not x.all) or x.all) and i.durability > 0: #if you actually count the defence
				prints("Armored! defence:")
				#Damage reduction
				if x.dfn == None: #all damage goes to armor
					tanked = dmg
				else: #some damage goes to armor
					tanked = x.dfn
				
				#Damage calculation
				prints(tanked)
				dmg -= tanked
				
				prints("newdmg:"+ str(dmg))
				#Durability reduction
				weapon.durability -= x.ench["destructive"]
				if not x.dur: #if durability is taken into account
					i.durability -= atk.ench["destructive"]
					if tanked > 0:
						i.durability -= tanked
					if i.durability < 0: #if armor is destroyed, only tank as much as it can
						dmg -= i.durability
						prints("Item destroyed: "+i.Name)
						#if dmg > prevdmg:  #only do this if rebounding is back
						#	dmg = prevdmg
				
				if x.ench["thorns"] != False: #if it has thorns
					if (x.ench["thorns"].proj != None) or (atk.proj == None): #if thorns applies #NEED AN EXCEPTION TO PREVENT THORNS LOOPING. THAT WOULD BE VERY BAD
						Damage(target, i, x.ench["thorns"], source)
						print(target.name+" has POKED")
				if x.ench["reflecting"] != 0:
					Damage (source, i, atkChunk(dmg*x.ench["reflecting"], atk.agil-10, False, False, atk.pierce-1), source) #NEED AN EXCEPTION TO PREVENT THORNS LOOPING
					prints(target.name+" has REFLECTED")
			if enchValues[0] < x.ench["layered"][1]: #test layered max
				if (random.randint(0, 100) < x.ench["layered"][0]):
					j -= 1
					enchValues[0] += 1
			prevdmg = dmg
			if enchValues[1] < atk.ench["heavy"]:
				enchValues[1] += 1
				dmg = initdmg
	dmg -= target.dfn
	if target.defending:
		if dmg < 0:
			dmg = 0
	else:
		if dmg < 1:
			dmg = 1
	message = source.name+" deals <strong>"+str(dmg)+"<strong> damage to "+ target.name
	target.hp -= dmg
	prints(target.name+": "+str(target.hp))
	prints("==============")
	check(target)
	return message

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
			atk = atkChunk(source.dmg, source.agil[0]) #give a base value in case weapon has no valid atkChunks
			#Make the atkChunk to use in this attack
			for i in weapon.atkChunks:
				if i.proj == None:
					atk = atkChunk(source.dmg + i.dmg, source.agil[0] + i.agil, i.dfn, i.etrn, i.pierce, i.proj, i.ench)
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
						atk.ench = addEnch(2, atk.ench, x.ench)
			if atk.dfn:
				source.defending = False
				Refresh(source)
			
			if atk.ench["sweeping"] > 0:
				enchValues[0] = 1+atk.ench["sweeping"]
			
			if atk.proj != None and atk.ench["returning"][0] != 0:
				if atk.ench["returning"][0] > random.randint(0, 100):
					weapon.ammo += atk.ench["returning"][1]
			
			#add agil mod of used chunk
			print source.name, "agil:", [source.agil[0]+atk.agil, source.agil[1]], "ATK agil:", atk.agil, "target agil:", target.agil
			newagil = [((target.agil[0]*(source.agil[1]+atk.agil))-(((source.agil[0]+atk.agil)*target.agil[1])/2)), (target.agil[1]*(source.agil[1]+atk.agil))]
			prints("Hit chance with mods: "+str(newagil)+" : "+str((100*(newagil[1]-newagil[0]))/newagil[1])+"% hit")
			if (rand(newagil[1]) <= newagil[0]):
				messages.append(target.name + " dodged "+ source.name +"'s attack")
				
			else:
				messages.append(Damage(source, weapon, atk, target))
			attacking = False
			for c in messages:
				prints(c)
			target.reStats()
			source.reStats()
			return messages, enchValues

#Battle actions
def Do(entity):
	global enm
	global pla
	enmdo, count = rand(entity.totalact), 0 #Doing stuff
	for i in entity.actions:
		if enmdo > count and enmdo <= count+i[1]: #if it's what you are doing
			if i[0] == "heal":
				Heal(entity)
			if i[0] == "defend":
				entity.defending = True
			if "atk" in i[0]:
				if entity in pla.minionTree:
					if i[0] == "atk1":
						attack(entity, entity.equipped[0], enm)
					if i[0] == "atk2":
						attack(entity, entity.equipped[1], enm)
					if i[0] == "atk3":
						attack(entity, entity.equipped[2], enm)
					if i[0] == "atk4":
						attack(entity, entity.equipped[3], enm)
				
				else:
					if i[0] == "atk1":
						attack(enm, enm.equipped[0], pla)
					if i[0] == "atk2":
						attack(enm, enm.equipped[1], pla)
					if i[0] == "atk3":
						attack(enm, enm.equipped[2], pla)
					if i[0] == "atk4":
						attack(enm, enm.equipped[3], pla)
			
			break
		count += i[1]
	Refresh(entity)


#Getting visuals for screens
looot = font.render("Loot", True, (0, 0, 0))
inveen = font.render("Inventory", True, (0, 0, 0))
baack = font.render("Back", True, (0, 0, 0))
heeal = font.render("Heal", True, (0, 0, 0))
meem = font.render("Meditate", True, (0, 0, 0))
craft = font.render("Craft", True, (0, 0, 0))
Fdfn = DispObj(ac2Img, (130, 199))
Fheal = DispObj(getImg("special/heal"), (190, 199))

SetBoss()
genRoom()

'''getitem(shurikenbag)
getitem(spoon)
getitem(sivgoggles)
getitem(jimarmor)
getitem(communism)
prepbattle(creepybaldguy)'''

#main loop
while running:
	for event in pygame.event.get(): #key input
		if event.type == pygame.QUIT: 
			running = False
			
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: #lclick
				mouse_down = True
			if event.button == 3: #rclick
				if Screen in [2, 3, 7]:
					Screen = 1
			if event.button == 4:
				if (hitDetect((115, 10), (370, 239), mouse_pos) and Screen == 2) or (hitDetect((10, 10), (370, 239), mouse_pos) and Screen == 7): #scrolling on the items list
					if netSize > 239: #Scrolling up
						if scrollMom >= -8:
							scrollMom += 10
						else:
							scrollMom = -10
					else:
						scrollMom = 0
				
			if event.button == 5:
				if (hitDetect((115, 10), (370, 239), mouse_pos) and Screen == 2) or (hitDetect((10, 10), (370, 239), mouse_pos) and Screen == 7): #scrolling on the items list
					if netSize > 239: #Scrolling down
						if scrollMom <= 8:
							scrollMom -= 10
						else:
							scrollMom = 10
					else:
						scrollMom = 0
						
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				mouse_down = False
				
		if event.type == pygame.KEYDOWN and debug:
			if event.key == K_1:
				op("allitems")
			if event.key == K_2:
				Screen = 2
			if event.key == K_3:
				Screen = 3
			if event.key == K_4:
				Screen = 4
			if event.key == K_5:
				Screen = 5
			if event.key == K_6:
				Screen = 6
			if event.key == K_q:
				pla.hp = 0
				check(pla)
				print "Killing player."
			if event.key == K_w:
				turn = 9
				print "prepped for adventurer"
			if event.key == K_e:
				turn = 14
				print "prepped for Coosome"
			if event.key == K_r:
				turn = 19
				print "prepped for Alpha"
			if event.key == K_t:
				turn = 24
				print "prepped for Jim"
			if event.key == K_y:
				turn = 44
				print "prepped for Final Boss:", endboss
			if event.key == K_a:
				pla.refresh()
				pla.reStats()
				gentables()
				print "----------"
				print "Sanity:", pla.sane
				print "Item modified sanity:", pla.sanity
				print "True sanity:", pla.trueSane
				print "Sanity Pool:", SanPool
				print "Defending:", pla.defending
				print "Final Boss:", endboss
				print "---CRAFTER INFO---"
				print "Mode:", C.mode
				print "Input stage:", C.Istage
				print "Output stage:", C.Ostage
				print "Cooking:", C.working
				print "---ENEMY INFO---"
				print enm.name
				print "Enemy Agility:", enm.agil, " Base:", enm.baseagil
				print "Player Agility:", pla.agil, " Base:", pla.baseagil
				print "Equipped enemy items:", len(enm.equipped)
			if event.key == K_s:
				op("Craft")
				print "Crafter enabled."
			if event.key == K_d:
				op("enchant")
				print "Enchanted"
			if event.key == K_f:
				print "LAPIS STATUS"
				print len(allitems)
				print lapis.atkChunks[0], "Core"
				if invenItems[0].Name == "Lapis":
					print invenItems[0].atkChunks[0], "Inven"
			if event.key == K_g:
				getitem(lapis)
				
	mouse_pos = pygame.mouse.get_pos()

	
	if Screen == 1: #main screen
		screen.fill(Cbacking)
		screen.blit(Smain, (0, 0))
		
		screen.blit(TM1.img, TM1.coords)
		screen.blit(TM2.img, TM2.coords)
		#buttons on side
		pygame.draw.rect(screen, Cbacking, [910, 10, 75, 24])
		screen.blit(inveen, (910, 10))
		pygame.draw.rect(screen, Cbacking, [910, 37, 75, 24])
		screen.blit(looot, (910, 37))
		pygame.draw.rect(screen, Cbacking, [910, 64, 75, 24])
		screen.blit(heeal, (910, 64))
		if inbattle:
			if C.inroom:
				pygame.draw.rect(screen, Cbacking, [910, 118, 75, 24])
				screen.blit(craft, (910, 118))
			else:
				pygame.draw.rect(screen, Cbacking, [910, 91, 75, 24])
				screen.blit(meem, (910, 91))
		elif C.inroom:
			pygame.draw.rect(screen, Cbacking, [910, 91, 75, 24])
			screen.blit(craft, (910, 91))
			
		screen.blit(Scompass, (910, 174))
		
		
		if mouse_down:
			mouse_down = False
			if hitDetect((935, 174), (25, 25), mouse_pos): #north
				move(1)
			if hitDetect((960, 199), (25, 25), mouse_pos): #east
				move(2)
			if hitDetect((935, 224), (25, 25), mouse_pos): #south
				move(3)
			if hitDetect((910, 199), (25, 25), mouse_pos): #west
				move(4)

			if hitDetect((910, 10), (75, 24), mouse_pos): #invetory, button size: 75 x 24 px
				Screen = 2
				pla.refresh()
			if hitDetect((910, 37), (75, 24), mouse_pos): #loot
				RDloot()
			if hitDetect((910, 64), (75, 24), mouse_pos): #heal
				TM2.all = wraptext(Heal(pla), 900, font, True)
				TM2.refresh()
			if inbattle:
				if hitDetect((910, 91), (75, 24), mouse_pos):
					Screen = 3
				if hitDetect((910, 118), (75, 24), mouse_pos) and C.inroom:
					Screen = 7
			else:
				if hitDetect((910, 91), (75, 24), mouse_pos) and C.inroom:
					Screen = 7
	
	if Screen == 2: #inven screen
		screen.fill(Cbacking)
		screen.blit(Smain, (0, 0))
		
		#equipped items
		if pla.equipped[0] != nothing: #dfn 1
			screen.blit(pla.equipped[0].div.mini, (10, 10))
		else:
			screen.blit(ac2Img, (10, 10))
		if pla.equipped[1] != nothing: #dfn 2
			screen.blit(pla.equipped[1].div.mini, (60, 10))
		else:
			screen.blit(ac2Img, (60, 10))
		if pla.equipped[2] != nothing: #atk 1
			screen.blit(pla.equipped[2].div.mini, (10, 60))
		else:
			screen.blit(me2Img, (10, 60))
		if pla.equipped[3] != nothing: #atk 2
			screen.blit(pla.equipped[3].div.mini, (60, 60))
		else:
			screen.blit(me2Img, (60, 60))
			
		screen.blit(ItemsDisp.img, ItemsDisp.coords)
			
		#buttons and stuff
		screen.blit(TI1.img, TI1.coords)
		pygame.draw.rect(screen, Cbacking, [10, 225 , 75, 24])
		screen.blit(baack, (10, 225))
		
				
		for i in invenItems: #equipping & alt display
			x = i.div.norm
			if hitDetect((115, x.baseCoords[1]+scrollMod), (370, 54), mouse_pos): #size of items
				pygame.draw.rect(i.div.side.img, LGREY, (0, 48, 50, 2))
				pygame.draw.rect(i.div.side.img, GREEN, (0, 48, (i.dfratio)*50, 2))#dura
				screen.blit(i.div.side.img, (487, 10)) #the side img
				if mouse_down:
					mouse_down = False
					equip(i)
					break
			
	
			#unequipping
		if hitDetect((10, 10), (50, 50), mouse_pos):
			pygame.draw.rect(pla.equipped[0].div.side.img, LGREY, (0, 48, 50, 2))
			pygame.draw.rect(pla.equipped[0].div.side.img, GREEN, (0, 48, (pla.equipped[0].dfratio)*50, 2))#dura
			screen.blit(pla.equipped[0].div.side.img, (487, 10)) #the side img
			if mouse_down:
				unequip(0)
		if hitDetect((60, 10), (50, 50), mouse_pos):
			pygame.draw.rect(pla.equipped[1].div.side.img, LGREY, (0, 48, 50, 2))
			pygame.draw.rect(pla.equipped[1].div.side.img, GREEN, (0, 48, (pla.equipped[1].dfratio)*50, 2))#dura
			screen.blit(pla.equipped[1].div.side.img, (487, 10)) #the side img
			if mouse_down:
				unequip(1)
		if hitDetect((10, 60), (50, 50), mouse_pos):
			pygame.draw.rect(pla.equipped[2].div.side.img, LGREY, (0, 48, 50, 2))
			pygame.draw.rect(pla.equipped[2].div.side.img, GREEN, (0, 48, (pla.equipped[2].dfratio)*50, 2))#dura
			screen.blit(pla.equipped[2].div.side.img, (487, 10)) #the side img
			if mouse_down:
				unequip(2)
		if hitDetect((60, 60), (50, 50), mouse_pos):
			pygame.draw.rect(pla.equipped[3].div.side.img, LGREY, (0, 48, 50, 2))
			pygame.draw.rect(pla.equipped[3].div.side.img, GREEN, (0, 48, (pla.equipped[3].dfratio)*50, 2))#dura
			screen.blit(pla.equipped[3].div.side.img, (487, 10)) #the side img
			if mouse_down:
				unequip(3)
				
		
		if mouse_down:
			if hitDetect((10, 225), (75, 24), mouse_pos):
				Screen = 1
	
	if Screen == 3: #battle
		screen.fill(Cbacking)
		screen.blit(Sbattle, (0, 0))
		if enm.mega:
			screen.blit(enm.img, (0, 0))
		else:
			screen.blit(enm.img, (856, 10))
			
		#stats
		pygame.draw.rect(screen, LGREY, (10, 10, 820, 9)) #backing
		if enm.defending:
			pygame.draw.rect(screen, GREY, (10, 10, 820, 9)) #backing
		pygame.draw.rect(screen, RED, (11, 11, enm.hpratio*818, 3))#enm hp

		pygame.draw.rect(screen, BLUE, (11, 15, enm.dfratio*818, 3))#enm armor durability
		
		pygame.draw.rect(screen, LGREY, (589, 240, 400, 9)) #backing
		if pla.defending:
			pygame.draw.rect(screen, GREY, (589, 240, 400, 9)) #backing

		pygame.draw.rect(screen, RED, (589, 241, pla.hpratio*400, 3))#you hp
		#you armor
		pygame.draw.rect(screen, BLUE, (589, 245, pla.dfratio*400, 3))#you armor durability
		
		#your items, make modular positions w/ dispobj
		screen.blit(pla.equipped[2].div.fight.img, pla.equipped[2].div.fight.coords)
		screen.blit(pla.equipped[3].div.fight.img, pla.equipped[3].div.fight.coords)
		screen.blit(Fdfn.img, Fdfn.coords)
		screen.blit(Fheal.img, Fheal.coords)
		
		if mouse_down:
			if hitDetect(pla.equipped[2].div.fight.coords, pla.equipped[2].div.fight.size, mouse_pos):
				if enm == adventurer:
					plaatk1 += 1
					plaTotal += 1
				attack(pla, pla.equipped[2], enm)
				pla.equipped[2].div.refresh(2)
			if hitDetect(pla.equipped[3].div.fight.coords, pla.equipped[3].div.fight.size, mouse_pos):
				if enm == adventurer:
					plaatk2 += 1
					plaTotal += 1
				attack(pla, pla.equipped[3], enm)
				pla.equipped[3].div.refresh(2)
			if hitDetect(Fdfn.coords, (52, 52), mouse_pos):
				pla.defending = True
				prints("DEFENDING")
				Refresh(pla)
				if enm == adventurer:
					pladfn += 1
					plaTotal += 1
			if hitDetect(Fheal.coords, (52, 52), mouse_pos):
				Heal(pla)
				prints("HEALED")
				if enm == adventurer:
					plaheal += 1
					plaTotal += 1
			mouse_down = False
		
	if Screen == 4: #Grave, limbo 1
		screen.fill(BLIMBO)
		screen.blit(TL1.img, TL1.coords)
		
	if Screen == 5: #Text & cliff, limbo 2
		screen.fill(BLIMBO)
		screen.blit(TL3.img, TL3.coords)
		if mouse_down:
			mouse_down = False
			genRoom()
			Screen = 1
	
	if Screen == 6: #Monoliths
		monolithTime -= 1
		screen.fill(BLIMBO)

		#pygame.draw.rect(screen, WHITE, [0, 0, monolithTime, 100])
		mult = (1.0 - (math.sqrt(3)/float(2))) / 2.0
		monoRatio = (monolithTime - 6) / float(1500) # -6 to prevent a drawing out of bounds problem with the arc
		sizeHalf = size[1] / float(2)
		pixFromCent = math.ceil((sizeHalf - (sizeHalf * monoRatio)))
		print pixFromCent, monoRatio, sizeHalf
		#print "fuck", (size[1] * (float(1) - (monolithTime / 1500)) / (mult)

		#SUpposedly the size should be the same, the second is height/2 - the added height from size on first
		#r1 = [0, (size[1] * (monolithTime - 6) / 3000), size[0], (pixFromCent / (mult * 2)) + 6]
		#r2 = [0,  2 * pixFromCent - (pixFromCent / (mult * 2)), size[0], (size[1] * (monolithTime - 6)/ 3000) + (pixFromCent / (mult * 2))]
		
		r1 = [0, sizeHalf * monoRatio, size[0], (pixFromCent / (mult * 2)) + 6]
		r2 = [0, sizeHalf + pixFromCent - (pixFromCent / (mult * 2)), size[0], (pixFromCent / (mult * 2)) + 6]

		print r1
		print r2

		#pygame.draw.rect(screen, GREY, (0, r1[1], size[0]/2, r1[3]))
		#pygame.draw.rect(screen, GREY, (size[0]/2, r2[1], size[0], r2[3		#print "um", (size[1] / 2), "urm", 600 * monolithTime / 3000
		pygame.draw.arc(screen, RED, r1, math.pi/4, 3*math.pi/4, 5)
		pygame.draw.arc(screen, RED, r2, 5*3.14/4, 7*3.14/4, 5)

		#pygame.draw.line(screen, WHITE, (0, size[1]/2), (size[0], size[1]/2))

		screen.blit(massive.render(str(monolithTime), False, RED), (200, 15)) #for now ;)
		screen.blit(TL2.img, TL2.coords)
		if mouse_down:
			mouse_down = False
			if hitDetect(TL2.coords, (50, 16), mouse_pos):
				dodged += 1
				localrand = runmessages[rand(len(runmessages)-1)]
				TL2.img = font.render(localrand, False, (250, 250, 250))
				TL2.coords = (10+rand(975-font.size(localrand)[0]), 10+rand(239-font.size(localrand)[1]))
				if (dodged == 5):
					dodging = False
					dodged = 0
					monolithTime = 1500
					turn = checkpoint
					roommessage = ""
					genRoom()
					Screen = 1
		if monolithTime <= 0:
			localrand = len(invenItems)
			for i in range(len(invenItems)):
				removeitem(invenItems[localrand-(i+1)])
			dodging = False
			dodged = 0
			monolithTime = 1500
			turn = checkpoint
			roommessage = ""
			genRoom()
			Screen = 1
		
	if Screen == 7: #Crafting
		screen.fill(Cbacking)
		screen.blit(Smain, (0, 0))
		
		#Crafter
		screen.blit(C.img, (390, 0))
		if C.inputs[0] != nothing: #dfn 1
			screen.blit(C.inputs[0].div.mini, (395, 100))
		if C.inputs[1] != nothing: #dfn 1
			screen.blit(C.inputs[1].div.mini, (395, 150))
		
		screen.blit(C.Iimg[C.Istage], (390, 149))
		screen.blit(C.Oimg[C.Ostage], (885, 122))
		
		if C.Ostage == 1: #open and ready to loot
			if C.output != nothing:
				screen.blit(C.output.div.mini, (910, 150))
				if mouse_down:
					if hitDetect((885, 122), (110, 137), mouse_pos):
						getitem(C.output)
						C.output = nothing
						mouse_down = False
						C.Ostage = 0
					
				
		if C.Ostage == 2 and not C.disabled: #cooking
			if mouse_down:
				if hitDetect((885, 122), (110, 137), mouse_pos): #generous opening area
					C.Ostage = 1
					mouse_down = False
					C.working = False
			
		screen.blit(C.Mimg[C.mode], (560, 121))
		#buttons and stuff
		screen.blit(ItemsDisp.img, (10, 10))
		pygame.draw.rect(screen, Cbacking, [910, 10 , 75, 24])
		screen.blit(baack, (910, 10))
		
		
		if mouse_down:
			if hitDetect((910, 10), (75, 24), mouse_pos): #Back
				Screen = 1
				mouse_down = False
				
			if C.Istage == 0: #Inserting items
				for i in invenItems: #item detect
					x = i.div.norm
					if hitDetect((10, x.baseCoords[1]+scrollMod), (370, 54), mouse_pos): #size of items
						success = False
						if C.inputs[0] == nothing:
							C.inputs[0] = i
							success = True
						elif C.inputs[1] == nothing:
							C.inputs[1] = i
							success = True
						if success:
							mouse_down = False
							invenItems.remove(i)
							refreshItems(1)
							break
				
			if hitDetect((395, 100), (50, 50), mouse_pos) and C.inputs[0] != nothing: #Removing items
				mouse_down = False
				invenItems.insert(0, C.inputs[0])
				C.inputs[0] = nothing
				refreshItems(1)
			if hitDetect((395, 150), (50, 50), mouse_pos) and C.inputs[1] != nothing:
				mouse_down = False
				invenItems.insert(0, C.inputs[1])
				C.inputs[1] = nothing
				refreshItems(1)
				
			if hitDetect((560, 120), (100, 111), mouse_pos) and not C.working: #Switch
				C.mode += 1
				if C.mode > 2:
					C.mode = 0
				mouse_down = False
				
			if hitDetect((330+390, 140), (140, 40), mouse_pos) and not (C.disabled or C.working): #CRAFT
				legit = False
				mouse_down = False
				ref = False
				if C.mode == 1 and C.inputs != [nothing, nothing]: #INFERRENCE
					if nothing == C.inputs[0] and C.inputs[1].ref != False:
						for x in C.inputs[1].ref:
							if x in room.isref:
								legit = True
					elif nothing == C.inputs[1] and C.inputs[0].ref != False:
						for x in C.inputs[0].ref:
							if x in room.isref:
								legit = True
					elif C.inputs[0].ref != False and C.inputs[1].ref != False:
						for i in C.inputs[0].ref:
							if i in C.inputs[1].ref:
								legit = True
								ref = i
									
						
				if (not (nothing in C.inputs)) and (not legit) and C.mode != 1:
					legit = True
						
				#see if craft is legit
				if legit:
					#generate a good result (dont enchant here, enchant on room load if invest)
					C.Istage = 1
					print "CRAFTING on mode:", C.mode
					if C.mode == 1: #Inferrence mode
						C.output = []
						for i in allitems:
							if ref in i.ref: #and i.score > 0:
								C.output.append(i)
								
						if C.inputs[0] == C.inputs[1]: #remove dupes
							C.inputs.remove(C.inputs[0])
						if nothing in C.inputs: #remove sweet nothings
							C.inputs.remove(nothing)
							
						if len(C.output) > len(C.inputs): #remove inputs from output to maximize varaity
							for i in C.inputs:
								if i in C.output:
									C.output.remove(i)
							C.output = random.choice(C.output)
							
						else: #special case when there arent enough
							C.output = Enchant(newItem(random.choice(C.inputs)))
						C.inputs = [nothing, nothing]
							
							
					if C.mode in [0, 2]:
						C.output = []
						if C.mode == 0: #hasty mode
							for i in lootitems:
								if i.lvl >= C.inputs[0].lvl and i.lvl >= C.inputs[1].lvl: #TO DO make better range
									C.output.append(i)
						if C.mode == 2: #investment mode
							for i in allitems:
								if C.inputs[0].lvl == -1 or C.inputs[1].lvl == -1:
									C.output.append(i)
								if (i.lvl >= math.floor((C.inputs[0].lvl+C.inputs[1].lvl)/1.5) and i.lvl < math.ceil((C.inputs[0].lvl+C.inputs[1].lvl)/1.5)+2): #TO DO make better range
									C.output.append(i)
						if C.inputs[0].lvl == -1 or C.inputs[1].lvl == -1:
							for i in allitems:
								if i.lvl == -1:
									C.output.append(i)
						if len(C.output) == 0:
							print "EMPTY RESULTS! scores & levels:"
							for i in C.inputs:
								print i.score, i.lvl
							print "'combined' lvl:", math.floor((C.inputs[0].lvl+C.inputs[1].lvl)/1.5)
							for i in allitems:
								if i.lvl == math.floor((C.inputs[0].lvl+C.inputs[1].lvl)/1.5):
									C.output.append(i)
						C.output = newItem(random.choice(C.output))
						C.inputs = [nothing, nothing]
						C.disabled = True
					
					if C.mode < 2:
						C.Ostage = 1
					if C.mode == 2:
						C.working = True
						C.Ostage = 2
				
				else:
					#do something to alert the player "failed"
					print "FAILED TO CRAFT: invalid recipie"
			else:
				#print "FAILED TO CRAFT: crafter not accepting"
				mouse_down = False
			
	if inbattle: #BATTLING
		enm.atkInt -= 1
		if (enm.atkInt == 0):
			enm.atkInt = enm.atkIntBase
			Do(enm)
			pla.refresh()
			
			if (enm.boss):
				hpratio = 100*(enm.hp/enm.hptop)
			else:
				hpratio = 100*(enm.hp/enm.maxhp)
			
			#Print enemy description based on health
			'''if (hpratio < 20):
				prints(enm.rundown[0])
			if (hpratio >= 20 && hpratio < 50){
				prints(enm.rundown[1]);
			}
			if (hpratio >= 50 && hpratio < 85){
				prints(enm.rundown[2]);
			}
			if (hpratio >= 85 && hpratio <= 100){
				printc(enm.rundown[3]);
			}
			if (enm.boss){
				if (hpratio > 100 && hpratio < 200){
					printc(enm.rundown[4]);
				}
				if (hpratio >= 200){
					printc(enm.rundown[5]);
				}
			}''' #VISUALS
			

		for i in pla.minionTree:
			i.atkInt -= 1
			if (i.atkInt <= 0):
				i.atkInt = i.atkIntBase
				Do(i)
		for i in enm.minionTree:
			i.atkInt -= 1
			if (i.atkInt <= 0):
				i.atkInt = i.atkIntBase
				Do(i)

		if (enm.name == "Adventurer" or enm.name == "Yourself"):
			plaTime += 1
		
		if (gravetime > 0):
			gravetime -= 1
			if (gravetime == 0):
				limbob(limbostuff[0], limbostuff[1])
	
	
	#little stuff all the time
	for i in invenItems:
		if i.mendTick != -1: #mending
			i.mendTick += 1
			if i.mendTick >= i.ench["mending"][0] and not i.broken:
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
	
	for x in range(len(pla.equipped)):
		i = pla.equipped[x]
		if i.mendTick != -1: #mending
			i.mendTick += 1
			if i.mendTick >= i.ench["mending"][0] and not i.broken:
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
					
		if i.regenTick != -1 and not i.broken and i.ammo < i.maxammo: #don't let them preload! that's weird!
			i.regenTick += 1
			if i.regenTick >= i.regenammo[0]:
				i.regenTick = 0
				i.ammo += i.regenammo[1]
				if i.ammo > i.maxammo:
					i.ammo = i.maxammo
		if Screen == 3:
			i.div.refresh(2)
			
	if (battleprep > 0):
		battleprep -= 1
	if (battleprep == 0):
		inbattle = True
		battleprep = -1
		if (enm.boss == False):
			enm.hp = enm.maxhp
		#customise fight screen to enemy
		#printc(enm, enm.cry); #VISUALS
		enm.reStats()
		pla.reStats()
		Screen = 3
	
	if gravetime > 0:
		gravetime -= 1
		if (gravetime == 0):
			limbob(limbostuff[0], limbostuff[1])
	
	if scrollMom != 0:
		if scrollMom < -70:
			scrollMom = -70
		if scrollMom > 70:
			scrollMom = 70

		if scrollMom < 0:
			if scrollMom < -45:
				scrollMom += 0.5
			else:
				scrollMom += 1
		if scrollMom > 0:
			if scrollMom > 45:
				scrollMom -= 0.5
			else:
				scrollMom -= 1
		scrollMod += scrollMom

		if scrollMod > 0: #make sure you didn't scroll too far
			scrollMod = 0
			scrollMom = 0
		refreshItems(2) #update display with new coords
		if scrollMod + netSize < 239: #make sure you didn't scroll too far
			scrollMod = 0-(netSize - 239)
			scrollMom = 0
		refreshItems(2) #make sure you didn't scroll too far

	pygame.display.update()
	clock.tick(50)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
