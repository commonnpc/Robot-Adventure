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
KLATKA = 0
ANIMACJA = 0
Przycisk_Menu = pygwidgets.CustomButton(SCENA, (480, 30), up = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-NA_MYSZY.png")
Przycisk_Ekran = pygwidgets.CustomButton(SCENA, (580, 30), up = f"Phantom/assets/przyciski/przycisk_ekran/PRZYCISK_EKRAN-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_ekran/PRZYCISK_EKRAN-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_ekran/PRZYCISK_EKRAN-NA_MYSZY.png")
Przycisk_Ekranik = pygwidgets.CustomButton(SCENA, (580, 30), up = f"Phantom/assets/przyciski/przycisk_ekranik/PRZYCISK_EKRANIK-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_ekranik/PRZYCISK_EKRANIK-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_ekranik/PRZYCISK_EKRANIK-NA_MYSZY.png")
Przycisk_Wyjscie = pygwidgets.CustomButton(SCENA, (680, 30), up = f"Phantom/assets/przyciski/przycisk_wyjscie/PRZYCISK_WYJSCIE-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_wyjscie/PRZYCISK_WYJSCIE-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_wyjscie/PRZYCISK_WYJSCIE-NA_MYSZY.png")
Przycisk_Jezyk = pygwidgets.CustomButton(SCENA, (162, 120), up = f"Phantom/assets/przyciski/przycisk_jezyk/PRZYCISK_JEZYK-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_jezyk/PRZYCISK_JEZYK-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_jezyk/PRZYCISK_JEZYK-NA_MYSZY.png")
Przycisk_Menu.show()
Przycisk_Jezyk.hide()
Przycisk_Wyjscie.show()
predkosc_y = 0
predkosc_odbicia_x = 0
SILA_SKOKU = -25
GRAWITACJA = 1
MAKS_PREDKOSC_SPADANIA = 20
fullscreen = False
Przycisk_Ekran.show()
Przycisk_Ekranik.hide()
menu = False
serca = 3
ANIMACJA_ENERGIA = 0
monety_liczba = 0
SKOK = False
pociski = []

while True:
    ostatni_czas_na_podlozu = pygame.time.get_ticks() - -101

    szerokosc_swiata = max(p.right for p in prostokaty_podloza)
    kamera_x = max(0, min(gracz.prostokat.centerx - SZEROKOSC // 2, szerokosc_swiata - SZEROKOSC))
    wysokosc_swiata = max(p.bottom for p in prostokaty_podloza)
    kamera_y = min(gracz.prostokat.centery - WYSOKOSC // 2, wysokosc_swiata - WYSOKOSC)
    na_podlozu = gracz.czy_dotyka_podloza()
    if na_podlozu:
        ostatni_czas_na_podlozu = pygame.time.get_ticks()

    for event in pygame.event.get():
        button_event = event
        if hasattr(event, "pos"):
            button_event = pygame.event.Event(event.type, {**event.dict, "pos": (int(event.pos[0] * SZEROKOSC / EKRAN.get_width()), int(event.pos[1] * WYSOKOSC / EKRAN.get_height()))})
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w and (na_podlozu or (pygame.time.get_ticks() - ostatni_czas_na_podlozu <= 100)) and not menu and not SKOK:
            ostatni_czas_na_podlozu = pygame.time.get_ticks() - 101
            predkosc_y = SILA_SKOKU
            klatki_skoku = 0
            na_podlozu = False
            gracz.STATE = "JUMP"
            SKOK = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pociski.append(Bullet(gracz.prostokat.center[0], gracz.prostokat.center[1], 1, gracz.KIERUNEK))
        elif event.type == pygame.KEYUP and event.key == pygame.K_w and predkosc_y < 0 and not menu:
            predkosc_y = int(predkosc_y * 0.45)
        if Przycisk_Menu.handleEvent(button_event):
            menu = True
            Przycisk_Jezyk.show()
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
        elif Przycisk_Jezyk.handleEvent(button_event):
            menu = False
            Przycisk_Jezyk.hide()
            #na razie to wyjscie z menu, ale bedzie jezykiem

    klawisze = pygame.key.get_pressed()
    ruch_x = 0
    if klawisze[pygame.K_a] and not klawisze[pygame.K_d] and not menu:
        ruch_x = -5
        gracz.KIERUNEK = "LEWO"
    elif klawisze[pygame.K_d] and not klawisze[pygame.K_a] and not menu:
        ruch_x = 5
        gracz.KIERUNEK = "PRAWO"

    ruch_poziomy = ruch_x + predkosc_odbicia_x
    gracz.prostokat.x += ruch_poziomy
    for prostokat_podloza in prostokaty_podloza:
        if gracz.prostokat.colliderect(prostokat_podloza):
            if ruch_poziomy > 0:
                gracz.prostokat.right = prostokat_podloza.left
            elif ruch_poziomy < 0:
                gracz.prostokat.left = prostokat_podloza.right
    if gracz.prostokat.right > szerokosc_swiata:
        gracz.prostokat.right = szerokosc_swiata
    elif gracz.prostokat.left < 0:
        gracz.prostokat.left = 0

    if predkosc_odbicia_x > 0:
        predkosc_odbicia_x = max(0, predkosc_odbicia_x - 1)
    elif predkosc_odbicia_x < 0:
        predkosc_odbicia_x = min(0, predkosc_odbicia_x + 1)

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
    if na_podlozu:
        SKOK = False

    if na_podlozu and predkosc_y > 0:
        predkosc_y = 0

    if gracz.STATE != "JUMP":
        gracz.STATE = "WALK" if ruch_x and na_podlozu else "IDLE"

    SCENA.fill((60, 160, 170))

    for obiekt in obiekty_podloza:
        obiekt.rysuj(ANIMACJA, SCENA, kamera_x, kamera_y)
    for energia in energie:
        if energia.BEING:
            energia.rysuj(ANIMACJA_ENERGIA, SCENA, kamera_x, kamera_y)
            if gracz.prostokat.colliderect(energia.prostokat) and serca != 3:
                energia.BEING = False
                serca += 1
    for moneta in monety:
       if moneta.BEING:
            moneta.rysuj(ANIMACJA_ENERGIA, SCENA, kamera_x, kamera_y)
            if gracz.prostokat.colliderect(moneta.prostokat):
                moneta.BEING = False
                monety_liczba += 1
    gracz.rysuj(ANIMACJA, SCENA, kamera_x, kamera_y)
    invincibility = False
    for kolec in kolce:
        kolec.rysuj(ANIMACJA, SCENA, kamera_x, kamera_y)
        if gracz.mask.overlap(kolec.mask, (gracz.prostokat.x - kolec.prostokat.x, gracz.prostokat.y - kolec.prostokat.y)) and not invincibility:
            if ruch_x > 0:
                predkosc_odbicia_x = -12
            elif ruch_x < 0:
                predkosc_odbicia_x = 12
            if predkosc_y > 0:
                gracz.prostokat.bottom = kolec.prostokat.top
                predkosc_y = -20
            elif predkosc_y < 0:
                gracz.prostokat.top = kolec.prostokat.bottom
                predkosc_y = 20
            gracz.zsynchronizuj_pozycje()
            serca -= 1
            invincibility = True
    invincibility = False
    pociski_do_usuniecia = []
    for pocisk in pociski:
        if pocisk.kierunek == "PRAWO":
            pocisk.x += 5
        else:
            pocisk.x -= 5
        pocisk.prostokat.center = pocisk.x, pocisk.y
        SCENA.blit(pocisk.obrazek, (pocisk.prostokat.x - kamera_x, pocisk.prostokat.y - kamera_y))
        if pocisk.prostokat.collidelist(prostokaty_podloza ) != -1:
            pociski_do_usuniecia.append(pocisk)

    pociski = list(set(pociski).difference(set(pociski_do_usuniecia)))
            

    Tekst_Monety = pygwidgets.DisplayText(SCENA, loc=(80, 110), value = str(monety_liczba), fontName = f"Phantom/assets/ARCADECLASSIC.TTF", fontSize = 60, textColor=(186, 164, 20))
    Tekst_Monety.show()
    Tekst_Monety.draw()
    SCENA.blit(pygame.transform.scale_by(pygame.image.load(f"Phantom/assets/MONEY_COUNTER.png"), 2), (20, 120))

    SCENA.blit(pygame.image.load(f"Phantom/assets/RAMA_PRZYCISKOW.png"), (460, 15))
    Przycisk_Menu.draw()
    Przycisk_Wyjscie.draw()
    if fullscreen:
        Przycisk_Ekranik.draw()
    else:
        Przycisk_Ekran.draw()

    for i in range(3):
        SCENA.blit(pygame.transform.scale_by(pygame.image.load(f"Phantom/assets/serca/SERCE_PUSTE.png"), 1/2), (70*i + 30, 30))
    for i in range(serca):
        SCENA.blit(pygame.transform.scale_by(pygame.image.load(f"Phantom/assets/serca/SERCE_PELNE.png"), 1/2), (70*i + 30, 30))

    if menu:
        SCENA.blit(pygame.image.load(f"Phantom/assets/MENU_USTAWIEN.png"), (36, 30))
        Przycisk_Jezyk.draw()

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
    if KLATKA % 15 == 0:
        if ANIMACJA_ENERGIA == 3:
            ANIMACJA_ENERGIA = 0
        else:
            ANIMACJA_ENERGIA += 1