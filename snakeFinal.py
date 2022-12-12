"""
This is the final program for Jack's Intermediate Python Class. This program uses pygame to replicate the classic game
of snake with a few additional features such as sound effects, music, and image files. Hope you enjoy!
"""

import pygame  # Import statements
import random
from pygame import time

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()  # Initializes pygame and its music mixer

# Creating the display screen
screen_width = 600
screen_height = 400

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
snake_block = 10
snake_speed = 15

background_image_size = (600, 400)


# Creating the snake
def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, green, [x[0], x[1], snake_block, snake_block])


# Keeps track of the players score as they progress through the game
def player_Score(score):
    points = score_font.render("Your Score: " + str(score), True, purple)
    display.blit(points, [0, 0])


# Creates a display message for the player
def message(msg, color):
    message_display = font_style.render(msg, True, color)
    message_rect = message_display.get_rect(center=(screen_width / 2, screen_height / 2))
    display.blit(message_display, message_rect)


def gameplay_music():
    pygame.mixer.music.load('Main Theme - Bloons TD 5.wav')
    pygame.mixer.music.play(-1)


def game_background():
    forest_backdrop = pygame.image.load('N_b6N3.png')
    forest_backdrop = pygame.transform.scale(forest_backdrop, background_image_size)
    display.blit(forest_backdrop, (0, 0))


def lose_screen():
    loss_image = pygame.image.load('cryingEmoji.jpg')
    loss_image = pygame.transform.scale(loss_image, background_image_size)
    display.blit(loss_image, (0, 0))
    message("Game Over! You can Play Again (C) or Close the Game (X).", purple)


def lose_sound():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(pygame.mixer.Sound('6f8d9670-7510-11ed-af8f-8f836243a50f.wav'), 0)


# Loop that handles gameplay and the interactions between the player, the snake, and the snake's food
def gameplay_loop():
    gameplay_music()

    close_Game = False
    game_Over = False

    snake_list = []
    snake_length = 1

    x_value = screen_width / 2
    y_value = screen_height / 2

    change_in_x = 0
    change_in_y = 0

    food_x_pos = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    food_y_pos = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    while not close_Game:

        while game_Over:

            lose_screen()
            player_Score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        game_Over = False
                        close_Game = True
                    if event.key == pygame.K_c:
                        gameplay_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_Game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change_in_x = snake_block
                    change_in_y = 0
                if event.key == pygame.K_LEFT:
                    change_in_x = -snake_block
                    change_in_y = 0
                if event.key == pygame.K_DOWN:
                    change_in_x = 0
                    change_in_y = snake_block
                if event.key == pygame.K_UP:
                    change_in_x = 0
                    change_in_y = -snake_block

        if x_value >= screen_width or x_value < 0 or y_value >= screen_height or y_value < 0:
            lose_sound()
            game_Over = True
        x_value += change_in_x
        y_value += change_in_y
        game_background()
        pygame.draw.rect(display, red, [food_x_pos, food_y_pos, snake_block, snake_block])
        snake_head = [x_value, y_value]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        if game_Over:
            lose_sound()

        for x in snake_list[:-1]:
            if x == snake_head:  # If the snake's head is colliding with its body you lose
                lose_sound()
                game_Over = True

        snake(snake_block, snake_list)
        player_Score(snake_length - 1)

        pygame.display.update()

        if x_value == food_x_pos and y_value == food_y_pos:
            food_x_pos = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            food_y_pos = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        game_clock.tick(snake_speed)

    pygame.quit()
    quit()


gameplay_loop()
