import io

doc = open("in.txt", 'r')
intext = doc.readline()
count = -1

watdo = raw_input("Type (1 for enm, 2 for boss, 3 for item):  ")

id = ""
outtext = ""

if watdo == "1" or watdo == "2":
	#hp, maxhp, atk, ddev, dfn, agil, heal, sane, name, img, message, cry, rundown, interval, actions = [], equip = [nothing], Boss = False, room = None, turn = -1):
	hp, maxhp, atk, ddev, dfn, agil, heal, sane, name, img, message, cry, rundown, interval, actions = "0", "0", "0", "0", "0", "[]", "0", "0", "", "", "", "", "[", "1", "actions"
	
	if watdo == "2":
		equip, boss, room, turn = "[", "True", "bossroom", "-1"
		#hp, atk, de, name, divname, maxhp, ddev, agil, heal, sane, loot, loot2, turn, message, cry, rundown, room, interval
		x = ""
		quote = False
		for i in intext:
			if i == '"':
				if quote:
					quote = False
				else:
					quote = True

			if (i == "," or i == ")") and not quote:
				print count, x
				if count == 0:
					hp = x
					x = ""
				if count == 1:
					atk = x
					x = ""
				if count == 2:
					dfn = x
					x = ""
				if count == 3:
					name = x
					x = ""
				if count == 4:
					img = x
					x = ""
				if count == 5:
					maxhp = x
					x = ""
				if count == 6:
					ddev = x
					x = ""
				if count == 7:
					x += ","
				if count == 8:
					agil = x
					x = ""
				if count == 10:	
					x = ""
				if count == 11:
					heal = x[:len(x)-1]
					x = ""
				if count == 12:
					sane = x
					x = ""
				if count in [13, 18, 19, 20, 21, 22]:
					x += ", "
				if count == 14:
					equip += x+"]"
					x = ""
				if count == 15:
					turn = x
					x = ""
				if count == 16:
					message = x
					x = ""
				if count == 17:
					cry = x
					x = ""
				if count == 23:
					rundown = x
					x = ""
				if count == 24:
					room = x
					x = ""
				if count == 25:
					interval = str(int(x)/2)
					x = ""
				count += 1
			else:
				if i == "=" and count == -1:
					id = x
				elif i == "(" and count == -1:
					count = 0
					x = ""
				else:
					if (i != " ") or quote:
						x += i
		outtext = id+" = Enm("+hp+", "+maxhp+", "+atk+", "+ddev+", "+dfn+", "+agil+", "+heal+", "+sane+", "+name+", "+img+", "+message+", "+cry+", "+rundown+", "+interval+", "+actions+", "+equip+", True, "+room+", "+turn+")"
		
		
	if watdo == "1":
		equip, boss, room, turn = "[", "True", "bossroom", "-1"
		#atk, de, name, pic, maxhp, ddev, agil, sane, message, cry, lvl, rundown, heal, interval)
		x = ""
		quote = False
		for i in intext:
			if i == '"':
				if quote:
					quote = False
				else:
					quote = True
			if (i == "," or i == ")") and not quote:
				print count, x
				if count == 0:
					atk = x
					x = ""
				if count == 1:
					dfn = x
					x = ""
				if count == 2:
					name = x
					x = ""
				if count == 3:
					pic = x
					x = ""
				if count == 4:
					maxhp = x
					hp = x
					x = ""
				if count == 5:
					ddev = x
					x = ""
				if count == 6:
					agil1 = int(x[1:])
					x += ""
				if count == 8:
					agil2 = int(x[:len(x)-1])
					x = ""
				if count == 9:
					sane = x
					x = ""
				if count == 10:
					message = x
					x = ""
				if count == 11:
					cry = x
					x = ""
				if count == 12:
					turn = x
					x = ""
				if count == 13:
					rundown = x
					x = ""


				if count == 15:	#skip first values of heal for now. NEED TO DO: turn into action value
					x = ""
				if count == 16:
					heal = x[:len(x)-1]
					x = ""

				if count in [13, 18, 19, 20, 21, 22]:
					x += ", "
				if count == 14:
					equip += x+"]"
					x = ""
				if count == 25:
					interval = str(int(x)/2)
					x = ""
				count += 1
			else:
				if i == "=" and count == -1:
					id = x
				elif i == "(" and count == -1:
					count = 0
					x = ""
				else:
					if (i != " ") or quote:
						x += i
		agil = "[", str(round(agil1/agil2*100)), ", 100]"
		outtext = id+" = Enm("+hp+", "+maxhp+", "+atk+", "+ddev+", "+dfn+", "+agil+", "+heal+", "+sane+", "+name+", "+img+", "+message+", "+cry+", "+rundown+", "+interval+", "+actions+", "+equip+")"
		
		
		
		
		
		
		
		
doc.close()
doc = open("out.txt", 'w')
doc.write(outtext)
doc.close()