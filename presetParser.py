
def parsePresetFile(filePath):
    presetsArray = []

    #replace with filePath
    f = open(filePath, "r")
    rawData = f.read()

    presetBlocks = rawData.split("PRESET")

    #loop through all the presets
    for preset in presetBlocks:
        if preset == '':
            continue
        
        objectsArray = []
        #split into individual objects
        objects = preset.split("OBJECT")

        presetName = objects.pop(0).split("\n")[0]
        print(presetName)

        for object in objects:
            #split into lines
            lines = object.split("\n")
            print(lines)

            ##check what kind of object it is
            if(lines[0] == " Star"):
                #noting
                x = lines[1].split(" ")[1]
                y = lines[2].split(" ")[1]
                w = lines[3].split(" ")[1]
                h = lines[4].split(" ")[1]
                r = lines[5].split(" ")[1]
                g = lines[6].split(" ")[1]
                b = lines[7].split(" ")[1]

                objectsArray.append(Star(x,y,w,h,1,1,[r,g,b],[r,g,b]))

            elif(lines[0] == " Circle"):
                
                x = lines[1].split(" ")[1]
                y = lines[2].split(" ")[1]
                r = lines[3].split(" ")[1]
                g = lines[4].split(" ")[1]
                b = lines[5].split(" ")[1]

                objectsArray.append(Circle(x,y,1,1,150,[r,g,b]))
                    
            elif(lines[0]) == " SineWave":
                h = lines[1].split(" ")[1]
                w = lines[2].split(" ")[1]
                r = lines[3].split(" ")[1]
                g = lines[4].split(" ")[1]
                b = lines[5].split(" ")[1]

                objectsArray.append(SineWave(1,1,h,w,[r,g,b]))
        
        presetsArray.append(objectsArray)

    return presetsArray

print(parsePresetFile("presets.txt"))