# Term Project - Block Hero
# Hekai Yue - hyue - section H

import math
import random
from Tkinter import *
from PIL import ImageTk

class Character(object):#obtained from invaders "physObject" class, modified
    def __init__(self,x,y,dx,dy,girth,color):
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.girth=girth
        self.color=color

        self.exists=True

    def draw(self, canvas):
        x,y,girth=self.x,self.y,self.girth
        canvas.create_rectangle(x-girth/2,y-girth/2,x+girth/2,
            y+girth/2,fill=self.color,outline=self.color)

    def move(self):
        self.x+=self.dx
        self.y+=self.dy

    def collides(self, other):#checks if anyone will collide with any good guy
        if isinstance(other,Hero):#checks if baddies collide with hero
            r=other.girth*0.5#radius of hero's head
            #take all the points on the edge of the enemy squares
            x,y=self.x,self.y
            if self.y<other.y-(other.girth*0.5):
                #if enemy is colliding with dome part
                points=[(x-r,y-r),(x,y-r),(x+r,y-r),
                        (x-r,y),          (x+r,y),
                        (x-r,y+r),(x,y+r),(x+r,y+r)]
                ox,oy=(other.x),(other.y-other.girth*0.5)
                for point in points:
                    dx,dy=point
                    #dx and dy are just the coordinates of enemy edge
                    distance=((dx-ox)**2+(dy-oy)**2)**0.5
                    if distance<r:
                        return True
                return False
            else:
                dx,dy=abs(self.x-other.x),abs(self.y-other.y)
                if dx<self.girth and dy<self.girth:
                    return True
                return False

        elif other.loyal:#checks if baddies collide wit the hero's minions
            dx,dy=abs(self.x-other.x),abs(self.y-other.y)
            if dx<self.girth and dy<self.girth:
                return True
            return False

class Hero(Character):
    def __init__(self,width,height):
        girth=20
        self.hasorders=False
        self.color="white"
        self.anti=False
        super(Hero,self).__init__(width/2,height/2,0,0,girth,self.color)
        self.dead=False#means the hero is not dead
        self.special=False

    def draw(self,canvas):
        x,y,girth=self.x,self.y,self.girth
        canvas.create_oval(x-girth/2,y-girth,x+girth/2,
            y,fill=self.color,outline=self.color)
        canvas.create_rectangle(x-girth/2,y-girth/2,x+girth/2,
            y+girth/2,fill=self.color,outline=self.color)

    def move(self, width,height):
        super(Hero, self).move()
        if self.x -self.girth/2 < 0:
            self.x = self.girth/2
            self.dx = 0
        if self.x+self.girth/2 > width:
            self.x = width-self.girth/2
            self.dx = 0
        if self.y-self.girth<0:
            self.y=self.girth
            self.dy=0
        if self.y+self.girth/2>height:
            self.y=height-self.girth/2
            self.dy=0

class Minion(Character):
    #width,height are canvas dimenions
    #anti=False signifies not an anti-minion
    #heroxy=None:hero coordinates not given
    def __init__(self,loyal,width,height,anti=False,givenxy=None):
        self.loyal=loyal
        self.anti=anti#whether or not it's an anti-minion
        self.hasorders=False#means it's just following the hero
        self.special=False#no special formation
        #Warning: if ever editing goodcolors/badcolors, find all other places
        #in code and edit, too!
        colors=["red","yellow","blue"]
        if loyal: #loyal means the minion is on the hero team
            x=random.randint(0,width)#random x coordinate for minion
            y=random.randint(0,height)#random y coordinate for minion
            if anti:#anti-minion, for capturing minions
                self.color=colors[random.randint(0,len(colors)-1)]
                super(Minion,self).__init__(x,y,0,0,20,self.color)#anti-minion
            else:
                self.color="white"
                super(Minion,self).__init__(x,y,0,0,20,self.color)#team minion
        else:#else evil minion
            x,y=givenxy
            self.color=colors[random.randint(0,len(colors)-1)]
            super(Minion,self).__init__(x,y,0,0,20,self.color)

    def draw(self, canvas):
        x,y,girth=self.x,self.y,self.girth
        if self.loyal:
            if self.anti:
                colors=["red","yellow","blue"]
                canvas.create_oval(x-girth/2,y-girth/2,x+girth/2,
                    y+girth/2,fill=self.color,outline=self.color)
            else:
                canvas.create_oval(x-girth/2,y-girth/2,x+girth/2,
                    y+girth/2,fill=self.color,outline=self.color)
        else:
            canvas.create_rectangle(x-girth/2,y-girth/2,x+girth/2,
                y+girth/2,fill=self.color,outline=self.color)
    def move(self,previous,delay=15):
        #if object is a badguy, previous always refers to the hero
        if self.loyal: #loyal means it's on your team
            if self.hasorders:
                speedfactor=0.05
                self.x+=self.dx*speedfactor
                self.y+=self.dy*speedfactor
            else:
                dx=previous.x-self.x#distance in x direction
                dy=previous.y-self.y#distance in y direction
                distance=((dx)**2+(dy)**2)**0.5 #distance between the two
                spacing=35 #distance in between minions
                if distance>(spacing):
                    self.x+=dx/delay
                    self.y+=dy/delay
        else:#it's a black one, will try to kill you
            self.speed=0.8
            dx=previous.x-self.x#distance in x direction
            dy=previous.y-self.y#distance in y direction
            if dx!=0:#prevent division by zero
                theta=math.atan(dy/dx)
            else:
                theta=math.atan(dy/1000)#failsafe ^^dw
            if self.x>previous.x and self.y>previous.y:
                self.x-=self.speed*math.cos(theta)
                self.y-=self.speed*math.sin(theta)
            elif self.x>previous.x and self.y<previous.y:
                self.x-=self.speed*math.cos(theta)
                self.y-=self.speed*math.sin(theta)
            elif self.x<previous.x and self.y>previous.y:
                self.x+=self.speed*math.cos(theta)
                self.y+=self.speed*math.sin(theta)
            elif self.x<previous.x and self.y<previous.y:
                self.x+=self.speed*math.cos(theta)
                self.y+=self.speed*math.sin(theta)

class SpecialMinion(Minion):
    def __init__(self,loyal,width,height,anti,givenxy,teamsize,position):
        super(SpecialMinion,self).__init__(loyal,width,
            height,anti,givenxy)
        self.health=teamsize #more teammates will give more original health
        self.pathradius=60 #size of rotation path
        self.theta=(2*math.pi/teamsize)*position #orginal angle (polar location)
        self.x=self.pathradius*math.cos(self.theta)
        self.y=self.pathradius*math.sin(self.theta)
        self.special=True

    def move(self,teamsize,heroxy):
        dtheta=.4/(teamsize)#speed of rotation
        self.theta+=dtheta
        herox,heroy=heroxy
        self.x=herox+self.pathradius*math.cos(self.theta)
        self.y=heroy+self.pathradius*math.sin(self.theta)


class Game(object):#original code obtained from invaders example in class
    def __init__(self, width, height):
        #NOTE: WHEN YOU CHANGE INIT, CHANGE RESTART TOO!!
        self.gameOver=False
        self.width=width
        self.height=height
        self.me=Hero(width,height)
        self.minions=[self.me]#yes,the Hero is a minion
        self.team=[self.me]#yes, the Hero is part of the team
        self.specialTeam=[]
        self.level=1
        self.score=0
        self.topscore=0#highest score in single instance,not in history of game
        self.root=Tk()
        self.view="title"#can be title,game,about,or instructions
        self.instructionpage=0 #which page you are on (0 means none)
        self.image=ImageTk.PhotoImage(file="instructions/background.jpg")

    def restart(self,width,height):
        self.gameOver=False
        self.width=width
        self.height=height
        self.me=Hero(width,height)
        self.minions=[self.me]#yes, the hero counts as a minion
        self.specialTeam=[]
        self.team=[self.me]#yes, the hero is part of the team
        self.level=1
        self.score=0
        self.topscore=0#highest score in single instance,not in history of game
        self.view="title"#can be title,game,about,or instructions
        self.instructionpage=0

    def moveHero(self):
        # Move the hero
        self.me.move(self.width,self.height)
        #Add friction to the equation
        if self.me.dx>0:
            self.me.dx-=0.05
        if self.me.dy>0:
            self.me.dy-=0.05
        if self.me.dx<0:
            self.me.dx+=0.05
        if self.me.dy<0:
            self.me.dy+=0.05

    def moveTeam(self):
        #moves minions in your team that don't have orders and aren't special
        tempteam=[]
        if len(self.team)>1:
            for teammate in self.team:
                if (not teammate.hasorders) and (teammate.special!=True):
                    tempteam.append(teammate)
            if len(tempteam)>1:
                for teammate in tempteam[1:]:
                    teammate.move(tempteam[tempteam.index(teammate)-1])

        #moves the minions in your team that have orders
        tempteam2=[]
        for teammate in self.team:
            if teammate.hasorders:
                tempteam2.append(teammate)
        for teammate in tempteam2:
            teammate.move(None)

    def moveSpecialTeam(self):
        teamsize=len(self.specialTeam)
        for teammate in self.specialTeam:
            teammate.move(teamsize,(self.me.x,self.me.y))

    def assembleSpecialTeam(self):
        self.specialTeam=[]
        teamsize=0
        counter=0
        for teammate in self.team:
            if (teammate.color=="white") and not (isinstance(teammate,Hero)):
                teamsize+=1
        for teammate in self.team:
            if (teammate.color=="white") and not (isinstance(teammate,Hero)):
                counter+=1
                self.specialTeam.append(SpecialMinion(True,self.width,
                    self.height,False,None,teamsize,counter))
                self.minions.remove(teammate)

    def findFirstFreeTeammate(self,team):
        #finds the first teammate that doesn't already have orders
        for teammate in team[1:]:
            if not teammate.hasorders:
                return team.index(teammate)
        return None#returns None if there are no free teammates

    def addCharacters(self):
        pass
        # Add new baddies
        if random.uniform(0.0, 4.0) < 0.02*self.level:
            #these next few lines make sure no bad guy appears on top of hero
            x,y=random.randint(0,self.width),random.randint(0,self.height)
            if (abs(x-self.me.x)**2+abs(y-self.me.y)**2)**0.5>200:
                self.minions.append(Minion(False,self.width,self.height,
                False,(x,y)))
        #Add new anti-minions
        if random.uniform(0.0,4.0)<0.005*self.level:
            minion=Minion(True,self.width,self.height,True,
                (self.me.x,self.me.y))
            self.team.append(minion)
            self.minions.append(minion)

    def evalCollisions(self,badminion,teammate):
        #in this function, badminion is the badguy and teammate is the goodguy
        if isinstance(teammate,Hero) and not badminion.loyal:
            #this means they killed the hero
            teammate.dead=True #the game-over case
        elif teammate.anti:#an anti-minion is converting a baddie into teammate
            colors=["red","yellow","blue"]
            if teammate.color==badminion.color:
                self.team.append(badminion)
                badminion.loyal=True
                badminion.anti=False
                badminion.color="white"
                self.team.remove(teammate)
                #I think the reason it crashed before was that there were
                #rare cases when python was unable to process the minion into
                #the list before trying to remove it, so it would crash.
                #therefore i had to use try
                try:
                    self.minions.remove(teammate)
                except:
                    None
                self.score+=100

            else:#suicide :O you're sending an anti-minion to the slaughter
                self.team.remove(teammate)
                self.minions.remove(teammate)
                self.score-=10

        elif isinstance(teammate,SpecialMinion) and not badminion.loyal:
            #if it's a special minion
            try:
                self.minions.remove(badminion)
            except:
                None
            teammate.health-=1
            if teammate.health<=0:
                    try:
                        self.specialTeam.remove(teammate)
                    except:
                        None
                    try:
                        self.minions.remove(teammate)
                    except:
                        None
            self.score+=50



        elif (not teammate.anti) and (not badminion.loyal):
            #teammate is either giving a baddie a pounding
            #or is getting destroyed
            try:
                self.minions.remove(badminion)
            except:
                None
            #try/except because it's too hard to predict the location of where
            #something is going, and it would crash when something appeared
            #on top of something else
            self.team.remove(teammate)
            try:
                self.minions.remove(teammate)
            except:
                None
            self.score+=50

    def moveBaddiesAndFindCollisions(self):
        #Moves non-team minions AND test for collisions.
        #The reason this does both at once is because it is much more efficient.
        #Otherwise, you would need multiple nested forloops, etc.
        for minion in self.minions:
            if minion not in self.team:
                minion.move(self.me,100)#moves the minion
                for teammate in self.team:#finds contact with follower minions
                    if minion.collides(teammate):
                        self.evalCollisions(minion,teammate)
                for teammate in self.specialTeam:
                    if minion.collides(teammate):
                        self.evalCollisions(minion,teammate)

    def checkIncreaseScore(self):
        if self.score>self.topscore+200:
                self.level+=1#increases the level every 500 points
                self.topscore=self.score

    def timerFired(self):
        if self.me.dead==False:
            self.moveHero()
            self.moveTeam()
            self.moveSpecialTeam()
            self.moveBaddiesAndFindCollisions()
            self.addCharacters()
            self.checkIncreaseScore()
        self.redrawAll()
        self.canvas.after(5, self.timerFired)

    def keyPressed(self, event):
        if self.view=="game":
            if not self.me.dead:
                if event.keysym == "a":
                    if self.me.dx>-10:
                        if self.me.dx>-5:
                            self.me.dx=-5
                        else:
                            self.me.dx-=2
                if event.keysym == "d":
                    if self.me.dx<10:
                        if self.me.dx<5:
                            self.me.dx=5
                        else:
                            self.me.dx+=2
                if event.keysym == "w":
                    if self.me.dy>-10:
                        if self.me.dy>-5:
                            self.me.dy=-5
                        else:
                            self.me.dy-=2
                if event.keysym == "s":
                    if self.me.dy<10:
                        if self.me.dy<5:
                            self.me.dy=5
                        else:
                            self.me.dy+=2
                if event.keysym == "e":#cycles through minions on team
                    if len(self.team)>2:
                        self.team=([self.team[0]]+list(self.team[2:])+
                                [self.team[1]])
                if event.keysym == "q":
                    self.assembleSpecialTeam()
                if event.keysym == "x":
                    for teammate in self.team:
                        teammate.hasorders=False
                if event.keysym == "space":
                    self.me.dx,self.me.dy=0,0
                if event.keysym == "1":#debugging purposes, creates evil minion
                    x=random.randint(0,self.width)
                    y=random.randint(0,self.height)
                    if (abs(x-self.me.x)**2+abs(y-self.me.y)**2)**0.5>400:
                        self.minions.append(Minion(False,self.width,self.height,
                            False,(x,y)))
                if event.keysym == "2":#debugging purposes, creates good minion
                    minion=Minion(True,self.width,self.height)
                    self.minions.append(minion)
                    self.team.append(minion)
                if event.keysym == "3":#debugging purposes, creates good minion
                    minion=Minion(True,self.width,self.height,True)
                    self.minions.append(minion)
                    self.team.append(minion)
            if event.keysym == "r":
                self.restart(self.width,self.height)
                self.view="game"

    def mousePressed(self,event):
        if self.view=="title":#YOU ARE AT THE TITLE SCREEN
            #I think the tkinter built-in buttons are kinda ugly x)
            if (773<event.x<897) and (352<event.y<564):#the Play! button
                self.view="game"
                self.canvas.destroy()
                game.run()
            elif (220<event.x<339) and (461<event.y<580): #the About button
                self.view="about"
                self.drawAbout()
            elif (34<event.x<178) and (435<event.y<578):#the Exit button
                self.root.destroy()
            elif (134<event.x<310) and (310<event.y<430):
                self.view="instructions"
                self.instructionpage+=1
                self.drawInstructions()

        elif self.view=="about":
            if (35<event.x<176) and (435<event.y<578):
                self.view="title"
                self.drawTitle()

        elif self.view=="instructions":
            if(34<event.x<180) and (436<event.y<577):#the back button
                if self.instructionpage>0:
                    self.instructionpage-=1
                if self.instructionpage==0:
                    self.view="title"
                    self.drawTitle()
                else:
                    self.drawInstructions()
            elif ((220<event.x<338) and (464<event.y<580)#the next button
                and (0<=self.instructionpage<8)):
                self.instructionpage+=1
                self.drawInstructions()
            elif ((self.instructionpage==8) and (381<event.x<682)
                and (445<event.y<561)):
                self.instructionpage=0
                self.view="title"
                self.drawTitle()

        elif self.view=="game":#YOU ARE IN THE GAME
            if len(self.team)>1:
                i=self.findFirstFreeTeammate(self.team)
                if i!=None:
                    self.team[i].hasorders=True
                    self.team[i].dx=event.x-self.team[i].x
                    self.team[i].dy=event.y-self.team[i].y

    def drawMap(self):
        self.canvas.create_rectangle(0,0,self.width,self.height,
            fill="black",outline="light green")

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_image(0,0,image=self.image,anchor=NW)
        self.me.draw(self.canvas)
        for minion in self.minions:
            minion.draw(self.canvas)
        for minion in self.specialTeam:
            minion.draw(self.canvas)
        #draw score
        self.canvas.create_text(self.width/2,20, text="Score: %s"%self.score,
            fill="dark green",font=("Helvetica",12))
        #draw level
        self.canvas.create_text(self.width/2,self.height-20,
            text="Level %s"%self.level,fill="dark green",font=("Helvetica",12))
        #draw gameover if dead
        if self.me.dead:
            self.canvas.create_rectangle(0,0,self.width,
                self.height,fill="black")
            self.canvas.create_text(self.width/2,self.height/2-70,
                text="Game Over",fill="white",font=("Helvetica", 32, "bold"))
            self.canvas.create_text(self.width/2,self.height/2-30,
                text="Score: %s"%self.score,
                fill="white",font=("Helvetica", 20))
            self.canvas.create_text(self.width/2,self.height/2,
                text="You reached Level %d"%self.level,
                fill="white",font=("Helvetica", 20))
            self.canvas.create_text(self.width/2,self.height/2+40,
                text="Press \"r\" to restart.",
                fill="white",font=("Helvetica", 20))

    def drawTitle(self):
        try:
            self.canvas.destroy()
        except:
            None
        self.width,self.height=1000,600
        self.canvas=Canvas(width=self.width,height=self.height,bg='black')
        self.canvas.pack(expand=NO,fill=BOTH)
        image = ImageTk.PhotoImage(file = "instructions/titlescreen.jpg")
        self.canvas.create_image(0, 0, image = image, anchor = NW)
        self.root.bind("<Button-1>", self.mousePressed)
        mainloop()

    def drawAbout(self):
        try:
            self.canvas.destroy()
        except:
            None
        self.canvas=Canvas(width=self.width,height=self.height)
        self.canvas.pack(expand=NO)
        image=ImageTk.PhotoImage(file = "instructions/aboutscreen.jpg")
        self.canvas.create_image(0,0,image=image,anchor=NW)
        mainloop()

    def drawInstructions(self):
        try:
            self.canvas.destroy()
        except:
            None
        self.canvas=Canvas(width=self.width,height=self.height)
        self.canvas.pack(expand=NO)
        thisfile="instructions/instructions%d.jpg"%self.instructionpage
        image=ImageTk.PhotoImage(file=thisfile)
        self.canvas.create_image(0,0,image=image,anchor=NW)
        mainloop()


    def run(self):
        if self.view=="title":
            self.drawTitle()
        elif self.view=="about":
            self.drawAbout()
        elif self.view=="game":
            try:
                self.canvas.destroy()
            except:
                None
            self.canvas = Canvas(self.root, width=self.width,height=self.height)
            self.canvas.pack()
            self.root.bind("<Key>", self.keyPressed)
            self.root.bind("<Button-1>", self.mousePressed)
            self.timerFired()

            ####################################################################
            ###Code below first obtained @http://effbot.org/tkinterbook/menu.htm
            def endGameWrapper():
                self.me.dead=True
            def initWrapper():
                self.restart(self.width,self.height)
                self.view="game"
            def about():
                self.view="about"
                self.run()
            def closeWindow():
                root.destroy()
            def quitToMenuWrapper():
                self.canvas.destroy()
                self.view="title"
                self.run()
            menubar = Menu(self.root)
            # create a pulldown menu, and add it to the menu bar
            filemenu = Menu(menubar, tearoff=0)
            filemenu.add_command(label="New Game",
                command=initWrapper)
            filemenu.add_command(label="End Game", command=endGameWrapper)
            filemenu.add_separator()
            filemenu.add_command(label="Quit to Menu",command=quitToMenuWrapper)
            menubar.add_cascade(label="File", menu=filemenu)

            # create more pulldown menus
            helpmenu = Menu(menubar, tearoff=0)
            helpmenu.add_command(label="About", command=about)
            menubar.add_cascade(label="Help", menu=helpmenu)

            # display the menu
            self.root.config(menu=menubar)
            ###
            ####################################################################
            self.root.mainloop()




game=Game(1000,600)
game.run()

