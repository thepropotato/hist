from secret import aws_access_key_id as aws_access_key_id
from secret import aws_secret_access_key as aws_secret_access_key
import boto3

def deletefile (username, filename, s3) :
    try:
        s3.delete_object(Bucket=username, Key="files/"+filename)
        print(f"\nFile '{filename}' deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        
def deletefolder (username, foldername, s3):
    try:
        objects = s3.list_objects_v2(Bucket=username, Prefix="folders/"+foldername).get('Contents', [])

        for obj in objects:
            s3.delete_object(Bucket=username, Key=obj['Key'])

        print(f"\nFolder '{foldername}' and its contents deleted successfully.")

    except Exception as e:
        print(f"Error: {e}")
        
def deletepass (username, webname, s3) :
    try:
        s3.delete_object(Bucket=username, Key="passwords/"+webname)
        print(f"\nCredentials for '{webname}' deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        
def delete (username, s3) :
    print("\nAvaialble options to DELETE : \n 1. Files\n 2. Folders\n 3. Passwords\n")
    oper = input("Enter the index of the type of data you want to delete : ")
    if oper == "1" :
        file_path = input("Enter the name of the file to delete : ")
        deletefile(username, file_path, s3)
    elif oper == "2" :
        folder_path = input("Enter the name of the folder to delete : ")
        deletefolder(username, folder_path, s3)
    elif oper == "3" :
        webname = input("Enter the name of the site to delete : ")
        deletepass(username, webname, s3)
    else :
        print("Invalid data type (index) selected. Please enter a valid index.")