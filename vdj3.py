import pyaudio
import numpy as np
import pygame
import math

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
WIDTH, HEIGHT = 1920, 1080
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

def getVolumeScalar():
    # Read audio data
    data = stream.read(CHUNK)
    data_int = np.frombuffer(data, dtype=np.int16)

    # Calculate sound intensity
    rms = np.sqrt(np.mean(np.square(data_int)))

    print(rms)

    # normalize rms value
    if math.isnan(rms) or rms>100:
        rms = 1
    else:
        rms = rms/100
    
    
    return rms



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

    # get volume
    volume = getVolumeScalar()

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
