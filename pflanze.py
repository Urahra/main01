from algoviz.svg import Circle, Image
import time
from projektil import Projektil

class Pflanze:
    def __init__(self, lebenspunkte, schaden, schuss_frequenz, svg_view, block_size):
        ''' 
        Klasse für das erzeugen einer Pflanze

        Args:
            lebenspunkte: Wie viel Leben hat die Pflanze
            schaden: Wie viel Schaden macht die Pflanze
            schuss_frequenz: Die Zeit zwischen zwei Schüssen (in Sekunden)
            svg_view: Die SVG-Ansicht 
            block_size: Größe eines Blocks im Spielfeld
        '''
        self._lebenspunkte = lebenspunkte
        self._schaden = schaden
        self._schuss_frequenz = schuss_frequenz
        self._projekte = []  
        self._pflanze_x = None
        self._pflanze_y = None
        self._zeit_seit_letztem_schuss = 0.0
        self.svg_view = svg_view
        self.block_size = block_size
        self.svg_circle = None
        self.last_shot_time = time.time()

    def set_pos(self, x, y):
        self._pflanze_x = x
        self._pflanze_y = y
        kreis_radius = self.block_size // 3
        self.svg_circle = Circle(x, y, kreis_radius, self.svg_view)
        self.svg_circle.set_fill("blue")

    def get_pflanze_x(self):
        return self._pflanze_x

    def get_pflanze_y(self):
        return self._pflanze_y
    
    def get_lebenspunkte(self):
        return self._lebenspunkte

    def get_schaden(self):
        return self._schaden

    def get_schuss_frequenz(self):
        return self._schuss_frequenz

    def schaden_erleiden(self, damage):
        self._lebenspunkte -= damage
        if self._lebenspunkte > 75:
            self.svg_circle.set_fill("blue")
        elif self._lebenspunkte > 50:
            self.svg_circle.set_fill("green")
        elif self._lebenspunkte > 25:
            self.svg_circle.set_fill("yellow")
        else:
            self.svg_circle.set_fill("red")

    def ist_tot(self):
        return self._lebenspunkte <= 0

    def entfernen(self):
        if self.svg_circle:
            self.svg_circle.hide()
            
    # Erhöht den Timer und schießt ein neues Projektil ab, wenn die Schussfrequenz erreicht ist
    def update(self, projektile_liste, spielfeld):
        current_time = time.time()
        if (current_time - self.last_shot_time) >= self._schuss_frequenz:
            self.last_shot_time = current_time
            self.schieße(projektile_liste, spielfeld)
            
    # Erzeugt ein Projektil und fügt es der Projektilliste hinzu
    def schieße(self, projektile_liste, spielfeld):
        if self._pflanze_x is not None and self._pflanze_y is not None:
            projektil = Projektil(
                self._pflanze_x, 
                self._pflanze_y, 
                geschwindigkeit=5, 
                schaden=self._schaden, 
                svg_view=spielfeld.get_svg()
            )
            projektile_liste.append(projektil)
