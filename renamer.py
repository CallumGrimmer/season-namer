# Renamer tool
# 
# This tool takes a folderpath and an imdb url then renames alphabetically sorted
# video files found at that path with the corresponding episode found at the url
#
# Callum Grimmer 2018

import os
import sys
import fleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

#
# Navigates to the folder, grabs only video files and renames them
# episodes: a list of strings
#
def rename( episodes ):
    i = 0
    #folderpath defaults to where program is run, otherwise grabs first input arg
    folderpath = os.path.dirname(os.path.abspath(__file__))
    if sys.argv[1] is not  None:
        folderpath = sys.argv[1]
    try:
        files = os.listdir(folderpath)
    except FileNotFoundError:
        print("ERROR: the given file path could not be found")
        print("check the following path is correct: ")
        print (str(folderpath))
        sys.exit()
    
    files.sort()

    #grabs video files
    for filename in files:
        
        #checking if object is directory as fleep cannot handle directories
        if os.path.isfile(os.path.join(folderpath,filename)):
            with open(os.path.join(folderpath,filename),"rb") as file:
                info = fleep.get(file.read(128))
            #print("filetype: ",info.type) #debug
            
            #fleep sometimes alters the file extension
            #so keeping the original file extension using os module
            fileExtension = os.path.splitext(filename)[1]
            #some smaller files or odd extensions don't have an file type
            if (len(info.type)) > 0:
                if info.type[0] == 'video':
                    #print(info.type[0]) #debug
                    #print("episode " + str(i+1)) #debug
                    if i+1 > len(episodes): #bounds checking
                        print("filename: ",filename)
                        return
                    else:
                        print("filename: ",filename, end=' -->  ') #debug
                        
                    os.rename(os.path.join(folderpath,filename),
                              os.path.join(folderpath,str(i+1) + '_' + episodes[i] + str(fileExtension)))
                    print(episodes[i] + str(i+1) + '_' + str(fileExtension))
                    i = i + 1
#        
# Removes quotation marks and trailing square brackets
#
def cleanText( title ):
    matches = re.findall('"(.*?)"',title)
    if len(matches) > 0:
        return matches[0]
    else:
        return title


#
# Makes the call to the imdb url and uses beautiful soup to get an episode list
#
def getEpisodeNames():
    episodes = []
    url = ''
    if(sys.argv[2]) is None:
        print("no imdb url detected. This should be passed as a second argument")
        print("format is: python3 renamer.py folderpath imdburl")
        return
    else:
        url = sys.argv[2]

    match = re.findall("imdb",url)
    if len(match) < 1:
        raise ValueError("given url is not for imdb")
        sys.exit()

    try:
        page = urlopen(url)
    except Exception as e:
        print(str(e))
        print("There was an networking error going to the following url:")
        print(str(url))
        sys.exit()
    
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all("a",attrs={'itemprop':'name'}):
        episodes.append(cleanText(link.getText()))

    if len(episodes) < 1:
        raise RuntimeError("no episodes were found at that url")
        sys.exit()
    

    rename(episodes)

    #for episode in episodes: #debug
        #print("found episode: " + episode)



getEpisodeNames()

