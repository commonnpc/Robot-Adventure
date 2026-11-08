import pygame

def podziel_klatki(arkusz, ile,  powiekszenie):
    klatki = []
    szerokosc, wysokosc = arkusz.get_size()
    for x in range(0, szerokosc, int(szerokosc/ile)):
        klatki.append(pygame.transform.scale(arkusz.subsurface(pygame.Rect(x, 0, int(szerokosc/ile), wysokosc)), (int(szerokosc/ile) * powiekszenie, wysokosc * powiekszenie)))
    return klatki
