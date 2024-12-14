import pyaudio
import numpy as np
import pygame
import math
import multiprocessing
from scipy.fft import fft

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
            transformed_surface = pygame.transform.rotozoom(rect_surface, (self.rotation + 45*loop), self.scale)

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
    
    def draw(self, screen):
        for x in range(self.width):
            y = int(self.amplitude * math.sin(self.frequency * x) + self.height)
            pygame.draw.circle(screen, self.color, (x, y), 2)  # Use small circles for smoother visualization
    
    def setFrequency(self, frequency):
        self.frequency = frequency

    def setAmplitude(self, amplitude):
        self.amplitude = amplitude
    
    def setColor(self, color):
        self.color = color


        

def display_window():
    # Initialize Pygame
    pygame.init()

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

    # star colors array
    rectColors = [
        [50,50,50],
        [150,150,150]
    ]



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
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sound Reactive Color")

    
    
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
        return f"{note_name}{octave}"


    # create objects
    objects = [
        SineWave(100, 0.02, HEIGHT // 2, WIDTH, [255,255,255]),
        Star(WIDTH // 3, HEIGHT // 2, 100, 100, rotRight, 1, [255,0,0], [0,255,0]), 
        Star((WIDTH // 3)*2, HEIGHT // 2, 100, 100, rotLeft, 1, [255,1,0], [0,255,0]),
    ]


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
        print(getNoteFromFrequency(frequency))

        # use volume to calculate stuff
        for object in objects:
            if type(object) is Star:
                object.setColor([100,0,volume*255],[100,0,volume*255])
                object.setRotation(rotLeft)
                object.setScale(1+3*volume)
            elif type(object) is SineWave:
                object.setAmplitude(25 + (75*volume))
                object.setFrequency(frequency/100000)

        # background color
        screen.fill(backgroundColor)

        # Draw on screen
        for object in objects:
            object.draw(screen)

        # Update the display
        pygame.display.flip()

    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
    pygame.quit()


if __name__ == "__main__":
    process_1 = multiprocessing.Process(target=display_window)

    process_1.start()

    process_1.join()
