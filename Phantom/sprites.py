import pygame
from arkusze_i_animacje import *

obiekty_podloza = []
prostokaty_podloza = []

class Sprite():
    def __init__(self, X, Y, IDLE = None, RUN = None, WALK = None, JUMP = None, STATE = "IDLE", KIERUNEK = "PRAWO"):
        self.STATE = STATE
        self.KIERUNEK = KIERUNEK
        self.X = X
        self.Y = Y
        self.STANY = []
        if IDLE != None:
            self.IDLEan = podziel_klatki(IDLE[0], IDLE[1],  3)
            self.STANY.append(self.IDLEan)
        if RUN != None:
            self.RUNan = podziel_klatki(RUN[0], RUN[1],  3)
            self.STANY.append(self.RUNan)
        if WALK != None:
            self.WALKan = podziel_klatki(WALK[0], WALK[1],  3)
            self.STANY.append(self.WALKan)
        if JUMP != None:
            self.JUMPan = podziel_klatki(JUMP[0], JUMP[1],  3)
            self.STANY.append(self.JUMPan)
        self.prostokat = self.IDLEan[0].get_rect(topleft=(X, Y))

    def rysuj(self, ANIMACJA, EKRAN):
        if self.KIERUNEK == "PRAWO":
            if self.STATE == "IDLE":
                EKRAN.blit(self.IDLEan[ANIMACJA], (self.X, self.Y))
            elif self.STATE == "RUN":
                pass #################
            elif self.STATE == "WALK":
                if ANIMACJA % 2 == 0:
                    EKRAN.blit(self.WALKan[2 * ANIMACJA], (self.X, self.Y))
                else:
                    EKRAN.blit(self.WALKan[2 * ANIMACJA + 1], (self.X, self.Y))
            elif self.STATE == "JUMP":
                EKRAN.blit(self.JUMPan[ANIMACJA], (self.X, self.Y))
        else:
            if self.STATE == "IDLE":
                EKRAN.blit((pygame.transform.flip(self.IDLEan[ANIMACJA], True, False)), (self.X, self.Y))
            elif self.STATE == "RUN":
                pass ################
            elif self.STATE == "WALK":
                if ANIMACJA % 2 == 0:
                    EKRAN.blit((pygame.transform.flip(self.WALKan[2 * ANIMACJA], True, False)), (self.X, self.Y))
                else:
                    EKRAN.blit((pygame.transform.flip(self.WALKan[2 * ANIMACJA + 1], True, False)), (self.X, self.Y))
            elif self.STATE == "JUMP":
                EKRAN.blit((pygame.transform.flip(self.JUMPan[ANIMACJA], True, False)), (self.X, self.Y))

    def czy_dotyka_podloza(self):
        hitbox_testowy = self.prostokat.move(0, 1)
        return hitbox_testowy.collidelist(prostokaty_podloza) != -1

    def zsynchronizuj_pozycje(self):
        self.X, self.Y = self.prostokat.topleft

    def zwieksz_lub_zmniejsz(self, zwiekszenie, SZEROKOSCW):
        if zwiekszenie:
            self.prostokat.scale_by_ip(SZEROKOSCW/800)
            self.X = self.X * SZEROKOSCW/800
            self.Y = self.Y * SZEROKOSCW/800
        else:
            self.prostokat.scale_by_ip(800/SZEROKOSCW)
            self.X = self.X * 800/SZEROKOSCW
            self.Y = self.Y * 800/SZEROKOSCW
        for stan in self.STANY:
            for klatka in stan:
                i = stan.index(klatka)
                if zwiekszenie:
                    klatka = pygame.transform.scale_by(klatka, SZEROKOSCW/800)
                else:
                    klatka = pygame.transform.scale_by(klatka, 800/SZEROKOSCW)
                stan[i] = klatka
        
gracz = Sprite(100, 100, IDLE = (pygame.image.load(f"Phantom/assets/gracz/PLAYER-IDLE.png"), 5), WALK = (pygame.image.load(f"Phantom/assets/gracz/PLAYER-WALK.png"), 10), JUMP = (pygame.image.load(f"Phantom/assets/gracz/PLAYER-JUMP.png"), 5))

for i in range(15):
    obiekty_podloza.append(Sprite(60*i, 540, IDLE = (pygame.image.load(f"Phantom/assets/GRASS.png"), 5)))
    prostokaty_podloza.append(obiekty_podloza[i].prostokat)
obiekty_podloza.append(Sprite(60, 480, IDLE = (pygame.image.load(f"Phantom/assets/GRASS.png"), 5)))
prostokaty_podloza.append(obiekty_podloza[-1].prostokat)
    





    