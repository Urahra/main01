from algoviz import AlgoViz
from spielfeld import Spielfeld
from pflanze import Pflanze
from zombie import Zombie
from projektil import Projektil
import math
import random
import time

class Spiel:
    def __init__(self):
        # Neues Spielfeld erstellen
        self._spielfeld = Spielfeld(5, 10, 50)
        self._spielfeld.spielfeld_erstellen()

        # Listen für die Pflanzen, Projektile und Zombies
        self._pflanzen_liste = []
        self._projektile_liste = []
        self._zombie_liste = []
        
        self._time_since_last_spawn = 0.0
        self._spawn_cooldown = random.uniform(2, 4)
        self._zombies_to_spawn = 4

        self._spiel_laeuft = True

    # Hier werden die Zombies erstellt
    def neuer_zombie(self):
        neuer_zombie = Zombie(
            lebenspunkte=225, 
            x=0, 
            y=0, 
            geschwindigkeit=30, 
            svg_view=self._spielfeld.get_svg()
        )
        neuer_zombie.zombie_platzieren(self._spielfeld, self._zombie_liste)

    # Diese Methode gugckt ob ein Projektil ein Zombie trifft
    def projektil_trifft(self, projektil, zombie):
        dx = zombie.get_center_x() - projektil.x
        dy = zombie.get_center_y() - projektil.y
        distance_squared = dx * dx + dy * dy
        return distance_squared < 100  

    # Guckt ob der Zombie die Pflanze berührt
    def zombie_beruehrt_pflanze(self, zombie, pflanze):
        dx = zombie.get_center_x() - pflanze.get_pflanze_x()
        dy = zombie.get_center_y() - pflanze.get_pflanze_y()
        distance_squared = dx * dx + dy * dy
        return distance_squared < 400 

    # Platziert eine Pflanze auf dem Spielfeld
    def pflanze_platzieren_bei_xy(self, x_klick, y_klick):
        x_spalte = int(x_klick // self._spielfeld.get_block())
        y_zeile = int(y_klick // self._spielfeld.get_block())

        if self._spielfeld.ist_frei(y_zeile, x_spalte):
            # Mittelpunkt wird berechnet
            mitte_x = (x_spalte * self._spielfeld.get_block()) + (self._spielfeld.get_block() // 2)
            mitte_y = (y_zeile * self._spielfeld.get_block()) + (self._spielfeld.get_block() // 2)
            
            # Pflanze wird erstellt und offiziel Platziert
            pflanze = Pflanze(
                lebenspunkte=100, 
                schaden=25, 
                schuss_frequenz=1.0, 
                svg_view=self._spielfeld.get_svg(), 
                block_size=self._spielfeld.get_block()
            )
            pflanze.set_pos(mitte_x, mitte_y)
            self._pflanzen_liste.append(pflanze)
            
            self._spielfeld.feld_besetzen(y_zeile, x_spalte)
            print(f"Pflanze an ({x_spalte}, {y_zeile}) platziert.")
        else:
            print(f"Feld ({x_spalte}, {y_zeile}) ist bereits besetzt.")
            
    # Hauptschleife
    def start_game_loop(self):
        self.last_frame_time = time.time()
        print("Du musst", self._zombies_to_spawn, "Zombies töten um zu gewinnen")
        while self._spiel_laeuft:
            try:
                current_time = time.time()
                delta_time = current_time - self.last_frame_time
                self.last_frame_time = current_time

                # Pflanzen updaten
                for pflanze in self._pflanzen_liste[:]:
                    pflanze.update(self._projektile_liste, self._spielfeld)
                
                self._time_since_last_spawn += delta_time

                # Zombie Spawn-Mechanik
                if self._time_since_last_spawn >= self._spawn_cooldown and self._zombies_to_spawn > 0:
                    self.neuer_zombie()  
                    self._time_since_last_spawn = 0.0 
                    self._spawn_cooldown = random.uniform(2, 4) 
                    self._zombies_to_spawn -= 1

                # Zombies bewegen
                for zombie in self._zombie_liste[:]:
                    zombie.bewegen(delta_time)
                    if zombie.ist_ausserhalb():
                        print("Die Zombies haben gewonnen")
                        self._spiel_laeuft = False

                # Zombie-Pflanzen-Kollision
                for zombie in self._zombie_liste[:]:
                    for pflanze in self._pflanzen_liste[:]:
                        if self.zombie_beruehrt_pflanze(zombie, pflanze):
                            if not zombie._is_attacking:
                                zombie.start_attack(pflanze)

                            # Prüfen, ob Pflanze sofort tot ist:
                            if pflanze.ist_tot():
                                self._pflanzen_liste.remove(pflanze)
                                pflanze.entfernen()

                # Zombie-Update für Angriff
                for zombie in self._zombie_liste[:]:
                    zombie.update_attack(zombie._current_target, delta_time)

                # Pflanze tot -> entfernen
                for pflanze in self._pflanzen_liste[:]:
                    if pflanze.ist_tot():
                        self._pflanzen_liste.remove(pflanze)
                        pflanze.entfernen()

                # Zombie tot -> entfernen
                for zombie in self._zombie_liste[:]:
                    if zombie.ist_tot():
                        self._zombie_liste.remove(zombie)
                        zombie.entfernen()

                # Projektile bewegen und prüfen
                for projektil in self._projektile_liste[:]:
                    projektil.bewegen()
                    if projektil.ist_ausserhalb(self._spielfeld):
                        projektil.entfernen()
                        self._projektile_liste.remove(projektil)
                    if not self._zombie_liste:
                        self.stoppen()
                        print("Die Pflanzen haben gewonnen!")

                # Prüfen, ob Projektile Zombies treffen
                for projektil in self._projektile_liste[:]:
                    for zombie in self._zombie_liste[:]:
                        if self.projektil_trifft(projektil, zombie):
                            zombie.schaden_erleiden(projektil.schaden)
                            projektil.entfernen()
                            self._projektile_liste.remove(projektil)
                            if zombie.ist_tot():
                                self._zombie_liste.remove(zombie)
                                zombie.entfernen()
                            break

                # Pflanzenplatzierung 
                state = self._spielfeld.get_svg().get_mouse_state() 
                if state.is_legal() and state.left():
                    x_klick = state.x()
                    y_klick = state.y()
                    self.pflanze_platzieren_bei_xy(x_klick, y_klick)
                
                AlgoViz.sleep(5)
            
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")
                self.stoppen() 

    # Kann aufgerufen werden um das Spiel zu beenden
    def stoppen(self):
        self._spiel_laeuft = False

    # Entfernt eine Pflanze
    def entfernen(self):
        for pflanze in self._pflanzen_liste:
            pflanze.entfernen()

    # Debug Methode
    def anzeigen_pflanzen(self):
        if self._pflanzen_liste:
            for i, pflanze in enumerate(self._pflanzen_liste, start=1):
                print(f"Pflanze {i} an Position x {pflanze.get_pflanze_x()}, y={pflanze.get_pflanze_y()}")
        else:
            print("Keine Pflanzen platziert.")
