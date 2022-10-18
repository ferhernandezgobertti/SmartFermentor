import sys
import time
import pygame, random
from ctypes import windll
from pygame.locals import *

WINDOWWIDTH = 1366
WINDOWHEIGHT = 768
BACKGROUNDCOLOR_ORT = (8, 80, 80)
FPS_DODGER = 40
BADDIEMINSIZE_DODGER = 10
BADDIEMAXSIZE_DODGER = 80 # 40
BADDIEMINSPEED_DODGER = 1
BADDIEMAXSPEED_DODGER = 8
ADDNEWBADDIERATE_DODGER = 6
PLAYERMOVERATE_DODGER = 5
SCORE_DODGER = 100

FPS_MEM = 30 # frames per second, the general speed of the program
REVEALSPEED_MEM = 8 # speed boxes' sliding reveals and covers
BOXSIZE_MEM = 80 # size of box height & width in pixels
GAPSIZE_MEM = 20 # size of gap between boxes in pixels
BOARDWIDTH_MEM = 10 # number of columns of icons
BOARDHEIGHT_MEM = 7 # number of rows of icons
assert (BOARDWIDTH_MEM * BOARDHEIGHT_MEM) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN_MEM = int((WINDOWWIDTH - (BOARDWIDTH_MEM * (BOXSIZE_MEM + GAPSIZE_MEM))) / 2)
YMARGIN_MEM = int((WINDOWHEIGHT - (BOARDHEIGHT_MEM * (BOXSIZE_MEM + GAPSIZE_MEM))) / 2)
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

FPS_NIBBLES = 15
WINDOWWIDTH_NIBBLES = 1360
WINDOWHEIGHT_NIBBLES = 760
CELLSIZE_NIBBLES = 40
assert WINDOWWIDTH_NIBBLES % CELLSIZE_NIBBLES == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT_NIBBLES % CELLSIZE_NIBBLES == 0, "Window height must be a multiple of cell size."
CELLWIDTH_NIBBLES = int(WINDOWWIDTH_NIBBLES / CELLSIZE_NIBBLES)
CELLHEIGHT_NIBBLES = int(WINDOWHEIGHT_NIBBLES / CELLSIZE_NIBBLES)
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0 # syntactic sugar: index of the worm's head

BLACK     = (  0,   0,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
ORT      = (  8,  80,  80)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BGCOLOR = ORT
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
ALLCOLORS_MEM = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES_MEM = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS_MEM) * len(ALLSHAPES_MEM) * 2 >= BOARDWIDTH_MEM * BOARDHEIGHT_MEM, "Board is too big for the number of shapes/colors defined."


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def Dodger():

    pygame.display.init()
    mainClock = pygame.time.Clock()
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    SetWindowPos = windll.user32.SetWindowPos
    SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 0x0001)
    pygame.display.set_caption('SMART DODGER')
    pygame.mouse.set_visible(False)

    playerImage = pygame.image.load('Images/GamesPic/DodgerPic/playerORT.png')
    playerRect = playerImage.get_rect()
    baddieImage = pygame.image.load('Images/GamesPic/DodgerPic/obstacleBath.png')

    points = 1200

    topScore = 0
    while True:

        baddies = []
        score = 0
        playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
        moveLeft = moveRight = moveUp = moveDown = False
        reverseCheat = slowCheat = False
        baddieAddCounter = 0

        while True:
            score += 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    return points

                if event.type == KEYDOWN:
                    if event.key == ord('z'):
                        reverseCheat = True
                    if event.key == ord('x'):
                        slowCheat = True
                    if event.key == K_LEFT or event.key == ord('a'):
                        moveRight = False
                        moveLeft = True
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveLeft = False
                        moveRight = True
                    if event.key == K_UP or event.key == ord('w'):
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveUp = False
                        moveDown = True

                if event.type == KEYUP:
                    if event.key == ord('z'):
                        reverseCheat = False
                        score = 0
                    if event.key == ord('x'):
                        slowCheat = False
                        score = 0
                    if event.key == K_ESCAPE:
                            pygame.display.quit()
                            pygame.quit()
                            return points

                    if event.key == K_LEFT or event.key == ord('a'):
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveRight = False
                    if event.key == K_UP or event.key == ord('w'):
                        moveUp = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveDown = False

                if event.type == MOUSEMOTION:
                    playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

            if not reverseCheat and not slowCheat:
                baddieAddCounter += 1

            if baddieAddCounter == ADDNEWBADDIERATE_DODGER:
                baddieAddCounter = 0
                baddieSize = random.randint(BADDIEMINSIZE_DODGER, BADDIEMAXSIZE_DODGER)
                newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                            'speed': random.randint(BADDIEMINSPEED_DODGER, BADDIEMAXSPEED_DODGER),
                            'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                            }
                baddies.append(newBaddie)

            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE_DODGER, 0)
            if moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVERATE_DODGER, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE_DODGER)
            if moveDown and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE_DODGER)

            pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

            for b in baddies:
                if not reverseCheat and not slowCheat:
                    b['rect'].move_ip(0, b['speed'])
                elif reverseCheat:
                    b['rect'].move_ip(0, -5)
                elif slowCheat:
                    b['rect'].move_ip(0, 1)

            for b in baddies[:]:
                if b['rect'].top > WINDOWHEIGHT:
                    baddies.remove(b)

            windowSurface.fill(BACKGROUNDCOLOR_ORT)
            windowSurface.blit(playerImage, playerRect)

            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])

            pygame.display.update()

            if playerHasHitBaddie(playerRect, baddies):
                if score > topScore:
                    topScore = score
                break

            mainClock.tick(FPS_DODGER)

        pygame.display.update()
        waitForPlayerToPressKey()



def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH_MEM):
        revealedBoxes.append([val] * BOARDHEIGHT_MEM)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS_MEM:
        for shape in ALLSHAPES_MEM:
            icons.append( (shape, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH_MEM * BOARDHEIGHT_MEM / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH_MEM):
        column = []
        for y in range(BOARDHEIGHT_MEM):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE_MEM + GAPSIZE_MEM) + XMARGIN_MEM
    top = boxy * (BOXSIZE_MEM + GAPSIZE_MEM) + YMARGIN_MEM
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH_MEM):
        for boxy in range(BOARDHEIGHT_MEM):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE_MEM, BOXSIZE_MEM)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE_MEM * 0.25) # syntactic sugar
    half =    int(BOXSIZE_MEM * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE_MEM - half, BOXSIZE_MEM - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE_MEM - 1, top + half), (left + half, top + BOXSIZE_MEM - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE_MEM, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE_MEM - 1), (left + BOXSIZE_MEM - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE_MEM, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE_MEM, BOXSIZE_MEM))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE_MEM))
    pygame.display.update()
    FPSCLOCK.tick(FPS_MEM)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE_MEM, (-REVEALSPEED_MEM) - 1, -REVEALSPEED_MEM):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE_MEM + REVEALSPEED_MEM, REVEALSPEED_MEM):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH_MEM):
        for boxy in range(BOARDHEIGHT_MEM):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE_MEM, BOXSIZE_MEM))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE_MEM + 10, BOXSIZE_MEM + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH_MEM):
        for y in range(BOARDHEIGHT_MEM):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False
    return True

def Memory():
    global FPSCLOCK, DISPLAYSURF
    pygame.display.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    SetWindowPos = windll.user32.SetWindowPos
    SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 0x0001)

    mousex = 0
    mousey = 0
    pygame.display.set_caption('SMART MEMORY')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                points = 1000
                points = points + 10
                pygame.display.quit()
                pygame.quit()
                return points
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:

            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True
                if firstSelection == None:
                    firstSelection = (boxx, boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:

                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        startGameAnimation(mainBoard)
                    firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS_MEM)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        GAMEOVER = True

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        GAMEOVER = True
    return keyUpEvents[0].key

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH_NIBBLES - 1), 'y': random.randint(0, CELLHEIGHT_NIBBLES - 1)}

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE_NIBBLES
        y = coord['y'] * CELLSIZE_NIBBLES
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE_NIBBLES, CELLSIZE_NIBBLES)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE_NIBBLES - 8, CELLSIZE_NIBBLES - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)
        DISPLAYSURF.blit(IMAGEWORM, (x,y))

def drawApple(coord):
    x = coord['x'] * CELLSIZE_NIBBLES
    y = coord['y'] * CELLSIZE_NIBBLES
    appleRect = pygame.Rect(x, y, CELLSIZE_NIBBLES, CELLSIZE_NIBBLES)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    DISPLAYSURF.blit(IMAGEOBJ, (x,y))

def drawGrid():
    for x in range(0, WINDOWWIDTH_NIBBLES, CELLSIZE_NIBBLES): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT_NIBBLES))
    for y in range(0, WINDOWHEIGHT_NIBBLES, CELLSIZE_NIBBLES): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH_NIBBLES, y))

def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH_NIBBLES - 6)
    starty = random.randint(5, CELLHEIGHT_NIBBLES - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    playerQuit = False

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
                playerQuit=True
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    playerQuit=True

        if(playerQuit):
            break

        playerLoose = False
        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH_NIBBLES or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT_NIBBLES:
            playerLoose = True
            #return len(wormCoords)-3 # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                playerLoose = True
                #return len(wormCoords)-3 # game over

        if(playerLoose):
            break

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)

        pygame.display.update()
        FPSCLOCK.tick(FPS_NIBBLES)

    print("SALGO WHILE 1")

    points = len(wormCoords)-3

    if(playerLoose):

        playerWantsToQuit = False
        pygame.display.update()
        pygame.time.wait(500)
        checkForKeyPress() # clear out any key presses in the event queue

        while True:
            print("WHILE WAIT")
            if checkForKeyPress():
                for event in pygame.event.get(): # event handling loop
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        print("ENTRO ESCAPE")
                        pygame.display.quit()
                        pygame.quit()
                        playerWantsToQuit = True
                break

        return [points, playerWantsToQuit]

    if(playerQuit):
        return [points, True]

def Nibbles():
    global FPSCLOCK, DISPLAYSURF, GAMEOVER, IMAGEOBJ, IMAGEWORM

    pygame.display.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH_NIBBLES, WINDOWHEIGHT_NIBBLES))
    SetWindowPos = windll.user32.SetWindowPos
    SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 0x0001)
    IMAGEOBJ = pygame.image.load('Images/GamesPic/NibblesPic/objectiveADN.bmp')
    IMAGEWORM = pygame.image.load('Images/GamesPic/NibblesPic/wormPiece.bmp')
    GAMEOVER = False

    pygame.display.set_caption('SMART NIBBLES')

    while True:
        puntos = runGame()
        if(puntos[1]):
            return puntos[0]



def GameController(gamesManager):

    while(gamesManager[0]>=0):

        if(gamesManager[0] == 1):
            gamesManager[1] = Dodger()
            gamesManager[0] = 0

        if(gamesManager[0] == 2):
            gamesManager[2] = Memory()
            gamesManager[0] = 0

        if(gamesManager[0] == 3):
            gamesManager[3] = Nibbles()
            gamesManager[0] = 0

    print("PUNTOS DODGER: ", gamesManager[1])
    print("PUNTOS MEMORY: ", gamesManager[2])
    print("PUNTOS NIBBLES: ", gamesManager[3])
