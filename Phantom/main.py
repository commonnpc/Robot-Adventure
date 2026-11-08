import pygame
from sprites import *
import sys
from przyciski_i_interfejs import *

SZEROKOSC = 800
WYSOKOSC = 600
KLATKI_NA_SEKUNDE = 60
pygame.init()
ZEGAR = pygame.Clock()
EKRAN = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("MONEY GAME")
KLATKA = 0
ANIMACJA = 0
Przycisk_Menu = stworz_przyciski(EKRAN)
Przycisk_Menu.show()
predkosc_y = 0
SILA_SKOKU = -25
GRAWITACJA = 1
MAKS_PREDKOSC_SPADANIA = 20

while True:
    na_podlozu = gracz.czy_dotyka_podloza()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w and na_podlozu:
            predkosc_y = SILA_SKOKU
            klatki_skoku = 0
            na_podlozu = False
            gracz.STATE = "JUMP"
        elif event.type == pygame.KEYUP and event.key == pygame.K_w and predkosc_y < 0:
            predkosc_y = int(predkosc_y * 0.45)
        if Przycisk_Menu.handleEvent(event):
            pass #menu

    klawisze = pygame.key.get_pressed()
    ruch_x = 0
    if klawisze[pygame.K_a] and not klawisze[pygame.K_d]:
        ruch_x = -5
        gracz.KIERUNEK = "LEWO"
    elif klawisze[pygame.K_d] and not klawisze[pygame.K_a]:
        ruch_x = 5
        gracz.KIERUNEK = "PRAWO"

    gracz.prostokat.x += ruch_x
    for prostokat_podloza in prostokaty_podloza:
        if gracz.prostokat.colliderect(prostokat_podloza):
            if ruch_x > 0:
                gracz.prostokat.right = prostokat_podloza.left
            elif ruch_x < 0:
                gracz.prostokat.left = prostokat_podloza.right
    gracz.zsynchronizuj_pozycje()

    predkosc_y = min(predkosc_y + GRAWITACJA, MAKS_PREDKOSC_SPADANIA)
    gracz.prostokat.y += predkosc_y
    for prostokat_podloza in prostokaty_podloza:
        if gracz.prostokat.colliderect(prostokat_podloza):
            if predkosc_y > 0:
                gracz.prostokat.bottom = prostokat_podloza.top
                predkosc_y = 0
            elif predkosc_y < 0:
                gracz.prostokat.top = prostokat_podloza.bottom
                predkosc_y = 0
    gracz.zsynchronizuj_pozycje()
    na_podlozu = gracz.czy_dotyka_podloza()
    if na_podlozu and predkosc_y > 0:
        predkosc_y = 0
    if gracz.STATE != "JUMP":
        gracz.STATE = "WALK" if ruch_x and na_podlozu else "IDLE"
    EKRAN.fill((60, 160, 170))
    gracz.rysuj(ANIMACJA, EKRAN)
    if gracz.STATE == "JUMP":
        klatki_skoku += 1
        if klatki_skoku == 16:
            gracz.STATE = "IDLE"
    for obiekt in obiekty_podloza:
        obiekt.rysuj(ANIMACJA, EKRAN)
    Przycisk_Menu.draw()
    ZEGAR.tick(KLATKI_NA_SEKUNDE)
    pygame.display.update()
    if KLATKA == 11:
        KLATKA = 0
    else:
        KLATKA += 1
    if KLATKA % 12 == 0:
        if ANIMACJA == 4:
            ANIMACJA = 0
        else:
            ANIMACJA += 1
