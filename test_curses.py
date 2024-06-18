# *****************************************************
# * Author: Charles Poulin-Bergevin
# * project: Automatic headers script
# * comment: automatically generate code files headers
# * file: header_script.py
# * need to use curses menu
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
    posy, posx = stdscr.getyx()
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
    
    stdscr.move(posy, posx)
    stdscr.refresh()
    return message

def printTitle(stdscr):
    stdscr.addstr( 2, 5, 'enter \'q\' to quit')

def printChoices(stdscr):
    stdscr.clear()
    stdscr.refresh()
    printTitle(stdscr)
    stdscr.addstr( 3, 5, '1. add header to a file in a directory:')
    stdscr.addstr( 4, 5, '2. add header to multiple files in a directory:')
    stdscr.addstr( 5, 5, '3. add header to types of files in a directory:')
    stdscr.addstr( 6, 5, '4. add header to all files in a directory:')
    stdscr.addstr( 7, 5, '5. add header to all files in all the sub-directories:')
    stdscr.move(7,5)
    return (7, 5)

def main(stdscr):
    
    while True:
                
        posy, posx = printChoices(stdscr)
        num_of_choices = posy - 3
        
        while True:
          i = stdscr.getkey()
          match i:
            case 'w':
                if posy > 3:
                    stdscr.move(posy - 1,posx)
                    posy = posy - 1
                    stdscr.refresh()
            case 's':
                if posy < num_of_choices:
                    stdscr.move(posy + 1,posx)
                    posy = posy + 1
                    stdscr.refresh()
            case ' ':
                i = stdscr.getyx()[0] - 3
                break
            case 'q':
                break

         
        if (i =='q'):
            break
        fields = []
        
        # 
        # fields.append(['Project', input('Enter  file(s) project name: ')])
        # fields.append(['Comment', input('Enter  file(s) project comment: ')])
        
        stdscr.clear()
        stdscr.addstr( 2, 5, 'enter \'q\' to quit')
        stdscr.addstr( 3, 5, 'file(s) author(s): ')
        stdscr.move(3, 24)
        posx = 24
        posy = 3
        answer = getString(stdscr, posy + 1, 5)
        stdscr.addstr(posy, posx, answer)
        stdscr.refresh()
        fields.append(['Author', answer])

        ##################HERE##################
        
        print(TAG + 'If you dont want to add fields enter \'q\' to quit')
        while True:
            fields.append([input(TAG + 'Enter field name: '), input(TAG + 'Enter field value: ')])
            if (fields[-1][0] == 'q'):
                fields.pop()
                break

        name = []

        match i:
            case '1':
                name.extend(' ')
                name[0] = input(TAG + 'Enter complete file path and name (including file extension): ')
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
