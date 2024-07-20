import imdb
import webbrowser
import os
import sys
import re
from pprint import pprint
from os import walk

# Using the Search movie method

def yesno(msg):
    user_input = input(msg)
    if user_input.lower() == "y":
        return True
    else:
        return False

def getarg():
    if(len(sys.argv) < 2):
        return os.getcwd()
    else:
        return sys.argv[1]

def sanitizename(orig_name):
    name = re.sub(r'(\[(.*?)\])|\((.*?)\)','',orig_name)
    name=name.strip()
    return name

def rename_file(path, orig_name, movieid):
    finalname = orig_name + " [imdbid-tt"+movieid+"]"
    if yesno('Correct Movie ?, Rename ? \''+finalname+'\' (y/n): '):
        os.rename(path+os.sep+orig_name, path+os.sep+finalname)
        return True
    return False

def display_option(i, movies):
    printlines(1)
    print(f'Index-{i+1} - \'{movies[i]['title']}\'')
    url = "https://www.imdb.com/title/tt"+ movies[i].movieID+"/"
    print(f'opening - {url}')
    webbrowser.open(url, autoraise=False)

def debug(msg):
    if DEBUG :
        print('=================:'+msg)

def get_regex(count):
    if(count < 10) :
        return r'^[sx1-'+str(count)+']{1}$'
    elif (count < 20) :
        return r'^([1-9]|1[0-'+str(count-10)+']|[sx])$'
    elif (count == 20) :
        return r'^([1-9]|1[0-9]|20|[sx])$'

def cap_count(count):
    if(count > 20):
        count = 20
    return count

def cap_list(movies):
    if(len(movies) > 20):
        movies = movies[:20]
    return movies

def custom_retry_options(movies):
    count = len(movies)
    option_regex = get_regex(count)
    debug(option_regex)

    retry_input = True
    while(retry_input):  
        printlines(1)  
        print('Select below options for retry:')    
        printmovies(movies)
        print(f's. Search with a custom movie name:')
        print(f'x. Skip this movie folder and try next entry:')
        x = input('Enter your choice :')
        if(re.search(option_regex,x)):
            return x
        else:
            print(f'ERROR : Incorrect entry : \'{x}\'')
    
def skip_movie(orig_name):
    if "[imdbid-" in orig_name:
        print(f"Skipping {orig_name}...")
        return True
    else :
        return False

def updatename(path, orig_name, handle):

    if skip_movie(orig_name):
        return False
    
    name = sanitizename(orig_name)
    print(f'Folder Name - \'{orig_name}\', Searching with \'{name}\'')

    keep_trying_options = True
    while(keep_trying_options) :
        movies = cap_list(handle.search_movie(name))
        # pprint(vars(movies[0]))
        searchlen = len(movies)

        if(searchlen == 0):
            print(f'No search results found for \'{name}\'')
            if yesno('Type movie name(y) or skip renaming this folder(n) - (y/n):'):
                name = input('Enter movie name to search:')
                continue
            else:
                keep_trying_options = False
                continue

        print(f'Search results for \'{name}\':{searchlen}')
        printmovies(movies)
        i = 0
        curr_search_valid = True
        while(curr_search_valid):
            display_option(i, movies)
            if rename_file(path, orig_name, movies[i].movieID):
                return True
            else:
                print(f'Current search list count :{searchlen}')
                x = custom_retry_options(movies)
                if(x == 'x'):
                    return False
                elif (x == 's'):
                    name = input('Enter movie name to search:')
                    curr_search_valid = False
                    continue
                else:
                    i = int(x) - 1


def printmovies(movies, count = 5):
    count = len(movies)
    for i,m in enumerate(movies):
        year = ''
        if 'year' in m.data:
            year = '(' + str(m['year']) + ')'
        print(f'{i+1}. {m['title']} {year} - tt{m.movieID}')




def printlines(n):
    for i in range(n):
        print('')

def printdivider(n):
    for i in range(n):
        print('-------------------------------------')

def printorderedlist(dir_list):
    for i, m in enumerate(dir_list, 1):
        print(f'{i}. {m}')
    print('')

def wipe_existing_imdbid(path):
    path = getarg()
    dir_list = os.listdir(path)
    if yesno('Wipe imdbid from folder names ? (y/n) :'):
        for m in dir_list:
            new_name = re.sub(r'\[imdbid-tt\d+\]','', m)
            if(new_name != m):
                os.rename(path+os.sep+m, path+os.sep+new_name)

def movie_rename(path):
    print('Starting movie renaming script')
    # MAIN creating an instance of the IMDB()
    # path = getarg()
    ia = imdb.IMDb()

    print(f'\nComputing for movies in path {path}')
    dir_list = os.listdir(path)
    printorderedlist(dir_list)
    yesno('Let\'s start ? (type any key to continue)')

    total_count = len(dir_list)
    for i,m in enumerate(dir_list, 1):
        print(f"Progress - {i}/{total_count}\n")
        updatename(path, m, ia)
        printlines(2)
        printdivider(1)

def list_metadata(path):
    dir_list = os.listdir(path)
    f = []
    e =set()
    for(dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        for file_name in filenames:
            e.add(get_ext_from_filename(file_name))
    print(e)

def wipe_metadata(path, exts, dry_run):
    dir_list = os.listdir(path)
    f = []
    exempt = []
    for(dirpath, dirnames, filenames) in walk(path):
        for file_name in filenames:
            if(does_file_match_extension(file_name, exts)):
                f.append(os.path.join(dirpath, file_name))
            else:
                exempt.append(os.path.join(dirpath, file_name))
    print("files to be deleted")
    print_list(f)
    # print("files to be exempted")
    # print_list(exempt)
    if(dry_run):
        print("this was a dry run, no files were deleted")
    else:
        for file in f:
            os.remove(file)
            print(f"deleted : {file}")

def does_file_match_extension(file_name, exts):
    ext = get_ext_from_filename(file_name)
    if ext in exts:
        return True
    return False

def print_list(list):
    for i,l in enumerate(list, 1):
        print(f"{i}. {l}")

def get_ext_from_filename(file_name):
    return os.path.splitext(file_name)[1][1:]

DEBUG = True
# START

if(len(sys.argv) < 2):
    command = "rename"
    path = os.getcwd() 
elif (len(sys.argv) < 3):
    command = "rename"
    path = sys.argv[1]
elif(len(sys.argv) >= 3):
    command = sys.argv[1]
    path = sys.argv[2]
    if(len(sys.argv) > 3):
        exts = sys.argv[3].split(",")
        

if(command == 'list-metadata'):
    print("listing metadata")
    list_metadata(path)
elif(command == 'wipe-metadata-soft'):
    print(f"dry run for wiping metadata for extensions {exts}")
    wipe_metadata(path, exts, True)
elif(command == 'wipe-metadata-hard'):
    print(f"wiping metadata for extensions {exts}")
    wipe_metadata(path, exts, False)    
elif(command == 'rename'):
    print(f"renaming movie for path: {path}")
    movie_rename(path)
else:
    print(f"command '{command}' does not exist")
# wipe_existing_imdbid(path)


    
