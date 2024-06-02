import imdb
import webbrowser
import os
import sys
import re


# Using the Search movie method

def getval(default):
    user_input = input(f'Search with name \'{default}\' ? (y/n): ')
    if user_input.lower() == "y":
        return default
    else:
        return input(f'Input new value: ')

def yesno(msg):
    user_input = input(msg)
    if user_input.lower() == "y":
        return True
    else:
        return False

def getpath():
    if(len(sys.argv) < 2):
        return os.getcwd()
    else:
        return sys.argv[1]

def sanitizename(orig_name):
    name = re.sub(r'\[(.*?)\]','',orig_name)
    name = re.sub(r'\((.*?)\)','',name)
    name=name.strip()
    return name

def updatename(path, orig_name, handle):
    
    if "[imdbid-" in orig_name:
        print(f"skipping {orig_name}...")
        return
    
    name = sanitizename(orig_name)
    name = getval(name)
    print(f'Folder Name - :{orig_name}:, Searching with :{name}:')
    movies = handle.search_movie(name)
    searchlen = len(movies)
    if (searchlen > 0):
        for i in range(searchlen):
            print(f'{i} Found - :{movies[i]['title']}:')
            url = "https://www.imdb.com/title/tt"+ movies[i].movieID+"/"
            print(f'opening - {url}')
            webbrowser.open(url)
            finalname = orig_name + " [imdbid-tt"+movies[i].movieID+"]"
            if yesno('Is this the correct one ? ( rename to :'+finalname+': (y/n): '):
                os.rename(path+"\\"+orig_name, path+"\\"+finalname)
                return
            else:
                print("Incorrect Search Result, skipping...")
                if yesno("Try next search option ? (y/n): "):
                    pass
                else:
                    return

# MAIN creating an instance of the IMDB()
path = getpath()
ia = imdb.IMDb()

print(f'Computing for movies in path {path}')
dir_list = os.listdir(path)
os.system('cls')

for m in dir_list:
    updatename(path, m, ia)
    os.system('cls')

    
