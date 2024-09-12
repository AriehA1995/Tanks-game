import pygame
import random
pygame.init()

# The game window size
win = pygame.display.set_mode ((500, 500))
#The game title
pygame.display.set_caption ("My first game!!!")


class obj:
    def __init__(self, x, y, width, height, speed = 5, lign="y"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.lign = lign
        self.health = 100

    def properties(self):
        return (self.x, self.y, self.width, self.height)

    def pointer(self, direction):
        #drawing a red triangle that point the dircetion of the player
        if direction["name"] == "right":
            triangle = [(self.x+25,self.y+5),(self.x+30,self.y+10),(self.x+25,self.y+15)]
        elif direction["name"] == "left":
            triangle = [(self.x-5,self.y+5),(self.x-10,self.y+10),(self.x-5,self.y+15)]
        elif direction["name"] == "up":
            triangle = [(self.x+5,self.y-5),(self.x+10,self.y-10),(self.x+15,self.y-5)]
        elif direction["name"] == "down":
            triangle = [(self.x+5,self.y+25),(self.x+10,self.y+30),(self.x+15,self.y+25)]
        # default: right direction
        else:
            triangle = [(self.x+25,self.y+5),(self.x+30,self.y+10),(self.x+25,self.y+15)]
        pygame.draw.polygon(win, (200,200,0), triangle)

    def auto_move(self):
        if self.lign == "x":
            self.x = self.x + self.speed
            if self.x > 500-(self.width+self.speed) or self.x < 0:
                self.speed = self.speed *-1
        else:
            self.y = self.y + self.speed
            if self.y > 500-(self.width+self.speed) or self.y <= 45:
                self.speed = self.speed *-1
    def hit(self, amount):
        self.health -= amount

    def healthBar(self, place = False):
        if place == False:
            #the default place of the helath bar is over the object
            place = (self.x, self.y-7, self.width, 5)
        pygame.draw.rect(win, (250,0,0), place)
        # if the health is 50, the width of the green rect should be 50% of the health
        greenWidth = int(place[2]*self.health/100)
        pygame.draw.rect(win, (0,200,0), (place[0], place[1], greenWidth, place[3]))
        pygame.draw.rect(win, (0,0,0), place, 1)
        

class projectile:
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.dir = direction
    # direction is a dictionary {name, lign, moving} used to know how to move the projectile

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        if self.dir["lign"] == "x":
            self.x = self.x + 10*self.dir["moving"]
        else:
            self.y = self.y + 10*self.dir["moving"]

def redrawWindow():
    if player.health <= 0:
        win.fill((255,255,255))
        gameover = font.render("Game Over", 1, (0, 0, 0))
        win.blit(gameover, (150, 200))
        yourscore = font.render("Your score: " + str(score), 1, (0, 0, 0))
        win.blit(yourscore, (150, 250))
    else:
        #background color (if not - all the object will be added)
        win.fill((100,255,255))
        #score bar
        pygame.draw.rect(win, (0,0,0), (0, 0, 500, 40))
        text = font.render("Score: " + str(score), 1, (255, 255, 255))
        win.blit(text, (10, 10))
        #add the player object
        pygame.draw.rect(win, (0,0,250), player.properties())
        player.healthBar((166, 10, 166, 20))
        for enemy in enemies: 
            pygame.draw.rect(win, (250, 0, 0), enemy.properties())
            enemy.healthBar()
            enemy.auto_move()
        player.pointer(direction)
        
        for ball in fire:
            ball.draw(win)
            # clear the ball if it get out from the window
            if ball.x < 500 and ball.x > 0 and ball.y < 500 and ball.y >= 50:
                ball.move()
            else:
                fire.pop(fire.index(ball))
            
    #display the window
    pygame.display.update()
    
run = True
player = obj(240, 240, 20, 20)
direction = {"name":"right","lign":"x", "moving":1}
fire = []
enemies = []
shoot = 3
timer = 0
font = pygame.font.SysFont("david", 30, False)
score = 0
level = 1

def levelSpeed (level):
    MIN_SPEED = 100
    ONE_SECONDE_LEVEL = MIN_SPEED / 20
    if level >= 20 + ONE_SECONDE_LEVEL:
        return 1
    elif level > ONE_SECONDE_LEVEL:
        return 20 - (level - ONE_SECONDE_LEVEL)
    else:
        return MIN_SPEED + 20 - (20 * level)

levSp = levelSpeed (level)

#mainloop
while run:
    #Refreh delay (in mS)
    pygame.time.delay(50)
    for event in pygame.event.get():
        #if you press on the X at the top right corner, the game stop
        if event.type == pygame.QUIT:
            run = False

    #new enemy comes every 5 secondes
    if timer % levSp == 0:
        if timer % (2 * levSp) == 0:
            enemyLign = "y"
        else:
            enemyLign = "x"
        enemies.append(obj(random.randint(0, 480), random.randint(52, 480), 20, 20, 5, enemyLign))
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # allow only five ball at the same time
        if len(fire) < 5 and shoot > 2:
            fire.append(projectile(player.x+10, player.y+10, 3, (250,0,0), direction))
            shoot = 0
    if keys[pygame.K_LEFT]:
        #if not, it is because it is in the end of the window
        if player.x >= 5:
            player.x -= 5
            direction = {"name":"left", "lign":"x", "moving":-1}
    if keys[pygame.K_RIGHT]:


        if player.x <= 475:
            player.x += 5
            direction = {"name":"right", "lign":"x", "moving":1}
    if keys[pygame.K_UP]:
        if player.y >= 45:
            player.y -= 5
            direction = {"name":"up", "lign":"y", "moving":-1}
    if keys[pygame.K_DOWN]:
        if player.y <= 475:
            player.y += 5
            direction = {"name":"down", "lign":"y", "moving":1}
    
    #define when the ball hit the enemy  
    for enemy in enemies:
        for ball in fire:
            if ball.x + ball.radius > enemy.x and ball.x < enemy.x + enemy.width:
                if ball.y + ball.radius > enemy.y and ball.y < enemy.y + enemy.height:
                    fire.pop(fire.index(ball))
                    enemy.hit(50)
                    if enemy.health<=0:
                        enemies.pop(enemies.index(enemy))
                        score += 10
                        if score >= 100 * level and score - 10 < 100 * level:
                            level += 1
                            levSp = levelSpeed (level)
                            print ("Score: ", score, "Level: ", level, "Speed: ", levSp)
        if player.x + player.width > enemy.x and player.x < enemy.x + enemy.width:
            if player.y + player.height > enemy.y and player.y < enemy.y + enemy.height:
                score -= int(enemy.health/10)
                enemies.pop(enemies.index(enemy))
                player.hit(34)
        
    shoot += 1
    timer += 1
    redrawWindow()

print("")
print("Your score: " + str(score))
time = int(timer/20)
secondes = time % 60
minutes = int((time - secondes)/60)
if secondes < 9:
    secondes = "0" + str(secondes)
else:
    secondes = str(secondes)
if minutes < 9:
    minutes = "0" + str(minutes)
else:
    minutes = str(minutes)
print("Game time: " + minutes + ":" + secondes)
pygame.quit()
