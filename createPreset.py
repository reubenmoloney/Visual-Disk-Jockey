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
            f.write("x " + str(obj.x) + "\n")
            f.write("y " + str(obj.y) + "\n")
            f.write("r " + str(obj.color[0]) + "\n")
            f.write("g " + str(obj.color[1]) + "\n")
            f.write("b " + str(obj.color[2]) + "\n")
        elif type(obj) is SineWave:
            f.write("OBJECT SineWave\n")
            f.write("h " + str(obj.x) + "\n")
            f.write("w " + str(obj.y) + "\n")
            f.write("r " + str(obj.color[0]) + "\n")
            f.write("g " + str(obj.color[1]) + "\n")
            f.write("b " + str(obj.color[2]) + "\n")




    presetsArray.append(newPreset)
    

"""
PRESET Wavy
OBJECT SineWave
h 200
w 1920
r 0
g 255
b 0
OBJECT SineWave
h 500
w 1920
r 255
g 255
b 255
OBJECT SineWave
h 800
w 1920
r 0
g 0
b 255
PRESET Circles
OBJECT Circle
x 960
y 540
r 255
g 255
b 255
OBJECT Circle
x 400
y 540
r 0
g 255
b 0
OBJECT Circle
x 1440
y 540
r 0
g 0
b 255
PRESET Starry
OBJECT Star
x 300
y 300
w 100
h 100
r 255
g 255
b 0
"""