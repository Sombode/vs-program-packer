# Program Packager
# 12-21-2023
# Period 1
# Levy Le

import sys
import os
import shutil

# Retrieve CLI arguments
# TODO: Add fallback functionality if none are provided -> do current folder/open gui??
basePath = r"" + sys.argv[1]
defaultDestinationPath = r"" + basePath + "\Packaged Files"
os.makedirs(defaultDestinationPath, exist_ok=True)

def checkSubdir(folder):
    global defaultDestinationPath
    destinationPath = defaultDestinationPath
    # Get the immediate subdirectories
    subdirectories = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

    # Iterate through each subdirectory
    for subdirectory in subdirectories:
        files = os.listdir(os.path.join(folder, subdirectory))
        targetFiles = []
        # Identify the number of .cpp files in the folder (if there are any)
        for file in files:
            if file.endswith(".cpp"):
                targetFiles.append(file)
                print(f"{file} found in '{os.path.join(folder, subdirectory)}'")
        print(f"Found {len(files)} files ({len(targetFiles)} C++) in '{os.path.join(folder, subdirectory)}'")
        
        if len(targetFiles) == 0:
            # If there are no .cpp files, check further subdirectories
            checkSubdir(os.path.join(folder, subdirectory))
        elif len(targetFiles) == 1:
            # If there's only one .cpp file, no folder will be made and it will simply be renamed to its parent project
            destinationPath = os.path.join(defaultDestinationPath, folder.replace(basePath, "")[1:])
            os.makedirs(destinationPath, exist_ok=True)
            # [1:] is needed to remove the leading \ of the folder file path
            destinationFilePath = os.path.join(basePath, "Packaged Files", folder.replace(basePath, "")[1:], f"{subdirectory}.cpp")
            shutil.copy2(os.path.join(folder, subdirectory, targetFiles[0]), destinationFilePath)
            print(f"Copied single-file project to {destinationFilePath}")
        else:
            destinationPath = os.path.join(defaultDestinationPath, folder.replace(basePath, "")[1:], subdirectory)
            os.makedirs(destinationPath, exist_ok=True)
            print(f"Instantiated folder for multi-file project {subdirectory} to destination {destinationPath}")

            for file in targetFiles:
                destinationFilePath = os.path.join(destinationPath, file)
                shutil.copy2(os.path.join(folder, subdirectory, file), destinationFilePath)
                print(f"Copied file from multi-file project to {destinationFilePath}")
    
        #source_file_path = os.path.join(folder, subdirectory, "source.cpp")

        # Check if the source file exists in the subdirectory
        #if os.path.exists(source_file_path):
            # Copy the source.cpp file to the new folder and rename it
            #destination_file_path = os.path.join(destination_path, f"{subdirectory}.cpp")
            #shutil.copy2(source_file_path, destination_file_path)
            #print(f"Copied '{source_file_path}' to '{destination_file_path}'")

if not os.path.exists(basePath):
    print(f"Error: Path '{basePath}' does not exist.")

checkSubdir(basePath)

# Zip and delete original folder
shutil.make_archive(defaultDestinationPath, "zip", defaultDestinationPath)
shutil.rmtree(defaultDestinationPath)

