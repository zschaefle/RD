import pygame
from pygame.locals import *


pygame.init()
pygame.font.init()
allfonts = pygame.font.get_fonts()
all = []
print "starting"
for i in allfonts:
	
	print "working on: "+i
	the = pygame.font.match_font(i)
	print the
	if the != None and (i not in ["cambria"]) and not (("bold" in i) or ("italics" in i)):
		font = pygame.font.SysFont(i, 15)
		all.append(font.render("Quick brown fox lol idk: "+i, False, (0, 0, 0)))
		del font
	else:
		print "Failed."

Screen = pygame.display.set_mode((500, 1000))

dood = 0
while True:
	Screen.fill((200, 200, 200))
	for i in range(len(all)):
		Screen.blit(all[i], (1, 16*i))
		print "doop"
	print "a"
	pygame.display.update()
	