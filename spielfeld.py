from algoviz import AlgoViz
from algoviz.svg import SVGView, Rect, Circle, Image, Text

class Spielfeld:
    def __init__(self, _zeilen, _spalten, _block):
        self._zeilen = _zeilen
        self._spalten = _spalten
        self._block = _block
        self._svg = SVGView(self._spalten * self._block, self._zeilen * self._block, "Tower Defense")

        # Status der Felder (0 = frei, 1 = besetzt)
        self._feld_status = [[0 for _ in range(self._spalten)] for _ in range(self._zeilen)]
        """
        Klasse für das erstellen des Spielfeldes

        Args:
            zeilen: Zeilenindex des Feldes
            spalten: Spaltenindex des Feldes
            block: Größe eines Feldes
        """
        
    # Überprüft ob das Feld frei ist
    def ist_frei(self, zeile, spalte):
        if 0 <= zeile < self._zeilen and 0 <= spalte < self._spalten:
            return self._feld_status[zeile][spalte] == 0
        else:
            raise ValueError("Ungültige Koordinaten: außerhalb des Spielfelds")

    # Markiert ein Feld als besetzt
    def feld_besetzen(self, zeile, spalte):
        if 0 <= zeile < self._zeilen and 0 <= spalte < self._spalten:
            self._feld_status[zeile][spalte] = 1
        else:
            raise ValueError("Ungültige Koordinaten: außerhalb des Spielfelds")

    # Feld wird freigegeben
    def feld_freigeben(self, zeile, spalte):
        if 0 <= zeile < self._zeilen and 0 <= spalte < self._spalten:
            self._feld_status[zeile][spalte] = 0
        else:
            raise ValueError("Ungültige Koordinaten: außerhalb des Spielfelds")

    # Das bekannte Rastermuster wird erstellt
    def spielfeld_erstellen(self):
        self._rects = [] 
        self._felder = []

        for x in range(self._spalten):
            _spalte = []          
            _rects_spalte = []  
            
            for y in range(self._zeilen):
                _typ = (x + y) % 2  
                
                _rect = Rect(
                    x * self._block,
                    y * self._block,
                    self._block,
                    self._block,
                    self._svg)
                
                if _typ == 0:
                    _rect.set_fill("lightgreen")  
                else:
                    _rect.set_fill("darkgreen")  

                
                _spalte.append(_typ)
                _rects_spalte.append(_rect)

            
            self._felder.append(_spalte)
            self._rects.append(_rects_spalte)

    def get_spalten(self):
        return self._spalten

    def get_svg(self):
        return self._svg

    def get_zeilen(self):
        return self._zeilen

    def get_block(self):
        return self._block
        
        