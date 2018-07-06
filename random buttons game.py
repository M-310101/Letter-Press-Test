import pygame, random, string, time, timeit

## pygame's initialisation
pygame.init()
pygame.font.init()

## set up dictionary corresponding with all of the letters and their corresponding numbers
keys = {97:"a",98:"b",99:"c",100:"d",101:"e",102:"f",103:"g",
        104:"h",105:"i",106:"j",107:"k",108:"l",109:"m",110:"n",
        111:"o",112:"p",113:"q",114:"r",115:"s",116:"t",117:"u",
        118:"v",119:"w",120:"x",121:"y",122:"z"}

## colours
BLACK = [  0,  0,  0]
WHITE = [255,255,255]
RED   = [255,  0,  0]
GREEN = [  0,255,  0]

## set up display window
SW = 720
SH = 480
pygame.display.set_caption("Speed Press")
SS = pygame.display.set_mode((SW,SH))

## set the sizes for the font
mainSize = 50
summarySize = 30
stateSize = 20

## clock for pygame to loop through
clock = pygame.time.Clock()
FPS = 60

## intro text as a list
introText = ["In this game you have to press",
             "the letter you see on the screen.",
             "Once you get 10 correct the game",
             "will end and you will get your time",
             "and the number you of letters",
             "got right and wrong"]

## quiting procedure
def quiting():
    pygame.quit()
    quit()

## creaiting text object to be displayed
def text_objects(text,font,colour):
    ## creates a surface for text to be displayed
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def message_display(text,x,y,textsize,colour):
    ## sets font and text size
    thetext = pygame.font.Font('freesansbold.ttf',textsize)
    ## creates the rectangle for the text to be set on
    TextSurf, TextRect = text_objects(text, thetext,colour)
    TextRect.center = (x,y)
    SS.blit(TextSurf, TextRect)

def ready():
    '''intro screen that gives information on the game'''
    ready = False
    while not ready:
        SS.fill(BLACK)
        message_display("READY?",SW/2,SH/2,mainSize,WHITE)
        pygame.display.update()
        clock.tick(FPS)
        time.sleep(2)
        ## countdown from 3 to be displayed
        for i in range(1,4):
            SS.fill(BLACK)
            message_display(str(4-i),SW/2,SH/2,mainSize,WHITE)
            pygame.display.update()
            clock.tick(FPS)
            time.sleep(1)
        ready = True

def game_loop():
    ready()
    ## variables to track the number of right and wrong inputs
    right = 0
    wrong = 0
    ## letter is taken from the ascii library as a random choice
    letter = random.choice(list(string.ascii_lowercase))
    quiting = False
    end_screen = False
    ## starting timer to indicate the time past
    start = timeit.default_timer()
    wait = 0
    while not quiting:
        ## loop through all the pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quiting = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                ## checks if the key entered is a letter
                if event.key in range(97,123):
                    ## checks if that key is the correct key
                    if keys[event.key] == letter:
                        ## starts a time that keeps track of the waiting time while the correct screen displays
                        waiting = time.time()
                        right += 1
                        ## fill with green to indicate correct key
                        SS.fill(GREEN)
                        ## displays information about the letter and their score
                        message_display("CORRECT",(SW/2),(SH/2)-140,summarySize,WHITE)
                        message_display(letter.upper(),(SW/2),(SH/2),mainSize,WHITE)
                        message_display("Correct: "+str(right),570,30,stateSize,WHITE)
                        message_display("Incorrect: "+str(wrong),120,30,stateSize,WHITE)
                        pygame.display.update()
                        time.sleep(0.25)
                        letter = random.choice(list(string.ascii_lowercase))
                        ## new variable taking the current time
                        waitingstop = time.time()
                        ## wait variable takes in the amount of time that the screen was displayed
                        wait += (waitingstop-waiting)
                        waiting = 0
                    else:
                        ## same procedure for an incorrect input
                        waiting = time.time()
                        wrong += 1
                        SS.fill(RED)
                        message_display("INCORRECT",(SW/2),(SH/2)-140,summarySize,WHITE)
                        message_display(letter.upper(),(SW/2),(SH/2),50,WHITE)
                        message_display("Correct: "+str(right),570,30,stateSize,WHITE)
                        message_display("Incorrect: "+str(wrong),120,30,stateSize,WHITE)
                        pygame.display.update()
                        time.sleep(0.25)
                        letter = random.choice(list(string.ascii_lowercase))
                        waitingstop = time.time()
                        wait += (waitingstop-waiting)
                        waiting = 0
                        
                    
        ## timer of the current time that will update with every loop
        current = timeit.default_timer()
        SS.fill(BLACK)
        message_display(letter.upper(),(SW/2),(SH/2),50,WHITE)
        ## set varaible to be the current time - the starting time - the waiting time
        times = current-start-wait
        message_display("%.2f s" % times,(SW/2),(SH/2)+80,mainSize,WHITE)
        message_display("Correct: "+str(right),570,30,stateSize,WHITE)
        message_display("Incorrect: "+str(wrong),120,30,stateSize,WHITE)
        pygame.display.update()
        clock.tick(FPS)
        ## if there have been 10 correct inputs, the game will end
        if right == 10:
            quiting = True
            end_screen = True
        while end_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quiting = True
                    pygame.quit()
                    quit()
            SS.fill(BLACK)
            message_display("%.2f s" % times,(SW/2),(SH/2)-mainSize,mainSize,WHITE)
            message_display("Correct: "+str(right),570,(SH/2)+50,summarySize,WHITE)
            message_display("Incorrect: "+str(wrong),120,(SH/2)+50,summarySize,WHITE)
            pygame.display.update()
            clock.tick(FPS)

def intro_screen():
    intro = True
    ## starting timer
    start = timeit.default_timer()
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                quiting()

        ## displays title
        SS.fill(BLACK)
        lineCount = 0
        message_display("SPEED PRESS",SW/2,mainSize,mainSize,RED)

        ## displays each item in the introText list on a different line 
        for i in introText:
            message_display(i,SW/2,SH/2+lineCount*summarySize-mainSize*2,summarySize,WHITE)
            lineCount += 1
        ## keeps track of the current time
        current = timeit.default_timer()

        ## once 6 seconds have past, a continue option will pop up to ensure the user has read the rules
        if current-start > 6:
            message_display("PRESS M TO CONTINUE",SW/2,SH-stateSize,stateSize,WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    quiting()
                
                if event.type == pygame.KEYDOWN:
                    if keys[event.key] == "m":
                        intro = False
                        game_loop()
                
        pygame.display.update()
        clock.tick(FPS)

intro_screen()
