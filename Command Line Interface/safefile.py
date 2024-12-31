import base64
import AES as aes
import os

def encfile (file, key) :
    filename = file[file.rfind("/")+1 :]
    newfile = file[: file.rfind("/")+1] + filename[:filename.rfind(".")] + ".bin"
    out = newfile
    with open(file, 'rb') as file:
        binary_data = file.read()
        text_data = base64.b64encode(binary_data).decode('utf-8')
        crypt = aes.enc(text_data, key).encode()
    
    with open(newfile, 'wb') as newfile:
        newfile.write(crypt)
        newfile.write("\n".encode())
        newfile.write(filename.encode())
        
    return out

def decfile (encfile, key) :
    path = encfile[: encfile.rfind("/")+1]
    out = encfile
    with open(encfile, 'rb') as file:
        crypt = file.read().decode()
    
    filename = crypt[crypt.rfind("\n")+1 :]
    crypt = crypt[:crypt.rfind("\n")]
    text_data = aes.dec(crypt, key)
    binary_data = base64.b64decode(text_data)
    newfile = path + filename
    with open(newfile, 'wb') as file:
        file.write(binary_data)
        
    return out
        

def encfolder(path, key):
    folder = path[path.rfind("/") + 1:]
    newfolder = path[: path.rfind("/") + 1] + "#" + folder
    os.makedirs(newfolder, exist_ok=True)

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    for file in files:
        fpath = os.path.join(path, file)
        with open(fpath, 'rb') as cfile:
            binary_data = cfile.read()
            text_data = base64.b64encode(binary_data).decode('utf-8')
            crypt = aes.enc(text_data, key).encode()

        newfile_path = os.path.join(newfolder, file[:file.rfind(".")] + ".bin")
        with open(newfile_path, 'wb') as newfile:
            newfile.write(crypt)
            newfile.write("\n".encode())
            newfile.write(file.encode())

    for folder_name in folders:
        subfolder_path = os.path.join(path, folder_name)
        encfolder(subfolder_path, key)
        
    return newfolder
        

def decfolder(path, key):
    folder = path[path.rfind("#") + 1 :]
    newfolder = os.path.join(path[: path.rfind("/")+1], folder)
    os.makedirs(newfolder, exist_ok=True)

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    for file_name in files:
        file_path = os.path.join(path, file_name)
        with open(file_path, 'rb') as file:
            crypt = file.read().decode()
            filename = crypt[crypt.rfind("\n")+1 :]
        crypt = crypt[:crypt.rfind("\n")]
        text_data = aes.dec(crypt, key)
        binary_data = base64.b64decode(text_data)

        newfile_path = os.path.join(newfolder, filename)

        with open(newfile_path, 'wb') as newfile:
            newfile.write(binary_data)

    for folder_name in folders:
        subfolder_path = os.path.join(path, folder_name)
        decfolder(subfolder_path, key)
        
    return path

#encfile("C://Users//Venu Pulagam//Desktop//AES.pdf", "Thats my Kung Fu")
#decfile("C://Users//Venu Pulagam//Desktop//created.bin", "Thats my Kung Fu")

#encfolder('C://Users//Venu Pulagam//Desktop//TEST', "Thats my Kung Fu")
#decfolder('C://Users//Venu Pulagam//Desktop\\#TEST', "@hellotesT123   ")

#encfile("C://Users//Venu Pulagam//Desktop//video.mp4", "Thats my Kung Fu")
#decfile("C://Users//Venu Pulagam//Desktop//video.bin", "Thats my Kung Fu")