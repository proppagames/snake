# Example file showing a basic pygame "game loop"
import pygame
import random
from collections import deque

screenWidth = 720
screenHeight = 720

grid = []
gridCellSize = 36
numRows = 20
numCols = 20

# maybe head is last element
# eating fruit inserts to front
playerParts = deque([(10, 8)])
playerDirX = 0
playerDirY = -1 
moveTime = 0.10 
moveTimer = moveTime 

fruitX = random.randint(0, numCols)
fruitY = random.randint(0, numRows)

gameOver = False

# TO DO:
# draw fruit which inserts to playerParts (make sure fruit doens't spawn on the snake)
# draw text to screen which shows your score (length of snake)
# make it possible to lose


def main():
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()
    running = True


    pygame.display.set_caption("Snake: 1")
    init()
    prevTime = 0
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w):
                    onPressW() 
                elif event.key == pygame.K_a:
                    onPressA()
                elif event.key == pygame.K_s:
                    onPressS()
                elif event.key == pygame.K_d:
                    onPressD()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        currTime = pygame.time.get_ticks()
        deltaTime = (currTime - prevTime) / 1000
        update(deltaTime)

        prevTime = pygame.time.get_ticks()
        # RENDER YOUR GAME HERE
        render(screen)

        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


def init():
    createGrid()

def createGrid():
    for i in range(numRows):
        row = []
        for j in range(numCols):
            x = (j * gridCellSize)
            y = (i * gridCellSize)
            tempRect = pygame.Rect(x, y, gridCellSize, gridCellSize)
            row.append(tempRect)
        grid.append(row.copy())

def update(deltaTime):
    if (gameOver == True):
        return

    global moveTimer

    if (moveTimer > 0):
        moveTimer -= deltaTime
    else:
        movePlayer()
        moveTimer = moveTime


def growSnake(prevTailPos):
    playerParts.appendleft(prevTailPos)
    score = len(playerParts)
    pygame.display.set_caption(f"Snake: {str(score)}") 
    # print("added snake tail")

def spawnFruit():
    global fruitX
    global fruitY

    fruitX = random.randint(0, numCols-1)
    fruitY = random.randint(0, numRows-1)
    while not fruitSpawnIsValid(fruitX, fruitY):
        fruitX = random.randint(0, numCols-1)
        fruitY = random.randint(0, numRows-1)

    # print("spawned new fruit at", fruitX, fruitY)

def fruitSpawnIsValid(fruitX, fruitY):
    for part in playerParts:
        if (fruitX, fruitY) == part:
            return False
    return True

def snakeContainsCell(x, y):
    for i in range(len(playerParts)-1):
        if (x, y) == playerParts[i]:
            return True
    return False

def movePlayer():
    global playerCol
    global playerRow
    global gameOver

    prevTailPos = (playerParts[0][0], playerParts[0][1])
    # print("start player parts", playerParts)
    for i in range(len(playerParts)-1):
        # print("prev location: ", part)
        nextPart = playerParts[i+1]
        playerParts[i] = (nextPart[0], nextPart[1])
        # print("player parts", playerParts)
        # print("next location: ", part)
    
    playerParts[-1] = (playerParts[-1][0] + playerDirX, playerParts[-1][1] + playerDirY)

    playerHead = playerParts[-1]

    if snakeContainsCell(playerHead[0], playerHead[1]):
        score = len(playerParts)
        pygame.display.set_caption(f"Snake: {str(score)} - Game Over") 
        gameOver = True

    if not bounded(playerHead[0], playerHead[1]):
        score = len(playerParts)
        pygame.display.set_caption(f"Snake: {str(score)} - Game Over") 
        gameOver = True

    # print("FruitX and Y", fruitX, fruitY)
    if (playerHead[0] == fruitX and playerHead[1] == fruitY):
        growSnake(prevTailPos)
        spawnFruit() 

def bounded(x, y):
    return (0 <= x < numCols and 0 <= y < numRows)

def onPressW():
    global playerDirX
    global playerDirY

    if (playerDirY == 1):
        return;
    playerDirX = 0
    playerDirY = -1

def onPressA():
    global playerDirX
    global playerDirY
    if (playerDirX == 1):
        return;
    playerDirX = -1
    playerDirY = 0

def onPressS():
    global playerDirX
    global playerDirY

    if (playerDirY == -1):
        return;
    playerDirX = 0
    playerDirY = 1

def onPressD():
    global playerDirX
    global playerDirY

    if (playerDirX == -1):
        return;
    playerDirX = 1
    playerDirY = 0

def render(screen):
    myrectangle = pygame.Rect(0, 0, 50, 50)
    pygame.draw.rect(screen, "blue", myrectangle)

    renderGrid(screen)
    renderPlayer(screen)
    renderFruit(screen)


    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render("HELLO WORLD", True, "orange", "red")

    textRect = text.get_rect()
    textRect.center = (50, 50)
    # flip() the display to put your work on screen

def renderGrid(screen):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            color = pygame.Color(70, 70, 70) 
            if (i % 2 == 0) and (j % 2 == 0):
                color = pygame.Color(100, 100, 100)
            elif (i % 2 == 1) and (j % 2 == 1):
                color = pygame.Color(100,  100, 100)

            pygame.draw.rect(screen, color, grid[i][j])

def renderPlayer(screen):
    for i in range(len(playerParts)-1):
        playerRect = pygame.Rect(playerParts[i][0] * gridCellSize, playerParts[i][1] * gridCellSize, gridCellSize, gridCellSize)
        pygame.draw.rect(screen, "yellow", playerRect)

    playerRect = pygame.Rect(playerParts[-1][0] * gridCellSize, playerParts[-1][1] * gridCellSize, gridCellSize, gridCellSize)
    pygame.draw.rect(screen, "yellow", playerRect)

def renderFruit(screen):
    fruitRect = pygame.Rect(fruitX * gridCellSize, fruitY * gridCellSize, gridCellSize, gridCellSize)
    pygame.draw.rect(screen, "red", fruitRect)

main()