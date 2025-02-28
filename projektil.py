from algoviz.svg import Circle

class Projektil:
    def __init__(self, x, y, geschwindigkeit, schaden, svg_view):
        '''
        Diese Klasse erzeugt die Projektile welche die Pflanze abschießt

        Args:
            x : Startposition x
            y : Startposition y
            geschwindigkeit : Geschwindigkeit des Projektils
            schaden : Schaden den das Projektil verursacht
            svg_view : Die SVG-Ansicht 
        '''
        self.x = x
        self.y = y
        self.geschwindigkeit = geschwindigkeit
        self.schaden = schaden
        self.svg_view = svg_view
        self.svg_circle = Circle(x, y, 5, svg_view) 
        self.svg_circle.set_fill("red")

    def bewegen(self):
        self.x += self.geschwindigkeit
        self.svg_circle.move_to(self.x, self.y)

    def ist_ausserhalb(self, spielfeld):
        außerhalb = self.x > spielfeld.get_spalten() * spielfeld.get_block()
        if außerhalb:
            return außerhalb

    def entfernen(self):
        if self.svg_circle:
            self.svg_circle.hide()
