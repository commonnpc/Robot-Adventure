import pygame
import pygwidgets
from sprites import *
import sys

SZEROKOSC = 800
WYSOKOSC = 600
KLATKI_NA_SEKUNDE = 60
pygame.init()
ZEGAR = pygame.Clock()
EKRAN = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
SCENA = pygame.Surface((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("MONEY GAME")
KLATKA = 0
ANIMACJA = 0
Przycisk_Menu = pygwidgets.CustomButton(SCENA, (680, 30), up = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-NA_MYSZY.png")
Przycisk_Ekran = pygwidgets.CustomButton(SCENA, (580, 30), up = f"Phantom/assets/przyciski/przycisk_ekran/PRZYCISK_EKRAN-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_ekran/PRZYCISK_EKRAN-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_ekran/PRZYCISK_EKRAN-NA_MYSZY.png")
Przycisk_Ekranik = pygwidgets.CustomButton(SCENA, (80, 30), up = f"Phantom/assets/przyciski/przycisk_ekranik/PRZYCISK_EKRANIK-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_ekranik/PRZYCISK_EKRANIK-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_ekranik/PRZYCISK_EKRANIK-NA_MYSZY.png")
Przycisk_Menu.show()
predkosc_y = 0
SILA_SKOKU = -25
GRAWITACJA = 1
MAKS_PREDKOSC_SPADANIA = 20
fullscreen = False
Przycisk_Ekran.show()

while True:
    na_podlozu = gracz.czy_dotyka_podloza()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        button_event = event
        if hasattr(event, "pos"):
            button_event = pygame.event.Event(
                event.type,
                {
                    **event.dict,
                    "pos": (
                        int(event.pos[0] * SZEROKOSC / EKRAN.get_width()),
                        int(event.pos[1] * WYSOKOSC / EKRAN.get_height()),
                    ),
                },
            )
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w and na_podlozu:
            predkosc_y = SILA_SKOKU
            klatki_skoku = 0
            na_podlozu = False
            gracz.STATE = "JUMP"
        elif event.type == pygame.KEYUP and event.key == pygame.K_w and predkosc_y < 0:
            predkosc_y = int(predkosc_y * 0.45)
        if Przycisk_Menu.handleEvent(button_event):
            pass #menu
        if Przycisk_Ekran.handleEvent(button_event):
            Przycisk_Ekran.hide()
            Przycisk_Ekranik.show()
            fullscreen = True
            szerokosc_pulpitu, wysokosc_pulpitu = pygame.display.get_desktop_sizes()[0]
            maks_szerokosc = szerokosc_pulpitu
            maks_wysokosc = wysokosc_pulpitu
            skala = min(maks_szerokosc / SZEROKOSC, maks_wysokosc / WYSOKOSC)
            EKRAN = pygame.display.set_mode((int(SZEROKOSC * skala), int(WYSOKOSC * skala)), pygame.NOFRAME)
            
        if Przycisk_Ekranik.handleEvent(button_event):
            Przycisk_Ekranik.hide()
            Przycisk_Ekran.show()
            fullscreen = False
            EKRAN = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))

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

    SCENA.fill((60, 160, 170))
    gracz.rysuj(ANIMACJA, SCENA)

    for obiekt in obiekty_podloza:
        obiekt.rysuj(ANIMACJA, SCENA)
    Przycisk_Menu.draw()
    if fullscreen:
        Przycisk_Ekranik.draw()
    else:
        Przycisk_Ekran.draw()

    EKRAN.blit(pygame.transform.scale(SCENA, EKRAN.get_size()), (0, 0))

    if gracz.STATE == "JUMP":
        klatki_skoku += 1
        if klatki_skoku == 16:
            gracz.STATE = "IDLE"

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
