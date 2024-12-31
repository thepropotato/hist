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

def createuser (s3) :
    print("")
    print("\nDo NOT use any UPPERCASE letters in the username !!! \n")
    print("Your password must follow the following rules :")
    print("  >>  Must be atleast 8 charecter long (>= 8),")
    print("  >>  Must be atmost 16 charecter long (<= 16),")
    print("  >>  Must consist atleast one UPPERCASE letter (A-Z),")
    print("  >>  Must consist atleast one NUMBER (0-9),")
    print("  >>  Must consist atleast one SPECIAL CHARECTER (@, #, $, %, ^, &, *),")
    username = input("\nUsername : ")
    upass    = maskpass("Password : ")
    
    while not passvalidity(upass) :
        upass = maskpass("Password : ")
    
    cpass = maskpass("Confirm your password : ")
    
    while cpass != upass :
        print("Wrong password entered !")
        cpass = maskpass("Confirm your password : ")
    
    password = cpass
    success = False
    
    while not success :
        success = createbucket(username, s3)
        if not success :
            print ("Username " + username + " not available. Please try again.")
            username = input("Username : ")
        
    try:
        
        print(print_colored("\nWrite a secret about you, in a sentence or two. This is for your password retrieval in case if you forget it !\nThis maybe your first school name, or pet name, or the name of your favourite music composer.\n", "magenta"))
        sec = input(print_colored("Secret : ", "yellow"))
        print("\nSecurity answer saved ! Write the exact same sentence when asked.\n")
        safesec = enc(sec, sec)
        
        safepword = enc(password, password)
        s3.put_object(Bucket=username, Key='files/', Body='')
        s3.put_object(Bucket=username, Key='folders/', Body='')
        s3.put_object(Bucket=username, Key='passwords/', Body='')
        s3.put_object(Bucket=username, Key='userdata', Body=safepword)
        s3.put_object(Bucket=username, Key='security', Body=safesec)
        login = True
        
    except Exception as e:
        print(f"Error in Signing you up : {e}")
        login = False
    
    return username, password, login

        
def signin (s3):
    login = False
    while not login :
        print("")
        username = input("Username : ")
        print(print_colored("Type @forgot if you forgot the password.", "yellow"))
        password = maskpass("Password : ")
        while password == "@forgot" :
            trust = forgotpassword(username, s3)
            if trust == True:
                newpass = maskpass("Enter new password : ")
                newcpass = maskpass("Re-Enter the new password : ")
                while newpass != newcpass :
                    print("Passwords didn't match !")
                    newcpass = maskpass("Re-Enter the new password : ")
                if newpass == newcpass :
                    password = newpass
                    safepword = enc(password, password)
                    s3.put_object(Bucket=username, Key='userdata', Body=safepword)
            else :
                print("Wrong security sentence entered. Try again !")
                password = "@forgot"
                
        password = key16(password)
        expass = readpass(username, password, s3)
        if expass == password :
            print(print_colored("Login Successful !", "magenta"))
            login = True
        else :
            print("Invalid credentials entered, Try again")
            
    return username, expass, login

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
        print(print_colored("\n--------------- RESTART HIST ! ---------------\n", "red"))

    else :
        print("\nAuthentication failed. Try again.")
        