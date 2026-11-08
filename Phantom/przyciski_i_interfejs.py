import pygwidgets

def stworz_przyciski(EKRAN):
    Przycisk_Menu = pygwidgets.CustomButton(EKRAN, (680, 30), up = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-IDLE.png", down = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-KLIKNIETY.png", over = f"Phantom/assets/przyciski/przycisk_menu/PRZYCISK_MENU-NA_MYSZY.png")
    return Przycisk_Menu
