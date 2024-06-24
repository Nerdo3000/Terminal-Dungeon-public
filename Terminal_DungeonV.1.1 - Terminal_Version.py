"""Hier werden die Module random (Für Zufallszahlen) und das Modul math (Für mathe) importiert"""
import random
import math


"Hier werde alle Emojis defienert/festegelegt, die Später gebraucht werden. Das macht es einfacher, einzelne Emojis zu ändern, da man nun nicht ALLE verwendungen dieses Emojis ändern muss, sondern nur die Variable."""
chr_hole =      "🕳️"#   "●"
chr_wall =      "🧱"#⬛"#   "▩"
chr_None =      "  "#   " "
chr_l_star =    "✨"#   "★"⭐
chr_b_star =    "🌟"#   "⚝"
chr_home =      "🏠"#   "⌂"
chr_play =      "👩"#   "♀︎"
chr_enem =      "💀"#   "☿"
chr_key =       "🗝 "
chr_spaceing =  "" 
chr_pet =       "🐢"
chr_portal =    "🌀"
chr_pin =       "📛"
chr_dia =       "💎"
chr_play_options = ["👧","👦","👨","👩","👴","👵","👶","👸","👼","🧑","🧒","🧓","🧔"]
chr_fauna = ["🐀","🐁","🐂","🐃","🐄","🐅","🐆",
             "🐇","🐈","🐉","🐊","🐋","🐌","🐍",
             "🐎","🐏","🐐","🐑","🐒","🐓","🐕",
             "🐖","🐘","🐢","🐤","🦖","🐦","🐧",
             "🐩","🐪","🐫","🦃","🦆","🦅","🦌",
             "🦍","🦏","🦔","🦕"]
chr_flora = ["🌲","🌳","🌴","🌵","🌷","🌹","🌺","🌻","🌾","🥀","🍄"]
chr_arrows = ["⇧ ", "⇦ ", "⇩ ", "⇨ "]


"""Diese Liste Spichert die Daten für den KI "pathfinding" (Wegfinder) Algorithmus."""
path_grid = []


def generate_tile_area(tile, area):
    """Hier wird eine Funktion definiert, die eine Fläche (Eigentlich eine Prozentzahl(area), die angibt, wie viel Prozent des Level gefüllt werden soll) mit dem Angegebenen Block(tile) füllt."""
    global map_data
    for i in range(int(area)): 
        y = random.randint(1, map_y-1)
        x = random.randint(1, map_x-1)
        if map_data[y][x] == chr_None:
            map_data[y][x] = tile
def generate_tile_amt(tile, amt, pos=False):
    """Hier wird eine Funktion definiert, die eine Anzahl(amt) an Blöcken mit dem angegebenen Block(tile) füllt."""
    global map_data
    while not str(map_data).count(tile) >= amt:
        y = random.randint(1, map_y-1)
        x = random.randint(1, map_x-1)
        if map_data[y][x] == chr_None:
            map_data[y][x] = tile
            if pos: return (y,x)


def generate_map():
    """Hier wird das Level generiert.
    1. Die Rechteckige Wand des Levels wird kreiert.
    2. Die Löcher werden Zufällig eingefügt. (30% des Levels sollen gefüllt werden.)
    3. Die Portale werden Zufällig eingefügt. (0.4% des Levels sollen gefüllt werden.)
    4. Die kleinen Sterne werden Zufällig eingefügt. (10% des Levels sollen gefüllt werden.)
    5. Die großen Sterne werden Zufällig eingefügt. (2.5% des Levels sollen gefüllt werden.)
    6. 1 Diamant wird generiert
    7. 1 Haus wird generiert
    8. Die Schlüssel werden gerneriert
    9. Die Spieler und Gegner Positionen werden frei gemacht (Damit der Spieler nicht in einem Loch startet)
    10.Die Pathgrid wird generiert (Diese dient wie eine Schablone, die genutz wird um die Player Grid zu generieren)
    11.Die Player Grid wird generiert
    12.Mit hilfe der Player Grid wird Überprüft, ob:
        a) Die Schlüssel erreichbar sind
        b) Das Haus erreichbar ist
        c) Der Gegner den Spieler erreichen kann
        -> Wenn eine dieser Bedingungen nicht erfüllt ist, wird ein Neues Level generiert (generate_map wird erneut aufgerufen)
    """
    global map_data,path_grid

    #Schrit 1
    map_data[0] = [chr_wall]*map_x
    for i in range(1, map_y-1):
        map_data[i] = [chr_wall]+[chr_None]*(map_x-2)+[chr_wall]
    map_data[map_y-1] = [chr_wall]*map_x

    generate_tile_area(chr_hole, (map_x*map_y*0.3))         #Schrit 2
    generate_tile_area(chr_portal, (map_x*map_y*0.004))     #Schrit 3
    generate_tile_area(chr_l_star, (map_x*map_y*0.1))       #Schrit 4
    generate_tile_area(chr_b_star, (map_x*map_y*0.025))     #Schrit 5
    generate_tile_amt(chr_dia, 1)                           #Schrit 6
    home_pos = generate_tile_amt(chr_home, 1, pos=True)     #Schrit 7

    #Schrit 8
    key_pos = []
    while str(map_data).count(chr_key) <= max_keys-1:
        y = random.randint(1, map_y-1)
        x = random.randint(1, map_x-1)
        if map_data[y][x] == chr_None:
            map_data[y][x] = chr_key
            key_pos.append((y,x))

    #Schrit 9
    map_data[1][1] = chr_None
    map_data[map_y-2][map_x-2] = chr_None

    path_grid = (make_pathgrid(map_data))       #Schrit 10
    player_grid = update_pathgrid(path_grid)    #Schrit 11

    #Schrit 12 a)
    keys_reachable = False
    for key in key_pos:
        y = key[0]
        x = key[1]
        if player_grid[y][x] == "#" or player_grid[y][x] == "?":
            keys_reachable = True

    if player_grid[home_pos[0]][home_pos[1]] == "#" or player_grid[home_pos[0]][home_pos[1]] == "?":            #Schrit 12 b)
        generate_map()
    elif player_grid[enemy_pos[1]][enemy_pos[0]] == "#" or player_grid[enemy_pos[1]][enemy_pos[0]] == "?":      #Schrit 12 c)
        generate_map()
    elif keys_reachable:                                                                                        #Schrit 12 a)
        generate_map()


def make_pathgrid(map_):
    """Hier wird die Pathgrid für den Pathfinding Algorithmus Generiert. 
    Dabei wird eine Kopie des Levels erstellt und dann wird jeder block der eine Wand oder ein Loch ist durch ein "#" ersetzt.
    Alle anderen Blöcken werden durch ein "?" ersetzt, dies bedeutet, das sich der Gegner durch diesen Block bewegen könnte."""
    path_grid = copy_nested_list(map_)

    for y in range(map_y):
        for x in range(map_x):
            tile = path_grid[y][x]
            if tile == chr_hole or tile==chr_wall:
                path_grid[y][x] = "#"
            else:
                path_grid[y][x] = "?"
    return path_grid

def update_pathgrid(map_path):
    """Hier wird die Player Grid erstellt, eine Spezifische version der Pathgrid. 
    Die Pathgrid dient wie eine Schablone, hier werden die "?" ausgefüllt mit Richtungs angaben, die zum Spieler führen.
    Zuerst wird hier die "Schablone" kopiert, dann wird die Spieler Position als Start Position genommen.
    Anstat von dem Gegner aus einen Weg zum Spieler zu finden, wird von dem Spieler aus ein Weg für jede erreichbare Position des Levels ermittelt.
    1. Von der Spieler Position ist der Weg ZUM Spieler einfach, der Gegner muss einfach nur da bleiben wo er ist.
    2. Für die Umliegenden 4 Blöcke ist es ebenfalls einfach, von dort aus muss man nur zu dem block aus Schritt 1.
    3. Für die Blöcke, die um die blöcke aus Schritt 2. liegen, ist es ebefalls einfach, von dort aus muss man nur zu den Blöcken aus Schritt 2.
    4. Für die Blöcke, die um die blöcke aus Schritt 3. liegen, ist es ebefalls einfach, von dort aus muss man nur zu den Blöcken aus Schritt 3.
    n. Für die Blöcke, die um die blöcke aus Schritt n-1 liegen, ist es einfach, von dort aus muss man nur zu den Blöcken aus Schritt n-1

    So breitet sich die Fläche immmer Weiter aus, auch um hindernisse, bis irgenwann jeder errichbare Block ausgefüllt ist.

    Visualsiert (Mit Zahlen):
                4
              4 3 4
            4 3 2 3 4
          4 3 2 1 2 3 4
            4 3 2 3 4
              4 3 4
                4

    Visualsiert (Mit den Richtungen):
                ⇩
              ⇨ ⇩ ⇦
            ⇨ ⇩ ⇩ ⇩ ⇦
          ⇨ ⇨ ⇨ ⇩ ⇦ ⇦ ⇦
            ⇨ ⇧ ⇧ ⇧ ⇦
              ⇨ ⇧ ⇦
                ⇧
    
                
    Nun muss der Gegner nur nachschauen, in welche Richtung er von seiner aktuellen Position aus gehen muss, so findet er den Weg zum Spieler."""
    path_grid = copy_nested_list(map_path)

    startX = player_pos[0]
    startY = player_pos[1]
    path_grid[startY][startX] = "0"
    to_do = [(startY, startX)]
    while len(to_do)>0:
        current_pos = (to_do.pop(0))
        for i in range(4):
            dir = (90*i)%360
            if dir == 270: dir=-90
            next_pos = (int(current_pos[0]+ math.cos(math.radians(dir))), int(current_pos[1]+ math.sin(math.radians(dir))))
            if path_grid[next_pos[0]][next_pos[1]]=="?":
                path_grid[next_pos[0]][next_pos[1]] = dir
                to_do.append(next_pos)
    return path_grid


def reset():
    """Alles wird Zurückgesezt. Es wird eine neues Level generiert, die Spielerposition, die vergangenen Züge, die Gesammelten Punkte, Schlüssel und die Hauptschliefe zurückgesetzt."""
    global player_pos, turns, points, main_loop, enemy_pos, keys, max_keys

    player_pos = [1,1]

    enemy_pos = [map_x-2, map_y-2]


    max_keys = (rounds+(mode-1))//mode

    generate_map()

    turns = 0
    keys = 0
    points = 0
    main_loop = True


def user_inputed(user_inputed):
    """Hier wird die Eingabe des Spielers Verarbeitet."""
    global main_loop, player_pos, message
    message = ""
    user_input = str(user_inputed).lower()
    if (user_input == "end") or (user_input == "ende") or (user_input == "exit") or (user_input == "esc"): #Die eingabe beendet das Spiel
        main_loop = False
        print("Spiel Beendet!")
    elif (user_input == "neu"): #Alles wird Zurückgesetzt
        reset()
    elif (user_input == "save") and False: #Das hier war für dass Debugen, um das Aktuelle Level ausgeben zu lassen
        print("P" + str(player_pos))
        print("E" + str(enemy_pos))
        print(map_data)
    elif (user_input == "a"): #Der Spieler bewegt sich nach links
        change_player_pos(0, -1)
    elif (user_input == "d"): #Der Spieler bewegt sich nach rechts
        change_player_pos(0, 1)
    elif (user_input == "s"): #Der Spieler bewegt sich nach unten
        change_player_pos(1, 1)
    elif (user_input == "w"): #Der Spieler bewegt sich nach oben
        change_player_pos(1, -1)
    elif (user_input == chr_None) or (user_input==""): #Der Spieler macht garnichts
        pass
    else: #Sonst ist es eine Ungültige eingabe!
        message = "Ungültige Eingabe!"

def change_player_pos(idx, val):
    """Es wird versucht, den Spieler in die Angegebene Richtung zu bewegen. Dafür wird, das Feld, auf dem der Spieler im nächsten Zug wäre überprüft.
    1. Es ist eine Wand: Der Spieler wird nicht auf das nächste Feld plaziert. Die Nachricht "Da ist eine Wand!" wird ausgegeben.
    2. Es ist ein loch: Der Spieler wird Zurück zum Start geschickt. Die Nachricht "Du bist in ein Loch gefallen! Zurück zum Anfang!" wird ausgegeben.
    3. Es ist ein Portal: Der Spieler an eine Zufällige Position geschickt, das alte Portal wird gelöscht und ein neues wird an einer Zufälligen Position Generiert. 
       Die Nachricht "Du hast ein Portal Gefunden! Du wirst an eine Zufällige Position Geschickt! Du bist jetzt hier: " + chr_pin +"." wird ausgegeben.
    4. Es ist das Haus: Der Spieler hat Gewonnen:
        4.1 Es wird ausgegeben, wie viele Züge der Spieler gebraucht hat und wie viele Punkte er gesammelt hat.
        4.2 Es wird der Score des Spielers berechnet, der Liste hinzugefügt und Zusammen mit dem Highscore ausgegeben.
        4.3 Der Spieler wird gefragt, ob er eine neue Runde anfangen möchte. Dies sind die 3 Möglichen antworten:
            'y' steht für 'yes': Der Spieler will eine neue Runde anfangen. Alles wird zurückgesetzt.
            'n' steht für 'no' : Der Spieler will das Spiel beenden. Die Hauptschleife wird beendet.
            Ungültige Eingabe: Die Funktion rufft sich selbst erneut auf, um erneut nach einer eingabe zu fragen.
    5. Ist keiner der Eben gennanten Fälle eingetreten, so ist der Weg für den Spieler Frei. Seine Position wird geändert.
    6. Unabhängig von den anderen Fällen wird überprüft, ob der Spieler auf ein Sternchen (groß, Klein und Diamant) oder einen Schlüssel getroffen ist, wenn ja wird es/er entfernt und der Spieler bekommt einen Punkt/Schlüssel."""
    global player_pos, main_loop, turns, points, message,rounds, map_x, keys, map_data, chr_play_disp
    tmp_player_pos = (player_pos[:])
    tmp_player_pos[idx] += val
    new_square = (map_data[tmp_player_pos[1]])[tmp_player_pos[0]]
    if new_square == chr_wall:
        message = "Da ist eine Wand!"
    elif new_square == chr_hole:
        player_pos = [1, 1]
        message = "Du bist in ein Loch gefallen! Zurück zum Anfang!"
    elif new_square == chr_portal:
        chr_play_disp = chr_pin
        (map_data[tmp_player_pos[1]])[tmp_player_pos[0]] = chr_None
        player_pos = [random.randint(1, map_x-2), random.randint(1, map_y-2)]
        while ((map_data[player_pos[1]])[player_pos[0]] != chr_None) or math.dist(player_pos, enemy_pos)<2:
            player_pos = [random.randint(1, map_x-2), random.randint(1, map_y-2)]
        message = "Du hast ein Portal Gefunden! Du wirst an eine Zufällige Position Geschickt! Du bist jetzt hier: " + chr_pin +"."
        while str(map_data).count(chr_portal) <= 2:
            y = random.randint(1, map_y-1)
            x = random.randint(1, map_x-1)
            if map_data[y][x] == chr_None:
                map_data[y][x] = chr_portal
    elif new_square == chr_home:
        if keys>=max_keys:
            print("Du hast es Geschafft, du bist nach Hause gekommen!")
            print("Du hast "+ str(turns) + " Züge gebraucht und " + str(points) + " Punkt" + str("e"*(not(points==1))) + " Gesammelt!")
            score = (((points+1)*2)/turns)*100
            scores.append(score)
            print("Dein Score: " + str(score) + "!      Dein Highscore ist: " + str(max(scores)) + "!")
            new_input = input("Willst du eine Neue Runde Anfangen (j/n)? ")
            new_input =  new_input.lower()
            if new_input == "j":
                rounds +=1
                reset()
            elif new_input == "n":
                main_loop = False
                print("Spiel Beendet!")
            else:
                print("Ungültige Eingabe!")
                change_player_pos(idx, val)
        else:
            message = "Du hast erst "+str(keys)+chr_key+" von "+str(max_keys)+chr_key+" eingesammelt!"
    else:
        player_pos[idx] += val
    if new_square == chr_l_star:
        (map_data[tmp_player_pos[1]])[tmp_player_pos[0]] = chr_None
        points += 1
    if new_square == chr_b_star:
        (map_data[tmp_player_pos[1]])[tmp_player_pos[0]] = chr_None
        points += 5
    if new_square == chr_key:
        (map_data[tmp_player_pos[1]])[tmp_player_pos[0]] = chr_None
        keys += 1
    if new_square == chr_dia:
        (map_data[tmp_player_pos[1]])[tmp_player_pos[0]] = chr_None
        points += 25

def print__prolog():
    """Der Prolog/die Erklärung des Spieles wird Ausgegeben."""
    print("Wilkommen bei 'Terminal Dungeon', einem Mininspiel in deiner Kommandozeile!")
    print("Du bist dieser kleine Charackter(" + chr_play + ") und dein Ziel ist es, so schnell wie möglich nach Hause(" + chr_home + ") zu kommen.")
    print("Auf dem Weg kannst du Löchern(" + chr_hole + "), großen Sternchen(" + chr_b_star + ") und kleinen Sternchen(" + chr_l_star + ") begegnen.")
    print("Vermeide Löcher(" + chr_hole + ") und Versuch so viele Sternchen(" + chr_b_star + chr_l_star + ") wie möglich zu sammeln. Große Sternchen(" + chr_b_star + ") bringen mehr Punkte als Kleine.")
    print("Fällst du in ein Loch(" + chr_hole + ") musst du zurück zum Anfang. Es gibt auch Wände(" + chr_wall + "), durch die kannst du nicht durch.")
    print("Um dich durch das Level zu bewegen, kannst du die 'w', 'a', 's' und 'd' Tasten benutzen, du wirst nach jedem Zug aufgefordert, eine Eingabe zu machen und enter zu drücken!")
    print("Willst du das Spiel beenden, dann schreibe einfach 'exit', kannst du das Level nicht schaffen, schreibe 'neu'.")
    print("Versuche in so wenig Zügen wie möglich zum Ziel(" + chr_home + ") zu kommen!")
    print("Doch bevor du das Haus(" + chr_home + ") betreten kannst, musst du alle Schlüsel(" + chr_key + ") eingesammelt haben.")
    print("Außerdem gibt es einen Gegner(" + chr_enem + "), dieser wird dich Verfolgen! Wenn du dich von ihm berühren lässt, stirbst dU!")
    print("Wenn du bereit bist, drücke Enter!")
    input()
def print__map_and_player(map_x, map_y, map_data, player_pos):
    """Das Level und der Spieler werden auf dem Bildschirm ausgegeben"""

    #Das hier ist für Debug Zwecke, anstat das Level auszugeben, wird die Pathgrid ausgegeben.
    """
    for y in range(map_y):
        for x in range(map_x):
            if player_pos == [x, y]:
                print(chr_play, end=chr_spaceing)
            elif enemy_pos == [x, y]:
                print(chr_enem, end=chr_spaceing)
            else:
                tile = (player_grid[y])[x]
                if tile != "#" and tile != "?":
                    m = chr_arrows[(int(tile))//90]
                else:
                    m = tile + " "
                print(m, end=chr_spaceing)
        print()
    """
    for y in range(map_y):
        for x in range(map_x):
            if player_pos == [x, y]:
                print(chr_play_disp, end=chr_spaceing)
            elif enemy_pos == [x, y]:
                print(chr_enem, end=chr_spaceing)
            else:
                print((map_data[y])[x], end=chr_spaceing)
        print()
    #"""
def print__charakter_options():
    "Hier wird der Spieler gefragt, welche Spielfigur er Wählen möchte. Er hat 13 zur auswahl."
    global chr_play
    print("Wähle deine Spielfigur:")
    for c in chr_play_options:
        print(c, end="   ")
    print()
    for n in range(1, len(chr_play_options)+1):
        print(n, end=(" "*(5-len(str(n)))))
    print()
    n = (input("Schreibe die Zahl der Spielfigur, die du benutzen möchtest: "))
    num = list(range(1,14))
    for i in range(0,13):
        num[i] = str(num[i])
    if n in num:
        chr_play = chr_play_options[int(n)-1]
        print()
        print()
        print()
        print()
        print()
    else:
        print("Ungültige Eingabe!")
        print__charakter_options()
def print__ask_for_mode():
    """Hier wird der Spieler gefragt, welchen modus er wählen möchte. Es werden Einfach, Normal und Schwer angeboten, jedoch gibt es einen "Geheimen" herr_sellung modus"""
    global mode
    print("Welchen Schwierigkeitsgrad möchtest du Wählen: Einfach, Normal oder Schwer?")
    awnser = input().lower()
    if awnser == "einfach":
        mode = 7
        print()
        print()
    elif awnser == "normal":
        mode = 3
        print()
        print()
    elif awnser == "schwer":
        mode = 1
        print()
        print()
    elif awnser == "herr_sellung":
        mode = 0.5
        print()
        print()
    else:
        print("Ungültige Eingabe!")
        print__ask_for_mode()
def print__ask_for_map_size():
    """Hier wird der Spieler gefragt, wie groß das Level sein soll."""
    global map_x, map_y
    print("Wie Groß soll das Level sein? Klein, Normal, groß oder SEHR GROß(Nicht Empfohlen)?")
    inp = input()
    inp = inp.lower()
    if inp == "klein":
        map_x = 10
        map_y = 10
    elif inp == "normal":
        map_x = 50
        map_y = 15
    elif inp == "groß":
        map_x = 80
        map_y = 30
    elif inp == "sehr groß":
        map_x = 100
        map_y = 50
    else:
        print("Ungültige Eingabe!")
        print__ask_for_map_size()

def copy_nested_list(list):
    """Da wir "nested lists" (Verschattelte Listen) benutzen, um das Level zu Speichern, müssen wir diese Funktion nutzten, um diese Listen zu Kopieren.
    Dies hängt damit zusammen, wie Python eine Verschattelte Liste Speichert. Angenommen, wie hätten die Liste L=[[2, 3], [4, 5]].
    Die Listen [2, 3] und [4, 5] werden als eigene Objekte gespeichert, in der liste "L" werden die Referenzen zu diesen sub listen gespeichert.
    Würden wir eine Neue liste L2=L[:] machen, dann würden nicht die sub-listen Kopiert werden, sondern nur die REFERENZEN zu diesen sub-listen.
    Würden wir dann in "L2" etwas verändern, würde das die sub-liste verändern und somit auch "L". Deswegen müssen wir diese Funktion nutzen.
    
    Sie Funktioniert Folgendermaßen: Die einzelnen werte der Sub-listen werden kopiert, und in eine Neue Liste eingefügt, 
    somit werden neue Objekte erzeugt, die unabhängig von der Orginal liste sind."""
    new_list = []
    for i in list:
        m = []
        for j in i:
            m.append(j)
        new_list.append(m)
    return new_list

def enemy_turn():
    """Hier bewegt sich der Gegner, indem er in der Player Grid nachschaut, in welche richtung er laufen muss."""
    global enemy_pos
    dir = player_grid[enemy_pos[1]][enemy_pos[0]]
    if dir=="#" or dir=="?": return
    enemy_pos[0] += int(math.sin(math.radians(int(dir)+180)))
    enemy_pos[1] += int(math.cos(math.radians(int(dir)+180)))
    if map_data[enemy_pos[1]][enemy_pos[0]]==chr_wall or map_data[enemy_pos[1]][enemy_pos[0]]==chr_hole:
        enemy_pos[0] -= int(math.sin(math.radians(int(dir)+180)))
        enemy_pos[1] -= int(math.cos(math.radians(int(dir)+180)))

"""Der Prolog wird ausgegeben."""
print__prolog()

"""Dies ist die Variable, die die Hauptschleife des Spiels steuert."""
main_loop = True

"""Dies sind die Variablen, die für das Level benuzt werden. map_x steht für die breite des Level, map_y für die höhe. Das Level ansich wird auch Initialisiert."""
map_x = 50
map_y = 15

"""Dies ist die Spieler Position. Der wert bei index (idx) 0 ist die X coordinate, der wert bei index (idx) 1 ist die Y coordinate."""
player_pos = [1,1]

enemy_pos = [map_x-2, map_y-2]

"""Turns gibt an, wie viele Züge schon verganagen sind, points gibt an, wie viele Sternchen Gesammelt wurden, scores beinhaltet alle vergangen Spielstände."""
turns = 0
points = 0
scores = []
rounds = 0
mode = 5

message = ""

keys = 0
max_keys = 0
"""Hier wird alles Zurückgesetzt/auf den Beginn des Spiels Vorbereitet"""
print__ask_for_mode()

print__ask_for_map_size()
map_data = [chr_None]*map_y
reset()

print__charakter_options()

chr_play_disp = chr_play

player_grid = update_pathgrid(path_grid)
"""Hier fängt die Hauptschleife des Spieles an. Alles was geschieht, wird hier aufgerufen."""
while main_loop:
    if player_pos == enemy_pos:                                 #Es wird überprüft, ob der Spieler Gefangen wurde
        message = "Du wurdest Gefangen! Versuche es nochmal!"
        reset()
    print__map_and_player(map_x, map_y, map_data, player_pos)   #Das Level und der Spieler werden Ausgegeben
    chr_play_disp = chr_play
    if message != "": print(message)                            #Fals eine Nachricht an den Spieler Ausgegeben werden soll, wird dies getan.
    user_input = input("Deine Eingabe>>> ")                     #Der Spieler wird nach einer Eingabe gefragt.
    user_inputed(user_input)                                    #Die Eingabe wird Ausgewärted.
    turns += 1   
    if player_pos == enemy_pos:                                 #Es wird überprüft, ob der Spieler Gefangen wurde
        message = "Du wurdest Gefangen! Versuche es nochmal!"
        reset()
    player_grid = update_pathgrid(path_grid)                    #Die Player Grid wird neu Generiert, dies Geschieht nach jedem Zug
    if (turns%((mode//2)+1))==0: enemy_turn()                   #Der Gegner ist am Zug
#ENDE