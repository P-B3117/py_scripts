# *****************************************************
# * Author: Charles Poulin-Bergevin
# * project: Automatic headers script
# * comment: automatically generate code files headers
# * file: header_script.py
# * need to have a function to get path: https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
# *****************************************************

import glob
import os
import pathlib
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

TAG = 'header_script.py: '

START_TAG = 'S-HEADER'
END_TAG = 'E-HEADER'
HEADER_LINE = '*****************************************************'
 
# the default comment sign is: // 
# so the languages that uses it may be not listed
supportedLangs = []
supportedLangs.append(['.py', '#'])
supportedLangs.append(['.cpp', '//'])
supportedLangs.append(['.hpp', '//'])
supportedLangs.append(['.c', '//'])
supportedLangs.append(['.h', '//'])
supportedLangs.append(['.java', '//'])
supportedLangs.append(['.kt', '//'])
supportedLangs.append(['.tex', '%'])
supportedLangs.append(['.rb', '#'])
supportedLangs.append(['.r', '#'])
supportedLangs.append(['.pl', '#'])


def header(filename, fields, commentsign = '//'):
    text = commentsign + START_TAG + '\n'
    text += f'{commentsign} {HEADER_LINE}\n'
    
    for i in fields:
        text += f'{commentsign} * {i[0]} : {i[1]}\n'
    
    text += f'{commentsign} * file: {filename}\n'
    text += f'{commentsign} {HEADER_LINE}\n'
    text += commentsign + END_TAG + '\n'
    return text


def writeHeader(paths, fields):

    print(TAG + paths.__str__())
    for file in paths:
        filename = os.path.basename(file)
        print(TAG + f'opening: {filename}')
        with open(file, 'r', encoding="utf-8") as f:
            filedata = f.read()

    # Write the new file
        if (filename == 'header_script.py'):
            print(TAG + 'can\'t rewrite the script file')

        else:
            name, extension = os.path.splitext(filename)
            sign = '//'
            STOPFLAG = False

            for x in supportedLangs:
                if x[0] == extension:
                    sign = x[1]
                    break
            
            if filedata.partition('\n')[0].__contains__(sign + START_TAG):

                i = input(TAG + 'There is already a header, what do you wanna do with it:\n1: update it\n2: keep it\n')
                match i:
                    case '1':
                        filedata = filedata.partition(sign + END_TAG + '\n')[1]

                    case '2':
                        STOPFLAG = True

            if STOPFLAG == False:
                with open(file, 'w', encoding="utf-8") as f:
                    f.write(header(filename, commentsign=sign, fields= fields) + '\n' + filedata)


def getFiles(typesTuple=('*.cpp', '*.h', '*.hpp'), filePath='/'):
    files_grabbed = []
    currentDir = pathlib.Path().resolve()
    if (os.name == 'posix'):
        if (filePath[-1] != '/'): filePath = filePath + '/'
        if (filePath[0] != '/'): filePath = '/' + filePath
    elif (os.name == 'nt'):
        if (filePath[-1] != '\\'): filePath = filePath + '\\'
        if (filePath[0] != '\\'): filePath = '\\' + filePath

    filePath = str(currentDir) + filePath

    if (typesTuple != '**'):
        for files in typesTuple:
            if files[0] == '/':
                files.pop(0)
            print(TAG + f'Processing {filePath + files}')
            files_grabbed.extend(glob.glob(filePath + files, recursive=True))
    else:
        print(TAG + f'Processing {filePath}')
        files_grabbed.extend(glob.glob(filePath + '**/*', recursive=True))

    files_grabbed = [file for file in files_grabbed if os.path.isfile(file)]

        # files_grabbed is the list of files corresponding to the types
    return files_grabbed

def getString(stdscr, y = 1, x = 2, width = 50, height = 5):
    editwin = curses.newwin(height,width, y+1,x+1)
    rectangle(stdscr, y,x, 1+y+height, 1+x+width)
    stdscr.refresh()

    box = Textbox(editwin)

    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()
    for i in range(height):
        stdscr.move(y + i, x)
        stdscr.clrtoeol()
    
    stdscr.move(y, x)
    stdscr.refresh()
    message = message.strip()
    return message

def printTitle(stdscr):
    stdscr.addstr( 2, 5, 'Use space to select and wasd to move     Ctrl+g to stop txt editing')



def choose(stdscr, choices):
    y = 2
    x = 5
    stdscr.clear()
    stdscr.refresh()
    printTitle(stdscr)
    for choice in choices:
        y += 1
        stdscr.addstr( y, x, str(y-2) + ': ' + choice)
    stdscr.move(y,x)
    num_of_choices = y - 2
        
    while True:
        i = stdscr.getkey()
        match i:
            case 'w':
                if y > 3:
                    stdscr.move(y - 1,x)
                    y = y - 1
                    stdscr.refresh()
            case 's':
                if y < num_of_choices + 2:
                    stdscr.move(y + 1,x)
                    y = y + 1
                    stdscr.refresh()
            case ' ':
                i = stdscr.getyx()[0] - 2
                break
            case 'q':
                break
    return (i, y, x)

def addField(stdscr, field_array, field = ''):
    if field == '':
        field_question = 'Enter the field name: '
        stdscr.clear()
        printTitle(stdscr)
        stdscr.addstr( 3, 5, field_question)
        x = 6 + len(field_question)
        y = 3
        stdscr.move(3, x)
        field = getString(stdscr, y + 1, 5)
    stdscr.clear()
    printTitle(stdscr)
    stdscr.addstr( 3, 5, field)
    x = 6 + len(field)
    y = 3
    stdscr.move(3, x)
    answer = getString(stdscr, y + 1, 5)
    stdscr.addstr(y, x, answer)
    stdscr.refresh()
    field_array.append([field + ': ', answer])

def main(stdscr):
    start_choices = []
    start_choices.append('add header to a file in a directory:')
    start_choices.append('add header to multiple files in a directory:')
    start_choices.append('add header to types of files in a directory:')
    start_choices.append('add header to all files in a directory:')
    start_choices.append('add header to all files in all the sub-directories:')
    start_choices.append('Exit:')

    editing_choices = []
    editing_choices.append('add a field')
    editing_choices.append('edit a field')
    editing_choices.append('remove a field')
    editing_choices.append('Exit: ')

    while True:
        

        i, y, x = choose(stdscr, start_choices)
        

         
        if (i == len(start_choices)):
            break
        fields = []
        
        addField(stdscr, fields, 'Author(s)')
        addField(stdscr, fields, 'Project')
        addField(stdscr, fields, 'Comment')
        
        while True:
            c, y, x  = choose(stdscr, editing_choices)
            if (c == len(editing_choices)):
                break
            match c:
                case 1:
                    addField(stdscr, fields)
                case 2:
                    break
                case 3:
                    break
        
        name = []

        match i:
            case 1:
                stdscr.clear()
                name.extend(' ')
                printTitle(stdscr)
                s = getString(stdscr, 3, 5)
                name[0] = s
            case '2':
                print(TAG + 'enter \'q\' to quit')
                names = []
                while True:
                    names.append(input(TAG + 'Enter complete file path and name (including file extension): '))
                    if (names[-1] == 'q'):
                        names.pop()
                        break
                name.extend(names)
            case '3':
                print(TAG + 'enter \'q\' to quit')
                types = []
                while True:
                    types.append('*' + input(TAG + 'Enter complete files type (ex: .cpp): '))
                    if (types[-1] == '*q'):
                        types.pop()
                        break
                path = input(TAG + 'what is the path of your files (/ for current directory):')
                name.extend(getFiles(typesTuple=tuple(types), filePath=path))
            case '4':
                path = input(TAG + 'what is the path of your files (/ for current directory):')
                name.extend(getFiles(typesTuple='*', filePath=path))
            case '5':
                path = input(TAG + 'what is the root of your files (/ for current directory):')
                name.extend(getFiles(typesTuple='**', filePath=path))
            case _:
                print(TAG + 'invalid input')

        writeHeader(paths= name, fields= fields)


if __name__ == '__main__':
    wrapper(main)
