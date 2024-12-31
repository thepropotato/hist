from accman import *
from upload import *
from download import *
import keyboard
from tabulate import tabulate
from delete import *
import sys


s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def main() :
    
    help = "ctrl+h"
    keyboard.add_hotkey(help, lambda : gethelp())
    
    
    print("\n")
    print(print_colored("       /HHHH/       /HHHH/   /IIII/   /SSSSSSSSSSSSS/   /TTTT/           ", "magenta"))
    print(print_colored("      /HHHH/       /HHHH/            /SSSSSSSSSSSSS/   /TTTT/            ", "magenta"))
    print(print_colored("     /HHHH/       /HHHH/   /IIII/   /SSSS/            /TTTTTTTTTTTTTT/   ", "magenta"))
    print(print_colored("    /HHHHHHHHHHHHHHHHH/   /IIII/   /SSSSSSSSSSSSS/   /TTTTTTTTTTTTTT/    ", "magenta"))
    print(print_colored("   /HHHHHHHHHHHHHHHHH/   /IIII/   /SSSSSSSSSSSSS/   /TTTT/               ", "magenta"))
    print(print_colored("  /HHHH/       /HHHH/   /IIII/            /SSSS/   /TTTT/    /TTTT/      ", "magenta"))
    print(print_colored(" /HHHH/       /HHHH/   /IIII/   /SSSSSSSSSSSSS/   /TTTTTTTTTTTTTT/       ", "magenta"))
    print(print_colored("/HHHH/       /HHHH/   /IIII/   /SSSSSSSSSSSSS/   /TTTTTTTTTTTTTT/        ", "magenta"))
    print("\n\n")
    print(print_colored("**************************  WELCOME TO HIST  **************************   ", "yellow"))
    print(print_colored("*********************  Hide Stuff, Trust me bro ! *********************   ", "yellow"))
    print("\n")
    print(print_colored("*********************   Press CTRL + H for help  **********************   ", "yellow"))
    print(print_colored("------------- ENTER THE INDEX TO EXECUTE AN OPERATION !!! -------------   ", "yellow"))
    print("\n\n")
    
    print("1. Sign In")
    print("2. Sign Up")
    
    user = ""
    while user == "" or user != "1" and user != "2":
        user = input("\nSign in / Sign Up : ")
        if user != "1" and user != "2" :
            print("Invalid request, Enter a valid index.")
        
    if user == "1":
        username, password, login = signin(s3)
    elif user == "2" :
        username, password, login = createuser(s3)
        
    print("Loading your data ...")
    getstuff(username, s3)
    
    upload_key = "ctrl+u"
    download_key = "ctrl+d"
    refresh = "ctrl+r"
    close = "ctrl+c"
    faq = "ctrl+f"
    remove = "ctrl+alt+r"
    deluser = "ctrl+alt+d"
    
    keyboard.add_hotkey(upload_key, lambda : upload(username, password, s3))
    keyboard.add_hotkey(download_key, lambda : download(username, password, s3))
    keyboard.add_hotkey(refresh, lambda : getstuff(username, s3))
    keyboard.add_hotkey(remove, lambda : delete(username, s3))
    keyboard.add_hotkey(deluser, lambda : deleteuser(username, s3))
    keyboard.add_hotkey(faq, lambda : askFAQ())

    keyboard.wait(close)

    
def gethelp():
    print(print_colored("\n-- HiSt : Keybindings and Actions --\n", "yellow"), "")
    l1 = ["Ctrl + U", "Ctrl + D", "Ctrl + Alt + R", "Ctrl + R", "Ctrl + H", "Ctrl + C", "Ctrl + Alt + D", "Ctrl + F"]
    l2 = ["Upload Data", "Download Data", "Remove Data", "Refresh Database", "HiSt Help", "Close HiSt", "Delete User", "See FAQ"]
    z = list(zip(l1, l2))
    header = ["KeyBindings", "Actions"]
    table = tabulate(z, headers=header, tablefmt="grid")
    print(print_colored(table, "yellow"), "")
    print("")


def askFAQ():
    print(print_colored("\n----------------------------------- HiSt : FAQ -------------------------------------\n", 'yellow'), "")

    # Question 1
    print(print_colored("1. Where is my data stored ?", 'red'))
    print("-->", print_colored("Your data is saved on the Amazon AWS servers", 'green'), "\n")

    # Question 2
    print(print_colored("2. Is my data safe with HiSt ?", 'red'))
    print("-->", print_colored("Your data is completely safe with HiSt, we save only encrypted files on the cloud.", 'green'), "\n")

    # Question 3
    print(print_colored("3. Why are the filenames changing when I upload them to HiSt ?", 'red'))
    print("-->", print_colored("That is due to the encryption of the files. Don't worry,\n    You will get back the original files when you download them.", 'green'), "\n")
    
    # Question 4
    print(print_colored("4. Can I retrieve the data that I have deleted ?", 'red'))
    print("-->", print_colored("Unfortunately, Data on HiSt once deleted cannot be retrieved", 'green'), "\n")
    
    # Question 5
    print(print_colored("5. What happens when I delete my account ?", 'red'))
    print("-->", print_colored("When you delete your account (Ctrl+Alt+D), all your files/folders/passwords\n    will be deleted at once, you can never sign in using the existing credentials again.", 'green'), "\n")
    
    
    print(print_colored("For support, mail us at --> histcustomercare@gmail.com\n", 'magenta'))
    

main()