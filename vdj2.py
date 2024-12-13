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

# RGB values
red = True
green = False
blue = False

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

rectScale = 1
rectGrowing = True
rectRot = 0

# Main loop
running = True
while running:
    # Handle rectangle scaling
    """
    if rectGrowing:
        rectScale += 0.01
    else:
        rectScale -= 0.01

    if rectScale > 1.5:
        rectGrowing = False
    elif rectScale < 0.5:
        rectGrowing = True
    """

    # Handle rectangle rotation
    rectRot += 1
    if rectRot > 360:
        rectRot = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read audio data
    data = stream.read(CHUNK)
    data_int = np.frombuffer(data, dtype=np.int16)

    # Calculate sound intensity
    rms = np.sqrt(np.mean(np.square(data_int)))

    print(rms)

    if math.isnan(rms):
        rms = 255
        rectScale = 6
    else:
        rectScale = (rms/100)*5 + 1
        rms = (rms/100)*255
    
    if(rms>255):
        rms = 255
    
    # change color on big noise
    if(rms>200):
        if(red):
            red = False
            green = True
        elif(green):
            green = False
            blue = True
        else:
            blue = False
            red = True
    



    # Determine color based on audio intensity
    if red:
        color = (int(rms), 0, 0)  # Red intensity based on RMS
    elif green:
        color = (0, int(rms), 0)  # Green intensity based on RMS
    else:
        color = (0, 0, int(rms))  # Blue intensity based on RMS

    # Clear the screen with the calculated color
    screen.fill(color)


    # calc star colors
    rectColors[0] = [rectColors[0][0] +1, rectColors[0][1], rectColors[0][2]+1]
    rectColors[1] = [rectColors[1][0] -1, rectColors[1][1] -2, rectColors[1][2] -3]
    # minmax
    for rectColor in range(0,2):
        for col in range(0,3):
            if rectColors[rectColor][col]>250:
                rectColors[rectColor][col] = 0
            elif rectColors[rectColor][col]<5:
                rectColors[rectColor][col] = 255

    # make star 1
    for loop in range(0,2):
        # Create a temporary Surface for the rectangle
        rect_width, rect_height = 60, 60
        rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        rect_surface.fill((0, 0, 0, 0))  # Transparent background

        # Draw the rectangle on the surface
        pygame.draw.rect(rect_surface, rectColors[loop], (0, 0, rect_width, rect_height))

        # Rotate and scale the rectangle
        transformed_surface = pygame.transform.rotozoom(rect_surface, (rectRot + 45*loop), rectScale)

        # Get the new rectangle for positioning
        rect_center = (WIDTH // 2, HEIGHT // 2)
        new_rect = transformed_surface.get_rect(center=rect_center)

        # Blit the transformed rectangle onto the screen
        screen.blit(transformed_surface, new_rect.topleft)
    
    # make star 2
    for loop in range(0,2):
        # Create a temporary Surface for the rectangle
        rect_width, rect_height = 60, 60
        rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        rect_surface.fill((0, 0, 0, 0))  # Transparent background

        # Draw the rectangle on the surface
        pygame.draw.rect(rect_surface, rectColors[loop], (0, 0, rect_width, rect_height))

        # Rotate and scale the rectangle
        transformed_surface = pygame.transform.rotozoom(rect_surface, (rectRot + 45*loop), rectScale)

        # Get the new rectangle for positioning
        rect_center = (WIDTH // 2, HEIGHT // 3)
        new_rect = transformed_surface.get_rect(center=rect_center)

        # Blit the transformed rectangle onto the screen
        screen.blit(transformed_surface, new_rect.topleft)
    
    # make star 3
    for loop in range(0,2):
        # Create a temporary Surface for the rectangle
        rect_width, rect_height = 60, 60
        rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        rect_surface.fill((0, 0, 0, 0))  # Transparent background

        # Draw the rectangle on the surface
        pygame.draw.rect(rect_surface, rectColors[loop], (0, 0, rect_width, rect_height))

        # Rotate and scale the rectangle
        transformed_surface = pygame.transform.rotozoom(rect_surface, (rectRot + 45*loop), rectScale)

        # Get the new rectangle for positioning
        rect_center = (WIDTH // 2, (HEIGHT // 3)*2)
        new_rect = transformed_surface.get_rect(center=rect_center)

        # Blit the transformed rectangle onto the screen
        screen.blit(transformed_surface, new_rect.topleft)

    # Update the display
    pygame.display.flip()

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
