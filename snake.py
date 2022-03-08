import pygame
import pygame.freetype
import random

#Variables and constants
FPS =  75
UNIT_SIZE = 25
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

xDirection = 1
yDirection = 0

foodX = 0
foodY = 0

score = 0
scoreText = "0"

run = False

#initial snake values
bodyParts = 5
snake = [
    {"x": UNIT_SIZE*4, "y": 0}, #head index 0
    {"x": UNIT_SIZE*3, "y": 0},
    {"x": UNIT_SIZE*2, "y": 0},
    {"x": UNIT_SIZE*1, "y": 0},
    {"x": UNIT_SIZE*0, "y": 0}  #tail index 5
]


pygame.init()

SCORE_FONT = pygame.freetype.SysFont('Comic Sans MS', 30)
GAME_OVER_FONT = pygame.freetype.SysFont('Comic Sans MS', 70)
RESET_FONT = pygame.freetype.SysFont('Comic Sans MS', 20)

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake in Python")


#methods
def startGame():
    global xDirection
    global yDirection

    xDirection = 1
    yDirection = 0

    newFood()
    gameLoop()

def newFood():

    global foodX
    global foodY

    foodY = random.randint(0, SCREEN_HEIGHT / UNIT_SIZE) * UNIT_SIZE
    foodX = random.randint(0, SCREEN_WIDTH / UNIT_SIZE) * UNIT_SIZE

    #Prevents food from spawning offscreen
    if foodX >= SCREEN_WIDTH:
        foodX -= UNIT_SIZE
    if foodY >= SCREEN_HEIGHT:
        foodY -= UNIT_SIZE

def drawFood():
    color = (255, 0, 0)
    pygame.draw.rect(window, color, pygame.Rect(foodX, foodY, UNIT_SIZE, UNIT_SIZE))
    

def drawSnake():
    for i in range(bodyParts):
        color = (0, 255, 0)
        pygame.draw.rect(window, color, pygame.Rect(snake[i]["x"], snake[i]["y"], UNIT_SIZE, UNIT_SIZE))

def moveSnake(xDir, yDir):
    
    global bodyParts
    global score
    global scoreText

    #moving the head of the snake
    snake.insert(0, {"x": (snake[0]["x"] + (xDir * UNIT_SIZE)), "y": (snake[0]["y"] + (yDir * UNIT_SIZE))})

    #if the snake eats food
    if snake[0]["x"] == foodX and snake[0]["y"] == foodY:
        score += 1
        scoreText = str(score)
        bodyParts += 1
        newFood()

    for i in range(bodyParts):
        if i == bodyParts:
            snake.pop(i)

def getDirection(key):
    #user input
    global xDirection
    global yDirection

    if key == pygame.K_w or key == pygame.K_UP:
        if yDirection != 1:
            yDirection = -1
            xDirection = 0
    elif key == pygame.K_s or key == pygame.K_DOWN:
        if yDirection != -1:
            yDirection = 1
            xDirection = 0
    elif key == pygame.K_a or key == pygame.K_LEFT:
        if xDirection != 1:
            xDirection = -1
            yDirection = 0
    elif key == pygame.K_d or key == pygame.K_RIGHT:
        if xDirection != -1:
            xDirection = 1
            yDirection = 0

def checkGameOver():
    
    if snake[0]["x"] >= SCREEN_WIDTH or snake[0]["x"] < 0 or snake[0]["y"] >= SCREEN_HEIGHT or snake[0]["y"] < 0:
        return False

    for i in range(bodyParts):
        if i != 0:
            if snake[0]["x"] == snake[i]["x"] and snake[0]["y"] == snake[i]["y"]:
                return False
    #if no game over occurs
    return True

def gameOver():

    global xDirection, yDirection, score, scoreText, snake, bodyParts

    window.fill((0,0,0))

    SCORE_FONT.render_to(window, (SCREEN_WIDTH/2 - 80, 10), "Final Score: "+scoreText, (0, 150, 255))
    GAME_OVER_FONT.render_to(window, (50, SCREEN_HEIGHT/2 - 20), "GAME OVER!", (255, 0, 50))
    RESET_FONT.render_to(window, (130, SCREEN_HEIGHT/2 + 75), "Press any key to restart", (0, 150, 255))

    pygame.display.update()

    resetCheck = True
    while resetCheck:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                resetCheck = False
                break
            elif event.type == pygame.KEYDOWN:

                #resetting to default values

                xDirection = 1
                yDirection = 0

                score = 0
                scoreText = "0"

                bodyParts = 5

                snake = [
                    {"x": UNIT_SIZE*4, "y": 0}, #head index 0
                    {"x": UNIT_SIZE*3, "y": 0},
                    {"x": UNIT_SIZE*2, "y": 0},
                    {"x": UNIT_SIZE*1, "y": 0},
                    {"x": UNIT_SIZE*0, "y": 0}  #tail index 5
                ]

                startGame()
                resetCheck = False
    


def gameLoop():

    global run

    #Game loop
    run = True
    while run:
        #resets window
        window.fill((0,0,0))

        #looks through events
        for event in pygame.event.get():
            #quits game
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                getDirection(event.key)

        if checkGameOver() == False:
            run = False
            gameOver()

        moveSnake(xDirection, yDirection)
        drawSnake()
        drawFood()

        SCORE_FONT.render_to(window, (SCREEN_WIDTH/2 - 60, 10), "Score: "+scoreText, (0, 150, 255))

        pygame.display.update()

        pygame.time.wait(int(FPS))

#testing
startGame()

pygame.quit()