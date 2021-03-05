# This project is used to organize your library and output a catalog of what is where.
# Main functions:
# -Separate PDF's or files with the same name into folders
# -Output a file with the names and contents of everything in the directory.
# Usage:
# Set the to be processed directory in the script.

import os
from os import listdir
import shutil
from math import log

# CHANGE ME to the directory with all the files.
walk_dir=r"C:\Users\user\Downloads\Moebius_MoreByHumanoids"

def countItemsInList(list, item):
    count = 0
    for element in list:
        if (element == item):
            count = count + 1
    return count

# The following is used for "infering spaces" from a String.
# Reference/Source https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("commonWordsAndNames.txt", encoding="utf8").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has been built for the i-1 first characters. Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))

def infer_caps(s):
    """Uses dynamic programming to infer the location of spaces in a string without spaces."""

    # Find the best match for the i first characters, assuming cost has been built for the i-1 first characters. Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    newOut = []
    for word in out:
        word = word[0:1].upper()+word[1:]
        newOut.append(word)

    #return " ".join(reversed(out))
    return "".join(reversed(newOut))

#######################################################################################################
############################################### MAIN ####################################################
#######################################################################################################

# Test if infer spaces works.
s = 'thumbgreenappleactiveassignmentweeklymetaphorbobsmithiscool'
print(infer_spaces(s))

print(walk_dir)

#Use this if you want to run via command line with args
#import sys
#walk_dir = sys.argv[1]

directory_contents = ""
folderCount = 0
fileCount = 0

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    print('--\nroot = ' + root)
    list_file_path = os.path.join(root, 'my-directory-list.txt')
    print('list_file_path = ' + list_file_path)
    directory_contents = directory_contents + 'list_file_path = ' + list_file_path + "\n"

    for subdir in subdirs: #For each subdirectory in this directory
        print('\t- subdirectory ' + subdir + "\n")
        directory_contents = directory_contents + '\t- subdirectory ' + subdir + "\n"
        folderCount = folderCount + 1

    extensionList = list()
    cleanFolderFileList = list()
    duplicateFileList = list()
    fullPathList = list()
    directoryModified = 0

    for filename in files: #For each file in this directory
        file_path = os.path.join(root, filename)

        #Track the contents of the directory
        splitList = filename.split(".")
        if len(splitList) != 2:
            if len(splitList) > 2: #if it's greater than 2, connect the first elements and return a list of two items.
                # {x.y.z}.{pdf}
                print("Fixing multiple periods in name.")
                #x,y,z,pdf
                #0,1,2,3

                countDown = len(splitList) - 1 #convert to list. Countdown is the largest number- contains .pdf
                firstPiece = ""
                while (countDown >= 1):
                    if countDown == len(splitList) - 1:
                        firstPiece = firstPiece + splitList[countDown - 1]
                    else:
                        firstPiece = splitList[countDown - 1] + "." + firstPiece
                    countDown = countDown - 1
                splitList[0] = "".join(firstPiece)
                splitList[1] = splitList[len(splitList)-1]
                print("Created " + splitList[0])
            else:
                print("Invalid File Name + [" + filename + "]")
                exit()
        # This will take the extention and be used to track what's in the directory later.
        print("Found: " + splitList[0])
        print("Full string is " + str(splitList[0]) + "(period)" + str(splitList[1]))
        extensionList.append(splitList[1])
        duplicateFileList.append("".join(splitList[0]+"."+splitList[1]))
        # This makes a list of the file name without the extension and special characters. TO be used to make folders
        cleanFolderFileList.append(''.join(e for e in "".join(splitList[0]) if e.isalnum()))

        print('\t- file %s (full path: %s)' % (filename, file_path) + "\n")
        fullPathList.append(file_path)
        directory_contents = directory_contents + '\t- file %s (full path: %s)' % (filename, file_path) + "\n"

    # If there are more than 1 type of file in the same directory, create a folder, put that file in it, then process it.
    finishedList = list()
    for x in extensionList:
        if x not in finishedList:
            print("Checking: " + x)
            count = countItemsInList(extensionList,x)
            print(x + " has " + str(count) + " occurrence.")
            if count > 1:
                directoryModified = 1
                print("\tThere are multiple items of [" + x + "] in this list.")
                directory_contents = directory_contents + "There are multiple items of [" + x + "] in this list." + "\n"

                # There is more than one of one item.
                # Go though each file and make a folder for it.
                iterator = 0
                #Create the folders
                print("Creating Folders")
                for file in cleanFolderFileList:
                    # removing substring from end
                    file = infer_caps(file)
                    if fullPathList[iterator].endswith(duplicateFileList[iterator]):
                        res = fullPathList[iterator][:-(len(duplicateFileList[iterator]))]
                        folder2Make = res + "\\" + file
                    else:
                        print("The file you are working with does not end with the file you thought.")
                        exit()
                    if not os.path.exists(folder2Make):
                        print("Creating folder: [" + folder2Make + "]")
                        os.makedirs(folder2Make)
                    folderCount = folderCount + 1
                    iterator = iterator + 1
                finishedList.append(x)

                # Move the files
                print("Moving Files")
                iterator = 0
                for file in duplicateFileList:
                    #print("Attempting to find [" + file + "] at the end of [" + fullPathList[iterator] + "]")
                    if fullPathList[iterator].endswith(file):
                        res = fullPathList[iterator][:-(len(file)+1)]
                    else:
                        print("The file you are working with does not end with the file you thought.")
                        exit()
                    # Move the file to the new folder. So move "path/to/current/file.foo" , "path/to/new/destination/for/file.foo"
                    shutil.move(res + "\\" + file, res + "\\" + cleanFolderFileList[iterator] + "\\" + file)
                    print("Moved [" + res + "\\" + file + "] to [" + res + "\\" + cleanFolderFileList[iterator] + "\\" + file + "]")
                    iterator = iterator + 1
                    directory_contents = directory_contents + "This directory has been updated to account for the duplicates.\n"

    directory_contents = directory_contents + "\n"

print("Done reading directories")
print(directory_contents)

with open(walk_dir+"\DiscorveredPaths.txt", 'w') as list_file:  # for each path found, report the concents
    list_file.write(directory_contents.encode('utf-8'))
    list_file.write(b'\n')

