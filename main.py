import math
import pygame
import sys
import random

#Pacman Spiel
if __name__ == "__main__":

    # Hauptmenü anzeigen
    def hauptmenu():
        pygame.init()
        menu_breite = 600
        menu_hoehe = 400
        screen = pygame.display.set_mode((menu_breite, menu_hoehe))
        pygame.display.set_caption("Pac-Man Hauptmenü")
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 50)
        optionen = ["Spiel starten", "Highscores anzeigen", "Spiel beenden"]

        auswahl = 0  # Aktuelle Auswahl
        running = True

        while running:
            screen.fill((0, 0, 0))  # Schwarzer Hintergrund

            # Menüoptionen anzeigen
            for index, text in enumerate(optionen):
                if index == auswahl:
                    label = font.render(text, True, (255, 255, 0))  # Gelbe Schrift für die aktuelle Auswahl
                else:
                    label = font.render(text, True, (255, 255, 255))  # Weiße Schrift
                screen.blit(label, (menu_breite // 2 - label.get_width() // 2, 100 + index * 60))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        auswahl = (auswahl - 1) % len(optionen)
                    elif event.key == pygame.K_DOWN:
                        auswahl = (auswahl + 1) % len(optionen)
                    elif event.key == pygame.K_RETURN:
                        if auswahl == 0:  # Spiel starten
                            running = False
                        elif auswahl == 1:  # Highscores anzeigen
                            anzeigen_highscores()
                        elif auswahl == 2:  # Spiel beenden
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
            clock.tick(30)
    # Highscores anzeigen
    def anzeigen_highscores():
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Highscores")
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 50)
        small_font = pygame.font.SysFont(None, 35)

        # Read the highscore with a comma at the end
        try:
            with open("highscore.csv", "r") as datei:
                line = datei.readline().strip()
                if line.endswith(","):
                    line = line[:-1]  # Remove the trailing comma
                highscore = int(line) if line.isdigit() else 0
        except FileNotFoundError:
            highscore = 0

        running = True

        while running:
            screen.fill((0, 0, 0))  # Schwarzer Hintergrund

            # Highscore label
            label = font.render("Highscore", True, (255, 255, 255))
            screen.blit(label, (300 - label.get_width() // 2, 100))

            # Highscore value
            score_label = small_font.render(f"Score: {highscore}", True, (255, 255, 0))
            screen.blit(score_label, (300 - score_label.get_width() // 2, 200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.flip()
            clock.tick(30)
    # Spielfeld (0: leer, 1: Wand, 2: Punkt, 3: Power-Up)
    def read_field():
        with open("pacman_field.txt", "r") as datei:
            text = datei.read()
            matrix = []
            row = []
            for zeichen in text:
                if zeichen in "0123":
                    row.append(int(zeichen))
                elif zeichen == "\n":
                    matrix.append(row)
                    row = []
            if row:
                matrix.append(row)
            return matrix
    # Farben Werte
    def farben():
        return {
            "SCHWARZ": (0, 0, 0),
            "WEISS": (255, 255, 255),
            "BLAU": (0, 0, 255),
            "GELB": (255, 255, 0),
            "ROT": (255, 0, 0),
            "PINK": (255, 105, 180),
            "ORANGE": (255, 165, 0),
        }
    # Start Werte
    def start_werte():
        return {
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
    def ghosts(farben):
        return [
            {"x": 9.0, "y": 7.0, "color": farben["ROT"], "speed": 2, "move": [0, 0]},
            {"x": 10.0, "y": 7.0, "color": farben["PINK"], "speed": 2, "move": [0, 0]},
            {"x": 8.0, "y": 7.0, "color": farben["BLAU"], "speed": 2, "move": [0, 0]},
            {"x": 9.0, "y": 6.0, "color": farben["ORANGE"], "speed": 2, "move": [0, 0]},
        ]
    # Geister Bilder
    def ghost_images(farben, PIXEL):
        ghost_img = {
            farben["ROT"]: pygame.image.load("./assets/red_ghost.png"),
            farben["PINK"]: pygame.image.load("./assets/pink_ghost.png"),
            farben["BLAU"]: pygame.image.load("./assets/blue_ghost.png"),
            farben["ORANGE"]: pygame.image.load("./assets/orange_ghost.png"),
            "POWER_UP": pygame.image.load("./assets/powerup.png"),  # Power-Up-Bild
        }
        for color, image in ghost_img.items():
            ghost_img[color] = pygame.transform.scale(image, (PIXEL // 2, PIXEL // 2))
        return ghost_img

    # PACMAN SPIEL !!!
    def pacman_spiel(PIXEL, pacman_field, farben, s_w, ghosts, ghost_images):

        SCREEN_WIDTH = len(pacman_field[0]) * PIXEL
        SCREEN_HEIGHT = len(pacman_field) * PIXEL

        # Pygame initialisieren
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        clock = pygame.time.Clock()

        # Zeichne Spielfeld
        def draw_field():
            for row in range(len(pacman_field)):
                for col in range(len(pacman_field[row])):
                    x = col * PIXEL
                    y = row * PIXEL
                    if pacman_field[row][col] == 1:  # Wand
                        pygame.draw.rect(screen, farben["BLAU"], (x, y, PIXEL, PIXEL))
                    elif pacman_field[row][col] == 2:  # Punkt
                        pygame.draw.circle(screen, farben["WEISS"], (x + PIXEL / 2, y + PIXEL / 2), PIXEL / 8)
                    elif pacman_field[row][col] == 3:  # Power-Up
                        pygame.draw.circle(screen, farben["WEISS"], (x + PIXEL / 2, y + PIXEL / 2), PIXEL / 4)
        # Zeichne Pacman
        def draw_pacman(x, y, ang, mouth):

            # Pacmans Mund bewegt sich
            if s_w["move"] != [0, 0]:
                s_w["schritt"] += 1
                s_w["mund"] = abs(math.sin(math.pi / PIXEL * s_w["schritt"] * 2)) * 45

            # Pacman zeichnen
            surface_1 = pygame.Surface((PIXEL, PIXEL), pygame.SRCALPHA)
            surface_2 = pygame.Surface((PIXEL, PIXEL), pygame.SRCALPHA)
            pygame.draw.circle(
                surface_1,
                farben["GELB"],
                (PIXEL / 2, PIXEL / 2),
                PIXEL / 3,
                draw_top_right=True, draw_top_left=True
            )
            pygame.draw.circle(
                surface_2,
                farben["GELB"],
                (PIXEL / 2, PIXEL / 2),
                PIXEL / 3,
                draw_bottom_right=True, draw_bottom_left=True
            )
            rotated_surface_1 = pygame.transform.rotate(surface_1, ang + mouth)
            rotated_surface_2 = pygame.transform.rotate(surface_2, ang - mouth)

            rotated_rect_1 = rotated_surface_1.get_rect(
                center=(int(x * PIXEL + PIXEL / 2), int(y * PIXEL + PIXEL / 2))
            )
            rotated_rect_2 = rotated_surface_2.get_rect(
                center=(int(x * PIXEL + PIXEL / 2), int(y * PIXEL + PIXEL / 2))
            )

            screen.blit(rotated_surface_1, rotated_rect_1.topleft)
            screen.blit(rotated_surface_2, rotated_rect_2.topleft)
        # Geister Zeichnen
        def draw_ghosts(ghosts, power_up_active, ghost_images):
            for ghost in ghosts:
                if power_up_active:
                    # Power-Up-Bild verwenden
                    ghost_image = ghost_images["POWER_UP"]
                else:
                    # Normales Bild basierend auf der Farbe des Geists
                    ghost_image = ghost_images[ghost["color"]]

                # Geisterposition berechnen
                ghost_x = ghost["x"] * PIXEL + PIXEL / 4
                ghost_y = ghost["y"] * PIXEL + PIXEL / 4

                # Geist zeichnen
                screen.blit(ghost_image, (ghost_x, ghost_y))
        # Pacman schaut, ob er einen Richtungswechsel machen kann
        def pacman_bewegung():
            if abs(s_w["player_pos"][0] - round(s_w["player_pos"][0])) < 0.01 and abs(
                    s_w["player_pos"][1] - round(s_w["player_pos"][1])) < 0.01:
                grid_x, grid_y = int(round(s_w["player_pos"][0])), int(round(s_w["player_pos"][1]))

                if s_w["next_direction"]:
                    if s_w["next_direction"] == "Up" and pacman_field[grid_y - 1][grid_x] != 1:
                        s_w["direction"] = s_w["next_direction"]
                        s_w["angle"] = 90
                    elif s_w["next_direction"] == "Down" and pacman_field[grid_y + 1][grid_x] != 1:
                        s_w["direction"] = s_w["next_direction"]
                        s_w["angle"] = -90
                    elif s_w["next_direction"] == "Right" and pacman_field[grid_y][grid_x + 1] != 1:
                        s_w["direction"] = s_w["next_direction"]
                        s_w["angle"] = 0
                    elif s_w["next_direction"] == "Left" and pacman_field[grid_y][grid_x - 1] != 1:
                        s_w["direction"] = s_w["next_direction"]
                        s_w["angle"] = 180

                if s_w["direction"] == "Up" and pacman_field[grid_y - 1][grid_x] != 1:
                    s_w["move"][:] = [0, -s_w["speed"] / PIXEL]
                elif s_w["direction"] == "Down" and pacman_field[grid_y + 1][grid_x] != 1:
                    s_w["move"][:] = [0, s_w["speed"] / PIXEL]
                elif s_w["direction"] == "Right" and pacman_field[grid_y][grid_x + 1] != 1:
                    s_w["move"][:] = [s_w["speed"] / PIXEL, 0]
                elif s_w["direction"] == "Left" and pacman_field[grid_y][grid_x - 1] != 1:
                    s_w["move"][:] = [-s_w["speed"] / PIXEL, 0]
                else:
                    s_w["move"][:] = [0, 0]

            s_w["player_pos"][0] += s_w["move"][0]
            s_w["player_pos"][1] += s_w["move"][1]
        # Power-Up: Ja oder Nein?
        def power_up_check(s_w, power_up_timer, run_away, ghosts, geister_bewegung_1, geister_bewegung_2):
            if s_w["power_up"]:
                power_up_timer += 1
                run_away(ghosts, s_w["player_pos"], pacman_field, PIXEL)

                if power_up_timer > 300:  # Power-Up endet
                    s_w["power_up"] = False
                    power_up_timer = 0
            else:
                wahl = random.choice([1, 2, 3])
                if wahl == 1:
                    geister_bewegung_1(ghosts, pacman_field, PIXEL)
                else:
                    geister_bewegung_2(ghosts, s_w["player_pos"], pacman_field, PIXEL)
            return power_up_timer
        # Geister können sich in eine random Richtung bewegen, oder ...
        def geister_bewegung_1(ghosts, pacman_field, PIXEL):
            for ghost in ghosts:
                x = round(ghost["x"])
                y = round(ghost["y"])

                if abs(ghost["x"] - x) < 0.01 and abs(ghost["y"] - y) < 0.01:
                    ghost["x"], ghost["y"] = x, y

                    valid_moves = []
                    if y - 1 >= 0 and pacman_field[y - 1][x] != 1:  # Up
                        valid_moves.append([0, -1])
                    if y + 1 < len(pacman_field) and pacman_field[y + 1][x] != 1:  # Down
                        valid_moves.append([0, 1])
                    if x + 1 < len(pacman_field[0]) and pacman_field[y][x + 1] != 1:  # Right
                        valid_moves.append([1, 0])
                    if x - 1 >= 0 and pacman_field[y][x - 1] != 1:  # Left
                        valid_moves.append([-1, 0])

                    # Wähle zufällige gültige Bewegung
                    if valid_moves:
                        ghost["move"] = random.choice(valid_moves)

                # Sanfte Bewegung basierend auf der aktuellen Richtung
                ghost["x"] += ghost["move"][0] * (ghost["speed"] / PIXEL)
                ghost["y"] += ghost["move"][1] * (ghost["speed"] / PIXEL)
        # ... Geister verfolgen Pacman
        def geister_bewegung_2(ghosts, pacman_pos, pacman_field, PIXEL):
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Bewegungsrichtungen
            for ghost in ghosts:
                ghost_x, ghost_y = ghost["x"], ghost["y"]
                if abs(ghost_x - round(ghost_x)) < 0.01 and abs(ghost_y - round(ghost_y)) < 0.01:
                    ghost_x, ghost_y = round(ghost_x), round(ghost_y)
                    queue = [(ghost_x, ghost_y)]
                    visited = set(queue)
                    parent = {}

                    while queue:
                        current_x, current_y = queue.pop(0)
                        for dx, dy in directions:
                            neighbor_x, neighbor_y = current_x + dx, current_y + dy
                            if (
                                    0 <= neighbor_x < len(pacman_field[0])
                                    and 0 <= neighbor_y < len(pacman_field)
                                    and pacman_field[neighbor_y][neighbor_x] != 1
                                    and (neighbor_x, neighbor_y) not in visited
                            ):
                                queue.append((neighbor_x, neighbor_y))
                                visited.add((neighbor_x, neighbor_y))
                                parent[(neighbor_x, neighbor_y)] = (current_x, current_y)
                                if (neighbor_x, neighbor_y) == (int(round(pacman_pos[0])), int(round(pacman_pos[1]))):
                                    queue = []  # Ziel gefunden
                    next_position = (ghost_x, ghost_y)
                    current_position = (int(round(pacman_pos[0])), int(round(pacman_pos[1])))

                    while current_position in parent:
                        next_position = current_position
                        current_position = parent[current_position]
                    next_x, next_y = next_position
                    ghost["move"] = [(next_x - ghost_x), (next_y - ghost_y)]

                ghost["x"] += ghost["move"][0] * (ghost["speed"] / PIXEL) # Bewegung
                ghost["y"] += ghost["move"][1] * (ghost["speed"] / PIXEL)
                ghost["x"] = max(0, min(len(pacman_field[0]) - 2, ghost["x"])) # Sicherstellen, dass die Geister innerhalb des Spielfelds bleiben
                ghost["y"] = max(0, min(len(pacman_field) - 2, ghost["y"]))
        # Geister rennen bei Power-Up weg
        def run_away(ghosts, pacman_pos, pacman_field, PIXEL):
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Bewegungsrichtungen: oben, unten, links, rechts

            for ghost in ghosts:
                ghost_x, ghost_y = ghost["x"], ghost["y"]
                pacman_x, pacman_y = pacman_pos[0], pacman_pos[1]

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
                                0 <= next_x < len(pacman_field[0]) and
                                0 <= next_y < len(pacman_field) and
                                pacman_field[next_y][next_x] != 1  # Keine Wand
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

                # Bewegung ausführen und prüfen, ob die neue Position gültig bleibt
                new_x = ghost["x"] + ghost["speed"] / 2 / PIXEL * ghost["move"][0]
                new_y = ghost["y"] + ghost["speed"] / 2 / PIXEL * ghost["move"][1]

                if (
                        0 <= round(new_x) < len(pacman_field[0]) and
                        0 <= round(new_y) < len(pacman_field) and
                        pacman_field[round(new_y)][round(new_x)] != 1  # Ziel ist keine Wand
                ):
                    ghost["x"] = new_x
                    ghost["y"] = new_y
                else:
                    # Wenn Bewegung ungültig ist, stoppe den Geist
                    ghost["move"] = [0, 0]
        # Pacman geht durch Tunnel
        def tunnel_logik(player_pos, direction, pacman_field):
            if player_pos[0] >= len(pacman_field[0]) - 1 and direction == "Right":
                player_pos[0] = 0
            elif player_pos[0] < 0 and direction == "Left":
                player_pos[0] = len(pacman_field[0]) - 1
        # Pacman sammelt Punkte oder Power-Ups
        def punkte_sammeln(s_w, field):
            grid_x, grid_y = int(round(s_w["player_pos"][0])), int(round(s_w["player_pos"][1]))
            if field[grid_y][grid_x] == 2:
                s_w["zaehler"] += 10
                field[grid_y][grid_x] = 0

            if field[grid_y][grid_x] == 3:
                s_w["power_up"] = True
                s_w["zaehler"] += 10
                field[grid_y][grid_x] = 0
        # Kollision Check
        def check_collision(s_w, ghosts, PIXEL):
            for ghost in ghosts:
                if int(round(s_w["player_pos"][0])) == round(ghost["x"]) and int(round(s_w["player_pos"][1])) == round(
                        ghost["y"]):
                    if s_w["power_up"] == False:
                        ausgabetext = "Game Over!"
                        font = pygame.font.SysFont(None, PIXEL)
                        text = font.render(ausgabetext, True, farben["ROT"])
                        text_breite = text.get_width()
                        screen.blit(text, [(SCREEN_WIDTH / 2) - text_breite / 2, PIXEL / 4])
                        save_highscore(s_w, ghosts)
                        pygame.display.flip()
                        pygame.time.delay(2500)
                        return True
                    elif s_w["power_up"] == True:
                        ghost["x"] = 9.0
                        ghost["y"] = 7.0
                        s_w["zaehler"] += 100

            return False
        # Highscore Auslesen
        def read_highscore():
            try:
                with open("highscore.csv", "r") as datei:
                    line = datei.readline().strip()
                    if line.endswith(","):
                        line = line[:-1]
                    current_highscore = int(line)
                    return current_highscore
            except FileNotFoundError:
                return 0  # Default highscore if file doesn't exist
        # Schauen, ob alle Punkte eingesammelt sind
        def check_finish(s_w, ghosts):
            Init = 0
            for row in range(len(pacman_field)):
                for col in range(len(pacman_field[row])):
                    if pacman_field[row][col] == 2:
                        Init += 1

            if Init == 0:
                s_w["zaehler"] += 200
                save_highscore(s_w, ghosts)
                ausgabetext = "Gewonnen!"
                font = pygame.font.SysFont(None, PIXEL)
                text = font.render(ausgabetext, True, farben["ROT"])
                text_breite = text.get_width()
                screen.blit(text, [(SCREEN_WIDTH / 2) - text_breite / 2, PIXEL / 4])
                save_highscore(s_w, ghosts)
                pygame.display.flip()
                pygame.time.delay(2500)
                return True
            return False
        # Highscore speichern
        def save_highscore(s_w, ghosts):
            s_w["move"] = [0, 0]
            for ghost in ghosts:
                ghost["move"] = [0, 0]

            current_highscore = read_highscore()

            if s_w["zaehler"] > current_highscore:
                with open("highscore.csv", "w") as datei:
                    datei.write(f"{s_w['zaehler']},")
                print("New Highscore!")
        # Highscore anzeigen
        def display_highscore(farben):
            current_highscore = str(read_highscore())
            font = pygame.font.SysFont(None, PIXEL)
            text = font.render(f"Highscore: {current_highscore}", True, farben["WEISS"])
            screen.blit(text, [PIXEL, PIXEL / 4])
        # Score anzeigen
        def display_score():
            font = pygame.font.SysFont(None, PIXEL)
            text = font.render(f"Score: {s_w['zaehler']}", True, farben["WEISS"])
            text_breite = text.get_width()
            screen.blit(text, [SCREEN_WIDTH - text_breite - PIXEL, PIXEL / 4])

        # Spieldurchlauf
        power_up_timer = 0  # Timer für den Power-Up Zustand
        frame_count = 0  # Counter für
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        s_w["next_direction"] = "Up"
                    elif event.key == pygame.K_DOWN:
                        s_w["next_direction"] = "Down"
                    elif event.key == pygame.K_RIGHT:
                        s_w["next_direction"] = "Right"
                    elif event.key == pygame.K_LEFT:
                        s_w["next_direction"] = "Left"

            # Pacman schaut, ob er einen Richtungswechsel machen kann
            pacman_bewegung()
            # Pacman sammelt Punkte und Power-Up
            punkte_sammeln(s_w, pacman_field)
            # Power Up falls Pacman Power Up isst
            power_up_timer = power_up_check(s_w, power_up_timer, run_away, ghosts, geister_bewegung_1, geister_bewegung_2)
            # Pacman geht durch Tunnel
            tunnel_logik(s_w["player_pos"], s_w["direction"], pacman_field)
            # Schwarzer Hintergrund
            screen.fill(farben["SCHWARZ"])
            # Zeichne Spielfeld
            draw_field()
            # Zeichne Pacman
            draw_pacman(s_w["player_pos"][0], s_w["player_pos"][1], s_w["angle"], s_w["mund"])
            # Zeichne Geister
            draw_ghosts(ghosts, s_w["power_up"], ghost_images)
            # Highscore anzeigen
            display_highscore(farben)
            # Score anzeigen
            display_score()
            # Kollisions Logik zwischen Pacman und Geister
            if check_collision(s_w, ghosts, PIXEL):  # Kollision Check
                return  # Return to main menu
            # Ist das Spiel fertig?
            if check_finish(s_w, ghosts):
                return  # Return to main menu
            # Aktualisieren
            pygame.display.flip()
            # Clock Frames
            clock.tick(60)
            # Frame Zähler
            frame_count += 1

        pygame.quit()
        sys.exit()
    # Raster Grösse
    PIXEL = 40
    # Pacman Spiel starten
    while True:
        hauptmenu()
        pacman_spiel(
            PIXEL,
            read_field(),
            farben(),
            start_werte(),
            ghosts(farben()),
            ghost_images(farben(),PIXEL)
        )