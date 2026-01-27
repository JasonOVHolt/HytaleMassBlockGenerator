import json
import os
import iconCreation

numIter = 38
id = "BirchPlank"
inputItem = "Wood_Birch_Trunk"
benchID = "MyBuilders"
particleColor = "#bdb3a9"
parent = "Wood_Birch_Trunk"
gatherType = "Woods"
cwd = os.getcwd()

file_path = cwd + "\\Blocks\\" + id + "\\"

image_path = cwd + "\\images\\"
os.chdir(image_path)
files = os.listdir(image_path)
os.chdir(cwd)
newFileNames = [w.replace(".png", "") for w in files]
newFiles = [w.replace("_", " ") for w in newFileNames]
newFiles = [w.title() for w in newFiles]

if os.path.exists(file_path) == False:
    os.makedirs(file_path)


for i in range(numIter):
    newData = {
    "TranslationProperties": {
    "Name": newFiles[i]
    },
    "Icon": "Icons/ItemsGenerated/"+newFileNames[i]+"_Icon.png",
    "Set": "",
    "Recipe": {
        "Input": [
        {
            "ItemId": inputItem
        }
        ],
        "BenchRequirement": [
        {
            "Id": benchID,
            "Type": "StructuralCrafting"
        }
        ]
    },"BlockType": {
        "Gathering": {
            "Breaking": {
                "GatherType": gatherType
            }
        },
        "Textures": [
        {
            "All": "Resources/"+files[i],
            "Weight": 1
        }
        ],
        "ParticleColor": particleColor
    },
    "Parent": parent,
    "IconProperties": {
    "Scale": 0.58823,
    "Rotation": [
      22.5,
      45,
      22.5
    ],
    "Translation": [
      0,
      -13.5
    ]
    }
    }

    with open(file_path+id+str(i)+".json", "w") as json_file:
        json.dump(newData, json_file, indent=2) # The 'indent' parameter makes the file human-readable



    if os.path.exists(cwd + "\\Icons\\" + id + "\\") == False:
        os.makedirs(cwd + "\\Icons\\" + id + "\\")

    iconCreation.generate_padded_cube(image_path + "\\" + files[i], cwd + "\\Icons\\" + id + "\\" + newFileNames[i] + "_Icon.png")