import os

def write_file(file_path, file_contents):

    directory = os.path.dirname(file_path)

    if not os.path.isdir(directory):
        os.makedirs(directory)

    file = open(file_path, 'w')
    file.write(file_contents)
    file.close()