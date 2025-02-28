from algoviz.svg import Rect
import random

class Zombie:
    def __init__(self, lebenspunkte, x, y, geschwindigkeit, svg_view):
        '''
        Erzeuge einen Zombie.

        Args:
            lebenspunkte : Lebenspunkte des Zombies
            x : Startposition x 
            y : Startposition y
            geschwindigkeit : Geschwindigkeit des Zombies
            svg_view : Die SVG-Ansicht 
        '''
        self.original_lebenspunkte = lebenspunkte
        self.lebenspunkte = lebenspunkte
        self.x = x
        self.y = y
        self.geschwindigkeit = geschwindigkeit
        self.original_geschwindigkeit = geschwindigkeit 
        self.svg_view = svg_view
        self.svg_rect = Rect(x, y, 30, 30, svg_view)  
        self.svg_rect.set_fill("grey")

        # Zombie Status
        self._is_attacking = False
        self._current_target = None

        # Für die Lebensbalcken
        self.bar_width = 50
        self.bar_height = 6

    # Zombie bewegen
    def bewegen(self, delta_time):
            if not self._is_attacking:
                self.x -= self.geschwindigkeit * delta_time
                self.svg_rect.move_to(self.x, self.y)
                self._healthbar_bg.move_to(self.x , int(self.y - 20))
                self._healthbar_fg.move_to(self.x , int(self.y - 20))

    # Zombie erleidet schaden
    def schaden_erleiden(self, schaden):
        self.lebenspunkte -= schaden
        if self.lebenspunkte <= 0:
            self.svg_rect.hide()
        self.update_healthbar()

    # Lebensbalcken updaten
    def update_healthbar(self):
        ratio = self.lebenspunkte / self.original_lebenspunkte
        bar_width = 50 * ratio
        self._healthbar_fg.set_width(bar_width)
        if self.lebenspunkte <= 0:
            self._healthbar_bg.hide()
            self._healthbar_fg.hide()

    def ist_ausserhalb(self):
        return self.x < 0

    def ist_tot(self):
        return self.lebenspunkte <= 0

    #  Der Zombie wechselt in den Angrifsmodus
    def start_attack(self, pflanze):
        self._is_attacking = True
        self.geschwindigkeit = 0
        self._current_target = pflanze
        self.svg_rect.rotate_to(45)
        self.svg_rect.set_fill("red")

    # Das Ziel kriegt Schaden 
    def update_attack(self, target, delta_time):
        if self._is_attacking and target:
            schaden = 10 * delta_time
            target.schaden_erleiden(schaden)
            if target.ist_tot():
                self._is_attacking = False
                self._current_target = None
                self.svg_rect.rotate_to(0)
                self.svg_rect.set_fill("grey")
                self.geschwindigkeit = self.original_geschwindigkeit

    # Zombie wird platziert
    def zombie_platzieren(self, spielfeld, zombie_liste):
        zeile = random.randint(0, spielfeld.get_zeilen() - 1)
        self.x = spielfeld.get_spalten() * spielfeld.get_block() - 10  
        self.y = zeile * spielfeld.get_block() + spielfeld.get_block() // 5 
        self.svg_rect.move_to(self.x, self.y)
        zombie_liste.append(self)

        self._healthbar_bg = Rect(
            self.x, 
            self.y - 20, 
            self.bar_width, 
            self.bar_height, 
            spielfeld.get_svg()
            )
        self._healthbar_bg.set_fill("gray")

        self._healthbar_fg = Rect(
            self.x, 
            self.y - 20,
            self.bar_width,
            self.bar_height,
            spielfeld.get_svg()
            )
        self._healthbar_fg.set_fill("red")

    def entfernen(self):
        if self.svg_rect:
            self.svg_rect.hide()

    def get_zombie_x(self):
        return self.x

    def get_zombie_y(self):
        return self.y

    def get_center_x(self):
        return self.x + 15  

    def get_center_y(self):
        return self.y + 15 


