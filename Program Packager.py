# Program Packager
# 12-21-2023
# Period 1
# Levy Le

import sys
import os
import shutil

base_path = r"" + sys.argv[1]
destination_path = r"" + sys.argv[1] + "/Packaged Files"
os.makedirs(destination_path, exist_ok=True)

def checkSubdir(folder):
    global destinationPath
    # Get the immediate subdirectories
    subdirectories = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

    # Iterate through each subdirectory
    for subdirectory in subdirectories:
        source_file_path = os.path.join(folder, subdirectory, "source.cpp")

        # Check if the source file exists in the subdirectory
        if os.path.exists(source_file_path):
            # Copy the source.cpp file to the new folder and rename it
            destination_file_path = os.path.join(destination_path, f"{subdirectory}.cpp")
            shutil.copy2(source_file_path, destination_file_path)
            print(f"Copied '{source_file_path}' to '{destination_file_path}'")

if not os.path.exists(base_path):
    print(f"Error: Path '{base_path}' does not exist.")

checkSubdir(base_path)

shutil.make_archive(destination_path, "zip", destination_path)
shutil.rmtree(destination_path)

