import glob
import os
import pathlib

def header(filename, author, project, project_comment, commentsign = '//'):
    text = f'{commentsign} *****************************************************\n'
    text += f'{commentsign} * Author: {author}\n'
    text += f'{commentsign} * project: {project}\n'
    text += f'{commentsign} * comment: {project_comment}\n'
    text += f'{commentsign} * file: {filename}\n'
    text += f'{commentsign} *****************************************************\n'
    return text
def writeHeader(paths, author, project, project_comment):
    print(paths)
    for file in paths:
        filename = os.path.basename(file)
        print(f'opening: {filename}')
        with open(file, 'r', encoding="utf-8") as f:
            filedata = f.read()

    # Write the new file
        if (filename.endswith('.py')) :
            with open(file, 'w', encoding="utf-8") as f:
                f.write(header(filename, commentsign='#', author=author, project=project, project_comment=project_comment) + '\n' + filedata)
        else:
            with open(file, 'w', encoding="utf-8") as f:
                f.write(header(filename, author=author, project=project, project_comment=project_comment) + '\n' + filedata)

def getFiles(typesTuple=('*.cpp', '*.h', '*.hpp'), filePath='/'):
    files_grabbed = []
    currentDir = pathlib.Path().resolve()

    if (filePath[-1] != '/' and filePath[-1] != '\\'): filePath = filePath + '\\'
    if (filePath[0] != '/' and filePath[0] != '\\'): filePath = '\\' + filePath
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
        i = input()

        if (i =='q'):
            print('have a great day!')
            break

        author = input('Enter  file(s) author(s): ')
        project_name = input('Enter  file(s) project name: ')
        project_comment = input('Enter  file(s) project comment: ')

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

        writeHeader(paths=name, author=author, project= project_name, project_comment= project_comment)


if __name__ == '__main__':
    main()
