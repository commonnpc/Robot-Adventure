import pygame, os, pygwidgets, sys
from sprites import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
SZEROKOSC = 800
WYSOKOSC = 600
KLATKI_NA_SEKUNDE = 60
pygame.init()
ZEGAR = pygame.Clock()
EKRAN = pygame.display.set_mode(((SZEROKOSC, WYSOKOSC)), pygame.NOFRAME)
SCENA = pygame.Surface((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("MONEY GAME")
KLATKA = 0
ANIMACJA = 0
Przycisk_Menu = pygwidgets.CustomButton(SCENA, (480, 30), up = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-NA_MYSZY.png")
Przycisk_Ekran = pygwidgets.CustomButton(SCENA, (580, 30), up = f"Phantom/assets/przyciski/przycisk_ekran/PRZYCISK_EKRAN-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_ekran/PRZYCISK_EKRAN-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_ekran/PRZYCISK_EKRAN-NA_MYSZY.png")
Przycisk_Ekranik = pygwidgets.CustomButton(SCENA, (580, 30), up = f"Phantom/assets/przyciski/przycisk_ekranik/PRZYCISK_EKRANIK-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_ekranik/PRZYCISK_EKRANIK-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_ekranik/PRZYCISK_EKRANIK-NA_MYSZY.png")
Przycisk_Wyjscie = pygwidgets.CustomButton(SCENA, (680, 30), up = f"Phantom/assets/przyciski/przycisk_wyjscie/PRZYCISK_WYJSCIE-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_wyjscie/PRZYCISK_WYJSCIE-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_wyjscie/PRZYCISK_WYJSCIE-NA_MYSZY.png")
Przycisk_Menu.show()
Przycisk_Wyjscie.show()
predkosc_y = 0
SILA_SKOKU = -25
GRAWITACJA = 1
MAKS_PREDKOSC_SPADANIA = 20
fullscreen = False
Przycisk_Ekran.show()
Przycisk_Ekranik.hide()

while True:
    szerokosc_swiata = max(p.right for p in prostokaty_podloza)
    kamera_x = max(0, min(gracz.prostokat.centerx - SZEROKOSC // 2, szerokosc_swiata - SZEROKOSC))
    wysokosc_swiata = max(p.bottom for p in prostokaty_podloza)
    kamera_y = min(gracz.prostokat.centery - WYSOKOSC // 2, wysokosc_swiata - WYSOKOSC)
    na_podlozu = gracz.czy_dotyka_podloza()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        button_event = event
        if hasattr(event, "pos"):
            button_event = pygame.event.Event(event.type, {**event.dict, "pos": (int(event.pos[0] * SZEROKOSC / EKRAN.get_width()), int(event.pos[1] * WYSOKOSC / EKRAN.get_height()))})
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w and na_podlozu:
            predkosc_y = SILA_SKOKU
            klatki_skoku = 0
            na_podlozu = False
            gracz.STATE = "JUMP"
        elif event.type == pygame.KEYUP and event.key == pygame.K_w and predkosc_y < 0:
            predkosc_y = int(predkosc_y * 0.45)
        if Przycisk_Menu.handleEvent(button_event):
            pass #menu
        elif Przycisk_Wyjscie.handleEvent(button_event):
            #czy na pewno
            pygame.quit()
            sys.exit()
        elif Przycisk_Ekran.handleEvent(button_event):
            fullscreen = True
            szerokosc_pulpitu, wysokosc_pulpitu = pygame.display.get_desktop_sizes()[0]
            maks_szerokosc = szerokosc_pulpitu
            maks_wysokosc = wysokosc_pulpitu
            skala = min(maks_szerokosc / SZEROKOSC, maks_wysokosc / WYSOKOSC)
            EKRAN = pygame.display.set_mode((int(SZEROKOSC * skala), int(WYSOKOSC * skala)), pygame.NOFRAME)
            Przycisk_Ekranik.show()
            Przycisk_Ekran.hide()
            
        elif Przycisk_Ekranik.handleEvent(button_event):
            fullscreen = False
            EKRAN = pygame.display.set_mode(((SZEROKOSC, WYSOKOSC)), pygame.NOFRAME)
            Przycisk_Ekranik.hide()
            Przycisk_Ekran.show()

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
        if gracz.prostokat.right > szerokosc_swiata:
            gracz.prostokat.right = szerokosc_swiata
        elif gracz.prostokat.left < 0:
            gracz.prostokat.left = 0

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
    gracz.rysuj(ANIMACJA, SCENA, kamera_x, kamera_y)

    for obiekt in obiekty_podloza:
        obiekt.rysuj(ANIMACJA, SCENA, kamera_x, kamera_y)
    SCENA.blit(pygame.image.load(f"Phantom/assets/RAMA_PRZYCISKOW.png"), (460, 15))
    Przycisk_Menu.draw()
    Przycisk_Wyjscie.draw()
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