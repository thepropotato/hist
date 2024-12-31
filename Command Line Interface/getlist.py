import boto3
from secret import aws_access_key_id as aws_access_key_id
from secret import aws_secret_access_key as aws_secret_access_key
import uuid
import zlib
import hashlib
import base64
from tabulate import tabulate

def getstuff(username, s3):
    
    bucket_name = username
    
    prefixes = ["files/", "folders/", "passwords/"]
    
    data = {}

    for prefix in prefixes:
        response = s3.list_objects(Bucket=bucket_name, Prefix=prefix) or {}
        top_level_items = set()

        if 'Contents' in response:
            for obj in response['Contents']:
                name = obj['Key'].split('/')[1]
                if name != '':
                    top_level_items.add(name)
            
        data[prefix] = list(top_level_items)

    files = data['files/']
    folders = data['folders/']
    passwords = data['passwords/']
    
    printstuff(files, folders, passwords)
    
    return files, folders, passwords

def createbucket(username, s3) :
    
    bucket_name = username
    
    try:
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
        return True
        
    except Exception as e:
        print(f"Error creating bucket: {e}")
        return False
    
def printstuff(l1, l2, l3) :
    len1 = len(l1)
    len2 = len(l2)
    len3 = len(l3)

    ml = max(len1, len2, len3)

    [l1.append("") for i in range (0, ml-len1)]
    [l2.append("") for i in range (0, ml-len2)]
    [l3.append("") for i in range (0, ml-len3)]

    zipped_lists = list(zip(l1, l2, l3))
    header = ["Files", "Folders", "Passwords"]
    table = tabulate(zipped_lists, headers=header, tablefmt="grid")
    print("\nYour Stuff : ")
    print(table)
    print("")
