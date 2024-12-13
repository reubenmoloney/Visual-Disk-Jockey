import pyaudio
import numpy as np
import pygame
import math
import multiprocessing
from scipy.fft import fft

starsArray = []

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

    def drawStar(x, y, width, height, rotation:int, scale, color1, color2):
        colors = [color1,color2]
        # make star
        for loop in range(0,2):
            # Create a temporary Surface for the rectangle
            rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            rect_surface.fill((0, 0, 0, 0))  # Transparent background

            # Draw the rectangle on the surface
            pygame.draw.rect(rect_surface, colors[loop], (0, 0, width, height))

            # Rotate and scale the rectangle
            transformed_surface = pygame.transform.rotozoom(rect_surface, (rotation + 45*loop), scale)

            # Get the new rectangle for positioning
            rect_center = (x, y)
            new_rect = transformed_surface.get_rect(center=rect_center)

            # Blit the transformed rectangle onto the screen
            screen.blit(transformed_surface, new_rect.topleft)
    
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


        # background color
        screen.fill(backgroundColor)

        # Draw on screen
        drawStar(WIDTH // 3, HEIGHT // 2, 100, 100, rotRight, 1+5*volume, [255*volume,1,100], [0,255*volume,0])
        drawStar((WIDTH // 3)*2, HEIGHT // 2, 100, 100, rotLeft, 1+5*volume, [255*volume,1,100], [0,255*volume,0])

        # Update the display
        pygame.display.flip()

    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
    pygame.quit()


#control pannel
def ui_window():

    # Colors
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    GREEN = (0, 200, 0) 

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("VJ control pannel")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Check if the button is clicked
        
        #rendering
        screen.fill(WHITE)  # Blue background

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    process_1 = multiprocessing.Process(target=display_window)
    process_2 = multiprocessing.Process(target=ui_window)
    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()