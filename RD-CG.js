 /*
http://steampoweredairship.com/unexpected-error/rd/
___CHANGELOG___
--1.3-fattening update--
    +does not actually fatten you
    +added room 31
    +added 3 new items
    +changing sanity is more viable
        +items affect sanity each room (item.sane/5)
        +healing repairs sanity (+.2)
        -killing enemies reduces sanity (-1)
    *fixed minions being too common
    *fixed adventurer recreation (didnt have div stat)
    *nerfed the coosome


--------------The late game update-----------------
    + zarol gets buffed based on player lvl
    +buffed base agility
    +limbo less penalizing
    *buffed the coosome

------------1.1 ----------------
    + bug fixes
    + balanced epics
    + minions now obtainable
    + added potato and otatop
    + added rooms 29 - 30
    



--0.1.9+1--the Beefy update--
    -didn't add beef
    +started to name updates
    +added minion related functions: killMinion, getMinionTree
    +added rooms 25-28
    + mimics now drop items
    +adjusted monolith time to fit the new sanity spawns
    *prettied up minion displaying
    *fixed spelling
    Balances
        *nerfed the coosome, again
        *buffed axeurlegs

--0.1.9-- the bug fix update-
    -Monoliths now unequip items
        -Code used unequip function with square brackets instead of parenthesis
    -All items equipable
        -Items had differing divnames and variable names
    -fixed ablerooms
        -used sqrt still, converted to cbrt

--0.1.8-the Bug Filled update-
    -Bugs  ------DO NOT ADD MORE ANYTHING TO ANYTHING UNTIL ALL BUGS ARE FIXED
        -Monoliths don't unequip items
        -Double loot from bosses (Latency of one room?)
        -some items not equipable
        -only gives maximum insanity room from sanity ~-30 and beyond
        -the thing with the minion healing?
    +minions



--0.1.7--
    -Separated fighting aspects (attacking, healing) in preparation for Companions
    -Standardised all fighting classes to the following attribute names: (name hp maxhp atk def ddev agil sane)
    -much balancing
    -fixed fighting final sanities repetitively

--------0.1.6---

    +Sanity
    -modified item tables
    -items now sorted by lvl
    +monoliths
    +more item graphics
    -Items that need graphics:
        *white chestplate
        *all of the orbs
        *Chicken
        *redball
        *True sanity
        *true insanity
        *Enchanted armor
        *alpha axe
        *alpha glasses
        *pencil
        *fishing rod
        *hat and boots
        *broken seashell
        

-another colton update-2.0-sanity update--
+added limbo
+fixed some spelling probably
+manipulated things into references
+might be some other stuff idk
Bug- dying in room after boss causes fighting dead boss, get loot again

--------0.1.4---
    + added agil modifiers
    + added a few new items
    + added secret boss
    + buffed all the enemies
    + nerfed the coosome
    + some new enemies

--------0.1.3---
    - balanced bosses
    + added some new items

---the colton update--
+fixed stuff
+fixed things
+probably fixed some spelling
+changed up the inventory order
-bugs maybe? I dunno

--------0.1.1---
    - Fixed item damage not being added to base stats
    

--------0.1.0--- 
    - Fixed grammar problems with new rooms
    - Fixed enemies not spawning
    - Added changelog


*/
//creates random number between 1 and num.
function rand(num){
    return (Math.ceil(Math.random() * num));
}


var score = 0;
var health = "about a hundred";
var damage = "dunno, 15?";
var defence = "How am I supposed to know?";
var sanity = "Quite sane. But that's what they all say.";
var bossesbeat = 0;
var runnum = 1;
function player(){
    this.name = "player";
    this.hp = 100;
    this.baseatk = 8;
    this.atk = 8;
    this.basedef = 0;
    this.def = 0
    this.ddev = 10;
    this.healval = 1;
    this.maxhp = 100;  
    this.hdev = 3;
    this.baseagil = [5, 100];
    this.agil = [15, 100];
    this.lvl = 1;
    this.sane = 8;
    this.trueSane = 0;
    this.minions = [];
    this.id = 0;
    this.minionTree = [];
}
var pla = new player();
function Room(plant, manmade, water, dark, animal, light, items, north, east, south, west, sane, message, exitA, exitB, exitFail){
    this.plant = plant;
    this.manmade = manmade;
    this.water = water;
    this.dark = dark;
    this.animal = animal;
    this.light = light;
    this.items = items;
    this.north = north;
    this.east = east;
    this.south = south;
    this.west = west;
    this.message = message;
    this.exitA = exitA;
    this.exitB = exitB;
    this.exitFail = exitFail;
    this.sanity = sane;
    
}

//room = new Room();
room1 = new Room(0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, -4 ,"Your eyes burn as you look into the lit black. \nGreen lines stretch to a vanishing point, showing you a door, a wall and a cliff. \nYour eyesight blurs, reduced to craggy blocks.", "Your legs jitter as you walk on thin green lines, forming an exit to what you believe to be ", ".", "You feel like taking any extra steps in may be fatal.");
room2 = new Room(1, 0, 0, 1, 1, 1, 1, rand(2)-1, 1, 2, rand(2)-1, 1, "This room is overrun by nature. There are twisted, moist vines covering the walls and most likely any exits.", "You carefully make your way to the ", ", occasionally tripping.", "You trip on your way over to the wall, only finding no exit.");
room3 = new Room(0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, "You\'re in a linoleum cube, bare and featureless. \n A circular opening appears behind you, and an open pit is just ahead. \n A featureless voice speaks to you through static speakers. \n You can\'t understand a single word.", "As you walk toward the ", ", the circular door smoothly opens in the wall ahead of you.", "The voice seems to be insulting you as you stumble about, slightly confused.");
room4 = new Room(1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, "You find yourself in a lonely forest. \nThe snow on the ground mists in the sun, slowly turning into slush. \nYou take a moment to mourn the death of winter. Global warming man. \nThat\'s what it does.", "There's a small door in one of the trees to the ", ".\nYou pull it open and and fall through.", "");
room5 = new Room(0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, -2, "You stand on clouds, up to your ankles in condensation. \nYou see birds flying nearby. \nYou could swear that you see a large animal lurching its way towards you on lopsided legs.", " ", " ", " ");
room6 = new Room(0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, -1, "You are in a room, a large centerpiece of machinery whirring to life, bursts of energy coming from within. There are voices yelling urgently at you from a viewport in the wall above.", "You manage to dodge the now falling rubble and make it through the ", "ern sliding doors.", "A zap of lightning from the core of the room leaps through the viewport, and you hear a scream of pain.");
room7 = new Room(0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, "The walls cave inwards, rough rock with red striped sedimentary motif. The floor is loose packed sand, soft against your feet. \nYou look ahead, where the walls become lower and the ground gets rough. \nYou\'ll need to crawl.", "You crawl to the ", " exit, scraping your elbow.", "You realize that this is not an indiana jones movie, and that this wall will not open with enough force.");
room8 = new Room(0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 4, "You see a single shelf, packed full of books, reaching upwards like a ladder into the darkness. ", "You grip the ", "ern shelves, pulling yourself up past musty tomes.", "You become distracted by the books, taking a moment to flip through one.");
room9 = new Room(0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, -1, "There are huge wooden beams stretching across an empty cavern. \nCoals smoulder in campfires across the expanse, lighting the room with grey dusk. \nRotting homes half-formed out of clay fill the room with a musty stench.", "You walk past small encampments and crusty artifacts to a hole in the ", "ern wall.", "You glance into one of the rooms.\nYou spot a skeleton and an old vase. No exits here.");
room10 = new Room(0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, -1, "The sun shines in your eyes. \nYou feel water underneath you. \nShielding your eyes from the glare, you see the boat you\'re standing on, a small and splintery craft. \nThe way it bobs under your weight alarms you. \nA curl of rope under your feet obscures the bottom of the boat.", "you take hold of the paddles,\npaddling the boat to the ", ".", "Paddle as you may, the swirling currents quickly rush  you back into place.");
room11 = new Room(0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, "You are on a cold, stormy beach. Litter is strewn across the sand, and a man with a prosthetic arm is purposefully cleaning it up, glancing around as if expecting someone, or some<i>thing</i>.", "As you meander your way to the ", ", the man shouts at you angrily, something about litter.", "You wade about in the ocean, unsure as to whether you are looking for something, or mourning.");
room12 = new Room(0, 1, 0, 0, 1, 1, 1, rand(2)-1, rand(2)-1, 0, 1, rand(2), "You are in a room, full of red books with no titles, no markings at all. They fill the room, but you can hear a sort of carnal snore from somewhere in the room. You decide that would be best to keep away from whatever is producing the noise.", "You manage to sneak your way through to the ", ", cringing at the occasional shifting book.", "You wander throughout the room, surprisingly small for the quantity of books it holds.");
room13 = new Room(rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, 1, 1, 1, 1, -7, "You find yourself in a room filled with bright darkness. Things seem to appear and disappear as if they were both there, and not there. You feel very dull all of a sudden, as if you have realized the futility of life.", "You walk slowly to what you think is a door, tripping over invisible things along the way to the ", ".", "You feel it would be best to leave as soon as possible.");
room14 = new Room(1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, -3, "You find yourself in what at first appears to be a dog park, but upon closer inspection of the large black walls surrounding the area as well as the absence of any dogs and the presence of many hooded figures, you realize that this is not a dog park. Not a dog park at all.","After searching the "," side of the dog park, you don't find an exit, yet.....","The hooded figures are staring, and coming closer.....");
room15 = new Room(0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, -1, "You stand before the barrier,your quest finally over, you are filled with DETERMINATION. That is until you realize that this was not the end off your quest and you must continue. Go on.","You walk through the "," side of the barrier","You bump into the barrier, and you realize that it lives up to it's name");
room16 = new Room(0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, -3, "You find yourself in a room full of mirrors. Seeing yourself repeated thousands of times causes you to realize the monster you have become. How many creatures have you killed since you came here? You realize that you are a murderer.","You step into the "," mirror.","You bump into yourself.");
room17 = new Room(1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 5, "You are momentarily blinded, when the light fades you look around. You seem to be in a tranquil cavern. There is a pond in the center, where lights dance peacefully on it's surface. You sit to rest for a time.", "You get up, though you wish to stay, but a hole to the ", " beckons you. You wave goodbye to the lights, they dance a farewell.", "A cavern wall seems to be where you are thinking of going, so you stay where you are..");
room18 = new Room(1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 3, "You find yourself standing in a river, with a waterfall nearby. You take some time to rest in the lush greenery that surrounds you. You feel at peace.","You explore the forest to the ", ".","You walk straight into the waterfall.");
room19 = new Room(rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, rand(2)-1, 1, rand(2)-1, rand(2)-1, -10, "you Are forsed to ponDer your doings, finding that you aRe in fact <i>perfectly</i> sane. buT that is what they all say\;", "northnorthwesteastsouth", "westeastnorthsouth", "eastnorthwestsouthsoutheastsouthnorthupwest");
room20 = new Room(0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, -2,"You find yourself in the very confined space that is the interior of an elevator. There is a corpse on the floor here, foaming at the mouth. A camera in one of the corners is watching you. A sound like fingernails on a chalkboard echoes throughout the room", "You leave through the elevator door on the ", " side.", "You bump into the wall.");
room21 = new Room(0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, -6, "You step somewhere, you can't tell where, because there is literally nothing.", "You will yourself out, towards the... ", ", yeah, the east, that's right, you always wanted to go south.", "The nothingness seems to extend to that direction, and moving that way is fruitless.");
room22 = new Room(0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, -5, "You step somewhere, you can't tell where, because there is literally nothing except a overwhelmingly bright light.", "You will yourself out, towards the… ", ", yeah, the west, that's right, you always wanted to go south.", "The nothingness seems to extend to that direction, and moving that way is fruitless.");
room23 = new Room(1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 10, "You step into a wondrous room filled with peaceful plants and animals. Waterfalls and large lush trees fill the landscape. It seems as if you have found a utopia.", "You must use all of your willpower to leave this peaceful utopia to the ","." );
room24 = new Room(0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, -8, "As soon as you enter this room, you know you should not have. Various instruments of torture are strewn about the room. The room is filled with the wailing of the not yet dead corpses and the torture machines at work. The smell is indescribable.", "You quickly leave to the ",".", "You find yourself lost among the horrors of this room." );
room25 = new Room(0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, -7, "It is dark. Creepily dark. You can hear a faint whispering.", "You somehow find the light in the ", ".", "The whispering is getting louder.")
room26 = new Room(0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 5, "You are in your bedroom. It is clean and tidy in here. there is a doorway that leads to the main room.", "You walk to the ", ", out of your bedroom and into the main room.", "You decide against the act of heading that direction, maybe later.");
room27 = new Room(0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, -2, "You are in your bedroom. It is messy and looks slightly looted. there is a doorway that leads to the main room.", "You walk to the ", ", out of your bedroom and into the main room.", "You decide against the act of heading north, maybe later.");
room28 = new Room(1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 2, "You are in a peaceful courtyard with a bird fountain in the center, surrounded by walls and a tower made of quartz and marble.", "You walk to the ", ", through an intricately carved doorway.", "There is a wall here, you decide it would be too much trouble to climb it.");
room29 = new Room(0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, "Your feet burn as you stand in the hot sand. You survey the endless expanse of desert around you, and realize that the in the years you have spent trekking through this wasteland have been useless.", "You continue your fruitless trek to the ", ".", "")
room30 = new Room(0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, "You stand on top of a factory, the clanging of machinery behind you. Smoke pollutes the sky and obscures the sun. The occasional sizzle of laser cutters quietly supports the clanging.", "You walk through the factory, carefully avoiding the dangerous machines. You exit to the ", ".", "You breath in some of the smoke. It burns in the back of your throat, making it hard to breath.")
room31 = new Room(0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, -2, "You are in a large warehouse, through the grimy windows you can see it is dusk. The occasional object is stored here, but everything is covered in spiderwebs.", "You open a large door in the ", "ern wall, someone helping from the other side.", "As you move, the strands of web begin catching.");
//room = new Room(plant, manmade, water, dark, animal, light, items, north, east, south, west, sane, message, exitA, exitB, exitFail);

bossroom = new Room(0,0,0,0,0,0,0,1,1,1,1, -2, "You find yourself in a wide open room. The ceiling is high and dark. An ominous feeling of doom hangs over you.", "Exhausted, you leave through the ", " door.", "You somehow walk into a nonexistent wall.")
roomBoss2 = new Room(0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, -2, "You are in a small stone cavern, many twisting passageways leading through a winding cave system. You feel a drop of water plop on your head.", "You climb out through a ", "ern cave.", "You climb through a tunnel, only to find yourself in a room similar to the one you came from.");

var rooms = [room1, room2, room3, room4, room5, room6, room7, room8, room9, room10, room11, room12, room13, room14, room15, room16, room17, room18, room19, room20, room21, room22, room23, room24, room25, room26, room27, room28, room29, room30, room31];

//heal: [end, switch, heal]
function Enemy(atk, de, name, pic, maxhp, ddev, agil, sane, message, cry, lvl, rundown, heal, interval){
    
        this.hp = 0;
        this.atk = parseInt(atk);
        this.def = parseInt(de);
        this.name = name.toString();
        this.div = pic.toString();
        this.ddev = parseInt(ddev);
        this.maxhp = parseInt(maxhp);
        this.agil = agil;
        this.message = message.toString();
        this.cry = cry.toString();
        this.lvl = lvl;
        this.heal = heal[2];
        this.rundown = rundown;
        this.healchance = [heal[0], heal[1]];
        this.boss = false;
        this.atkInt = interval;
        this.atkIntBase = interval;
        this.sane = sane;
        this.minions = [];
        this.minionTree = [];
}
var nullenm = new Enemy(0, 0, "", "", 0, 0, [1,100], "", "", 0, ["", "", "", "", ""], [2, 3, 4], 1000);
var creepybaldguy = new Enemy(5, 10, "Creepy Bald Guy", "creep", 15, 2, [1,100], -1, "You know you are being watched.\nAlways...\n", "you feel it staring through your eyes,\nInto your Soul.", 1, ["Even though it seems nearly dead, it continues its steady gaze deep into your eyes.", "it seems to have lost some hair in this fight. You blink, realizing it was already bald.", "it seems to be observing, only attacking to see how you react.", "it is sitting there, observing you. Waiting and observing your every move."], [2,3,4], 200)
var terracotta = new Enemy(0, 12, "clay soldier", "terracotta", 5, 5, [1,8], 0, "Intricately carved hinges begin to move,", "Beginning its advance towards you.", 1, ["It lays on the ground, cracks running through it.", "It wobbles, an arm and a leg missing.", "There are small cracks beginning to run through its body.", "it stands there, it's carefully carved tiny eyes staring at you."],[1,2,0], 100)
var thug = new Enemy(7, 0, "Thug", "thug", 100, 5, [1,1000], 0, "A thug approaches you on the street.\nYou prepare your fists, being much stronger than your lean appearance implies.", "'Hey, Idiot. Whose territory do you think you're Waltzing around in?'", 0, ["", "", "", "He holds his hands up in front of his face, posture like that of a fake wrestler."], [3,2,4], 300)
var bookofdeath = new Enemy(10, 20, "Flailing Broken Binding", "bookofdeath", 3, 1, [5,100], -1, "A nearby book seems to stir..", "A book snaps into a row of paper teeth.....", 2, ["", "", "",""], [10,7,4], 75)
var catwatcher = new Enemy(15, 5, "Watcher Catling", "catwatcher", 65, 2, [20,100], -1, "You feel as though something is watching you.....", "A small Furry leaps at you!", 3, ["","","",""], [20, 11, 20], 100)
var axeurlegs = new Enemy(2, 10, "Axeurlegs", "axeurlegs", 10, 1, [0,1], -2, "One of the plants seems to be twitching.....", "Steel blades click into place as the plant spins into action!", 1, ["", "","", ""],[1,3,1],8)
var anenemy = new Enemy(5, 7, "Anenemy", "anenemy", 38, 10, [10,100], 0, "A sloshing sound alerts you to anenemy in the water......", "Anenemy attacks you!", 1, ["","", "", ""], [10, 8, 8], 75)
var lightorb = new Enemy(12, 20, "Light Orb", "lightorb", 5, 3, [4,5], 0, "A glowing orb floats gently towards you", "", 2, ["It's light is so dim, you can almost make out the creature emitting it.", "it is no longer floating quite as high as before, and it's light is fading.", "It's light is getting duller, and it sways from side to side.", "It darts around in front of you, a streak of light across your vision."], [1,2,3], 100)
var mimic = new Enemy(5, 15, "Mimic", "mimic", 20, 5, [1,100], -1, "A golden chest sits with elegant details and pure beauty.", "The chest snaps open, revealing not loot, \nBut a row of Teeth!", 2, ["","", "", ""], [1,2,3], 75)
var nerveball = new Enemy(20, 8, "the ball of nerves", "nerveball", 20, 8, [10,100], -3, "You see a swirling ball of...\nnerves?", "it turns towards you,\nscreaming with silence\n \n...and electrical currents.", 3, ["", "", "", ""], [1,2,3], 50)
var clone = new Enemy(15, 10, "Your clone", "clone", 100, 5, [1,20], -5, "You see a more menacing version of yourself in what you think is a mirror....", "", 2, ["", "", "", ""], [10, 9, 10], 75)
var koi = new Enemy(20, -2, "Koi", "koi", 250, 3, [1,100], 0,"There is a very strange looking fish swimming in the water....","It leaps at you, with it's blunt teeth!",3,["", "", "", ""],[10,9,50], 75)
var slime = new Enemy(3, 15, "Slime", "slime", 150, 2, [1,100], -3, "The ceiling seems to be dripping some strange substance...","You are consumed by a large blob of jelly!",3,["", "", "", ""],[40,39,2], 26)
var dog = new Enemy(10,10,"Dog", "dog", 175, 20, [1,25], 0, "The sounds of a happy dog are getting louder....", "ARF ARF!",3,["","","",""],[99,100,0], 75)

//Items. All of the items.
function item(offence, defence, agility, sanity, score, name, divname, desc){
        this.atk = offence;
        this.def = defence;
        this.agil = agility;
        this.score = score;
        this.sane = sanity;
        this.Name = name;
        this.div = divname;
        this.desc = desc;
        this.quant = 0;
        this.bossitem = 0;
        
}
//If an item has a score of over 5, it is considered a reference, and Coosome shall act swiftly to Counter-reference toward the same topic.

// lvl 1 items ----
var nothing = new item(0, 0, 0, 0, 0, "", "no_thing", "");
var acorncap = new item(0, 1, 1, 2, 3, "Acorn Cap", "acorncap", "If you were really tiny, like, smaller than a squirrel, this would be the perfect armor.\nYou place it over your heart \nYou call it a kiss");
var boardgame = new item(0, 2, -1, 2, 2, "Board Game", "boardgame", "The cardboard is battered \nfrom years of wear, but you can see the winding \npath your piece would take if you were a winner. \n\nYou're not a winner.");
var bobbypin = new item(1, 0, 1, 1, 1, "Bobby Pin", "bobbypin", "Ow..., it's sharp.");
var woodstick = new item(1, 0, 1, 3, 2, "Wooden Stick", "woodstick", "It might not be the best sword, but hey, it's worth a try.");
var brokenglasses = new item(0, 1, 3, -1, 2, "Broken Glasses", "brokenglasses", "The few shards of perfectly clear glass in these frames could have only been made by magic.");
var fakesword = new item(1, 1, 0, 2, 1, "Fake Sword", "fakesword", "This is actually just an inflatable party favor");
var hoodie = new item(0, 1, -1, 2, 1, "Hoodie", "hoodie", "It has a flannel pattern on the inside");
var journal = new item(0, 1, 0, 4, 5, "Journal", "journal", "It's dusty and old");
var keyboard = new item(0, 1, 0, 1, 4, "Keyboard", "keyboard", "Learn to type right and you won't ruin your wrists. Also use Dvorak.");
var lamp = new item(1, 0, 0, 2, 3, "Lamp", "lamp","Rub it hard enough and it'll be cleaner");
var no_thing = new item(0,0,0,-2,-1, "Nothing", "no_thing","You stare off into the distance....\nYou realize that you can't just get loot from nowhere.");
var reflectivevest = new item(0, 1, 1, 1, 1, "Reflective Vest", "reflectivevest","At least you won't get hit by a car");
var sharktooth = new item(2, 0, 2, 1, 2, "Shark Tooth", "sharktooth","Maybe you can give it to the tooth fairy and get some money.");
var steeltoedboots = new item(1, 5, -2, 1, 1, "Steel Boots", "steeltoedboots", "Your enemy might be able to kill you, but hey at least your toes will be fine.");
var styrofoamchestplate = new item(0, 1, -1, 2, 2, "White Chestplate", "styrofoamchestplate","It's hefty with beautiful detailing that shines in even the blackest cavern. \nYou wish it was made out of something other than styrofoam.");
var wandofwater = new item(2, 0, 1, -1, 3, "Wand of Water", "wandofwater","You'll never be thirsty again");
var wings = new item(1, 1, -1, -1, 1, "Wings","wings","Now you can fly! \n(No you can't)");
var organs = new item(1, 1, 3, -5, 5, "Organs", "organs", "A wet gooey mass that drips on your hand. \nYou can hear an almost musical wheeze.");
var rotflesh = new item(3,2, 0, -7, 4,"Rotting Flesh","rotflesh","It's a rotting leg, snatched off a carcass that was probably dead. \n Probably.");
var crate = new item(-1, 3, -3, 2, 3, "Crate", "crate","It cowers, trying to get away from you. \nYou can hear it whimper. \nIt knows what's coming.");
var redbook = new item(1, 2, 0, 2, 6, "Red Book", "redbook", "There are no markings, but you feel as though there are many others much like it.");
var onepin = new item(4, 0, 1, 1, 2, "One Pin", "onepin", "The tip is dull from overuse.");
var nerfgun = new item(2, 0, 1, 1, 3, "Nerf Gun", "nerfgun", "Sometimes Styrofoam bullets can hurt.");
var brokenseashell = new item(-1, 2, 4, 5, 7, "Broken seashell", "brokenseashell", "It appears recently broken, but you keep it for sentimental value. Towards what, even you cannot quite tell.");
var redball = new item(-1, 2, 1,10, 6, "Red Ball", "redball", "It is comforting, yet oddly unnerving. You keep it as an anchor to remind you of the 'real world.'");
var crowbar = new item(3, 3, -2, 1, 3, "Crowbar", "crowbar", "A red crowbar.\nYou feel as though the fact that it\nhas three points is significant.");
var fakebeard = new item(0,1,3,4,4,"Beard", "fakebeard", "It's a beard. You suddenly feel like you have been here for longer than you think you have.");
var gear = new item(3, 2, 2, 2, 1, "Gear", "gear", "A small gear. It looks like it fell out of some machine.");
var catears = new item(2, 2, 2, 2, 2, "Cat Ears", "catears", "nekomimi");
var bikeweel = new item(2, 1, -3, 2, 3, "Bike Wheel", "bikeweel", "It's part of your bike. Did you have a bike?");
var recording = new item(7, -2, 1, -2, 6, "Recording", "recording", "Nyan cat recording");
var potato = new item(2, 2, 1, 8, 6, "Potato", "potato", "Quite a normal potato.");
var otatop = new item(0, 7, -2, -2, 6, "Otatop", "otatop", "Quite a inverted potato.");

var squiglasses = new item(2, 1, 2, 4, 7, "Glasses", "squiglasses", "They are non-prescription, acting more as a mask, allowing you to be someone else.");
var buttton = new item(0, 1, -3, 3, 9, "Button", "buttton", "Even though it is just a normal button, you feel as though it marks you for a death from an unknown source.");
var map = new item(0, 1, 3, 1, 8, "Map", "map", "A roughly drawn map, you dont recognize any of the landmarks. You deem it useless.");
//lvl 2 items ----
var heavenchip = new item(4, 4, 4, 4, 4, "Heaven Chip", "heavenchip", "Tastes like heaven");
var planc = new item(8, 1, 4, -8, 7, "Plan C", "planc", "It's your backup plan.");
var shinedisk = new item(6,6, 4, 8, 4, "Shine Disk", "shinedisk", "It's a disk of pure light. You can see your reflection in it.");
var circularsaw = new item(15, 0, 0, -15, 9, "Circular saw", "circularsaw", "You feel as though only a psychopath would use this as a weapon. The stains of blood imply that it already has.");
var septagram = new item(10,-3,2,-10,7,"Septagram","septagram","A seven pointed star painted in blood on a tablet. You have the urge to use it for some evil cause. Like murder.");
var sissors = new item(7, 2, 9, -9, 7,"Sissors", "sissors", "It's a pair of those kiddy scissors. At least that what you thought it was before you saw the blood.");
var lifethread = new item(2, 7, 9, -3, 6, "Life Thread", "lifethread", "This ball of thread seems to be pulsing with blood.") ;
var ashjar = new item(1, 10, -2, -3, 5, "Jar of Ash", "ashjar", "A small jar of ash. It smells of burnt corpses.");
var cookie = new item(3, 1, 4, 2, 7, "Cookie", "cookie", "click        yum");
var tornclaw = new item(8, 4, 7, -12, 5, "Torn Claw", "tornclaw", "A claw that must have been brutaly ripped off the creature while it was still alive. ");
var antmound = new item(5,3, -2, -4, 6, "Ant Mound", "antmound", "It's strangely slush like.");
var planck = new item(0, 2, 11, 2, 5, "Plan ck", "planck", "like plan c, but more, and smaller. Like 1.616199x10<sup>-35</sup> meters small.");
//lvl 3 items ----
var ichor = new item(7, 7, -4, -8, 5, "Ichor", "ichor", "Blood of the gods. How did you even get this?");
var err = new item(0, 0, 0, 0, 0, "Error", "err", "It was quite unexpected.");
var bloodpill= new item(7,5,4,-5,8,"Blood Pill","bloodpill","A small capsule that contains a small amount of blood. Using it has strange effects on the environment. Blood is everywhere.");
var darkcrystal = new item(13, 2, -2, -13, 4, "Darkened Crystal", "darkcrystal", "Contained in a forcefield, this crystal fires lasers at anything nearby.");
//lvl 4+ items ----




var lapis = new item(1000, 1000, 1000, 0, 1000, "coo33's Lapis", "lapis", "The Jem of the Gods.\n\nOr at least the god of 7.");
var hatandboots = new item(5, 50, 8, 0, 10, "Hat and Boots", "hatandboots", "Can't Bump your head anymore, and probably won't stub your toes.");
var zaroltrophy = new item(0, 0, 0, 20, 50, "Zarol Trophy", "zaroltrophy", "Thinking back, Seriously.\nHow the hell did you do that?");
var heroshield = new item(0, 8, -2, 0, 10, "Heroes Shield", "heroshield", "You feel a bit bad,\nkilling someone with origins probably alike yours.");
var herosword = new item(6, 0, 2, 0, 10, "Heroes Sword", "herosword", "A fitting weapon for a hero. But are <i>you</i> a hero?");
var fishingrod = new item(5, 4, 2, 0, 10, "Fishing Rod", "fishingrod", "Hook, Line, and Sink.");
var pencil = new item(7, 2, -1, -5, 10, "The Pencil", "pencil", "Quite oversized, you use it as a blunt weapon. But you feel there is more to it.");
var spoon = new item(50, 1, 7, -8, 10, "the Spoon", "spoon", "It's just a spoon. But something feels powerful about it...");
var alphaxe = new item(20, -2, -2, 0, 10, "Alpha's Axe", "alphaxe", "A large heavy axe, with surprisingly powerful hits.");
var sivgoggles = new item(4, 6, 35, -15, 10, "Alpha's Glasses", "sivgoggles", "Gazing through them, You can see things. Where they are, and where they are going.");
var hair = new item(0, 1, 2, -100, 10, "Alpha's Hair", "hair", "You stole this from a boss. Well, stole isn't the right word. More of Generated through Desire.");
var shurikenbag = new item(35, 2, 45, -35, 20, "Shuriken Pouch", "shurikenbag", "A small, blood filled pouch, when you reach your hand into it, you always pull out a shuriken.");
var jimsword = new item(25, 5, -5, 0, 10, "Jim's Sword", "jimsword", "");
var jimarmor = new item(0, 35, -20, 0, 10, "Enchanted Armor", "jimarmor", "Glimmering metallic armor, Material flowing smoothly within it to fill the gaps in its structure.");
var inactivecube = new item(25, 7, 20, 0, 10, "Inactive Cube", "inactivecube", "");
var card = new item(2, 25, 25, 0, 20, "00000111", "card", "");
var device = new item(40, 0, 6, 0, 20, "Electrical device", "device", "You have no idea how it works, but it looks far beyond any tech you have seen.");
var godrobe = new item(5,15, 5,-1,10,"God Robe","godrobe","It's name means god robe. \n Fitting, you think.");
var xissors = new item(22, 4, 15, -1, 10, "Xissors", "xissors", "It's actually only half of a scissor. \n Good for cutting clothing");
var otherxissors = new item(22, 4, 15, -1, 10, "Other Xissors", "otherxissors", "It's actually only half of a scissor. \n Good for cutting clothing");
var compxissors = new item(45, 10, 24, -6, 20, "Complete Xissors", "compxissors", "It's finaly complete.");
var trueinsanity = new item(35, -3, -10, -3, 5, "True Insanity", "trueinsanity", "You feel at peace. You have achived true insanity.");
var truesanity = new item(15, 15, 30, 7, 5, "True Sanity", "truesanity", "You feel at peace. You have achieved true sanity.");



var bossitems = [truesanity,trueinsanity,heroshield, herosword, fishingrod, pencil, spoon, alphaxe, sivgoggles, shurikenbag, jimsword, jimarmor, inactivecube, card, device, lapis, hatandboots, godrobe, xissors, otherxissors, compxissors];
var allitems = [lapis, trueinsanity, truesanity, inactivecube, spoon, shurikenbag, hatandboots, device, card, jimsword, jimarmor, alphaxe, sivgoggles, pencil, fishingrod, heroshield, herosword, xissors, otherxissors, compxissors, godrobe, onepin, woodstick, acorncap, boardgame, brokenglasses, bobbypin, crowbar, recording, crate, fakesword, hoodie, journal, keyboard, lamp, nerfgun, organs, reflectivevest, sharktooth, steeltoedboots, styrofoamchestplate, wandofwater, wings, circularsaw, redbook, brokenseashell, redball, rotflesh, no_thing, sissors ,bloodpill, fakebeard, planc, ashjar, lifethread, septagram, shinedisk, tornclaw, bikeweel, cookie, heavenchip, catears, antmound, err, ichor, darkcrystal, potato, otatop, squiglasses, map, buttton];
var lootitems = [];
var equippeditems = [nothing, nothing];

function Boss(hp, atk, de, name, divname, maxhp, ddev, agil, heal, sane, loot, loot2, turn, message, cry, rundown, room, interval){
    
        this.hp = hp;
        this.rehp = hp;
        this.atk = parseInt(atk);
        this.def = parseInt(de);
        this.name = name.toString();
        this.div = divname;
        this.ddev = parseInt(ddev);
        this.maxhp = parseInt(maxhp);
        this.agil = agil;
        this.message = message.toString();
        this.cry = cry.toString();
        this.lvl = turn;
        this.heal = heal[2];
        this.rundown = rundown;
        this.healchance = [heal[0], heal[1]];
        this.boss = true;
        this.atkInt = Math.ceil(interval);
        this.atkIntBase = Math.ceil(interval);
        this.turn = turn;
        this.loot = loot;
        this.loot2 = loot2;
        this.boss = 1;
        this.sane = sane;
        this.minions = [];
        this.room = room;
        this.minionTree = [];
}

function buildZarol(){
    var zarol = new Boss(550 + score * 2, 0 + score / 4, 22, "Zarol", "zarol", 10000 + score * 2, 135, [1,15], [70,69,10000], -10, zaroltrophy, zaroltrophy, 50, "You stand in the final room, reveling in your victory. \nFrom just over your left shoulder, you hear heavy breathing.", "Your head slowly swivels, back poker straight,\n to look into three wide red eyes.",["Everything you can see is unrecognizable, even the boss that has now dispersed to the point of surrounding you.","It is infuriated by your damage, darkness billowing from its wounds, disintegrating all it touches.","You seem to have gotten its attention, but it's cold glare assures you this is not a good.","It seems almost to be ignoring you, focusing solely on destruction.", "You feel an aura of confidence, coming from it as it methodically destroys all that surrounds it.", "You feel a burst of energy from it, enveloping you with searing pain."], bossroom, 150);
    return zarol
}
zarol = buildZarol()
var adventurer = new Boss(190, 20, 0, "Adventurer", "adventurer", 190, 5, [5,100], [100,50,30], -7, herosword, heroshield, 10, "You hear the footsteps of someone else.", "It is an Adventurer, \nReadying his stance for Battle!", ["He seems oddly unaware of the massive amounts of damage you have dealt him.\nMuch like you are.", "", "", "", "He seems more confident of himself,\nmore sure of his strides.",""],bossroom,100);
var coosome = new Boss(125, 10, 10, "coo33", "coosome", 177, 75, [19, 64], [64,64-13,10], -2, fishingrod, pencil, 15, "You hear something behind you.", "\'Here,\n Fishy..\n  Fishy...\'", ["It's bloodied eyes dart across you, searching for ways to finish you off quickly.", "It looks angry, but seems to have survived worse.", "It is smiling, although panting. It seems as though it's malnourishedness is taking effect.", "He seems unfazed,\na low growl and a chuckle murmured from within.","It takes a deep breath, the type one might take after a good nights sleep.","It seems to be toying with you, darting through the room."],roomBoss2,68);
var jimgrind = new Boss(200, 35, 35, "Jim Grind", "jimgrind", 200, 2, [1, 44], [12, 11, 12], -2, jimsword, jimarmor, 25, "Someone is in the room with you. You turn just fast enough to see him. He knows he has been spotted.", "A stern look on his face; A deadly look in his eyes.", ["", "You can see small gaps in his defence now, chinks in his armor.", "His breathing is heavy, and his swings are slower, yet just as powerful.", "He stands with a confident air about him, holding his sword firmly.", "His armor is beginning to glow, even the largest chinks in his armor closing as the armor reshapes into its original form.", "He seems unaware of your blows, simply tanking all damage you may deal to him."],bossroom, 260);
var strangecube = new Boss(250, 1, -5,"Strange Cube", "", 350, 2, [10,100], [100,99,75], -3, inactivecube, device, 30,"A strange cube is sitting on the ground in front or you.","Sudden arcs of electricity jump across its surface as it rises into the air.", ["Although grounded, it still musters up powerful shocks upon you.", "It appears to have physical damage, and is barely able to keep itself aloft.", "It is wavering now, seeming to have less energy within it, focusing on attacks.", "It floats evenly in front of you, electricity visibly through internal circuits.", "electricity is visible streaking across its surface, arcing to nearby surfaces.", "It's magnetic fields are powerful, you can feel them pulling on your magnetic accessories."],bossroom,75)
var alpha = new Boss(350, 34, 0, "Alpha", "alpha", 500, 6, [2,3], [5,4,10], -3, alphaxe, sivgoggles, 20, "You hear sudden quick footsteps from behind you.", "you turn to see someone dashing at you, Swinging a large axe!", ["", "", "", "", "", ""],bossroom, 120);

var xissor = new Boss(200, 9, 20, "Xissor", "xissor", 200, 20, [1,10], [100,99,25], -2, xissors, godrobe, -100, "Somebody smashes through the ceiling....", "She turns around quickly, then charges at you while screaming!",["","","","","",""], bossroom, 75)
var otherXissor = new Boss(400, 25, 35, "The Other Xissor", "otherxissor", 400, 40, [1,5], [100,90,25], -10, otherxissors, godrobe, -100, "Sombody else is here.", "She turns around slowly, then quickly draws her blade on you.",["","","","","",""], bossroom, 75)
var epicalpha = new Boss(450, 50, 10, "Alpha 949", "epicalpha", 450, 12, [5, 6], [10, 8, 20], -6, sivgoggles, shurikenbag, -100, "You find yourself in a familiar looking room. Looking around, you realize you have some unfinished business. You hear sudden quick footsteps from behind you.", "you turn to see a familiar figure dashing towards you, Swinging a large axe!", ["", "", "", "", "", ""],bossroom, 120);
var epicjim = new Boss(500, 70, 55, "Jim Grind", "epicjim", 1000, 4, [2, 88], [24, 22, 24], -4, jimarmor, hatandboots, -100, "You find yourself in a familiar looking room. Looking around, you realize you have some unfinished business. Someone is in the room with you. You turn to face him. You both know who won last time. ", "A stern look on his face; A deadly look in his eyes.", ["", "You can see small gaps in his defence now, chinks in his armor.", "His breathing is heavy, and his swings are slower, yet just as powerful.", "He stands with a confident air about him, holding his sword firmly.", "His armor is beginning to glow, even the largest chinks in his armor closing as the armor reshapes into its original form.", "He seems unaware of your blows, simply tanking all damage you may deal to him."],bossroom, 260);
var epiccoo = new Boss(300, 20, 28, "coo33", "epiccoo", 400, 150, [19, 64], [64,64-13,20], -4, pencil, spoon, -100, "You find yourself in a familiar looking room. Looking around, you realize you have some unfinished business. You hear a familiar chilling voice behind you.", "\'Here,\n Fishy..\n  Fishy...\'", ["It's bloodied eyes dart across you, searching for ways to finish you off quickly.", "It looks angry, but seems to have survived worse.", "It is smiling, although panting. It seems as though it's malnourishedness is taking effect.", "He seems unfazed,\na low growl and a chuckle murmured from within.","It takes a deep breath, the type one might take after a good nights sleep.","It seems to be toying with you, darting through the room."],roomBoss2,68)
var lastsanity = new Boss(500, 18, 16, "Last Remnants of Sanity", "lastsanity", 500, 5, [2,7], [100, 95, 100], -100, trueinsanity, trueinsanity, -100, "You feel parts of your mind fighting back, with nonsense of '<i>Something is wrong</i>.'", "You realize you need to silence these nagging voices.",["<i>You are destroying yourself...</i>","<i>Do you even know the names of the people you killed?</i>","<i></i>","<i>Something is seriously wrong with you,</i>"],bossroom, 60);
var lastinsanity = new Boss(1000, 15, 10, "Last Remnants of Insanity", "lastinsanity", 1000, 90, [1,64], [1, 2, 3], 100, truesanity, truesanity, -100, "You feel parts of your mind begin to come together.......", "You have come to a realization: the only way to obtain your goal is to wipe insanity from your mind.",["but.. What is this place?","How do you not return to what was already there?","",""],bossroom, 25);

var bosses = [adventurer, coosome, zarol, alpha, strangecube, jimgrind, xissor, otherXissor, epicalpha, epicjim, epiccoo, lastsanity, lastinsanity];

function Minion(hp, maxhp, atk, ddev, de, agil, heal, sane, lvl, name, pic, message, desc, interval, distract){
        this.hp = hp;
        this.maxhp = maxhp;
        this.atk = parseInt(atk);
        this.ddev = parseInt(ddev);
        this.def = parseInt(de);
        this.agil = agil;
        this.heal = heal[2];
        this.healchance = [heal[0], heal[1]];
        this.sane = sane;
        this.lvl = lvl;
        this.name = name;
        this.div = pic
        this.message = message;
        this.desc = desc;
        this.atkInt = interval;
        this.atkIntBase = interval;
        this.dist = distract;
        this.boss = false;
        this.minions = [];
        this.id = 0;
        this.minionTree = [];
}
//takes enemy or boss, new name and divname, and distract chance, returns minion
function toMinion(minion, newname, distract){
    return new Minion(minion.hp, minion.maxhp, minion.atk, minion.ddev, minion.def, minion.agil, [minion.healchance[0], minion.healchance[1], minion.heal], minion.sane, minion.turn, newname, minion.div, minion.message, minion.cry, minion.atkIntBase, distract);
}

var coompanion = toMinion(coosome, "Coompanion", 100);
var fairy = new Minion(10, 10, 1, 0, 1, [9,10], [30, 29, 1], -2, 4, "A fairy", "fairy", " You feel a presence nearby.", "When did this get here? All it seems to do is say watch out, and tell you to listen.", 170, 1);
var nyancat = new Minion(30, 35, 7, 2, 1, [7, 8], [20, 1, 1], -15, 6, "Nyan Cat", "nyancat", "You see a.. Cat? It jumps up, flying toward you, Rainbows trailing it.", "Nyaning", 16, 45);
var strikorb = new Minion(35, 45, 17, 3, -5, [1,4], [15, 14, 7], -3, 5, "Red Orb", "strikorb", "There seems to be a floating red orb here.","It's a reddish, transparent, sphere, floating next to you. It's presence sets your blood boiling, making you ready to pounce.", 70, 8);
var balorb = new Minion(50, 50, 10, 1, 10, [1,5], [4,3,6], 5, 5, "White Orb", "balorb", "There seems to be a floating white orb here.", "It's a whitish, transparent, sphere, floating next to you. It's presence cools your blood, Balancing your thoughts.", 80, 10);
var tankorb = new Minion(75, 100, 1, 1, 25, [1,50], [2,1, 10], -3, 5, "Green Orb", "tankorb", "There seems to be a floating green orb here.", "It's a greenish, transparent, sphere, floating next to you. It's presence makes you feel as though your blood is of iron, Steeling against any attack.", 100, 25);
var miniminion = new Minion(1, 1, 0, 0, 0, [1, 15], [2, 3, 0], 1, 4, "Minion", "miniminion", "A single tiny sphere, hugely out of place. It approaches you hesitantly. ", "A single tiny sphere, hanging close by.", 180, 5);
var superminion = new Minion(40, 40, 1, 1, 2, [1, 50], [50, 49, 4], -5, 5, "The Group", "superminion", "uhh, minions follow you", "A huge grouping of small orbs, swarming around you like fruit flies around fruit.", 20, 4);
var cube = new Minion(1,1,1,1,20,[10,100], [10,11,0], -1, 6, "Cube", "cube", "There is a cube here. It is small.", "A small cube. It hungers for it's friends.", 100, 75);
var chicken = new Minion(46, 46, 1, 4, 1, [1,100], [100, 99, 10], 6, 4,"Chicken","chicken","There's a chicken here.", "Loot?", 150, 25);


for (var i = 0; i < 30; i++){
    getMinion(superminion, miniminion);
}
for (var i = 0; i < 30; i++){
    getMinion(strangecube, cube);
}

minions = [cube, coompanion, nyancat, balorb, strikorb, tankorb, superminion, miniminion, fairy, chicken];

function getMinion(source, minion){
    //if source is player, make div of minion with id=minion.div+minion.id.   new div is only hp
    source.minions.push(new Minion(minion.hp, minion.maxhp, minion.atk, minion.ddev, minion.def, minion.agil, [minion.healchance[0], minion.healchance[1], minion.heal], minion.sane, minion.lvl, minion.name, minion.div, minion.message, minion.desc, minion.atkIntBase, minion.dist));
    if (source == pla){
        pla.minions[pla.minions.length-1].id = pla.id;
        pla.id += 1;
        screen = document.getElementById(minion.div+"hp");
        screen.innerHTML += '<div class="invis hpbar" style="width:361px;" id="'+pla.minions[pla.minions.length-1].div+pla.minions[pla.minions.length-1].id+'"><div class="invis" style="width:100%;height:100%;background-color:#f00"></div></div>';
    }
    getMinionTree(source, 1);
    source.minionTree = minionTree;
    prints("Gave "+source.name+" "+minion.name);
}



var ablerooms = [];
var finalsanity = 0;
//based on player level, changes aspects of game such as tiers of items, and rooms.
function gentables(){
    

    //loot tables
    lootitems = [];
    //add sanity levels and agility to calculation
    //&& item.sane >= sanity-2 && item.sane <= sanity+2 ?
    for (i in allitems){
        item = allitems[i];
        if (item.bossitem == 0){ 
            if (pla.lvl == 1 && (item.atk + item.def + (item.agil / 3) + (item.sane / 3)) <= 5) {lootitems.push(item);}
            if (pla.lvl == 2 && (item.atk + item.def + (item.agil / 2) + (item.sane / 2)) <= 10) {lootitems.push(item);}
            if (pla.lvl == 3 && (item.atk + item.def + item.agil + item.sane) <= 15) {lootitems.push(item);}
            if (pla.lvl >= 4) {lootitems.push(item);}
        }
    }

    
    //Math.floor(Math.cbrt(sanity)+-2)
    //
    ablerooms = [];
    for (i in rooms){
        var localrand = rooms[i];
        if (sanity < 2){
            if (localrand.sanity >= Math.floor(Math.cbrt(sanity) - pla.lvl) && localrand.sanity <= Math.floor(Math.cbrt(sanity) + (pla.lvl * 1.5))){
            ablerooms.push(rooms[i]);
            } 
        }
        else if (sanity >= 2){
            if (localrand.sanity <= Math.floor(Math.cbrt(sanity) + pla.lvl) && localrand.sanity >= Math.floor(Math.cbrt(sanity) - (pla.lvl * 1.5))){
            ablerooms.push(rooms[i]);
            } 
        }
        /*if (localrand.sanity >= Math.floor(Math.cbrt(sanity)-2) && localrand.sanity <= Math.floor(Math.cbrt(sanity)+2)){
            //console.log(localrand);
            ablerooms.push(rooms[i]);
        } */
    
    }
    
    if (ablerooms.length == 0 && pla.trueSane == 0){
        prints("Ablerooms empty. Sanity: "+ sanity + " pla.sane: " + pla.sane);
        if (sanity < 0){
            ablerooms = [room19];
            finalsanity = -1;
        }
        if (sanity > 0){
            ablerooms = [room23];
            finalsanity = 1;
        }
    } 
    
    //when reached true sanities
    if (pla.trueSane != 0){
        var item;
        lootitems = [];
        for (i in allitems){
            item = allitems[i];
            if (item.sane <= 0 && pla.trueSane < 0){
                lootitems.push(item);
            }
            if (item.sane >= 0 && pla.trueSane > 0){
                lootitems.push(item);
            }
        }
        for (i in rooms){
            item = rooms[i];
            if (item.sanity <= 0 && pla.trueSane < 0){
                ablerooms.push(item);
            }
            if (item.sanity >= 0 && pla.trueSane > 0){
                ablerooms.push(item);
            }
        }
    }
}




//Room related variables
var turn = 0;
var room;
var lootable = false;
var chestmessages = ["There is a small chest about the size of your fist lurking in the corner. ", "A golden chest sits with elegant details and pure beauty.", "There\'s a lumpy sack over there", "You hear the wheeze of a chest. \n\"Open me\" it calls, with the music of its collapsing wood.", "In a rotting monster carcass, you glimpse something... interesting.", "There\'s a lump in the ground. Like a squirrel buried a tasty rock and then ran off and died.", "Something calls your attention. It sucks you in. You imagine riches.", "You smell something. \nIt smells like goods.", "You glimpse a confection of wood and nails, almost big enough to hold something.", "There is a small door that seems to have something sticking out, perhaps something useful."];
var runmessages = ["Run", "Dodge", "Sprint", "Jump", "Duck", "Roll", "Slide", "Feint", "Fake", "Switch", "Distract", "Twist", "Lurch", "Insult", "Shout"];
var score = 0;
var isBossRoom = false;
var healable = true;
var noKillXissor = true;
var noKillOtherXissor = true;
var turnKillXissor = 0;
var noKillEpic = true;
var roommessage = "";
function genRoom() {
    prints("Generating room.");
    RDrefresh();
    gentables();
    turn ++;
    healable = true;
    //console.log(ablerooms);
    //leveling up
    if (score >= 10 && pla.lvl == 1){
        pla.lvl = 2;
        roommessage += "You can sence something.. Change, or Alter, in the dongeons around you..";
    }
    if (score >= 35 && pla.lvl == 2){
        pla.lvl = 3;
        roommessage += "You hear the calls of things, Unknown Creatures, from close by..";
    }
    if (score >= 80 && pla.lvl == 3){
        pla.lvl = 4;
        roommessage += "You can feel the Anger, the Hatred in the dongeon, Radiating from the surfaces, Aimed at you...";
    }
    if (score >= 140 && pla.lvl == 4){
        pla.lvl = 5;
        roommessage += "Level up!";
    }
    if (score >= 200 && pla.lvl == 5){
        pla.lvl = 6;
        roommessage += "Level up!";
    }
    
    var search = true;
    if (turn == 1){
        search = false;
    }
    for (i in bosses){
        var localrand = bosses[i];
        if (localrand.turn == turn){
            
            search = false;
            room = localrand.room
        }
    }
    if (search || turn == 1){
         room = ablerooms[rand(ablerooms.length)-1];
    }
   
    
    roommessage += room.message;
    
    
    localrand = rand(15);
    if (localrand == 1){roommessage += " Your feet are suddenly covered in water, with more rising from an unseen source."; room.water = 1}
    if (localrand == 2){roommessage += " Vines lazily wind their way towards you."; room.plant = 1}
    if (localrand == 3){roommessage += " You feel a gust of wind from the south."; room.south = 1}
    if (localrand == 4){roommessage += " The very air around you seems to emit a warm glow."; room.dark = 0; room.light = 1;}
    if (localrand == 5){roommessage += " The air muffles and dilutes not sound, but light."; room.dark = 1; room.light = 0;}
    if (localrand == 6){roommessage += " You can hear the clicking and whirring\n of unseen machinery."; room.manmade = 1;}
    if (localrand == 7){roommessage += " A large crowd of flies is hovering in a corner, seemingly growling at you."; room.animal = 1;}
    if (localrand == 8){roommessage += " You become lost in a cloud of dark light."; room.dark = 1, room.light = 1;}
    if (localrand == 9){roommessage += " There seems to be a lot of gold here. You must resist the urge to loot it all."; room.items = 1;}
    if (localrand == 10){roommessage += " Everything around you seems smoother, or Curvier"; room.manmade = 1;}
    if (localrand == 11){roommessage += " You have a moment of dizziness, a thought of doubt."; pla.sane -= 1;}
    if (localrand == 12){roommessage += " You hear whispering. You turn quickly, but nothing is there."; pla.sane -= 3;}
    if (localrand == 13){roommessage += " You feel a tap on your shoulder, and turn around to find that there is nothing there."; pla.sane -= 5;}
    if (localrand == 14){roommessage += " No matter to the circumstances, you are tired. You take a moment to rest."; pla.sane += 5;}
    if (localrand == 15){
        roommessage += " You blink. Something seems off.";
        var item = room.north;
        room.north = room.east;
        room.east = room.south;
        room.south = room.west;
        room.west = item;
    }
    pla.sane += room.sanity;
    pla.sane += (equippeditems[0].sane)/5;
    pla.sane += (equippeditems[1].sane)/5;
    for (i in pla.minions){
        pla.sane += (pla.minions[i].sane / 5);
    }
    
    //Determining lootable
    if (rand(2) == 1 && room.items == 1){
        lootable = true;
        roommessage += chestmessages[rand(chestmessages.length-1)];
    } else {
        lootable = false;
    }

    ableminions = [];
    for (i in minions){
        minion = minions[i];
        if (minion.lvl <= pla.lvl){
            ableminions.push(minion);
        }
    }
    if (rand(8) == 1 && ableminions.length > 0){
        var minion = ableminions[rand(ableminions.length)-1];
        roommessage += minion.message;
        getMinion(pla, minion);
    }

    var enemyspawn = rand(6); 
    
     for (i in bosses){
        var localrand = bosses[i];
        if (localrand.turn == turn){
            roommessage += prepbattle(localrand);
            search = false;
            
        }
    }
    
    if (search){
        if (equippeditems[0].Name == "Sissors" && equippeditems[1].Name == "Life Thread" && noKillXissor){
               roommessage += prepbattle(xissor);
               search = false;
               noKillXissor = false;
               turnKillXissor = turn;
            }
        if (turnKillXissor + 20 == turn && equippeditems[0].Name == "Xissors" && noKillOtherXissor){
               roommessage += prepbattle(otherXissor);
               search = false;
               noKillOtherXissor = false;
            
        }
        if (finalsanity == 1 && turn > 20 && pla.trueSane == 0){
               roommessage += prepbattle(lastinsanity);
               search = false;
               finalsanity = 0;
        }
        
        if (finalsanity == -1 && turn > 20 && pla.trueSane == 0){
               roommessage += prepbattle(lastsanity);
               search = false;
               finalsanity = 0;
        }
        
        if (noKillEpic && turn == 35){
            if (pla.atk >= pla.def && pla.atk >= pla.agil[0]){
                roommessage = ""
                roommessage += prepbattle(epicalpha);
                search = false;
            } else if (pla.def >= pla.atk && pla.def >= pla.agil[0]){
                roommessage = ""
                roommessage += prepbattle(epiccoo);
                search = false;
            } else if (pla.agil[0] >= pla.atk && pla.agil[0] >= pla.def){
                roommessage = ""
                roommessage += prepbattle(epicjim);
                search = false;
            } else{
                if (pla.sane <= 0){
                    finalsanity = -1
                    
                }
                if (pla.sane > 0){
                    finalsanity = 1
                }
            }
        }
        
        if (pla.lvl >= 3 && search){
            if (enemyspawn == 4 && room.plant == 1 && room.animal == 1){
                roommessage += prepbattle(dog);
                search = false;
                
            }
            if (enemyspawn == 5){
                roommessage += prepbattle(slime);
                search = false;
            }
            if (enemyspawn == 2 && room.water == 1){
                roommessage += prepbattle(koi);
                search = false;
            }
            if (enemyspawn <= 2 && room.water == 0 && room.dark == 1 && room.animal == 1 && room.light == 0){
                roommessage += prepbattle(catwatcher);
                search = false;
            }
            if (enemyspawn == 3 && room.animal == 1 && room.light == 1){
                roommessage += prepbattle(nerveball);
                search = false;
            }
        }
        if (pla.lvl >= 2 && search){
            //--
            
            //--
            if (enemyspawn == 1 && room.manmade == 1 && room.water == 0){
                roommessage += prepbattle(bookofdeath);
                search = false;
            }
            if (enemyspawn == 2 && room.manmade == 1){
                roommessage += prepbattle(clone);
                search = false;
            }
            if (enemyspawn == 3 && room.light == 1){
                roommessage += prepbattle(lightorb);
                search = false;
            }
            if (enemyspawn == 4 && room.items == 0){
                roommessage += prepbattle(mimic);
                lootable = true
                search = false;
            }
            //----
            
        }
        if (pla.lvl >= 1 && search){
            if (enemyspawn == 1 && room.water == 1 && room.animal == 1){
                roommessage += prepbattle(anenemy);
                search = false;
            }
            if (enemyspawn == 2 && room.plant == 1 && room.water == 0){
                roommessage += prepbattle(axeurlegs);
                search = false;
            }
            if (enemyspawn == 3){roommessage += prepbattle(creepybaldguy);}
        }
    }
    printa(roommessage);
}

var lastmove;
function move(direction){
    roommessage = "";
    if (battleprep == -1){
        var success = false;
        //north
        if (room.exitA == "" || room.exitA == " ") {room.exitA = "You go ";}
        if (room.exitB == "" || room.exitB == " ") {room.exitB = ".";}
        if(direction === 1){
            if (room.north === 1){
                success = true;
                roommessage = room.exitA + "north" + room.exitB;
            }
            else {roommessage = room.exitFail;}
        }
        //east
        if(direction === 2){
            if (room.east === 1){
                success = true;
                roommessage = room.exitA + "east" + room.exitB;
            }
            else {roommessage = room.exitFail;}
        }
        //south
        if(direction === 3){
            if (room.south === 1){
                success = true;
                roommessage = room.exitA + "south" + room.exitB;
            }
            else {roommessage = room.exitFail;}
        }
        //west
        if(direction === 4){
            if (room.west === 1){
                success = true;
                roommessage = room.exitA + "west" + room.exitB;
            }
            else {roommessage = room.exitFail;}
        }
        if (success == true) {
            printb("");
            roommessage += "<br/>";
            genRoom();
            lastmove = direction;
        } else {printb(roommessage);}
    }
    //if (battleprep >= 1) {battleprep = 0; enmFight();}
}

//Refreshing and Displaying
function screenchange(number) {
    screen1 = document.getElementById("RDmain");
    screen2 = document.getElementById("RDinven");
    screen3 = document.getElementById("RDfight");
    screen4 = document.getElementById("RDlimbo");
    screen5 = document.getElementById("RDmono");
    screen1.style.height = "0";
    screen1.style.padding = "0";
    screen2.style.height = "0";
    screen2.style.padding = "0";
    screen3.style.height = "0";
    screen3.style.padding = "0";
    screen4.style.height = "0";
    screen4.style.padding = "0";
    screen5.style.height = "0";
    screen5.style.padding = "0";
    if (number === 1) {
        screen1.style.height = "239px";
        screen1.style.padding = "10px";
    }
    if (number === 2) {
        screen2.style.height = "239px";
        screen2.style.padding = "10px";
    }
    if (number === 3) {
        screen3.style.height = "239px";
        screen3.style.padding = "10px";
    }
    if (number === 4) {
        screen4.style.height = "239px";
        screen4.style.padding = "10px";
    }
    if (number === 5) {
        screen5.style.height = "239px";
        screen5.style.padding = "10px";
    }
    console.log("changed to screen "+number);
}

function RDinit() {
    testu();
    RDrefresh();
    screenchange(1);
    gentables();
    genRoom();
    for (i in allitems) {
        item = allitems[i];
        var screen = document.getElementById(item.div);
        var itemdiv = screen.childNodes;
        quantity = itemdiv[2].childNodes;
        quantity[0].innerHTML = item.Name;
        quantity[2].innerHTML = item.desc;
        itemdiv[1].innerHTML = "<img src='img/"+item.div+".png'>"
    }

    for (i in bossitems) {bossitems[i].bossitem = 1;}
    setInterval('enmFight()',10);
}

function testu(){
    var localrand = "";
    for (i in allitems){
        var item = allitems[i];
        var item = "<div class=\"RDitem\" onclick=\"equip("+item.div+")\" id=\""+item.div+"\"> <div class=\"RDpic\"></div><div class=\"itemwords\"><div class=\"name\">name</div><div class=\"quant\">null</div><div class=\"desc\">desc</div></div></div>";
        localrand += item;
    }
    var screen = document.getElementById("items");
    screen.innerHTML = localrand;
    //do minion divs
    localrand = "";
    for (i in minions){
        var item = minions[i];
        var item = "<div class=\"RDminion\" onclick=\"prints(\'boop\')\" id=\""+item.div+"\"><div class=\"RDpic\"><img src='img/"+item.div+".png'></div><div class=\"itemwords\"><div class=\"name\" style=\"width:100%\">"+item.name+"</div><div class=\"desc\">"+item.desc+"</div></div><div class=\"invis\" style=\"float:left;clear:left;width:50%;height:34px\">Damage: "+item.atk+"<br/>Defence: "+item.def+"</div><div class=\"invis\" style=\"float:left;width:50%;height:34px\">dist agil</div><div class=\"invis\" style=\"float:left;clear:left;width:100%;min-height:0\" id=\""+item.div+"hp\"></div></div>";
        localrand += item;
    }
    var screen = document.getElementById("minions");
    screen.innerHTML = localrand;
}

function dispminions(){
    for (i in minions){
        searching = true;
        for (n in pla.minions){
            if (pla.minions[n].name == minions[i].name){searching = false}
        } 
        var screen = document.getElementById(minions[i].div);
        if (searching){
            //minimize minions[i].div
            screen.style.maxHeight = "0px";
            screen.style.border = "0px solid black";
            screen.style.padding = "0px";
        } else {
            screen.style.maxHeight = "99999999999999999999999999999999px";
            screen.style.border = "1px solid black";
            screen.style.padding = "2px";
        }
    }
}

function dispitem(item) {
    var screen = document.getElementById(item.div);
    if (item.quant >= 1) {
        screen.style.height = "50px";
        screen.style.border = "1px solid black";
        screen.style.padding = "2px";
    }
    else {
        screen.style.height = "0px";
        screen.style.border = "0px solid black";
        screen.style.padding = "0px";

    }
    var quantity = screen.childNodes;
    quantity = quantity[2].childNodes;
    quantity[1].innerHTML = item.quant;
}
function RDrefresh() {
    for (i in allitems){dispitem(allitems[i]);}
    dispminions();
    //gentables();
    for (i in pla.minions){
        var minion = pla.minions[i];
        screen = document.getElementById(minion.div+minion.id);
        screen = screen.childNodes;
        var health = 100*(minion.hp/minion.maxhp);
        if (health < 0){health = 0;}
        screen[0].style.width = health + "%";
        
    }
    
    health = pla.hp;
    pla.atk = pla.baseatk + equippeditems[0].atk + equippeditems[1].atk;
    pla.def = pla.basedef + equippeditems[0].def + equippeditems[1].def;
    pla.agil[0] = pla.baseagil[0] + equippeditems[0].agil + equippeditems[1].agil;
    sanity = Math.floor(pla.sane + equippeditems[0].sane + equippeditems[1].sane);
    if (score <0){sanity += score*2}

    var screen = document.getElementById("hp");
    screen.innerHTML = health;
    screen = document.getElementById("dmg");
    screen.innerHTML = pla.atk;
    screen = document.getElementById("dfn");
    screen.innerHTML = pla.def;
    //screen = document.getElementById("agl");
    //screen.innerHTML = pla.agil[0];
    screen = document.getElementById("score");
    screen.innerHTML = score;
    screen = document.getElementById("lvl");
    screen.innerHTML = pla.lvl;
    screen = document.getElementById("turn");
    screen.innerHTML = turn;

    screen = document.getElementById("enmhp");
    var health = 100*(enm.hp/enm.maxhp);
    if (health < 0){health = 0;}
    screen.style.width = health + "%";
    screen = document.getElementById("plahp");
    health = 100*(pla.hp/pla.maxhp);
    if (health < 0){health = 0;}
    screen.style.width = health + "%";
    
    
    
    var misc;
    var item = equippeditems[0];
    screen = document.getElementById("equip1");
    var childs = screen.childNodes;
    
    misc = childs[3].childNodes;
    misc[1].innerHTML = item.Name;
    misc[5].innerHTML = item.atk;
    misc[9].innerHTML = item.def;
    item = equippeditems[1];
    screen = document.getElementById("equip2");
    childs = screen.childNodes;
    misc = childs[3].childNodes;
    misc[1].innerHTML = item.Name;
    misc[5].innerHTML = item.atk;
    misc[9].innerHTML = item.def;
    

}

function printa(stuff) {
    var screen = document.getElementById("roomdesc");
    screen.innerHTML = stuff;
}
function printb(stuff) {
    var screen = document.getElementById("maindesc");
    screen.innerHTML = stuff;
}
function printc(thing, stuff) {
    switch (thing){
        case 1:
            where = "fightdesc";
            break;
        default:
            if (thing == enm || thing in enm.minionTree){
                where = "enmdesc";
            } else {where = "pladesc";}
            break;
    }
    var screen = document.getElementById(where);
    screen.innerHTML = stuff;
}
function prints(stuff) {
    console.log(stuff)
}

//Looting and getting items
function RDloot() {
    if (lootable) {
        gentables();
        getitem(lootitems[rand(lootitems.length)-1]);
        lootable = false;
    } else {printb("there is nothing to loot here.")}
}
function getitem(item){
    item.quant += 1;
    score += item.score;
    printb("You found "+item.Name + ".<br/>you place the newfound loot in your backpack.");
    RDrefresh();
}

//Everything with equipping

function equip(item) {
    if (item.quant >= 1) {
        if (equippeditems[0] == nothing) {equippeditems[0] = item; item.quant -= 1;} 
        else {if (equippeditems[1] == nothing) {equippeditems[1] = item; item.quant -= 1;} else {console.log("Cannot equip. All equip slots used.")}}
        
        var item = equippeditems[0];
        screen = document.getElementById("equip1");
        var childs = screen.childNodes;
        childs[1].innerHTML = "<img src = 'img/" + item.div + ".png'>";
        
        var item = equippeditems[1];
        screen = document.getElementById("equip2");
        var childs = screen.childNodes;
        childs[1].innerHTML = "<img src = 'img/" + item.div + ".png'>";
        
        
        RDrefresh();
    } else {console.log("Cannot equip. Not enough items.")}
}
function unequip(number){
    item = equippeditems[number];
    equippeditems[number] = nothing;
    screen = document.getElementById("equip"+(number+1));
    var childs = screen.childNodes;
    childs[1].innerHTML = "<img src = 'img/no_thing.png'>";
    item.quant += 1;
    prints("Unequipped "+item.Name);
    RDrefresh();
}

function op(thing) {
    switch (thing){
        case "allitems":
            for (i in allitems) {getitem(allitems[i])}
            break;
        case "loot":
            lootable = 1;
            RDloot();
            break;
        case "revive":
            pla.hp = pla.maxhp;
            prints("Revived");
            enm.hp = 0;
            plaFight(1);
            break;
        case "insane":
            pla.trueSane = -1;
            pla.baseatk = 16;
            pla.ddev = 20;
            pla.maxhp = 110;
            pla.baseagil = [2, 25];
            pla.basedef = -5;
            break;
        case "sane":
            pla.trueSane = 1;
            pla.maxhp = 110;
            pla.basedef = 5;
            pla.healval = 2;
            pla.ddev = 5;
            pla.baseagil = [1, 18];
            break;
        case "minions":
            for (var i = 0; i < 3; i++){
                getMinion(pla, miniminion);
            }
            for (i in pla.minions){
                for (var i = 0; i < 3; i++){
                    getMinion(pla.minions[i], miniminion);
                }
                
            }
            break;
    }
}


//roommessage += prepbattle
//battleprep 0 is starting fight, battleprep -1 is not attempting to enter fight.
var battleprep = -1;
var inbattle = false;
var enm = nullenm;
//All refer to enm, set to current enemy. Set enm in roomgen, set battleprep

//Figuring player stats
var plaTime = 0;
var plaHeal = 0;
var plaTotal = 0;

function prepbattle(enemy){
    
    enm = enemy;
    console.log(enm.name);
    if (enm.name == zarol.name || enm.name == lastinsanity.name){
        
        screen = document.getElementById("RDfight");
        screen.style.backgroundImage = "url('img/screen"+enm.div+".png')";
        screen.style.color = "#eef";
        screen = document.getElementById("enmPic");
        screen.innerHTML = "";
    } else {
        screen = document.getElementById("enmPic");
        screen.innerHTML = "<img src = 'img/enms/" + enm.div + ".png'>";
        screen = document.getElementById("RDfight");
        screen.style.backgroundImage = "url('img/screenmain.png')";
    }
    
    if (enm.name == zarol.name){
        zarol = buildZarol()
        enm = zarol
    }
    battleprep = 500;
    printc(1, "");
    printc(enm, "");
    printc(pla, "");
    getMinionTree(pla, 1);
    pla.minionTree = minionTree;
    getMinionTree(enm, 1);
    enm.minionTree = minionTree;
    for (i in enm.minionTree){
        enm.minionTree[i].atkInt = rand(enm.minionTree[i].atkIntBase);
    }
    for (i in pla.minionTree){
        pla.minionTree[i].atkInt = rand(pla.minionTree[i].atkIntBase);
    }
    return enm.message;
}
function enmFight(){
    RDrefresh();
    if (battleprep >= 1){battleprep -= 1;}
    if (battleprep == 0){
        inbattle = true;
        battleprep = -1;
        if (enm.boss == false) {enm.hp = enm.maxhp}
        //customise fight sceren to enemy
        printc(enm, enm.cry);
        screenchange(3);
    }
    if (inbattle){
        enm.atkInt -= 1;
        var deviation;
        if (enm.atkInt == 0){
            enm.atkInt = enm.atkIntBase;
            
            if (enm.boss){hpratio = enm.hp/enm.hptop}
            else {var hpratio = 100*(enm.hp/enm.maxhp);}
            
            //Print enemy description based on health
            if (hpratio < 20){
                printc(1, enm.rundown[0]);
            }
            if (hpratio >= 20 && hpratio < 50){
                printc(1, enm.rundown[1]);
            }
            if (hpratio >= 50 && hpratio < 85){
                printc(1, enm.rundown[2]);
            }
            if (hpratio >= 85 && hpratio <= 100){
                printc(1, enm.rundown[3]);
            }
            if (enm.boss){
                if (hpratio > 100 && hpratio < 200){
                    printc(1, enm.rundown[4])
                }
                if (hpratio >= 200){
                    printc(1, enm.rundown[5])
                }
            }
            var enmdo = rand(enm.healchance[0]);
            if (enmdo >= enm.healchance[1]){enmdo = "heal"} else {enmdo = "atk";}
            
            if (enmdo == "heal"){
                heal(enm);
            }
            
            var message = "";
            var dmg = 0;
            if (enmdo == "atk" && enm.hp > 0){
                attack(enm, pla);
            }
        }

        for (i in pla.minionTree){
            var minion = pla.minionTree[i];
            minion.atkInt -= 1;
            if (minion.atkInt <= 0){
                minion.atkInt = minion.atkIntBase;
                var enmdo = rand(minion.healchance[0]);
                if (enmdo >= minion.healchance[1]){enmdo = "heal"} else {enmdo = "atk";}
                
                if (enmdo == "heal"){
                    heal(minion);
                }
                
                var message = "";
                var dmg = 0;
                if (enmdo == "atk" && minion.hp > 0){
                    attack(minion, enm);
                }
            }
        }
        for (i in enm.minionTree){
            var minion = enm.minionTree[i];
            minion.atkInt -= 1;
            if (minion.atkInt <= 0){
                minion.atkInt = minion.atkIntBase;
                var enmdo = rand(minion.healchance[0]);
                if (enmdo >= minion.healchance[1]){enmdo = "heal"} else {enmdo = "atk";}
                
                if (enmdo == "heal"){
                    heal(minion);
                }
                
                var message = "";
                var dmg = 0;
                if (enmdo == "atk" && minion.hp > 0){
                    attack(minion, pla);
                }
            }
        }

        if (enm.name == "Adventurer" || enm.name == "Yourself"){
            plaTime += 1;
        }

    }
    if (dodging && monolithTime >= 0) {
        monolithTime -= 1;
        var monoPer = 100 * ((monolithOrig - monolithTime)/monolithOrig);
        prints(monoPer)
        monoAnimation(Math.floor(monoPer), 4)
        if (monolithTime <= 0) {
            prints("Monolith touch");
            dodging = false;
            score -= 10;
            turn = checkpoint;
            pla.hp = 100;
            unequip(0);
            unequip(1);
            for (i in allitems) {allitems[i].quant = 0;}
            for (i in bosses) {bosses[i].hp = bosses[i].rehp}
            genRoom();
            screenchange(1);
        }
    }
}
var checkpoint = 0
function plaFight(watdo){
    RDrefresh();
    switch (watdo){
        //attacking
        case 1:
            if (pla.hp > 0){
                if (enm.name == "Adventurer" || enm.name == "Yourself"){
                    plaTotal += 1;
                }
                attack(pla, enm);
            }
            break;
        //healing
        case 2:
            heal(pla);
            if (enm.name == "Adventurer" || enm.name == "Yourself"){
                plaHeal += 1;
                plaTotal += 1;
            }
            break;
    }
}


function attack(source, target){
    var attacking = true;
    for (i in target.minions){
        var minion = target.minions[i];
        if (rand(100) <= minion.dist && attacking){
            attack(source, minion);
            if (minion.hp <= 0) {
                killMinion(target, minion);
                getMinionTree(enm, 1);
                enm.minionTree = minionTree;
                getMinionTree(pla, 1);
                pla.minionTree = minionTree;
            }
            attacking = false;
        }
    } if (attacking) {
        Damage(source, target);
        check(target);
        attacking = false;
    }
}
function Damage(source, target){
    var message;
    if (rand(target.agil[1]) <= target.agil[0]){
        message = target.name + " dodged "+ source.name +"'s attack";
    } else {
        var deviation = rand(source.ddev * 2)- source.ddev;
        var dmg = (source.atk+deviation)-(target.def);
        if (dmg <= 0){
            dmg = 1;
        }
        message = source.name+" deals <strong>"+dmg+"</strong> damage to "+ target.name;
        target.hp = target.hp-dmg;
    }
    printc(target, message);
    //prints(message);
}
var minionTree = [];
function getMinionTree(entity, type){
    switch(type){
        case 2:
            if (entity.minions.length > 0){
                for (i in entity.minions){
                    minionTree.push(entity.minions[i]);
                    if (entity.minions[i].minions.length > 0 ){
                        getMinionTree(entity.minions[i], 2);
                    }
                }
                return minionTree;
            }
            break;
        case 1:
            minionTree = [];
            getMinionTree(entity, 2);
            return minionTree;
    }
}
function killMinion(source, minion){
    for (i in source.minions){
        if (source.minions[i] == minion){
            if (source == pla){
                var element = document.getElementById(minion.div+minion.id);
                prints(element);
                element.parentNode.removeChild(element);
            }
            printc(minion, source.name+"'s "+ minion.name+ " is dead.");
            prints(source.name+"'s "+ minion.name+ " is dead.");
            source.minions.splice(i, 1);
        }
    }
}

function check(entity){
    if (entity.hp <= 0){
        if (entity.name == enm.name && inbattle){
            inbattle = false;
            message = "You Kill the enemy.";
            score += 1;
            pla.sane -= 1;
            pla.sane += entity.sane; 
            if (entity.boss == 1){
                if (entity.name == "Zarol"){
                    
                    limbo(1, "At the moment of your victory, a swirling vortex of malevolence forms. You attempt in vain to escape it, but you are not yet strong enough. You find yourself in a familiar place...");
                    
                }
               
                if (entity.name !== "Xissor" || entity.name !== "The Other Xissor" || entity.name !== "True Insanity" || entity.name !== "True Sanity" || entity.name !== "Zarol" || entity.name !== "epicalpha" || entity.name !== "epiccoo" || entity.name !== "epicjim"){
                    checkpoint = entity.turn;
                }
                    
                var localrand = rand(4);
                if (localrand == 1){
                    message += "<br/>You Claim your rare prize.";
                    getitem(entity.loot2);
                } else {
                     message += "<br/>You Claim your prize.";
                    getitem(entity.loot);
                }
                bossesbeat += 1;
               
                if (entity.name == "Adventurer" || entity.name == "Yourself"){
                    RDrefresh();
                    prints("Recreating Adventurer.");
                    var miscA;
                    var miscB;
                    if (equippeditems[0] == nothing){miscA = herosword} else {miscA = equippeditems[0]}
                    if (equippeditems[1] == nothing){miscB = heroshield} else {miscB = equippeditems[1]}
                    //function Boss(    hp,         atk,        de,      name,      divname,    maxhp,      ddev, atkgil, heal, sane, loot, loot2, turn, message, cry, rundown, room, interval){

                    bosses[0] = new Boss(pla.maxhp, pla.atk, pla.def, "Yourself", "adventurer", pla.maxhp, pla.ddev, [pla.agil,100], [plaTotal, plaTotal-plaHeal, 4], sanity, miscA, miscB, 10, "You hear the footsteps of someone else.", "It is an Adventurer, \nReadying his stance for Battle!", ["He seems oddly unaware of the massive ammounts of damage you have delt him.\nMuch like you were.", "", "", "", "He seems more confident of himself,\nmore sure of his strides.",""], bossroom, (Math.floor(plaTime/plaTotal)));
                    bosses[0].minions = pla.minions;
                    bosses[0].atkInt = (plaTime/plaTotal)
                    bosses[0].atkIntBase = (plaTime/plaTotal)
                }
                if (entity.name == "Last Remnants of Sanity") {
                    pla.trueSane = -1;
                    pla.baseatk = 16;
                    pla.ddev = 20;
                    pla.maxhp = 110;
                    pla.baseagil = [2, 25];
                    pla.basedef = -5;
                }
                if (entity.name == "Last Remnants of Insanity") {
                    pla.trueSane = 1;
                    pla.maxhp = 110;
                    pla.basedef = 5;
                    pla.healval = 2;
                    pla.ddev = 5;
                    pla.baseagil = [1, 18];
                }
            }
            screenchange(1);
            printb(message);
        }
        if (entity.name == pla.name){
            printc(pla, "The enemy Kills you.");
            inbattle = false;
            RDrefresh();
           
            if (enm.name == "Zarol"){
                limbo(1, "At the moment of your death, a swirling vortex of malevolence forms. You attempt in vain to escape it, but you are not yet strong enough. You find yourself in a familiar place...");
                screen = document.getElementById("RDfight");
                screen.style.backgroundImage = "url('img/screenmain.png')";
            } else {limbo(0, "After experiencing a moment of extreme pain due to your inevitable death, you find yourself in a suprisingly calm dark space. The only landmarks are a large cliff dropping off into endlessness infront of you, and strange floating structures to high for you to reach. You realize that there is only one thing you can do....");}
        }
        if (entity in pla.minions){
           killMinion(entity.id, 1);
        }
    }
}



function heal(entity){
    if (entity == pla && pla.hp > 0){
        if (inbattle){
            var heal = pla.healval + rand(2*pla.hdev)-pla.hdev;
            pla.hp = pla.hp+heal;
            prints("\nyou heal "+heal+" hp!");
            if (pla.hp > pla.maxhp){pla.hp = pla.maxhp}
        }
        if (healable && !inbattle){
            var heal = pla.healval*10 + rand(4*pla.hdev)-pla.hdev;
            pla.hp = pla.hp+heal;
            pla.sane += 0.2;
            prints("\nyou heal "+heal+" hp!");
            if (pla.hp > pla.maxhp){pla.hp = pla.maxhp}
            healable = false;
        }
    } else {
        if (entity.hp + entity.heal > entity.maxhp){
            healval = entity.maxhp - entity.hp;
        } else {healval = entity.heal}
        entity.hp = entity.hp+healval;
        printc(entity, entity.name + " heals <strong>"+ healval+ "</strong> hp");
    }
}


var dodging = false;
var dodged = 0;
var monolithTime = 1500;
var monolithOrig = monolithTime;

function limbo(type, message){
    roommessage = "";
    switch (type) {
        //normal death
        case 0:
            score -= 1;
            pla.sane -= 5;
            if (checkpoint < 0){
                checkpoint = 1
            }
            
            turn = checkpoint;
            if (turn < -2) {turn = -2}
            pla.hp = 80+rand(20);
            var screen = document.getElementById("limbotext")
            screen.innerHTML = message;
            
            if (sanity < 0){
                //if (rand(100) <= sanity*-1){
                    //monolith spawn.
                    console.log("Monolith spawn");
                    dodging = true;
                    dodged = 0;
                    monolithTime = 1500 + (sanity * 1.5);
                    if (monolithTime <= 1){monolithTime = 5}
                    monolithOrig = monolithTime;
                    screenchange(5);
                //}
                
            } else {
                screenchange(4);
            }
            
            break;
        //anything zarol
        case 1:
            score += 10;
            turn = 0;
            checkpoint = 0
            pla.sane = pla.sane / 1.1
            pla.hp = 100
            unequip(0);
            unequip(1);
            var screen = document.getElementById("limbotext");
            screen.innerHTML = message;
            for (i in allitems) {
                allitems[i].quant = 0;
            }
            for (i in bosses) {bosses[i].hp = bosses[i].rehp}
            //for (i in pla.minions){killMinion(pla, pla.minions[0])}
            
            localrand = pla.minions.length;
            for (var i = 0; i < localrand; i ++){
                killMinion(pla, pla.minions[0])
            }
            screenchange(4);
            break;
        //jumping
        case 2:
            genRoom();
            screenchange(1);
            break;
        //dodging monoliths
        case 3:
            dodged += 1;
            var buton = document.getElementById("dodger");
            buton.style.margin = (rand(15)-1) + "% 0 0 " + (rand(80)-1) + "%";
            buton = document.getElementById("dodgeButton");
            buton.innerHTML = runmessages[rand(runmessages.length-1)];
            if (dodged == 5){
                dodging = false
                dodged = 0;
                monolithTime = 1500;
                turn = checkpoint;
                genRoom();
                screenchange(1);
                currentFram = 1;
            }
            break;

    }
}

currentFram = 1;
function monoAnimation(percentage, frams){

    if (percentage == (100/frams) * currentFram){
        
        var screen = document.getElementById("RDmono");
        screen.style.backgroundImage = "url('img/monoAnimation/mono" + currentFram + ".png')";
        currentFram += 1;
        prints(screen);
    }
}

































