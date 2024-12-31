import os
import boto3
from botocore.exceptions import NoCredentialsError
from secret import aws_access_key_id as aws_access_key_id
from secret import aws_secret_access_key as aws_secret_access_key
from tqdm import tqdm
import time
import tkinter as tk
from tkinter import filedialog
import json
from safefile import *
from accman import *
from passman import *
import shutil

def uploadfile(username, file_path, word, s3):
    
    bucket_name = username
    pword = readpass(username, word, s3)

    try:
        newfile = encfile(file_path, pword)
        file_name = newfile.split('/')[-1]
        s3.upload_file(newfile, bucket_name, "files/"+file_name)
        print("Upload successfull\n")
        os.remove(newfile)

    except Exception as e:
        print(f"Error uploading file: {e}\n")
        

def uploadfolder(username, folder_path, word, s3):
    bucket_name = username  
    pword = readpass(username, word, s3)

    enfold = encfolder(folder_path, pword)
    fname = enfold.split("/")[-1]

    try:
        total_size = sum(os.path.getsize(os.path.join(root, file)) for root, dirs, files in os.walk(enfold) for file in files)
        
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"\033[94mUploading {fname}\033[0m", ncols=80,
                  bar_format="{l_bar}\033[95m{bar}\033[0m{r_bar}", dynamic_ncols=True) as pbar:
            # Upload each file in the folder
            for root, dirs, files in os.walk(enfold):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    s3_file_path = os.path.relpath(local_file_path, enfold)
                    s3_object_key = f"folders/{fname}/{s3_file_path.replace(os.path.sep, '/')}"

                    s3.upload_file(local_file_path, bucket_name, s3_object_key, Callback=lambda x: pbar.update(x))
        shutil.rmtree(enfold)

        print("Upload successful\n")

    except Exception as e:
        print(f"Error uploading folder: {e}\n")
        

def uploadpass(username, webname, uname, password, word, s3):

    pword = readpass(username, word, s3)
    
    try:
        password = enc(password, pword)
        passdata = json.dumps([{"username": uname, "password": password}], indent=2)
        s3.put_object(Body=passdata, Bucket=username, Key="passwords/"+webname)
        print("Upload successful\n")
        return True
    except FileNotFoundError:
        print("The file was not found\n")
        return False
    except NoCredentialsError:
        print("Credentials not available\n")
        return False
    
def upload(username, word, s3) :
    print("\nAvaialble options to UPLOAD : \n 1. Files\n 2. Folders\n 3. Passwords\n")
    oper = input("Enter the index of the type of data you want to upload : ")
    if oper == "1" :
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select a file")
        "Encrypting and Uploading the file..."
        uploadfile(username, file_path, word, s3)
    elif oper == "2" :
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select a folder")
        "Encrypting and Uploading..."
        uploadfolder(username, folder_path, word, s3)
    elif oper == "3" :
        webname = input("Enter the name of the site : ")
        uname = input("Enter the username/ email-id/ mobile number to be saved : ")
        pword = input("Enter the password to be saved : ")
        "Encrypting and Uploading the folder..."
        uploadpass(username, webname, uname, pword, word, s3)
    else :
        print("Invalid data type (index) selected. Please enter a valid index.")
