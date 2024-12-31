from secret import aws_access_key_id as aws_access_key_id
from secret import aws_secret_access_key as aws_secret_access_key
import boto3

res = ""

def deletefile (username, filename, s3) :
    try:
        s3.delete_object(Bucket=username, Key="files/"+filename)
        res = (f"\nFile '{filename}' deleted successfully.")
    except Exception as e:
        res = (f"Error: {e}")
        
    print(res)
    return res
        
def deletefolder (username, foldername, s3):
    try:
        objects = s3.list_objects_v2(Bucket=username, Prefix="folders/"+foldername).get('Contents', [])

        for obj in objects:
            s3.delete_object(Bucket=username, Key=obj['Key'])

        res = (f"\nFolder '{foldername}' and its contents deleted successfully.")

    except Exception as e:
        res = (f"Error: {e}")
        
    print(res)
    return res
        
def deletepass (username, webname, s3) :
    try:
        s3.delete_object(Bucket=username, Key="passwords/"+webname)
        res = (f"\nCredentials for '{webname}' deleted successfully.")
    except Exception as e:
        res = (f"Error: {e}")
    print(res)
    return res
        
        
        
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