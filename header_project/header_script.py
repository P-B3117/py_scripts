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


def main():
    while True:
        print(TAG + 'enter \'q\' to quit')
        print(TAG + '1. add header to a file in a directory:')
        print(TAG + '2. add header to multiple files in a directory:')
        print(TAG + '3. add header to types of files in a directory:')
        print(TAG + '4. add header to all files in a directory:')
        print(TAG + '5. add header to all files in all the sub-directories:')
        i = input(TAG + 'your choice: ')

        if (i =='q'):
            print(TAG + 'have a great day!')
            break

        fields = []
        
        fields.append(['Author', input('Enter  file(s) author(s): ')])
        fields.append(['Project', input('Enter  file(s) project name: ')])
        fields.append(['Comment', input('Enter  file(s) project comment: ')])
        
        
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
    main()
