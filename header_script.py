# *****************************************************
# * Author: Charles Poulin-Bergevin
# * project: Automatic headers script
# * comment: automatically generate code files headers
# * file: header_script.py
# * need to implement this reference: https://dotnetcrunch.in/comments-in-different-programming-languages/#Comments_in_Different_Programming_Languages
# * need to use curses menu
# *****************************************************

import glob
import os
import pathlib
import curses

def header(filename, fields, commentsign = '//'):
    text = f'{commentsign} *****************************************************\n'
    
    for i in fields:
        text += f'{commentsign} * {i[0]} : {i[1]}\n'
    
    text += f'{commentsign} * file: {filename}\n'
    text += f'{commentsign} *****************************************************\n'
    return text


def writeHeader(paths, fields):
    print(paths)
    for file in paths:
        filename = os.path.basename(file)
        print(f'opening: {filename}')
        with open(file, 'r', encoding="utf-8") as f:
            filedata = f.read()

    # Write the new file
        if (filename == 'header_script.py'):
            print('can\'t rewrite this script file')
        elif (filename.endswith('.py')) :
            with open(file, 'w', encoding="utf-8") as f:
                f.write(header(filename, commentsign='#', fields= fields) + '\n' + filedata)
        else:
            with open(file, 'w', encoding="utf-8") as f:
                f.write(header(filename, fields= fields) + '\n' + filedata)


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
            print(f'Processing {filePath + files}')
            files_grabbed.extend(glob.glob(filePath + files, recursive=True))
    else:
        print(f'Processing {filePath}')
        files_grabbed.extend(glob.glob(filePath + '**/*', recursive=True))

    files_grabbed = [file for file in files_grabbed if os.path.isfile(file)]

        # files_grabbed is the list of files corresponding to the types
    return files_grabbed


def main():
    while True:
        print('enter \'q\' to quit')
        print('1. add header to a file in a directory:')
        print('2. add header to multiple files in a directory:')
        print('3. add header to types of files in a directory:')
        print('4. add header to all files in a directory:')
        print('5. add header to all files in all the sub-directories:')
        i = input('your choice: ')

        if (i =='q'):
            print('have a great day!')
            break

        fields = []
        
        fields.append(['Author', input('Enter  file(s) author(s): ')])
        fields.append(['Project', input('Enter  file(s) project name: ')])
        fields.append(['Comment', input('Enter  file(s) project comment: ')])
        
        
        print('If you dont want to add fields enter \'q\' to quit')
        while True:
            fields.append([input('Enter field name: '), input('Enter field value: ')])
            if (fields[-1][0] == 'q'):
                fields.pop()
                break

        name = []

        match i:
            case '1':
                name.extend(' ')
                name[0] = input('Enter complete file path and name (including file extension): ')
            case '2':
                print('enter \'q\' to quit')
                names = []
                while True:
                    names.append(input('Enter complete file path and name (including file extension): '))
                    if (names[-1] == 'q'):
                        names.pop()
                        break
                name.extend(names)
            case '3':
                print('enter \'q\' to quit')
                types = []
                while True:
                    types.append('*' + input('Enter complete files type (ex: .cpp): '))
                    if (types[-1] == '*q'):
                        types.pop()
                        break
                path = input('what is the path of your files (/ for current directory):')
                name.extend(getFiles(typesTuple=tuple(types), filePath=path))
            case '4':
                path = input('what is the path of your files (/ for current directory):')
                name.extend(getFiles(typesTuple='*', filePath=path))
            case '5':
                path = input('what is the root of your files (/ for current directory):')
                name.extend(getFiles(typesTuple='**', filePath=path))
            case _:
                print('invalid input')

        writeHeader(paths= name, fields= fields)


if __name__ == '__main__':
    main()
