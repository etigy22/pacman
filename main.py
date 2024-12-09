import math
import pygame
import sys
import random

#Pacman Spiel
class PacManGame:
    def __init__(self,farben,s_w,ghost,ghost_img,PIXEL=40):
        self.farbe = farben
        self.s_w = s_w
        self.PIXEL = PIXEL
        self.ghosts = ghost
        self.pacman_field = self.read_gamefield()
        self.ghost_img = ghost_img
        self.power_up_timer = 0
        self.screen_WIDTH = 0
        self.screen_HEIGHT = 0
        self.screen =self.innit_scrren()
        self.pacman_spiel()
        
    def innit_scrren(self):
        self.screen_WIDTH = len(self.pacman_field[0]) * self.PIXEL
        self.screen_HEIGHT = len(self.pacman_field) * self.PIXEL
        screen = pygame.display.set_mode((self.screen_WIDTH, self.screen_HEIGHT))
        return screen
    def read_gamefield(self):
        with open("pacman_field.txt", "r") as datei:
            text = datei.read()
            pacman_field = []
            row = []
            for zeichen in text:
                if zeichen in "0123": # Spielfeld (0: leer, 1: Wand, 2: Punkt, 3: Power-Up)
                    row.append(int(zeichen))
                elif zeichen == "\n":
                    pacman_field.append(row)
                    row = []
            if row:
                pacman_field.append(row)
        return pacman_field
        
    # Spielfeld Zeichnen
    def draw_field(self):
            for row in range(len(self.pacman_field)):
                for col in range(len(self.pacman_field[row])):
                    x = col * self.PIXEL
                    y = row * self.PIXEL
                    if self.pacman_field[row][col] == 1:  # Wand
                        pygame.draw.rect(self.screen, farben["BLAU"], (x, y, self.PIXEL, self.PIXEL))
                    elif self.pacman_field[row][col] == 2:  # Punkt
                        pygame.draw.circle(self.screen, farben["WEISS"], (x + self.PIXEL / 2, y + self.PIXEL / 2), self.PIXEL / 8)
                    elif self.pacman_field[row][col] == 3:  # Power-Up
                        pygame.draw.circle(self.screen, farben["WEISS"], (x + self.PIXEL / 2, y + self.PIXEL / 2), self.PIXEL / 4)
    # PacMan Zeichnen                    
    def draw_pacman(self):

            # Pacmans Mund bewegt sich
            if self.s_w["move"] != [0, 0]:
                self.s_w["schritt"] += 1
                self.s_w["mund"] = abs(math.sin(math.pi / self.PIXEL * self.s_w["schritt"] * 2)) * 45

            # Pacman zeichnen
            surface_1 = pygame.Surface((self.PIXEL, self.PIXEL), pygame.SRCALPHA)
            surface_2 = pygame.Surface((self.PIXEL, self.PIXEL), pygame.SRCALPHA)
            pygame.draw.circle(
                surface_1,
                farben["GELB"],
                (self.PIXEL / 2, self.PIXEL / 2),
                self.PIXEL / 3,
                draw_top_right=True, draw_top_left=True
            )
            pygame.draw.circle(
                surface_2,
                farben["GELB"],
                (self.PIXEL / 2, self.PIXEL / 2),
                self.PIXEL / 3,
                draw_bottom_right=True, draw_bottom_left=True
            )
            rotated_surface_1 = pygame.transform.rotate(surface_1, self.s_w["angle"] + self.s_w["mund"])
            rotated_surface_2 = pygame.transform.rotate(surface_2, self.s_w["angle"] - self.s_w["mund"])
           
            rotated_rect_1 = rotated_surface_1.get_rect(
                center=(int(self.s_w["player_pos"][0] * self.PIXEL + self.PIXEL / 2), int(s_w["player_pos"][1] * self.PIXEL + self.PIXEL / 2))
            )
            rotated_rect_2 = rotated_surface_2.get_rect(
                center=(int(s_w["player_pos"][0] * self.PIXEL + self.PIXEL / 2), int(s_w["player_pos"][1] * self.PIXEL + self.PIXEL / 2))
            )

            self.screen.blit(rotated_surface_1, rotated_rect_1.topleft)
            self.screen.blit(rotated_surface_2, rotated_rect_2.topleft)
    # Geister Zeichnen
    def draw_ghosts(self):
        for ghost in ghosts:
            if self.s_w["power_up"]:
                # Power-Up-Bild verwenden
                ghost_image = ghost_img["POWER_UP"]
            else:
                # Normales Bild basierend auf der Farbe des Geists
                ghost_image = ghost_img[ghost["color"]]

            # Geisterposition berechnen
            ghost_x = ghost["x"] * self.PIXEL + self.PIXEL / 4
            ghost_y = ghost["y"] * self.PIXEL + self.PIXEL / 4

            # Geist zeichnen
            self.screen.blit(ghost_image, (ghost_x, ghost_y))
    
    
        # Pacman schaut, ob er einen Richtungswechsel machen kann
    # Bewegung von PacMan
    def pacman_bewegung(self):
        if abs(self.s_w["player_pos"][0] - round(self.s_w["player_pos"][0])) < 0.01 and abs(
                self.s_w["player_pos"][1] - round(self.s_w["player_pos"][1])) < 0.01:
            grid_x, grid_y = int(round(self.s_w["player_pos"][0])), int(round(self.s_w["player_pos"][1]))

            if self.s_w["next_direction"]:
                if self.s_w["next_direction"] == "Up" and self.pacman_field[grid_y - 1][grid_x] != 1:
                    self.s_w["direction"] = self.s_w["next_direction"]
                    self.s_w["angle"] = 90
                elif self.s_w["next_direction"] == "Down" and self.pacman_field[grid_y + 1][grid_x] != 1:
                    self.s_w["direction"] = self.s_w["next_direction"]
                    self.s_w["angle"] = -90
                elif self.s_w["next_direction"] == "Right" and self.pacman_field[grid_y][grid_x + 1] != 1:
                    self.s_w["direction"] = self.s_w["next_direction"]
                    self.s_w["angle"] = 0
                elif self.s_w["next_direction"] == "Left" and self.pacman_field[grid_y][grid_x - 1] != 1:
                    self.s_w["direction"] = self.s_w["next_direction"]
                    self.s_w["angle"] = 180

            if self.s_w["direction"] == "Up" and self.pacman_field[grid_y - 1][grid_x] != 1:
                self.s_w["move"][:] = [0, -self.s_w["speed"] / self.PIXEL]
            elif self.s_w["direction"] == "Down" and self.pacman_field[grid_y + 1][grid_x] != 1:
                self.s_w["move"][:] = [0, self.s_w["speed"] / self.PIXEL]
            elif self.s_w["direction"] == "Right" and self.pacman_field[grid_y][grid_x + 1] != 1:
                self.s_w["move"][:] = [self.s_w["speed"] / self.PIXEL, 0]
            elif self.s_w["direction"] == "Left" and self.pacman_field[grid_y][grid_x - 1] != 1:
                self.s_w["move"][:] = [-self.s_w["speed"] / self.PIXEL, 0]
            else:
                self.s_w["move"][:] = [0, 0]

        self.s_w["player_pos"][0] += self.s_w["move"][0]
        self.s_w["player_pos"][1] += self.s_w["move"][1]
    # Power-Up: Ja oder Nein?
    def power_up_check(self):
        timer=self.power_up_timer
        if self.s_w["power_up"]:
            timer += 1 
            self.power_up_timer = timer 
            self.run_away()

            if timer > 300:  # Power-Up endet
                self.s_w["power_up"] = False
                timer = 0
                
        else:
            # Neue Logik hinzufügen
            if not self.s_w["power_up"]:  # Wenn kein Power-Up aktiv ist
                for ghost in self.ghosts:
                    if ghost["move"] == [0, 0]:  # Sicherstellen, dass Bewegung vorhanden ist
                        self.geister_bewegung_1()

            # Normale Bewegungslogik der Geister
            wahl = random.choice([1, 2])
            if wahl == 1:
                self.geister_bewegung_1()
            else:
                self.geister_bewegung_2()
        
    # Geister können sich in eine random Richtung bewegen, oder ...
    def geister_bewegung_1(self):
        for ghost in ghosts:
            x = round(ghost["x"])
            y = round(ghost["y"])
            xn = ghost["x"] - x
            yn = ghost["y"] - y
            #if abs(ghost["x"] - x) < 0.01 and abs(ghost["y"] - y) < 0.01:
            if abs(xn) < 0.01 and abs(yn) < 0.01:
                ghost["x"], ghost["y"] = x, y

                valid_moves = []
                if y - 1 >= 0 and self.pacman_field[y - 1][x] != 1:  # Up
                    valid_moves.append([0, -1])
                if y + 1 < len(self.pacman_field) and self.pacman_field[y + 1][x] != 1:  # Down
                    valid_moves.append([0, 1])
                if x + 1 < len(self.pacman_field[0]) and self.pacman_field[y][x + 1] != 1:  # Right
                    valid_moves.append([1, 0])
                if x - 1 >= 0 and self.pacman_field[y][x - 1] != 1:  # Left
                    valid_moves.append([-1, 0])
                if(ghost["color"] == farben["BLAU"]):
                    print("Valid Moves",ghost["color"],valid_moves)
                # Wähle zufällige gültige Bewegung
                if valid_moves:
                    ghost["move"] = random.choice(valid_moves)

            # Sanfte Bewegung basierend auf der aktuellen Richtung
            ghost["x"] += ghost["move"][0] * (ghost["speed"] / self.PIXEL)
            ghost["y"] += ghost["move"][1] * (ghost["speed"] / self.PIXEL)
    # ... Geister verfolgen Pacman
    def geister_bewegung_2(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Bewegungsrichtungen

        for ghost in ghosts:
            ghost_x, ghost_y = ghost["x"], ghost["y"]
            ghost_x, ghost_y = round(ghost_x), round(ghost_y)
            xn = ghost["x"] - ghost_x
            yn = ghost["y"] - ghost_y
            
            #if abs(ghost_x - round(ghost_x)) < 0.01 and abs(ghost_y - round(ghost_y)) < 0.01:
            if abs(xn) < 0.01 and abs(yn) < 0.01:

                ghost_x, ghost_y = round(ghost_x), round(ghost_y)

                queue = [(ghost_x, ghost_y)]
                visited = set(queue)
                parent = {}

                while queue:
                    current_x, current_y = queue.pop(0)

                    for dx, dy in directions:
                        neighbor_x, neighbor_y = current_x + dx, current_y + dy
                        if (
                                0 <= neighbor_x < len(self.pacman_field[0])
                                and 0 <= neighbor_y < len(self.pacman_field)
                                and self.pacman_field[neighbor_y][neighbor_x] != 1
                                and (neighbor_x, neighbor_y) not in visited
                        ):
                            queue.append((neighbor_x, neighbor_y))
                            visited.add((neighbor_x, neighbor_y))
                            parent[(neighbor_x, neighbor_y)] = (current_x, current_y)
                            
                            
                            if (neighbor_x, neighbor_y) == (int(round(self.s_w["player_pos"][0])), int(round(self.s_w["player_pos"][1]))):
                                if(ghosts[2]["color"] == farben["BLAU"]):
                                    print(queue,"Que Pathfinding")
                                queue = []  # Ziel gefunden
                            

                next_position = (ghost_x, ghost_y)
                current_position = (int(round(self.s_w["player_pos"][0])), int(round(self.s_w["player_pos"][1])))

                while current_position in parent:
                    next_position = current_position
                    current_position = parent[current_position]

                next_x, next_y = next_position
                ghost["move"] = [(next_x - ghost_x), (next_y - ghost_y)]

            ghost["x"] += ghost["move"][0] * (ghost["speed"] / self.PIXEL)
            ghost["y"] += ghost["move"][1] * (ghost["speed"] / self.PIXEL)
            
        
            # Sicherstellen, dass die Geister innerhalb des Spielfelds bleiben
            ghost["x"] = max(0, min(len(self.pacman_field[0]) - 1, ghost["x"]))
            ghost["y"] = max(0, min(len(self.pacman_field) - 1, ghost["y"]))
    # Geister rennen bei Power-Up weg
    def run_away(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Oben, Unten, Links, Rechts

        for ghost in ghosts:
            ghost_x, ghost_y = ghost["x"], ghost["y"]
            pacman_x, pacman_y = self.s_w["player_pos"][0], self.s_w["player_pos"][1]

            # Prüfen, ob der Geist genau im Zentrum einer Zelle ist
            if abs(ghost_x - round(ghost_x)) < 0.01 and abs(ghost_y - round(ghost_y)) < 0.01:
                ghost_x, ghost_y = round(ghost_x), round(ghost_y)

                # Liste für gültige Bewegungen, die vom Pac-Man wegführen
                best_moves = []
                max_distance = -1

                for dx, dy in directions:
                    next_x, next_y = ghost_x + dx, ghost_y + dy

                    # Prüfen, ob das Ziel gültig ist (keine Wand)
                    if (
                            0 <= next_x < len(self.pacman_field[0]) and
                            0 <= next_y < len(self.pacman_field) and
                            self.pacman_field[next_y][next_x] != 1
                    ):
                        # Abstand zum Pac-Man berechnen
                        distance = math.sqrt((next_x - pacman_x) ** 2 + (next_y - pacman_y) ** 2)
                        if distance > max_distance:
                            best_moves = [(dx, dy)]
                            max_distance = distance
                        elif distance == max_distance:
                            best_moves.append((dx, dy))

                # Zufällige Bewegung aus den besten Optionen wählen
                if best_moves:
                    move = random.choice(best_moves)
                    ghost["move"] = [move[0], move[1]]

            # Geist sanft bewegen
            ghost["x"] += ghost["speed"] / 2 / self.PIXEL * ghost["move"][0]
            ghost["y"] += ghost["speed"] / 2 / self.PIXEL * ghost["move"][1]

            # Zentriere den Geist erneut, falls nahe genug
            if abs(ghost["x"] - round(ghost["x"])) < 0.01:
                ghost["x"] = round(ghost["x"])
            if abs(ghost["y"] - round(ghost["y"])) < 0.01:
                ghost["y"] = round(ghost["y"])

            # Sicherstellen, dass die Geisterkoordinaten innerhalb des Spielfelds bleiben
            if ghost["x"] < 0:
                ghost["x"] = 0
            elif ghost["x"] >= len(self.pacman_field[0]):
                ghost["x"] = len(self.pacman_field[0]) - 1

            if ghost["y"] < 0:
                ghost["y"] = 0
            elif ghost["y"] >= len(self.pacman_field):
                ghost["y"] = len(self.pacman_field) - 1

            if round(pacman_x) == round(ghost["x"]) and round(pacman_y) == round(ghost["y"]):
                ghost["x"] = 9.0
                ghost["y"] = 7.0
                self.s_w["zaehler"] += 100
    # Pacman geht durch Tunnel
    def tunnel_logik(self):
        if self.s_w["player_pos"][0] >= len(self.pacman_field[0]) - 1 and self.s_w["direction"] == "Right":
            self.s_w["player_pos"][0] = 0
        elif self.s_w["player_pos"][0] < 0 and self.s_w["direction"] == "Left":
            self.s_w["player_pos"][0] = len(self.pacman_field[0]) - 1
    # Pacman sammelt Punkte oder Power-Ups
    def punkte_sammeln(self):
        grid_x, grid_y = int(round(self.s_w["player_pos"][0])), int(round(self.s_w["player_pos"][1]))
        if  self.pacman_field[grid_y][grid_x] == 2:
            self.s_w["zaehler"] += 10
            self.pacman_field[grid_y][grid_x] = 0

        if  self.pacman_field[grid_y][grid_x] == 3:
            self.s_w["power_up"] = True
            self.s_w["zaehler"] += 10
            self.pacman_field[grid_y][grid_x] = 0
    # Kollision Check
    def check_collision(self):
        for ghost in ghosts:
            if int(round(self.s_w["player_pos"][0])) == round(ghost["x"]) and int(round(self.s_w["player_pos"][1])) == round(
                    ghost["y"]):
                if self.s_w["power_up"] == False:
                    ausgabetext = "Game Over!"
                    font = pygame.font.SysFont(None, self.PIXEL)
                    text = font.render(ausgabetext, True, farben["ROT"])
                    text_breite = text.get_width()
                    self.screen.blit(text, [(self.screen_WIDTH / 2) - text_breite / 2, self.PIXEL / 4])
                    self.save_highscore()
    # Highscore Auslesen
    def read_highscore(self):
        with open("highscore.txt", "r") as datei:
            current_highscore = int(datei.readline().strip())
        return current_highscore
    # Schauen, ob alle Punkte eingesammelt sind
    def check_finish(self):
        Init = 0
        for row in range(len(self.pacman_field)):
            for col in range(len(self.pacman_field[row])):
                if self.pacman_field[row][col] == 2:
                    Init += 1

        if Init == 0:
            self.save_highscore(self.s_w, ghosts)
    # Highscore speichern
    def save_highscore(self):
        self.s_w["move"] = [0, 0]
        for ghost in ghosts:
            ghost["move"] = [0, 0]
        # print("Finish")
        current_highscore = self.read_highscore()

        if self.s_w["zaehler"] > current_highscore:
            with open("highscore.txt", "w") as datei:
                datei.write(str(self.s_w["zaehler"]))  # Neuer Highscore wird gespeichert
            print("New Highscore!")
    # Highscore anzeigen
    def display_highscore(self):
        current_highscore = str(self.read_highscore())
        font = pygame.font.SysFont(None, self.PIXEL)
        text = font.render(f"Highscore: {current_highscore}", True, farben["WEISS"])
        self.screen.blit(text, [self.PIXEL, self.PIXEL / 4])
    # Score anzeigen
    def display_score(self):
        font = pygame.font.SysFont(None, self.PIXEL)
        text = font.render(f"Score: {self.s_w['zaehler']}", True, farben["WEISS"])
        text_breite = text.get_width()
        self.screen.blit(text, [self.screen_WIDTH - text_breite - self.PIXEL, self.PIXEL / 4])
        
    def pacman_spiel(self):
            pause = False
            

            # Pygame initialisieren
            pygame.init()
            
            pygame.display.set_caption("Pac-Man")
            clock = pygame.time.Clock()
            
            # Spieldurchlauf
            frame_count= 0 # Counter für Frames
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.s_w["next_direction"] = "Up"
                        elif event.key == pygame.K_DOWN:
                            self.s_w["next_direction"] = "Down"
                        elif event.key == pygame.K_RIGHT:
                            self.s_w["next_direction"] = "Right"
                        elif event.key == pygame.K_LEFT:
                            self.s_w["next_direction"] = "Left"
                        elif event.key == pygame.K_p:
                            pause=True

                if(pause==True):
                    running=False
                    while(pause):
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    pause=False
                                    running=True
                                    
                                    
                self.screen.fill(self.farbe["SCHWARZ"])
                 # Zeichne Spielfeld
                self.draw_field()
                # Zeichne Pacman
                self.draw_pacman()
                # Zeichne Geister
                self.draw_ghosts()
                # Pacman schaut, ob er einen Richtungswechsel machen kann
                self.pacman_bewegung()
                # Pacman sammelt Punkte und Power-Up
                self.punkte_sammeln()
                # Power Up falls Pacman Power Up isst
                
                # Pacman geht durch Tunnel
                self.tunnel_logik()
                # Schwarzer Hintergrund
                
               
                # Ist das Spiel fertig?
                self.check_finish()
                # Highscore anzeigen
                self.display_highscore()
                # Score anzeigen
                self.display_score()
                self.power_up_check()
                # Kollisions Logik zwischen Pacman und Geister
                self.check_collision()  # Kollision Check
                # Aktualisieren
                pygame.display.flip()
                # Clock Frames
                clock.tick(60)
                # Frame Zähler
                frame_count += 1
                

            pygame.quit()
            sys.exit()

        
        # Pacman Spiel starten
        
if __name__ == "__main__":
    farben = {
                "SCHWARZ": (0, 0, 0),
                "WEISS": (255, 255, 255),
                "BLAU": (0, 0, 255),
                "GELB": (255, 255, 0),
                "ROT": (255, 0, 0),
                "PINK": (255, 105, 180),
                "ORANGE": (255, 165, 0),
            }
    
    s_w = {
                "player_pos": [9.0, 9.0],  # [x, y]
                "move": [0, 0],  # [move_x, move_y]
                "speed": 2,
                "angle": 0,
                "mund": 0,
                "schritt": 0,
                "direction": None,
                "next_direction": None,
                "zaehler": 0,
                "power_up": False
            }
            # Geister Werte
    ghosts = [
                {"x": 9.0, "y": 7.0, "color": farben["ROT"], "speed": 2, "move": [0, 0]},
                {"x": 10.0, "y": 7.0, "color": farben["PINK"], "speed": 2, "move": [0, 0]},
                {"x": 8.0, "y": 7.0, "color": farben["BLAU"], "speed": 2, "move": [0, 0]},
                {"x": 9.0, "y": 6.0, "color": farben["ORANGE"], "speed": 2, "move": [0, 0]},
            ]
        # Geister Bilder
    ghost_img = {
                farben["ROT"]: pygame.image.load("./assets/red_ghost.png"),
                farben["PINK"]: pygame.image.load("./assets/pink_ghost.png"),
                farben["BLAU"]: pygame.image.load("./assets/blue_ghost.png"),
                farben["ORANGE"]: pygame.image.load("./assets/orange_ghost.png"),
                "POWER_UP": pygame.image.load("./assets/powerup.png"),  # Power-Up-Bild
            }
    for color, image in ghost_img.items():
        ghost_img[color] = pygame.transform.scale(image, (40 // 2, 40 // 2)) #KONSTANTEN 40
        
    PacManGameMain = PacManGame(farben,s_w,ghosts,ghost_img)