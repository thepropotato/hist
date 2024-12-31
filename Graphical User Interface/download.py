import os
import boto3
from botocore.exceptions import NoCredentialsError
from secret import aws_access_key_id as aws_access_key_id
from secret import aws_secret_access_key as aws_secret_access_key
from tqdm import tqdm
import json
import tkinter as tk
from tkinter import filedialog
from safefile import *
from passman import *
import shutil
from AES import *
from tkinter import simpledialog

res = ""

def downloadfile(username, filename, downpath, word, s3):
    
    bucket_name = username
    pword = readpass(username, word, s3)

    try:
        s3.download_file(bucket_name, "files/"+filename, downpath+"//"+filename)
        oldfile = decfile(downpath+"//"+filename, pword)
        res = ("Download successfull\n")
        os.remove(oldfile)

    except Exception as e:
        res = (f"Error Downloading file: {e}\n")
        
    print(res)
    
    return res
        
        

def downloadfolder(username, folder_prefix, local_folder_path, word, s3):
    
    bucket_name = username
    pword = readpass(username, word, s3)

    local_folder_path = local_folder_path + "//" + folder_prefix
    os.makedirs(local_folder_path, exist_ok=True)

    try:
        objects = s3.list_objects_v2(Bucket=bucket_name, Prefix="folders/" + folder_prefix).get('Contents', [])
        if objects:
            print("Downloading...")
            for obj in objects:
                # Extract the relative path from the object's key
                rel_path = os.path.relpath(obj['Key'], "folders/" + folder_prefix)
                local_file_path = os.path.join(local_folder_path, rel_path)

                # Create necessary directories for nested folders
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                s3.download_file(bucket_name, obj['Key'], local_file_path)
                
            res = ("Download successfull\n")
                
        else:
            res = ("Folder is empty\n")
            
        oldfold = decfolder(local_folder_path, pword)
        shutil.rmtree(oldfold)

    except Exception as e:
        res = (f"Error downloading folder: {e}\n")
        
    print(res)
    
    return res
        
    

def downloadpass(username, webname, word, s3) :
    
    word = readpass(username, word, s3)

    try:
        response = s3.get_object(Bucket=username, Key="passwords/"+webname)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)[0]
        uname = data.get("username")
        pword = data.get("password")
        pword = dec(pword, word)
        
        print(f"Credentials for the website {webname} : ")
        print(f"username/ email-id/ mobile number : {uname}")
        print(f"Password : {pword}\n")
        
        return str(uname) + "+" + str(pword)
    
    except FileNotFoundError:
        print(f"The website '{webname}' does not exist '{username}'.")
    except NoCredentialsError:
        print("Credentials not available or incorrect.")
        

def download(username, word, s3) :
    print("\nAvaialble options to DOWNLOAD : \n 1. Files\n 2. Folders\n 3. Passwords\n")
    oper = input("Enter the index of the type of data you want to Download : ")
    if oper == "1" :
        root = tk.Tk()
        root.withdraw()
        filename = input("Enter the name of the file you want to download : ")
        file_path = filedialog.askdirectory(title="Select a location to save the file")
        print("Decrypting and Downloading the file...")
        downloadfile(username, filename, file_path, word, s3)
    elif oper == "2" :
        root = tk.Tk()
        root.withdraw()
        foldername = input("Enter the name of the folder you want to download : ")
        folder_path = filedialog.askdirectory(title="Select a location to save the folder")
        print("Decrypting and Downloading the folder...")
        downloadfolder(username, foldername, folder_path, word, s3)
    elif oper == "3" :
        webname = input("Enter the name of the site : ")
        downloadpass(username, webname, word, s3)
    else :
        print("Invalid data type (index) selected. Please enter a valid index.")
        

def download_file_gui(username, word, s3, filename):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(title="Select a location to save the file")
    print("Decrypting and Downloading the file...")
    res = downloadfile(username, filename, file_path, word, s3)
    return res
    
def download_folder_gui(username, word, s3, foldername):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a location to save the folder")
    print("Decrypting and Downloading the folder...")
    res = downloadfolder(username, foldername, folder_path, word, s3)
    return res
    
def download_password_gui(username, webname, word, s3):
    out = downloadpass(username, webname, word, s3)
    un, pw = out.split('+')
    mess = "Username : "+ un + "\n" + "Password : " + pw
    simpledialog.messagebox.showinfo("Credentials for "+ webname + " : ", mess)

    