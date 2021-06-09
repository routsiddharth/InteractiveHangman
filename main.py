import pygame, sys, random, re, math, time
from pygame.locals import *

# Setup Window
# This sets up the Pygame window
pygame.init()
MAX_FPS = 308
clock = pygame.time.Clock()
pygame.display.set_caption('Hangman!')

WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors and fonts
# This defines the key colours and fonts for later use
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

FONT_S = pygame.font.SysFont('comicsans', 40)
FONT_L = pygame.font.SysFont('comicsans', 100)

# Setup images

images = []

for i in range(7):
    image = pygame.image.load(f"Images/{str(i)}.png")
    images.append(image) # This for loop adds the images to the list



random_words = ['coats' , 'boats' , 'float' , 'bored' , 'keeps',
                'glass' , 'spine' , 'apple' , 'grape' , 'creep',
                'bread' , 'sword' , 'arrow' , 'brass' , 'cheap',
                'tears' , 'steer' , 'stare' , 'flare' , 'phone',
                'heart' , 'heard' , 'cards' , 'witch' , 'goofy',
                'noble' , 'fools' , 'crazy' , 'sunny' , 'ready',
                'brown' , 'sheep' , 'hedge' , 'steal' , 'steel',
                'drown' , 'crown' , 'feast' , 'flame' , 'kites',
                'clock' , 'stock' , 'stack' , 'steep' , 'shave',
                'brave' , 'cruel' , 'stool' , 'chair' , 'crack',
                'black' , 'worst' , 'gross' , 'flags' , 'beaks',
                'steak' , 'break' , 'freak' , 'groan' , 'grown',
                'fears' , 'guess' , 'bloom' , 'groom' , 'broom',
                'rooms' , 'gloom' , 'water' , 'beard' , 'weird',
                'crate' , 'floor' , 'store' , 'tiers' , 'dream',
                'cream' , 'blast' , 'class' , 'deals' , 'death',
                'grass' , 'blade' , 'blame' , 'stamp' , 'camps',
                'theft' , 'heals' , 'shelf' , 'fakes' , 'lakes',
                'tails' , 'tales' , 'lease' , 'least' , 'bleak',
                'board' , 'dread' , 'snail' , 'frail' , 'beast',
                'north' , 'blaze' , 'craze' , 'drone', 'stone', 
                'loner', 'mouse', 'lucky']

# I have kept all of the words to 5 letters to simplify the drawing function (see below for draw())

# Buttons and draw()
# This creates the buttons and adds letters to the buttons
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH-(RADIUS*2+GAP)*13)/2)
starty = 400

str_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for i in range(26):
    
    x = startx + GAP*2 + ((RADIUS*2+GAP) * (i % 13))
    y = starty + ((i//13) * (GAP+RADIUS*2))
    
    letter = str_letters[i]
    
    letters.append([x, y, letter, True])

# This is the func to execute when the game is over   
def fin():
    
    draw()
    
    time.sleep(5)
    
    window.fill(WHITE)
    
    if win == True:
        
        t = FONT_L.render("YOU WON!", 1, BLACK)
        
        xpos = (WIDTH /2) - (t.get_width()/2)                
        ypos = (HEIGHT /2) - (t.get_height()/2)  
                          
        window.blit(t, (xpos, ypos))
    
    else:
        t = FONT_L.render("YOU LOST!", 1, BLACK)
        
        xpos = (WIDTH /2) - (t.get_width()/2)                
        ypos = (HEIGHT /2) - (t.get_height()/2)  
                          
        window.blit(t, (xpos, ypos))
        
    text = FONT_S.render(f"The word was {word}", 1, BLACK)
    
    xpos = (WIDTH /2) - (text.get_width()/2) 
    ypos = (HEIGHT /2) - (t.get_height()/2)+t.get_height()
    
    window.blit(text, (xpos, ypos))
    
    text = FONT_S.render("Press any key to play again.", 1, BLACK)
    
    xpos = xpos = (WIDTH /2) - (text.get_width()/2) 
    ypos = 25
    
    window.blit(text, (xpos, ypos))
        
    pygame.display.update()
                          
def draw(): # Function which draws the screen with updated variables every loop
    
    window.fill(WHITE)
    window.blit(images[hangman], (185, 90))
    
    for letter in letters:
        x, y, l, b = letter
        
        if b == True:
            pygame.draw.circle(window, BLACK, (x,y), RADIUS, 3)

            text = FONT_S.render(l, 1, BLACK)
            window.blit(text, (x-text.get_width()/2,y-text.get_height()/2))
    
    xpos = 450
    ypos = 125
    
    for i in range(5):
        
        letter = hidden[i]
        
        x = xpos + (50*i)
    
        t = FONT_L.render(letter, 1, BLACK)
        window.blit(t, (x, ypos))
    
    pygame.display.update()
    
# Game loop

#These are the main variables required to play the game

wait_for_key = False 
hangman = 0
word = random.choice(random_words)
word = word.upper()
hidden = '_'*len(word) # We will only display hidden and compare hidden to the chosen word
guessed = []
win = None
running = True # Is the main variable, when set to False, the game loop is stopped

while running:
    
    clock.tick(MAX_FPS)
    
    if wait_for_key == False:
        draw()
    else:
        pass
    
    for e in pygame.event.get():
        
        if e.type == pygame.QUIT:
            
            running = False
            
        if e.type == pygame.KEYDOWN: # This is only relevant when we require a key to be pressed (end of game)
            
            if wait_for_key == True:
                
                wait_for_key = False
                hangman = 0
                word = random.choice(random_words)
                word = word.upper()
                hidden = '_'*len(word) 
                guessed = []
                win = None
                
                for letter in letters:
                    letter[3] = True
            
        if e.type == pygame.MOUSEBUTTONDOWN:
            
            mx, my = pygame.mouse.get_pos()
            
            for letter in letters:
                
                x, y, l, b = letter
                
                if l not in guessed:
                    
                    dis = math.sqrt((x-mx)**2+(y-my)**2)

                    if dis < RADIUS:
                        
                        letter[3] = False
                        ltr = l
            
                        if ltr in word:

                            for i in range(len(word)):

                                if word[i] == ltr:

                                    hidden = hidden[:i:] + word[i] + hidden[i+1::]

                            if hidden == word:

                                win = True
                                wait_for_key = True
                                fin()

                        else:

                            hangman += 1
                          
                            if hangman == 6:
                                win = False
                                wait_for_key = True
                                fin()
            
pygame.quit()