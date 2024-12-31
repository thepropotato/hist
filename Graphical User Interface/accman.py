from upload import *
from passman import *
from getlist import *
from mask import *
from AES import *
import sys
import time

def print_colored(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
        'end': '\033[0m',
    }
    return colors[color] + text + colors['end']

def createuser (username, password, secret, s3) :

    print("\nDo NOT use any UPPERCASE letters in the username !!! \n")
    print("Your password must follow the following rules :")
    print("  >>  Must be atleast 8 charecter long (>= 8),")
    print("  >>  Must be atmost 16 charecter long (<= 16),")
    print("  >>  Must consist atleast one UPPERCASE letter (A-Z),")
    print("  >>  Must consist atleast one NUMBER (0-9),")
    print("  >>  Must consist atleast one SPECIAL CHARECTER (@, #, $, %, ^, &, *),")
    
    createbucket(username, s3)
    res = ""
        
    try:
        
        safesec = enc(secret, secret)
        safepword = enc(password, password)
        
        s3.put_object(Bucket=username, Key='files/', Body='')
        s3.put_object(Bucket=username, Key='folders/', Body='')
        s3.put_object(Bucket=username, Key='passwords/', Body='')
        s3.put_object(Bucket=username, Key='userdata', Body=safepword)
        s3.put_object(Bucket=username, Key='security', Body=safesec)
        
        login = True
        res = "Registration succesful. Login to continue."
        
    except Exception as e:
        res = f"Error in Signing you up : {e}"
        login = False
    
    return res, login

        
def signin (username, password, s3):
    login = False
    res = ""
    password = key16(password)
    expass = readpass(username, password, s3)
    if expass == password :
        login = True
        res = "Login Successful !"
    else :
        res = "Invalid credentials entered, Try again"
        login = False
            
    return res, login


def forgotpassword (username, s3) :
    trust = False
    try :
        given = input("\nEnter the secret that you have given at the time of Registration : ")
        response = s3.get_object(Bucket=username, Key='security')['Body'].read().decode('utf-8')
        decresponse = dec(response, given)
        if decresponse == key16(given) :
            trust = True
        
    except Exception as e:
        response = f"Unable to verify you : {e}"
        print(response)
        
    return trust

def deleteuser (username, s3) :
    pword = maskpass("\nEnter your password to delete your data (All the data will be erased) : ")
    orgpword = readpass(username, pword, s3)
    if orgpword == key16(pword) :
        objects = s3.list_objects_v2(Bucket=username).get('Contents', [])
        for obj in objects:
            s3.delete_object(Bucket=username, Key=obj['Key'])

        s3.delete_bucket(Bucket=username)
        print(f"\nUser '{username}' deleted successfully.")
        print(("\n--------------- RESTART HIST ! ---------------\n", "red"))

    else :
        print("\nAuthentication failed. Try again.")
        
        
def deleteuser_gui(username, s3, pword) :
    orgpword = readpass(username, pword, s3)
    if orgpword == key16(pword) :
        objects = s3.list_objects_v2(Bucket=username).get('Contents', [])
        for obj in objects:
            s3.delete_object(Bucket=username, Key=obj['Key'])

        s3.delete_bucket(Bucket=username)
        res = f"User '{username}' deleted successfully. Exiting HiSt in 5 seconds."
        print(print_colored("\n--------------- RESTART HIST ! ---------------\n", "red"))

    else :
        res = ("\nAuthentication failed. Try again.")
        
    return res
        
        
def forgotpassword_gui (username, given, s3) :
    trust = False
    try :
        response = s3.get_object(Bucket=username, Key='security')['Body'].read().decode('utf-8')
        decresponse = dec(response, given)
        if decresponse == key16(given) :
            trust = True
        
    except Exception as e:
        response = f"Unable to verify you : {e}"
        print(response)
        
    return trust, username
