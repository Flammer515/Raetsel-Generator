import os

from classes.puzzle import Raetsel, Raetsel_step

# Variable für inhalt der config datei
config = {}

#standardöffnungsmodus => anlegen der config datei
mode = "w+"

# prüfen ob config dati vorhanden und öffnungsmodus anpassen
if os.path.isfile(".\\config.txt"): 
    mode = "r"

with open(".\\config.txt", mode) as f:
    for line in f:
       (key, val) = line.split(': ')
       val = val.replace("\n", "")
       config[key] = val

# gobale Variable mit ausgabepaf, standard ist .\\output
global outputFolder
outputFolder = ".\\output"

# laden eines ausgabepafed wenn in config vorhanden
if "outputFolder" in config:
    outputFolder = config["outputFolder"]

# Hauptprogramm
#
# Übergaben:
# - page: Seite im Hauptmenü die angezeigt werden soll
# - subpage: Seite im untermenü die angezeigt werden soll
#
# Rückgaben:
# -  ret = "0" : zurückspringen in Untermenü-Auswahl
def main( page, subpage = "" ):

        global outputFolder

        ret = ""
        filename = ""
        print( "=========================================================================================" )
        print( "|| Rätsel Generator v0.2" )
        print( "|| " )
        print( "|| Hinweis: Es werden aktuell keine Umlaute als Eingabe unterstützt!" )
        print( "=========================================================================================" )

        ##### Hauptmenü
        if page == "":  # page "" == Hauptmenü (Menüauswahl)
            print( "Hauptmenü:\r\n" )
            print( "(1) Rätsel" )
            print( "(2) Konfiguration" )
            print( "\r\n(0) Beenden" )

        ##### Menü: (1) Raetsel
        if page == "1":  # Auswahl des Untermenüs
            if subpage == "":
                print( "Raetsel\r\n" )
                print( "(1) Neu" )
                print( "(2) Bearbeiten" )
                print( "\r\n(0) zurück" )

            #####   Untermenü: (1) Neu 
            if subpage == "1":

                print( "Raetsel - Neu\r\n" )
                print( "Alle Eingaben können später noch angepasst werden!\r\n" )
                name = input( "Name des Rätsels eingeben: ")
                beschreibung = input( "Beschreibung des Rätsels eingeben: ")
                schwierigkeit = input( "Schwierigkeit des Rätsels eingeben: ")
                
                # Erstellen eines neuen Rätsels mit Eingaben
                new_raetsel = Raetsel(name, beschreibung, "0", schwierigkeit)
                # Speichern des Rästels als XML Datei
                new_raetsel.save_to_XML(outputFolder)

                edit = input( "Rätsel wurde erstellt. Mit bearbeitung fortfahren? (J/N): " )
                edit.lower()

                if edit == "j" or edit == "ja":
                    subpage = "2"
                    filename = name + ".xml"
                else:
                    ## Nach Erstellung zurück in Untermenü
                    ret = "0"
                    
            pass    
            #####   Ende Untermenü: (1) Neu

            #####   Untermenü: (2) Bearbeiten 
            if subpage == "2":
                print( "Raetsel - Bearbeiten (" + outputFolder + ") \r\n" )

                if( filename == "" ):       ## filename kann bereits vom vorhereigen Untermenü gefüllt werden ( (1) Neu)
                    # Anzeigen aller XML Dateien im Ausgabepfad; Auswahl der vorhandenen Rätsel
                    i = 1
                    files = []
                    for file in os.listdir(outputFolder):
                        if file.endswith(".xml"):
                            files.append(file)
                            print("(" + str(i) + ") " + file.title())
                            i = i+1

                    print( "\r\n(0) zurück" )

                    selection = input( "Auswahl:")

                    if selection.isnumeric():
                        iselection = int(selection)
                        if iselection <= len(files) and iselection != 0:
                            filename = files[iselection-1]
                    
                    ## auswahl (0) zurück wurde eingegeben, zurück in Untermenü
                    if( selection == "0"):
                        ret = "0"

                if( filename != "" ):
                    edit_puzzle = Raetsel( "Null", "Null", "Null", "Null" )
                    edit_puzzle.load_from_XML( outputFolder + "\\" + filename )

                    while( True ): ## Endlosschleife für Bearbeitung
                        os.system('cls')
                        print( "Rätsel - " + filename )
                        print( "====================================" )
                        print( "(1) Name:\t\t" + str(edit_puzzle.name) )
                        print( "(2) Beschreibung:\t" + str(edit_puzzle.description) )
                        print( "(3) Schwierigkeit:\t" + str(edit_puzzle.difficulty) )
                        print( "Anzahl Schritte:\t" + str(edit_puzzle.steps) )
                        print( "====================================" )
                        print( "Schritte:" )

                        i = 4
                        isteps = 1
                        for step in edit_puzzle.raetsel_step:
                            print( "(" + str(i) + ") Schritt " + str(isteps) + ":" )
                            print( "\tName:\t\t" + str(step.name) )
                            print( "\tHinweis:\t" + str(step.hint) )
                            print( "\tSensor:\t\t" + str(step.sensor) )
                            print( "\tWert:\t\t" + str(step.exactvalue) )
                            print( "\tAbweichung:\t" + str(step.max_range) )
                            i = i+1
                            isteps = isteps+1

                        print( "(N) Neuen Schritt anlegen" )
                        if( int(edit_puzzle.steps) > 0):
                            print( "(D) Schritt löschen" )
                        print( "\r\n(0) Speichern und zurück" )

                        edit = input( "Bearbeiten:")
                        if edit == "1":
                            print("Hinweis: Bei der Änderung des Namens wird ein neues Raetsel erstellt (Kopie)")
                            edit_puzzle.name = input("Neuer Name: ")
                        if edit == "2":
                            edit_puzzle.description = input("Neue Beschreibung: ")
                        if edit == "3":
                            edit_puzzle.difficulty = input("Neue Schwierieglkeit: ")
                        if edit == "0":
                            break

                        edit.lower()
                        if edit == "n":
                            new_stepname = input("Name des neuen Schritts: ")
                            # anhängen des neuen Rätselschrittes mit eingegebenem Namen
                            edit_puzzle.add_step(new_stepname)
                        if edit == "d":
                            if( int(edit_puzzle.steps) > 0 ):
                                del_step = input("Welchen Schritt löschen?: ")
                                if( del_step.isnumeric() and del_step <= edit_puzzle.steps ):
                                    # entfernen des Rätselschrittes an gewählter Stelle
                                    edit_puzzle.remove_step(del_step)

                        if edit.isnumeric():
                            iedit = int(edit)
                            if iedit > 3:
                                iedit = iedit-3
                                if iedit <= len(edit_puzzle.raetsel_step):
                                    edit_step = edit_puzzle.get_step(iedit)
                                    os.system('cls')
                                    print( "Rätsel - " + filename + "Schritt " + str(iedit) )
                                    print( "(1) Name:\t" + str(edit_step.name) )
                                    print( "(2) Hinweis:\t" + str(edit_step.hint) )
                                    print( "(3) Sensor:\t" + str(edit_step.sensor) )
                                    print( "(4) Wert:\t" + str(edit_step.exactvalue) )
                                    print( "(5) Abweichung:\t" + str(edit_step.max_range) )

                                    print( "\r\n(0) zurück" )

                                    edit = input( "Bearbeiten:")

                                    if edit == "1":
                                        edit_step.name = input("Neuer Name: ")
                                    if edit == "2":
                                        edit_step.hint = input("Neuer Hinweis: ")
                                    if edit == "3":
                                        # Erstellen eines Dictionary damit andere werte geschrieben als angezeigt werden können
                                        sensors = {
                                            "Tastenfeld" : "keyboard",
                                            "Temperatur" : "temp",
                                            "Luftfeuchtigkeit" : "humidity",
                                            "(Licht) Farbe" : "color",
                                            "Licht" : "light",
                                            "Gyroskop" : "gyro"
                                        }
                                        i = 1
                                        for key in sensors:
                                            # anzeigen aller Sensoren aus Dictionary
                                            print( "(" + str(i) +") " + key )
                                            i = i + 1

                                        sensor_sel = input("Neuer Sensor: ")
                                        if( sensor_sel.isnumeric() ):
                                            isensor = int( sensor_sel ) - 1

                                            sensorvalues = sensors.values()
                                            sensorlist = list(sensorvalues)

                                            # Speichern des Sensors mit Speicherwert
                                            edit_step.sensor = sensorlist[isensor]

                                    if edit == "4":
                                        edit_step.exactvalue = input("Neuer Wert: ")
                                    if edit == "5":
                                        edit_step.max_range = input("Neue Abweichung: ")

                    # schreiben des "neuen" rätsels, bestehendes rätsel wird überschrieben
                    edit_puzzle.save_to_XML(outputFolder) 

                    del( edit_puzzle )
                    ret = "0"
            pass
            #####   Untermenü: (2) Bearbeiten 

        pass
        ##### Ende Menü: (1) Raetsel

        ##### Menü: (2) Konfiguration
        if page == "2":
            print( "Konfiguration\r\n" )
            print( "(1) Ausgabepfad festlegen" )
            print( "\r\n(0) zurück" )

            #####   Untermenü: (1) Ausgabepfad festlegen 
            if subpage == "1":
                print( "Alter Pfad: " + outputFolder )
                outputFolder = input("neuer Pfad: ")

                with open(".\\config.txt", "w+") as f:
                    f.write("outputfolder: " + outputFolder)
        pass
        ##### Ende Menü: (2) Konfiguration

        ## Rückgabewert ist "0" wenn ins Untermenü zurückgesprungen wird
        return ret


page = ""       ## Speichert die Menüauswahl
subpage = ""    ## Speichert dei Untermenü Auswahl

while True:     ## Hauptrogramm als Endlosschleife

    os.system('cls')

    ret = main(page, subpage)

    if( page == "" ):                                       ## Keine Seite ausgewählt => Hauptmenü
        page = input("\r\nAuswahl eingeben: ")              ## Eingabe der Auswahl Hauptmenü
    else:                                                   ## Seite ausgewählt => Untermenü
        if( subpage == "" ):                                    ## Kein Untermenü ausgewählt
            subpage = input("\r\nAuswahl eingeben: ")           ## Eingabe der Auswahl im Untermenü

    if( ret == "0" ):
        subpage = ""

    ### Bereinigen der Eingaben:

    if( not page.isnumeric() ):  ## page muss nummerisch sein
        page = ""

    if( not subpage.isnumeric() ):  ## subpage muss nummerisch sein
        subpage = ""

    ### zurück funktion

    if( subpage == "0" ):   
        subpage = ""
        page = ""
    
    if page == "0":         ## Eingabe 0 im Hauptmenü => Ende
        break