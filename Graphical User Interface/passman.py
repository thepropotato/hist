# AES based password manager from scratch
# @author - venupulagam

import boto3
from botocore.exceptions import NoCredentialsError
from AES import *

def passvalidity (password) :
    out = False
    if len(password) < 8 :
        print("Invalid password ! Password must consist of atleast 8 charectors")
    elif len(password) >= 8 and len(password) <= 16 :
        if contains_digit(password) :
            if contains_uppercase(password) :
                if contains_special(password) :
                    out = True
                    print("Password valid")
                else :
                    print("Invalid password ! Password must consist of atleast one special charector")
            else :
                print("Invalid password ! Password must consist of atleast one uppercase letter")
        else :
            print("Invalid password ! Password must consist of atleast one digit")
    return out
        
        
def contains_uppercase(word):
    if any(char.isupper() for char in word) :
        return True
    else :
        return False
    
def contains_digit(word) :
    if any(char.isdigit() for char in word) :
        return True
    else :
        return False
    
def contains_special (word) :
    special = ['@', '#', '$', '%', '^', '&', '*']
    if any(char in word for char in special) :
        return True
    else :
        return False
    
def readpass (username, pword, s3) :
    
    try :
        response = s3.get_object(Bucket=username, Key='userdata')['Body'].read().decode('utf-8')
        response = dec(response, pword)
        
    except Exception as e:
        response = f"Unable to verify you : {e}"
        
    return response