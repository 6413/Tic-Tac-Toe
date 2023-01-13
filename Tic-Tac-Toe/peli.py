import pygame, sys, math
from math import *
from pygame.locals import *
from random import seed
from random import randint
import time

# palauttaa totuusarvon jos hiiri on neliön sisällä
def mouse_inside(position, size):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x > position[0] and mouse_x < position[0] + size[0] and mouse_y > position[1] and mouse_y < position[1] + size[1]: 
        return True
    else:
        return False

def left_click():
    return pygame.mouse.get_pressed()[0]

# alustaa pygame kirjaston
pygame.init()

#ikkunoiden leveys ja korkeus, HUOM!! älä vaihda näitä arvoja, koska sijainteja laskiessa ei ole otettu huomioon ikkunan koko
WIDTH = 900
HEIGHT = 900

ALOITA_SOUND = "aloita_peli.wav"
GAMEMODE_SOUND = "peli_alkaa.wav"
PLACE_SOUND = "place.wav"
LOPETUS_SOUND = "lopetus.wav"
BACKGROUND_SOUND = "background.wav"


# päävalikon otsikot
GAME_TITLE = "RISTINOLLAPELI"
ALOITA_PELI = "Aloita peli"
JATKA_PELI = "Jatka peliä"
LOPETA_PELI = "Lopeta peli"
YKSINPELI = "Yksinpeli"
KAKSINPELI = "Kaksinpeli"

RISTI_VOITTI = "Risti voitti!"
NOLLA_VOITTI = "Nolla voitti!"
TASAPELI = "Tasapeli"
PALAA_VALIKKOON = "Palaa päävalikkoon"

# päävalikon äänet päälle/pois valinta
image_volume_on = pygame.image.load("volume_on.png")
image_volume_off = pygame.image.load("volume_off.png")

VOLUME_SIZE = (100, 100)
VOLUME_POSITION = (WIDTH - VOLUME_SIZE[0], HEIGHT - VOLUME_SIZE[1])

image_volume_on = pygame.transform.scale(image_volume_on, VOLUME_SIZE)
image_volume_off = pygame.transform.scale(image_volume_off, VOLUME_SIZE)

#toistaa voitto äänen kerran
play_sound_once = True

volume_on = True

#peli-ikkuna
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption(GAME_TITLE)

#tekstin fontin koko
FONT_SIZE = 36
MEDIUM_FONT_SIZE = int(FONT_SIZE * 1.5)
BIG_FONT_SIZE = FONT_SIZE * 2

#luodaan fontti FONT_SIZE muuttujan arvon kooksi
default_font = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", FONT_SIZE)
font = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", FONT_SIZE)
medium_font = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", MEDIUM_FONT_SIZE)
big_font = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", BIG_FONT_SIZE)

# funktio tekstin renderöintiin
def render_text(font, text, position, color):
    window.blit(font.render(text, True, color), (int(position[0]), int(position[1])))
                                                    #^ muutetaan float intiksi, koska warning
# yleisiä väri muuttujia
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)   
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

VICTORY_COLOR = [138, 0, 133]

#pygame.mouse.set_visible(False)

# päävalikon tekstien sijainnit ja koot
ALOITAPELI_TEXT_SIZE = default_font.size(ALOITA_PELI)
ALOITAPELI_POSITION = (WIDTH * 0.15, HEIGHT * 0.3)

JATKA_PELI_TEXT_SIZE = default_font.size(JATKA_PELI)
JATKA_PELI_POSITION = ALOITAPELI_POSITION

LOPETAPELI_TEXT_SIZE = default_font.size(LOPETA_PELI)
LOPETAPELI_POSITION = (WIDTH * (1 - 0.15) - LOPETAPELI_TEXT_SIZE[0], HEIGHT * 0.3)

GAME_TITLE_TEXT_SIZE = font.size(GAME_TITLE)
GAME_TITLE_POSITION = (WIDTH / 2 - GAME_TITLE_TEXT_SIZE[0] / 2, HEIGHT * 0.1)

RISTI_VOITTI_TEXT_SIZE = big_font.size(RISTI_VOITTI)
RISTI_VOITTI_POSITION = (WIDTH / 2 - RISTI_VOITTI_TEXT_SIZE[0] / 2, HEIGHT * 0.1)

NOLLA_VOITTI_TEXT_SIZE = big_font.size(NOLLA_VOITTI)
NOLLA_VOITTI_POSITION = (WIDTH / 2 - NOLLA_VOITTI_TEXT_SIZE[0] / 2, HEIGHT * 0.1)

TASAPELI_TEXT_SIZE = big_font.size(TASAPELI)
TASAPELI_POSITION = (WIDTH / 2 - TASAPELI_TEXT_SIZE[0] / 2, HEIGHT * 0.1)

PALAA_VALIKKOON_TEXT_SIZE = medium_font.size(PALAA_VALIKKOON)
PALAA_VALIKKOON_POSITION = (WIDTH / 2 - PALAA_VALIKKOON_TEXT_SIZE[0] / 2, HEIGHT / 2 - PALAA_VALIKKOON_TEXT_SIZE[1] / 2)

YKSINPELI_TEXT_SIZE = default_font.size(YKSINPELI)
YKSINPELI_POSITION = (WIDTH / 2 - YKSINPELI_TEXT_SIZE[0] / 2, HEIGHT / 2 + HEIGHT * -0.1)

KAKSINPELI_TEXT_SIZE = default_font.size(KAKSINPELI)
KAKSINPELI_POSITION = (WIDTH / 2 - KAKSINPELI_TEXT_SIZE[0] / 2, HEIGHT / 2 + HEIGHT * 0.1)

#muuuttuja joka kertoo, että renderöidäänkö päävalikko
render_main_menu = True

class gamemode:
    SINGLEPLAYER, MULTIPLAYER = range(0, 2)

render_gamemode_select = False
single_or_multiplayer = gamemode.SINGLEPLAYER

def play_sound(sound):
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound))

# pelikäynnissä-funktio
def game_is_on():
    global cross_positions
    global circle_positions

    return len(cross_positions) or len(circle_positions)

bot_delay = 0

#päävalikko-funktio
def main_menu():
    global render_main_menu
    global GAMEMODE_SOUND
    global render_gamemode_select

    render_text(default_font, GAME_TITLE, GAME_TITLE_POSITION, WHITE)
    if game_is_on(): # peli käynnissä valikko
        render_text(default_font, JATKA_PELI, JATKA_PELI_POSITION, WHITE)
        if mouse_inside(JATKA_PELI_POSITION, JATKA_PELI_TEXT_SIZE) and action:
            if volume_on:
                play_sound(ALOITA_SOUND)
            render_main_menu = False    
    else:
        render_text(default_font, ALOITA_PELI, ALOITAPELI_POSITION, WHITE) 
        #jos klikkaa hiirellä "Aloita peli" -nappia, aloittaa pelin 
        if mouse_inside(ALOITAPELI_POSITION, ALOITAPELI_TEXT_SIZE) and action:
            if volume_on:
                play_sound(ALOITA_SOUND)
            render_main_menu = False
            render_gamemode_select = True

    render_text(default_font, LOPETA_PELI, LOPETAPELI_POSITION, WHITE)

    #jos klikkaa hiirellä "Lopeta peli" -nappia, lopettaa pelin
    if mouse_inside(LOPETAPELI_POSITION, LOPETAPELI_TEXT_SIZE) and mouse_down:
        pygame.quit()

player_turn = 0

# yksin- tai kaksinpeli valikko
def single_multiplayer(action):
    global single_or_multiplayer
    global render_gamemode_select
    global bot_delay
    global player_turn

    render_text(default_font, YKSINPELI, YKSINPELI_POSITION, WHITE)
    render_text(default_font, KAKSINPELI, KAKSINPELI_POSITION, WHITE)
    if (mouse_inside(YKSINPELI_POSITION, YKSINPELI_TEXT_SIZE) and action): # valitsee joko yksin- tai kaksinpelin painaessa
        single_or_multiplayer = gamemode.SINGLEPLAYER
        render_gamemode_select = False
        bot_delay = int(round(time.time() * 1000))
        player_turn = randint(0, 1)
        if volume_on:
            play_sound(GAMEMODE_SOUND)
    elif(mouse_inside(KAKSINPELI_POSITION, KAKSINPELI_TEXT_SIZE) and action):
        single_or_multiplayer = gamemode.MULTIPLAYER
        render_gamemode_select = False
        if volume_on:
            play_sound(GAMEMODE_SOUND)
    

game_finished = False

def finished_game(found):
    global play_sound_once
    global cross_or_circle
    global cross
    global circle
    global game_finished
    global render_main_menu
    global player_map
    global player_turn

    render_text(medium_font, PALAA_VALIKKOON, PALAA_VALIKKOON_POSITION, WHITE)
    if play_sound_once and volume_on:
        play_sound(LOPETUS_SOUND)
        play_sound_once = False
    if mouse_inside(PALAA_VALIKKOON_POSITION, PALAA_VALIKKOON_TEXT_SIZE) and action:
        player_map.clear()
        player_map = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        circle_positions.clear()
        cross_positions.clear()
        game_finished = False
        render_main_menu = True
        cross_or_circle = False
        play_sound_once = True

#ms
BOT_MOVE_TIME = 750

# yksinpeli
def singleplayer(action, cross_positions, circle_positions):
    # tarvittavat muuttujat globalista
    global cross_or_circle
    global cross
    global circle
    global game_finished
    global render_main_menu
    global player_map
    global player_turn
    global bot_delay

    # timer joka tauottaa botin siirrot
    timer_finished = (int(round(time.time() * 1000)) - bot_delay) > BOT_MOVE_TIME

    render_image(image_wallpaper, (0, 0))
    grid_pos = (0, 0)
    coordinate = (0, 0)
    grid_pos = (0, 0)
    
    # lasketaan sijainnit ristille ja nollalle
    if player_turn and not(game_finished):
        grid_pos = (floor(mouse_position[0] / (WIDTH / 3)) + 1, floor(mouse_position[1] / (WIDTH / 3)) + 1)
        coordinate = grid_to_coordinate(grid_pos)
        grid_pos = (grid_pos[0] - 1, grid_pos[1] - 1)
    elif not(game_finished) and timer_finished:
        random_ = (randint(0, 2), randint(0, 2))
        while player_map[random_[1]][random_[0]]:
            random_ = (randint(0, 2), randint(0, 2))
        grid_pos = random_
        coordinate = grid_to_coordinate((grid_pos[0] + 1, grid_pos[1] + 1))

    coordinate_selected = (coordinate[0] != 0 and coordinate[1] != 0)

    # muuttuja joka katsoo onko paikka viety
    found = False
    if player_map[grid_pos[1]][grid_pos[0]]:
        found = True

    if (action and not(game_finished)) or (not(player_turn) and not(game_finished) and timer_finished):
        if not(found) and coordinate_selected:
            # lisää ristin ja nollan listaan graafista piirtoa varten
            if not(cross_or_circle):
                cross_positions.append(coordinate)
            else:
                circle_positions.append(coordinate)

    # piirtää ristin ja nollan ruudulle
    for i in cross_positions:
        render_image(cross, i)
    for i in circle_positions:
        render_image(circle, i)

    # risti tai nolla joka näyttää minne kohtaan risti tai nolla laitetaan
    if not(cross_or_circle) and not(found) and not(game_finished) and player_turn:
        render_image(cross, coordinate)
    elif not(found) and not(game_finished) and player_turn:
        render_image(circle, coordinate)

    if action or (not(player_turn) and timer_finished) and coordinate_selected:
        if not(player_map[grid_pos[1]][grid_pos[0]]) and coordinate[0] and coordinate[1]:
            # varaa paikan ristille tai nollalle pelikentältä
            if not(cross_or_circle):
                player_map[grid_pos[1]][grid_pos[0]] = 1
            else:
                player_map[grid_pos[1]][grid_pos[0]] = 2

    if not(found) and not(game_finished) and coordinate_selected:
        # vaihtaa vuorotellen ristin ja nollan välillä
        if action or (not(player_turn) and timer_finished):
            cross_or_circle = not(cross_or_circle)

    # katsoo onko joku voittanut tai onko tasapeli
    state = get_board_state(player_map)
    if state == 1:
        render_text(big_font, RISTI_VOITTI, RISTI_VOITTI_POSITION, VICTORY_COLOR)
        game_finished = True
    elif state == 2:
        render_text(big_font, NOLLA_VOITTI, NOLLA_VOITTI_POSITION, VICTORY_COLOR)
        game_finished = True
    elif state == 3:
        render_text(big_font, TASAPELI, TASAPELI_POSITION, VICTORY_COLOR)
        game_finished = True
        
    # Pelin päätyttyä palaa pelivalikkoon
    if game_finished:
        finished_game(found)
    elif not(found):
        if action and volume_on and not(game_finished) and player_turn:
           play_sound(PLACE_SOUND)
        elif not(player_turn) and volume_on and not(game_finished) and timer_finished:
            play_sound(PLACE_SOUND)
    if not(found):
        if action and player_turn and not(game_finished) and coordinate_selected:
            player_turn = not(player_turn)
            bot_delay = int(round(time.time() * 1000))
        elif not(player_turn) and timer_finished  and not(game_finished):
            player_turn = True

def multiplayer(action, cross_positions, circle_positions):
    global cross_or_circle
    global cross
    global circle
    global game_finished
    global render_main_menu
    global player_map
    global play_sound_once

    render_image(image_wallpaper, (0, 0))
    grid_pos = (floor(mouse_position[0] / (WIDTH / 3)) + 1, floor(mouse_position[1] / (WIDTH / 3)) + 1)
    coordinate = grid_to_coordinate(grid_pos)
    grid_pos = (grid_pos[0] - 1, grid_pos[1] - 1)
    found = False
    if player_map[grid_pos[1]][grid_pos[0]]:
        found = True
    if action and not(game_finished):
        if not(found):
            if not(cross_or_circle):
                cross_positions.append(coordinate)
            else:
                circle_positions.append(coordinate)
    
    #risti ja ympyrän sijainnit ruudukossa
    for i in cross_positions:
        render_image(cross, i)
    for i in circle_positions:
        render_image(circle, i)
    
    #Jos ruutu on tyhjä, varaa sen joko X- tai O-vuorolle 
    if not(cross_or_circle) and not(found) and not(game_finished):
        render_image(cross, coordinate)
    elif not(found) and not(game_finished):
        render_image(circle, coordinate)

    if action:
        if not(player_map[grid_pos[1]][grid_pos[0]]):
             # varaa paikan ristille tai nollalle pelikentältä
            if not(cross_or_circle):
                player_map[grid_pos[1]][grid_pos[0]] = 1
            else:
                player_map[grid_pos[1]][grid_pos[0]] = 2
    
    if not(found):
        if action:
            cross_or_circle = not(cross_or_circle)

    # katsoo onko joku voittanut tai onko tasapeli
    state = get_board_state(player_map)
    if state == 1:
        render_text(big_font, RISTI_VOITTI, RISTI_VOITTI_POSITION, VICTORY_COLOR)
        game_finished = True
    elif state == 2:
        render_text(big_font, NOLLA_VOITTI, NOLLA_VOITTI_POSITION, VICTORY_COLOR)
        game_finished = True
    elif state == 3:
        render_text(big_font, TASAPELI, TASAPELI_POSITION, VICTORY_COLOR)
        game_finished = True
        
    # Pelin päätyttyä palaa pelivalikkoon
    if game_finished:
        finished_game(found)
    elif not(found):
        if action and volume_on and not(game_finished):
            play_sound(PLACE_SOUND)
        

# katsotaan kumpi pelimuoto on valittu ja täten valitaan kumpaan pelimuotoon mennään
def game(action, cross_positions, circle_positions):
    if single_or_multiplayer == gamemode.SINGLEPLAYER:
        singleplayer(action, cross_positions, circle_positions)
    elif single_or_multiplayer == gamemode.MULTIPLAYER:
        multiplayer(action, cross_positions, circle_positions)

# 0 ei tasapeliä tai voittoa, 1 risti voittaa, 2 nolla voittaa, 3 tasapeli
def get_board_state(player_map):
    for x in range(1, 3):
        for i in range(0, 3):
            if player_map[i][0] == x and player_map[i][1] == x and player_map[i][2] == x:
                return x
            if player_map[0][i] == x and player_map[1][i] == x and player_map[2][i] == x:
                return x

        if player_map[0][0] == x and player_map[1][1] == x and player_map[2][2] == x:
            return x
        if player_map[0][2] == x and player_map[1][1] == x and player_map[2][0] == x:
            return x
    
    for l in player_map:
        for i in l:
            if not(i):
                return 0
    return 3

#funktio, joka piirtää kuvan ruudulle
def render_image(image,position):
    window.blit(image, (int(position[0]), int(position[1])))

image_main_menu = pygame.image.load("main_menu.png")
image_main_menu = pygame.transform.scale(image_main_menu, (WIDTH, HEIGHT))

image_wallpaper = pygame.image.load("pelikentta.png")
image_wallpaper = pygame.transform.scale(image_wallpaper, (WIDTH, HEIGHT))

GRID_LINE_SIZE = (int(WIDTH / (900 / 31)), int(HEIGHT / (900 / 31)))

GRID_SIZE = 260
GRID_LINE_SIZE = 30
PLAYER_SIZE = (200, 200)

def grid_to_coordinate(position):
    global GRID_SIZE
    global GRID_LINE_SIZE
    global PLAYER_SIZE
    # shape-muuttujiin tulee taulukon keskipisteet
    shape_x = GRID_LINE_SIZE * position[0] + (GRID_SIZE * (position[0] - 1) + ((GRID_SIZE / 2) * 1) - PLAYER_SIZE[0] / 2)
    shape_y = GRID_LINE_SIZE * position[1] + (GRID_SIZE * (position[1] - 1) + ((GRID_SIZE / 2) * 1) - PLAYER_SIZE[1] / 2)

    return [shape_x, shape_y]

circle = pygame.image.load("circle.png")
circle = pygame.transform.scale(circle, PLAYER_SIZE)

cross = pygame.image.load("cross.png")
cross = pygame.transform.scale(cross, PLAYER_SIZE)

cross_or_circle = False

#moniulotteinen lista ruudukosta
player_map = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
cross_positions = []
circle_positions = []

mouse_down = False

#muuttuja joka ottaa vain yhden vasemman hiiren painalluksen
action = False

pygame.mixer.Channel(1).play(pygame.mixer.Sound(BACKGROUND_SOUND), -1)

while True:
    #ikkunan taustaväri
    window.fill(WHITE)

    if (left_click() and not(mouse_down)):
        action = True
        mouse_down = True
        
    #print(left_click(), action)
    #tallentaa hiiren x ja y koordinaatin mouse_position muuttujaan
    mouse_position = pygame.mouse.get_pos()
    #lisää näppäimistön painallukset keys muuttujaan
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        render_main_menu = True

    # lukee sekä hiiren että näppäimistön tapahtumia esim. painalluksia
    for event in pygame.event.get():
        if event.type == QUIT: # ohjelman lopettamis toiminto
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

    if render_main_menu: #renderöidään päävalikko jos muuttuja niin sallii
        render_image(image_main_menu, (0, 0))
        main_menu()
    elif render_gamemode_select:
        render_image(image_main_menu, (0, 0))
        single_multiplayer(action)
    else:
        game(action, cross_positions, circle_positions)
    #renderöi main menuun äänet päällä/pois kuvan
    if render_main_menu:
        if volume_on:
            render_image(image_volume_on, VOLUME_POSITION)
        else:
            render_image(image_volume_off, VOLUME_POSITION)

        if mouse_inside(VOLUME_POSITION + VOLUME_SIZE, VOLUME_SIZE) and action:
            volume_on = not(volume_on)
            if volume_on:
                pygame.mixer.Channel(1).unpause()
            else:
                pygame.mixer.Channel(1).pause()
    
    action = False

    pygame.display.update()