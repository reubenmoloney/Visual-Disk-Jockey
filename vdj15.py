import pyaudio
import numpy as np
import pygame
import math
import multiprocessing
from scipy.fft import fft
import random
import pygame_gui
import keyboard

programIcon = pygame.image.load('icon.ico')

class Star:

    def __init__(self, x, y, width, height, rotation, scale, color1, color2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.scale = scale
        self.color1 = color1
        self.color2 = color2
    
    def setColor(self, color1, color2):
        self.color1 = color1
        self.color2 = color2
    
    def setRotation(self, rotation):
        self.rotation = rotation

    def setScale(self, scale):
        self.scale = scale
    
    def draw(self, screen):
        # make star
        colors = [self.color1, self.color2]

        for loop in range(0,2):
            # Create a temporary Surface for the rectangle
            rect_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            rect_surface.fill((0, 0, 0, 0))  # Transparent background

            # Draw the rectangle on the surface
            pygame.draw.rect(rect_surface, colors[loop], (0, 0, self.width, self.height))

            # Rotate and scale the rectangle
            transformed_surface = pygame.transform.rotozoom(rect_surface, (self.rotation + loop*45), self.scale)

            # Get the new rectangle for positioning
            rect_center = (self.x, self.y)
            new_rect = transformed_surface.get_rect(center=rect_center)

            # Blit the transformed rectangle onto the screen
            screen.blit(transformed_surface, new_rect.topleft)

class SineWave:
    def __init__(self, amplitude, frequency, height, width, color):
        self.amplitude = amplitude
        self.frequency = frequency
        self.height = height
        self.width = width
        self.color = color
        self.xscale = 2*math.pi / width
    
    def draw(self, screen):
        for x in range(self.width):
            y = int(self.amplitude * math.sin(self.frequency * x * self.xscale) + self.height)
            pygame.draw.circle(screen, self.color, (x, y), 2)  # Use small circles for smoother visualization
    
    def setFrequency(self, frequency):
        self.frequency = frequency

    def setAmplitude(self, amplitude):
        self.amplitude = amplitude
    
    def setColor(self, color):
        self.color = color
    
    def useNoteForfrequency(self, note):
        if note == "A":
            self.frequency = 11
        elif note == "A#":
            self.frequency = 13
        elif note == "B":
            self.frequency = 15
        elif note == "C":
            self.frequency = 17
        elif note == "C#":
            self.frequency = 19
        elif note == "D":
            self.frequency = 5
        elif note == "D#":
            self.frequency = 7
        elif note == "E":
            self.frequency = 9
        elif note == "F":
            self.frequency = 21
        elif note == "F#":
            self.frequency = 23
        elif note == "G":
            self.frequency = 25
        else:# G#
            self.frequency = 27

class Circle:
    def __init__(self, center, radius, squiggle_amount, point_count, color):
        self.cx, self.cy = center
        self.radius = radius
        self.squiggle_amount = squiggle_amount
        self.point_count = point_count
        self.color = color
    
    def setSquiggleAmount(self, squiggle_amount):
        self.squiggle_amount = squiggle_amount
    
    def setRadius(self, radius):
        self.radius = radius
    
    def draw(self, screen):
        points = []
        for i in range(self.point_count):
            angle = 2 * math.pi * i / self.point_count
            r = self.radius + random.uniform(-self.squiggle_amount, self.squiggle_amount)  # Randomize radius
            x = self.cx + r * math.cos(angle)
            y = self.cy + r * math.sin(angle)
            points.append((x, y))

        # Draw lines between points
        for i in range(len(points)):
            pygame.draw.line(screen, self.color, points[i], points[(i + 1) % len(points)], 2)


class Triangle:
    def __init__(self, center, initial_size, color):
        self.center = center
        self.color = color
        self.size = initial_size  # Initial size of the triangle
        self.growth_rate = 2  # Initial growth rate in pixels per frame

    def draw(self, screen):
        # Calculate the vertices of the triangle based on the current size
        vertices = [
            (self.center[0], self.center[1] - self.size),  # Top vertex
            (self.center[0] - self.size * math.sin(math.pi / 3), self.center[1] + self.size / 2),  # Bottom-left vertex
            (self.center[0] + self.size * math.sin(math.pi / 3), self.center[1] + self.size / 2),  # Bottom-right vertex
        ]

        # Draw the triangle
        pygame.draw.polygon(screen, self.color, vertices, 2)  # 2 for outline thickness

        # Update the size
        self.size += self.growth_rate
        self.growth_rate += 0.05  # Increase growth rate as size increases

        # Reset size and growth rate if the triangle exceeds the screen boundaries
        if self.size > max(screen.get_width()+100, screen.get_height()+100):
            self.size = 0
            self.growth_rate = 2

class TrianglesEffect:
    def __init__(self, triangle_count, color):
        self.triangles = []
        self.triangle_count = triangle_count
        self.color = color
        for loop in range(triangle_count):
            center = ((WIDTH // 2), (HEIGHT // 2))
            initial_size = 150*loop
            color = color
            self.triangles.append(Triangle(center, initial_size, color))

    def draw(self, screen):
        for triangle in self.triangles:
            triangle.draw(screen)
#square outline
#triangles - vaporwave - make it look like ur going through infinite triangles
#spiral triangles
#fibinachi
#fractals

WIDTH, HEIGHT = 1920, 1080

# create objects
#objects = [    SineWave(100, 0.02, HEIGHT // 2, WIDTH, [255,255,255]),    Star(WIDTH // 3, HEIGHT // 2, 100, 100, 0, 1, [255,0,0], [0,255,0]),    Star((WIDTH // 3)*2, HEIGHT // 2, 100, 100, 0, 1, [255,1,0], [0,255,0]),    Circle((WIDTH // 2, HEIGHT // 2), 100, 0, 150, [0,0,255])]


def display_window(objects):
    # Initialize Pygame
    pygame.init()
    pygame.display.set_icon(programIcon)

    # Set up audio stream
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    # background color
    backgroundColor = [0,0,0]

    #global roation
    rotRight = 0
    rotLeft = 360



    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=1)

    # Set up Pygame window
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("VDJ Display")

    
    
    def getAudioData():
        # Read audio data
        data = stream.read(CHUNK)
        data_int = np.frombuffer(data, dtype=np.int16)
        return data_int

    def getVolumeScalar(audioData):
        # Calculate sound intensity
        rms = np.sqrt(np.mean(np.square(audioData)))

        # normalize rms value
        if math.isnan(rms) or rms>100:
            rms = 1
        else:
            rms = rms/100
        
        return rms

    def getFrequency(audioData):
        # Perform FFT on the audio data
        fft_data = fft(audioData)

        # Calculate the magnitude of the FFT
        magnitude = np.abs(fft_data[:CHUNK // 2])  # Keep only the positive frequencies

        # Find the index of the maximum magnitude
        dominant_index = np.argmax(magnitude)

        # Map the index to the corresponding frequency
        frequency = dominant_index * (RATE / CHUNK)

        # Print the dominant frequency (pitch)
        # print(f"Dominant Frequency: {frequency:.2f} Hz")

        # normalize rms value
        if math.isnan(frequency):
            frequency = 1

        return frequency

    def getNoteFromFrequency(frequency):
        # Reference frequency for A4
        A4 = 440.0
        NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        # Calculate the number of semitones from A4
        n = 12 * math.log2(frequency / A4)
        
        # Find the closest note
        n = round(n)
        
        # Determine the note name and octave
        note_index = (n + 9) % 12  # +9 because A is the 9th note in the scale
        octave = 4 + (n + 9) // 12  # Calculate octave from A4's position
        
        note_name = NOTES[note_index]
        return note_name


    


    # Main loop
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # global rotation
        rotRight += 1
        if(rotRight>360):
            rotRight = 0

        rotLeft -= 1
        if(rotLeft<0):
            rotLeft = 360

        audioData = getAudioData()
        # get volume
        volume = getVolumeScalar(audioData)

        #get pitch
        frequency = getFrequency(audioData)
        
        # note = getNoteFromFrequency(frequency)

        # use volume to calculate stuff
        for i in range(len(objects)):
            obj = objects[i]
            if type(obj) is Star:
                obj.setColor([100,0,volume*255],[100,0,volume*255])
                obj.setRotation(rotLeft)
                obj.setScale(1+3*volume)
            elif type(obj) is SineWave:
                obj.setAmplitude(volume*100)
                obj.setFrequency(frequency/100)
                #object.useNoteForfrequency(note)
            elif type(obj) is Circle:
                obj.setRadius(volume*125 + 75)
                obj.setSquiggleAmount(volume*100)
            
            objects[i] = obj
        # background color
        screen.fill(backgroundColor)

        # Draw on screen
        """for object in objects:
            if(type(object) is TrianglesEffect):
                newObj = object
                newObj.draw(screen)
                object = newObj
            else:
                object.draw(screen)"""
        for loop in range(len(objects)):
            if(type(objects[loop]) is TrianglesEffect):
                newObj = objects[loop]
                newObj.draw(screen)
                objects[loop] = newObj
            else:
                objects[loop].draw(screen)

        # Update the display
        pygame.display.flip()

    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
    pygame.quit()

global form_elements

def parsePresetFile(filePath):
    presetsArray = []

    #replace with filePath
    f = open(filePath + ".txt", "r")
    rawData = f.read()
    f.close()

    presetBlocks = rawData.split("PRESET")

    #loop through all the presets
    for preset in presetBlocks:
        if preset == '':
            continue
        
        objectsArray = []
        #split into individual objects
        objects1 = preset.split("OBJECT")

        presetName = objects1.pop(0).split("\n")[0]
        print(presetName)

        for object1 in objects1:
            #split into lines
            lines = object1.split("\n")
            print(lines)

            ##check what kind of object it is
            if(lines[0] == " Star"):
                #noting
                x = int(lines[1].split(" ")[1])
                y = int(lines[2].split(" ")[1])
                w = int(lines[3].split(" ")[1])
                h = int(lines[4].split(" ")[1])
                r = int(lines[5].split(" ")[1])
                g = int(lines[6].split(" ")[1])
                b = int(lines[7].split(" ")[1])

                objectsArray.append(Star(x,y,w,h,1,1,[r,g,b],[r,g,b]))

            elif(lines[0] == " Circle"):
                
                x = int(lines[1].split(" ")[1])
                y = int(lines[2].split(" ")[1])
                r = int(lines[3].split(" ")[1])
                g = int(lines[4].split(" ")[1])
                b = int(lines[5].split(" ")[1])

                objectsArray.append(Circle([x,y],1,1,150,[r,g,b]))
                    
            elif(lines[0]) == " SineWave":
                h = int(lines[1].split(" ")[1])
                w = int(lines[2].split(" ")[1])
                r = int(lines[3].split(" ")[1])
                g = int(lines[4].split(" ")[1])
                b = int(lines[5].split(" ")[1])

                objectsArray.append(SineWave(1,1,h,w,[r,g,b]))
            
            elif(lines[0]) == " TrianglesEffect":
                c = int(lines[1].split(" ")[1])#triangles count
                r = int(lines[2].split(" ")[1])
                g = int(lines[3].split(" ")[1])
                b = int(lines[4].split(" ")[1])

                objectsArray.append(TrianglesEffect(c,[r,g,b]))
        
        presetsArray.append(objectsArray)

    return presetsArray

def savePreset(presetName, objects):
    fileName = presetName + ".txt"

    #create new file
    f = open(fileName, "x")

    f.write("PRESET " + fileName + "\n")
    
    for obj in objects:
        #handle all types of objects
        if type(obj) is Star:
            f.write("OBJECT Star\n")
            f.write("x " + str(obj.x) + "\n")
            f.write("y " + str(obj.y) + "\n")
            f.write("w " + str(obj.width) + "\n")
            f.write("h " + str(obj.height) + "\n")
            f.write("r " + str(obj.color1[0]) + "\n")
            f.write("g " + str(obj.color1[1]) + "\n")
            f.write("b " + str(obj.color1[2]) + "\n")
        elif type(obj) is Circle:
            f.write("OBJECT Circle\n")
            f.write("x " + str(obj.cx) + "\n")
            f.write("y " + str(obj.cy) + "\n")
            f.write("r " + str(obj.color[0]) + "\n")
            f.write("g " + str(obj.color[1]) + "\n")
            f.write("b " + str(obj.color[2]) + "\n")
        elif type(obj) is SineWave:
            f.write("OBJECT SineWave\n")
            f.write("h " + str(obj.height) + "\n")
            f.write("w " + str(obj.width) + "\n")
            f.write("r " + str(obj.color[0]) + "\n")
            f.write("g " + str(obj.color[1]) + "\n")
            f.write("b " + str(obj.color[2]) + "\n")
        elif type(obj) is TrianglesEffect:
            f.write("OBJECT TrianglesEffect\n")
            f.write("c " + str(obj.triangle_count) + "\n")
            f.write("r " + str(obj.color[0]) + "\n")
            f.write("g " + str(obj.color[1]) + "\n")
            f.write("b " + str(obj.color[2]) + "\n")
    f.close()

presetsArray = parsePresetFile("presets") #############################################################################################################REMOVE THIS LATER

def display_ui(objects):
    pygame.init()
    pygame.display.set_icon(programIcon)

    def addObject(objectData):
        print("adding object to array")
        objectColor = [int(objectData["colorR"]), int(objectData["colorG"]), int(objectData["colorB"])]
        if objectData["name"] == "Star":
            objects.append(Star(
                int(objectData["x"]), # x pos
                int(objectData["y"]), # y pos
                int(objectData["width"]), # width
                int(objectData["height"]), # height
                int(objectData["rotation"]), # rotation
                float(objectData["scale"]),# scale
                objectColor,#color 1
                objectColor,#color 2
            ))
        elif objectData["name"] == "Circle":
            objects.append(Circle(
                (int(objectData["x"]), # x pos
                int(objectData["y"])), # y pos
                1,# radius
                1,# squiggle ammount
                150, # point count
                objectColor
            ))
        elif objectData["name"] == "SineWave":
            objects.append(SineWave(
                0, # amplitude
                0, #frequency
                int(objectData["height"]), # y pos
                int(objectData["width"]), # length(0 -> x)
                objectColor # color
            ))
        elif objectData["name"] == "TrianglesEffect":
            objects.append(TrianglesEffect(
                int(objectData["Triangle Count"]),
                objectColor
            ))
        print("Objects: ", objects)
    # Screen dimensions
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("VDJ Control Panel")

    # Set up manager for pygame_gui
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Initial states
    running = True
    show_star_form = False
    show_circle_form = False
    show_sine_wave_form = False
    show_preset_form = False
    show_save_preset_form = False
    show_triangles_effect_form = False


    # Colors
    WHITE = (255, 255, 255)

    # Create the "Add Star" button
    add_star_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 50), (100, 50)),
        text="Add Star",
        manager=manager
    )

    # Create the "Add Circle" button
    add_circle_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 50), (100, 50)),
        text="Add Circle",
        manager=manager
    )

    # Create the "Add Sine Wave" button
    add_sine_wave_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 50), (120, 50)),
        text="Add Sine Wave",
        manager=manager
    )

    # Create the "Add Triagnles Effect" button
    add_triangles_effect_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 100), (120, 50)),
        text="Add Triagnles Effect",
        manager=manager
    )

    # create the "Clear Objects" button
    clear_objects_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((500, 50), (120, 50)),
        text="Clear Objects",
        manager=manager
    )

    # create save as preset button
    save_as_preset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((500, 150), (120, 50)),
        text="Save as Preset",
        manager=manager
    )

    ####################################################################PRESET BUTTONS
    #load preset button
    load_preset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((500, 100), (120, 50)),
        text="Load Preset",
        manager=manager
    )

    #get presets from file
    presetButtonYOffset = 100
    preset_buttons = []  # Create a list to store preset buttons

    for loop in range(len(presetsArray)):
        titleString = "Preset " + str(loop + 1)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 160 + presetButtonYOffset), (120, 50)),
            text=titleString,
            manager=manager
        )
        preset_buttons.append(button)  # Store the button in the list
        presetButtonYOffset += 60

    # Placeholder for form elements
    form_elements = {}

    def create_star_form():
        """Create the form for adding a star."""
        form_elements.clear()

        labels = ["x", "y", "width", "height", "rotation", "scale", "colorR", "colorG", "colorB"]
        y_offset = 120
        x_offset = 600
        
        for label in labels:
            form_elements[label] = {
                "label": pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect((50+x_offset, y_offset), (100, 30)),
                    text=label,
                    manager=manager
                ),
                "input": pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((160+x_offset, y_offset), (200, 30)),
                    manager=manager
                )
            }
            y_offset += 40

        # Submit button
        form_elements["submit"] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((160+x_offset, y_offset), (100, 40)),
            text="Create Star",
            manager=manager
        )

    def create_circle_form():
        """Create the form for adding a circle."""
        form_elements.clear()

        labels = ["x", "y", "colorR", "colorG", "colorB"]
        y_offset = 120
        x_offset = 600

        for label in labels:
            form_elements[label] = {
                "label": pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect((50+x_offset, y_offset), (100, 30)),
                    text=label,
                    manager=manager
                ),
                "input": pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((160+x_offset, y_offset), (200, 30)),
                    manager=manager
                )
            }
            y_offset += 40

        # Submit button
        form_elements["submit"] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((160+x_offset, y_offset), (100, 40)),
            text="Create Circle",
            manager=manager
        )

    def create_sine_wave_form():
        """Create the form for adding a sine wave."""
        form_elements.clear()

        labels = ["height", "width", "colorR", "colorG", "colorB"]
        y_offset = 120
        x_offset = 600

        for label in labels:
            form_elements[label] = {
                "label": pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect((50+x_offset, y_offset), (100, 30)),
                    text=label,
                    manager=manager
                ),
                "input": pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((160+x_offset, y_offset), (200, 30)),
                    manager=manager
                )
            }
            y_offset += 40

        # Submit button
        form_elements["submit"] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((160+x_offset, y_offset), (120, 40)),
            text="Create Sine Wave",
            manager=manager
        )

    def create_triangles_effect_form():
        """Create the form for adding a Triangles Effect."""
        form_elements.clear()

        labels = ["Triangle Count", "colorR", "colorG", "colorB"]
        y_offset = 120
        x_offset = 600

        for label in labels:
            form_elements[label] = {
                "label": pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect((50+x_offset, y_offset), (100, 30)),
                    text=label,
                    manager=manager
                ),
                "input": pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((160+x_offset, y_offset), (200, 30)),
                    manager=manager
                )
            }
            y_offset += 40

        # Submit button
        form_elements["submit"] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((160+x_offset, y_offset), (100, 40)),
            text="Create Triangles",
            manager=manager
        )

    def load_preset_form():
        ###########TODO
        form_elements.clear()

        labels = ["File Name"]
        y_offset = 120
        x_offset = 600

        for label in labels:
            form_elements[label] = {
                "label": pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect((50+x_offset, y_offset), (100, 30)),
                    text=label,
                    manager=manager
                ),
                "input": pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((160+x_offset, y_offset), (200, 30)),
                    manager=manager
                )
            }
            y_offset += 40

        # Submit button
        form_elements["submit"] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((160+x_offset, y_offset), (120, 40)),
            text="Load Preset",
            manager=manager
        )
    
    def save_as_preset_form():
        form_elements.clear()

        labels = ["Preset Name"]
        y_offset = 120
        x_offset = 600

        for label in labels:
            form_elements[label] = {
                "label": pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect((50+x_offset, y_offset), (100, 30)),
                    text=label,
                    manager=manager
                ),
                "input": pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect((160+x_offset, y_offset), (200, 30)),
                    manager=manager
                )
            }
            y_offset += 40

        # Submit button
        form_elements["submit"] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((160+x_offset, y_offset), (120, 40)),
            text="Save Preset",
            manager=manager
        )
    
    #clear form off screen
    def clear_form():
        for element in form_elements.values():
            if isinstance(element, dict):
                for sub_element in element.values():
                    sub_element.kill()
            else:
                element.kill()
        form_elements.clear()


    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == add_star_button:
                        clear_form()
                        show_star_form = True
                        show_circle_form = False
                        show_sine_wave_form = False
                        show_preset_form = False
                        show_save_preset_form = False
                        show_triangles_effect_form = False
                        create_star_form()
                    elif event.ui_element == add_circle_button:
                        clear_form()
                        show_circle_form = True
                        show_star_form = False
                        show_sine_wave_form = False
                        show_preset_form = False
                        show_save_preset_form = False
                        show_triangles_effect_form = False
                        create_circle_form()
                    elif event.ui_element == add_sine_wave_button:
                        clear_form()
                        show_sine_wave_form = True
                        show_star_form = False
                        show_circle_form = False
                        show_preset_form = False
                        show_save_preset_form = False
                        show_triangles_effect_form = False
                        create_sine_wave_form()
                    elif event.ui_element == add_triangles_effect_button:
                        clear_form()
                        show_sine_wave_form = False
                        show_star_form = False
                        show_circle_form = False
                        show_preset_form = False
                        show_save_preset_form = False
                        show_triangles_effect_form = True
                        create_triangles_effect_form()
                    elif event.ui_element == save_as_preset_button:
                        clear_form()
                        show_sine_wave_form = False
                        show_star_form = False
                        show_circle_form = False
                        show_preset_form = False
                        show_save_preset_form = True
                        show_triangles_effect_form = False
                        save_as_preset_form()
                    elif (show_star_form or show_circle_form or show_sine_wave_form or show_preset_form or show_save_preset_form or show_triangles_effect_form) and event.ui_element == form_elements["submit"]:
                        # Handle form submission
                        data = {}

                        # this creates a dictionary
                        for key, elements in form_elements.items():
                            if key != "submit":
                                data[key] = elements["input"].get_text()
                        
                        # add type of object
                        if(show_star_form):
                            data["name"] = "Star"
                            addObject(data)
                        elif(show_circle_form):
                            data["name"] = "Circle"
                            addObject(data)
                        elif(show_sine_wave_form):
                            data["name"] = "SineWave"
                            addObject(data)
                        elif(show_triangles_effect_form):
                            data["name"] = "TrianglesEffect"
                            addObject(data)
                        elif(show_preset_form):
                            ###### WHAT DOESS IT DO WHEN PRESET NAME IS GIVEN
                            newPreset = parsePresetFile(data["File Name"])
                            presetsArray.append(newPreset)
                            for newObjects in newPreset:
                                for object in newObjects:
                                    objects.append(object)
                        elif(show_save_preset_form):
                            savePreset(data["Preset Name"], objects)
                        print("Form Data:", data)
                        show_star_form = False
                        show_circle_form = False
                        show_sine_wave_form = False
                        show_preset_form = False
                        show_save_preset_form = False
                        show_triangles_effect_form = False
                        clear_form()
                        
                    elif(event.ui_element == clear_objects_button):
                        objects[:] = []
                    elif(event.ui_element == load_preset_button):
                        clear_form()
                        show_star_form = False
                        show_circle_form = False
                        show_sine_wave_form = False
                        show_preset_form = True
                        show_save_preset_form = False
                        show_triangles_effect_form = False
                        load_preset_form()
                    elif event.ui_element in preset_buttons:
                        for loop, button in enumerate(preset_buttons):
                            if event.ui_element == button:
                                newObjects = presetsArray[loop]
                                for obj in newObjects:
                                    objects.append(obj)
                                break



                        

            # Pass events to the UI manager
            manager.process_events(event)

        # Clear the screen
        screen.fill(WHITE)

        # Draw the UI
        manager.update(time_delta)
        manager.draw_ui(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()

# for opening control pannel
def start_display_ui(objects):
    # Function to start the display_ui process
    process = multiprocessing.Process(target=display_ui, args=(objects,))
    process.start()
    return process

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        objects = manager.list()

        # Start both processes
        display_ui_process = start_display_ui(objects)
        display_window_process = multiprocessing.Process(target=display_window, args=(objects,))
        display_window_process.start()

        try:
            while display_window_process.is_alive():
                # Monitor the display_ui process
                if(keyboard.is_pressed('c')):
                    if not display_ui_process.is_alive():
                        print("display_ui process closed. Restarting...")
                        display_ui_process = start_display_ui(objects)

                #time.sleep(1)  # Poll every second
        except KeyboardInterrupt:
            print("Shutting down processes...")

        # Terminate both processes
        if display_ui_process.is_alive():
            display_ui_process.terminate()
        display_window_process.terminate()
