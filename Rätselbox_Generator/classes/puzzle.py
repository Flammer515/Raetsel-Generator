import xml.etree.ElementTree as ET

class Raetsel_step:
    name = "Dummy name"     # Name
    hint = "Dummy hint"     # Hinweis
    sensor = "0"            # Sensor
    exactvalue = "0"        # genauer Wert
    max_range = "0"         # Abweichung vom Wert

    # Konstruktor
    def __init__(self, name, hint="", sensor="", exactvalue="", max_range=""):
        self.name = name
        self.hint = hint
        self.sensor = sensor
        self.exactvalue = exactvalue
        self.max_range = max_range

    # Destruktor
    def __del__(self):
        pass

    def set_name(self, name):
        self.name = name

    def set_hint(self, hint):
        self.hint = hint

    def set_step(self, sensor):
        self.sensor = sensor

    def set_exactvalue(self, exactvalue):
        self.exactvalue = exactvalue

    def set_max_range(self, max_range):
        self.max_range = max_range

class Raetsel:
    name = "Dummy name"                 # Name
    description = "Dummy desciption"    # Beschreibung
    steps = "0"                         # Anzahl Schritte
    difficulty = "0"                    # Schierigkeitsgrad
    raetsel_step = []                   # Liste der Schritte
    
    # Konstruktor
    def __init__(self, name, description, steps, difficulty):
        self.name = name
        self.description = description
        self.steps = steps
        self.difficulty = difficulty

    # Destruktor
    def __del__(self):
        for del_step in self.raetsel_step:
            del(del_step)
        self.raetsel_step.clear()

    # Schritt hinzufügen
    def add_step(self, name, hint="", sensor="", exactvalue="", max_range=""):
        self.raetsel_step.append(Raetsel_step(name, hint, sensor, exactvalue, max_range))
        self.steps = str( len(self.raetsel_step) )
    
    #Schritt entfernen
    def remove_step(self, step):
        self.raetsel_step.pop(int(step)-1)
        self.steps = str( len(self.raetsel_step) )

    # Schritt an bestimmter Stelle holen; begint bei 1
    def get_step(self, step):
        return self.raetsel_step[step-1]

    # Schritt Name drucken, begint bei 1
    def print_step(self, step):
        print( self.raetsel_step[step-1].name)

    # Rätsel als xml Datei speichern
    # Übergabe: path: Pfad zum Speicherort der Datei, Dateiname = [Rätselname].xml
    def save_to_XML(self, path):
        # Anlegen der Rätsel struktur
        data = ET.Element('data')
        raetseldata = ET.SubElement(data, 'Raetsel')
        field = ET.SubElement(raetseldata, 'name')
        field.text = self.name
        field = ET.SubElement(raetseldata, 'description')
        field.text = self.description
        field = ET.SubElement(raetseldata, 'difficulty')
        field.text = self.difficulty
        Schritte = ET.SubElement(data, 'Steps')

        # Erstellen der Einzelnen Schritte
        i = 0
        for schritt in self.raetsel_step:
            i = i+1
            Step = ET.SubElement(Schritte, 'Step' + str(i))
            field = ET.SubElement(Step, 'name')
            field.text = str(schritt.name)
            field = ET.SubElement(Step, 'hint')
            field.text = str(schritt.hint)
            field = ET.SubElement(Step, 'sensor')
            field.text = str(schritt.sensor)
            field = ET.SubElement(Step, 'exactvalue')
            field.text = str(schritt.exactvalue)
            field = ET.SubElement(Step, 'max_range')
            field.text = str(schritt.max_range)
            

        field = ET.SubElement(raetseldata, 'steps')
        field.text = str(i)

        # Speichern der des Rätsels als XML
        mydata = ET.tostring(data, "utf-8")
        myfile = open( path + "\\" + self.name + ".xml", "w+")
        myfile.write( mydata.decode("utf-8") )

    # Laden des Rätsels aus XML Datei
    # Übergabe: path: Pfad zur gespeicherten Datei
    def load_from_XML(self, path):
        tree = ET.parse(path)
        root = tree.getroot()

        # Laden der Rätseltrukstur
        raetsel = root.find('Raetsel')
        stepList = root.find('Steps')

        # Befüllen des Rätsels
        self.name = raetsel.find('name').text
        self.description = raetsel.find('description').text
        self.steps = raetsel.find('steps').text
        self.difficulty = raetsel.find('difficulty').text

        # Befüllen der Schritte
        for singlestep in stepList:
            stepname = singlestep.find('name').text
            stephint = singlestep.find('hint').text
            stepsensor = singlestep.find('sensor').text
            stepvalue = singlestep.find('exactvalue').text
            steprange = singlestep.find('max_range').text
            self.add_step(stepname, stephint, stepsensor, stepvalue, steprange )
        
