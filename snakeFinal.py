"""
This is the final program for Jack's Intermediate Python Class. This program uses pygame to replicate the classic game
of snake with a few additional features such as sound effects, music, and image files. Hope you enjoy!
"""

import pygame  # Import statements
import random
import time

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()  # Initializes pygame and its music mixer

# Creating the display screen
screen_width, screen_height = 600, 400
background_image_size = (600, 400)  # Setting dimensions for later image scaling

# Creating colors to be used in-game in following lines
red = (136, 8, 8)
green = (57, 255, 20)
blue = (135, 206, 235)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (191, 64, 191)

# Initializes the display
display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jack\'s Intermediate Python Snake Game :D")

# Setting the game's font
font_style = pygame.font.SysFont("Ariel", 25)
score_font = pygame.font.SysFont("Corbel", 35)

# Creating the game clock
game_clock = pygame.time.Clock()

# Creating snake blocks and setting snake's movement speed
block = 10
snake_speed = 15


def snake(snake_block, snake_list):  # Draws the snake
    for x in snake_list:
        pygame.draw.rect(display, green, [x[0], x[1], snake_block, snake_block])


def message(msg, color):  # Function that when called displays a message to the user
    message_display = font_style.render(msg, True, color)
    message_rect = message_display.get_rect(center=(screen_width / 2, screen_height / 2))
    display.blit(message_display, message_rect)


def player_Score(score):  # Displays the player's score adjusting as they progress through the game
    points = score_font.render("Your Score: " + str(score), True, purple)
    display.blit(points, [0, 0])


def gameplay_music():  # Plays bloons music while the user plays the game to create a jungle theme
    pygame.mixer.music.load('Main Theme - Bloons TD 5.wav')
    pygame.mixer.music.play(-1)


def game_background():  # Generates a forest background to immerse the player in the jungle theme
    forest_backdrop = pygame.image.load('N_b6N3.png')
    forest_backdrop = pygame.transform.scale(forest_backdrop, background_image_size)
    display.blit(forest_backdrop, (0, 0))


def lose_screen():  # Changes the background image and displays game over message
    loss_image = pygame.image.load('cryingEmoji.jpg')
    loss_image = pygame.transform.scale(loss_image, background_image_size)
    display.blit(loss_image, (0, 0))
    message("Game Over! You can Play Again (C) or Close the Game (X).", purple)


def lose_sound():  # Plays a sound effect whenever the player loses the game
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(pygame.mixer.Sound('6f8d9670-7510-11ed-af8f-8f836243a50f.wav'), 0)


def gameplay_loop():  # Main loop that handles gameplay, the snake, and interaction between the snake and its food
    gameplay_music()

    close_Game = False
    game_Over = False

    snake_list = []  # Creates list to contain all the parts of the snake's body as it grows and sets its length to 1
    snake_length = 1

    x_value, y_value = screen_width / 2, screen_height / 2  # Sets snake's start position to middle of the screen

    change_in_x, change_in_y = 0, 0

    # Generates food in random position on the screen
    food_x_pos = round(random.randrange(0, screen_width - block) / 10.0) * 10.0
    food_y_pos = round(random.randrange(0, screen_height - block) / 10.0) * 10.0

    while not close_Game:
        game_background()

        while game_Over:  # While the user has lost the game and has yet to restart

            lose_screen()  # Display game over message, show user their score, update display
            player_Score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:  # If the user presses X, the game closes
                        game_Over = False
                        close_Game = True
                    if event.key == pygame.K_c:  # If the user presses C, the game starts again
                        gameplay_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_Game = True
            if event.type == pygame.KEYDOWN:  # Handles snake's directional changes based off user input
                if event.key == pygame.K_RIGHT:
                    change_in_x = block
                    change_in_y = 0
                if event.key == pygame.K_LEFT:
                    change_in_x = -block
                    change_in_y = 0
                if event.key == pygame.K_DOWN:
                    change_in_x = 0
                    change_in_y = block
                if event.key == pygame.K_UP:
                    change_in_x = 0
                    change_in_y = -block

        x_value += change_in_x  # Changes x and y values based off position of snake
        y_value += change_in_y
        pygame.draw.rect(display, red, [food_x_pos, food_y_pos, block, block])  # Draw's food blocks
        snake_head = [x_value, y_value]
        snake_list.append(snake_head)

        if x_value == food_x_pos and y_value == food_y_pos:  # If snake collides with food, move food to a new position
            food_x_pos = round(random.randrange(0, screen_width - block) / 10.0) * 10.0
            food_y_pos = round(random.randrange(0, screen_height - block) / 10.0) * 10.0
            snake_length += 1

        if len(snake_list) > snake_length:  # Deletes last snake block if list of snake blocks is > length of the snake
            del snake_list[0]
            if len(snake_list) < snake_length:  # Test case that closes program if snake_list is working improperly
                break

        for x in snake_list[:-1]:  # If snake's head collides with its body, game over
            if x == snake_head:
                lose_sound()
                game_Over = True

        # If snake leaves game boundaries, game over
        if x_value >= screen_width or x_value < 0 or y_value >= screen_height or y_value < 0:
            lose_sound()
            game_Over = True
            if game_Over is not True:  # Test case that closes program if boundaries work improperly
                break

        snake(block, snake_list)  # Draws snake
        player_Score(snake_length - 1)  # Displays the player's score

        game_clock.tick(15)  # Sets the movement speed of the snake

        pygame.display.update()

    pygame.quit()
    quit()


gameplay_loop()
