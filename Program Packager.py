# Program Packager
# 12-21-2023
# Period 1
# Levy Le

import sys
import os
import shutil

verbose = True
count = 0

# Retrieve CLI arguments
# TODO: Add fallback functionality if none are provided -> do current folder/open gui??
basePath = r"" + sys.argv[1]
baseDestPath = r"" + basePath + "\Packaged Files"

def checkSubdir(folder):
    global basePath, baseDestPath, count

    # Get the immediate subdirectories
    subdirs = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

    # Iterate through each subdirectory
    for subdir in subdirs:
        # Avoid checking the destination folder for programs
        if subdir == "Packaged Files": continue
        subdirPath = os.path.join(folder, subdir)
        files = os.listdir(subdirPath)
        targetFiles = []
        # Identify the number of .cpp files in the folder (if there are any)
        for file in files:
            if file.endswith(".cpp") or file.endswith(".h"):
                targetFiles.append(file)
                if verbose: print(f"{file} found in '{subdirPath}'")
        if verbose: print(f"Found {len(files)} files ({len(targetFiles)} .cpp) in '{subdirPath}'")
        
        if len(targetFiles) == 0:
            # If there are no .cpp files, check further subdirectories
            checkSubdir(subdirPath)
        elif len(targetFiles) == 1:
            # Create any needed subdirectories in the destination path
            destPath = os.path.join(baseDestPath, folder.replace(basePath, "")[1:])
            os.makedirs(destPath, exist_ok=True)

            # If there's only one .cpp file, no folder will be made and it will simply be renamed to its parent project
            # [1:] is needed to remove the leading \ of the folder file path
            destFile = os.path.join(destPath, f"{subdir}.cpp")
            shutil.copy2(os.path.join(subdirPath, targetFiles[0]), destFile)
            count += 1
            if verbose: print(f"Copied single-file project to '{destFile}'")
        else:
            destPath = os.path.join(baseDestPath, folder.replace(basePath, "")[1:], subdir)
            os.makedirs(destPath, exist_ok=True)
            if verbose: print(f"Created folder for multi-file project {subdir} to '{destPath}'")

            for file in targetFiles:
                destFile = os.path.join(destPath, file)
                shutil.copy2(os.path.join(subdirPath, file), destFile)
                count += 1
                if verbose: print(f"Copied file from multi-file project to '{destFile}'")

if not os.path.exists(basePath):
    print(f"Error: Path '{basePath}' does not exist.")

# Run main script
os.makedirs(baseDestPath, exist_ok=True)
checkSubdir(basePath)

# Zip and delete original folder
shutil.make_archive(baseDestPath, "zip", baseDestPath)
shutil.rmtree(baseDestPath)

print(f"Packaged {count} files to '{baseDestPath}.zip'")
