import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from accman import *
from HiSt import *
import GUI_PAGE_2 as page
import io
from images import bg_image as bg
import os
import sys

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Callback for login button
def on_login_click():
    username = username_login.get()
    password = password_login.get()
    
    out = signin(username, password, s3)
    
    login_log_text.delete(1.0, tk.END)

    login_log_text.insert(tk.END, f"{out[0]}\n\n")
    
    if out[0] == "Login Successful !" :
        root.destroy()
        page.page2(username, password)
        

# Callback for signup button
def on_signup_click():
    username = username_signup.get()
    password = password_signup.get()
    repass = confirm_password_signup.get()
    secret = secret_signup.get("1.0", tk.END).strip()
    
    signup_log_text.delete(1.0, tk.END)
    
    if password == repass :
        out = createuser(username, password, secret, s3)
        signup_log_text.insert(tk.END, f"{out[0]}\n\n")
    else :
        out = "Two passwords didn't match. Try again"
        signup_log_text.insert(tk.END, f"{out}\n\n")
        
    
    

# Callback for focusing on secret_signup entry
def on_secret_focus_in(event):
    # Clear default text when user clicks on the entry
    if secret_signup.get("1.0", tk.END).strip() == default_secret_text:
        secret_signup.delete("1.0", tk.END)
        secret_signup.config(fg='black')  # Change text color to black

# Callback for leaving secret_signup entry
def on_secret_focus_out(event):
    # Restore default text if the user leaves it empty
    if not secret_signup.get("1.0", tk.END).strip():
        secret_signup.delete("1.0", tk.END)
        secret_signup.insert(tk.END, default_secret_text)
        secret_signup.config(fg='grey')  # Change text color to grey

# Set the font style for the entire GUI
font_style = ("Arial", 12)  # Replace with your preferred font name and size

# Create the main window
root = tk.Tk()
root.title("Login/Signup")
root.attributes('-fullscreen', True)
root.option_add("*Font", font_style)  # Set font style

# Set the font size for tab headers
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 12))  # Set the desired font size


# Load background image without zooming
bg = Image.open(io.BytesIO(base64.b64decode(bg)))
#bg_image = Image.open(get_resource_path("C://Users//venup//Desktop//HiSt-UI//bg.jpg"))
bg = bg.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)  # Use Resampling.LANCZOS
bg = ImageTk.PhotoImage(bg)
bg_label = tk.Label(root, image=bg)
bg_label.place(relwidth=1, relheight=1)

# Create tabs
notebook = ttk.Notebook(root)

# Login Tab
login_tab = ttk.Frame(notebook)
notebook.add(login_tab, text="   Log In   ")  # Rename the tab here

# Labels for Login Tab
username_label_login = tk.Label(login_tab, text="Username :")
username_label_login.grid(row=0, column=0, pady=(100, 0), padx=150, sticky="N")

password_label_login = tk.Label(login_tab, text="Password :")
password_label_login.grid(row=1, column=0, pady=(40, 0), padx=150, sticky="S")

username_login = tk.Entry(login_tab)
username_login.grid(row=0, column=1, pady=(100, 0))

password_login = tk.Entry(login_tab, show="*")
password_login.grid(row=1, column=1, pady=(40, 0))

login_button = tk.Button(login_tab, text="Log In", command=on_login_click)
login_button.grid(row=2, column=1, pady=(60, 20))

def on_forgot_password_click():
    # Create a new window for password upload
    forgot_password_window = tk.Toplevel(root)
    forgot_password_window.title("Forgot Password")
        
    username_label = tk.Label(forgot_password_window, text="Username")
    username_label.grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(forgot_password_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)
        
    secret_label = tk.Label(forgot_password_window, text="Enter the Secret entered at :\nthe time of Registration")
    secret_label.grid(row=1, column=0, padx=10, pady=10)
    secret_entry = tk.Entry(forgot_password_window)
    secret_entry.grid(row=1, column=1, padx=10, pady=10)
        
    # Upload Button
    def on_forgot_password_button_click():
        # Get the values from the entries
        username = username_entry.get()
        secret = secret_entry.get()
        
        login_log_text.delete(1.0, tk.END)
        login_log_text.insert(tk.END, "Verification in progress.")
        # Call your upload function with the obtained values
        # #upload_function(app_name, username, password)
        out, un = forgotpassword_gui(username, secret, s3)
        
        if out == True :
            login_log_text.delete(1.0, tk.END)
            login_log_text.insert(tk.END, "Verification Succesful")
                
            forgot_password_window.destroy()
                
            def reset_password_gui(username, s3) :
                # Create a new window for password upload
                reset_password_window = tk.Toplevel(root)
                reset_password_window.title("Reset Password")

                # Application Name Entry
                pd_name_label = tk.Label(reset_password_window, text="Enter New Password :")
                pd_name_label.grid(row=0, column=0, padx=10, pady=10)
                pd_name_entry = tk.Entry(reset_password_window)
                pd_name_entry.grid(row=0, column=1, padx=10, pady=10)
                    
                cpd_name_label = tk.Label(reset_password_window, text="Re-Enter New Password :")                    
                cpd_name_label.grid(row=1, column=0, padx=10, pady=10)
                cpd_name_entry = tk.Entry(reset_password_window)
                cpd_name_entry.grid(row=1, column=1, padx=10, pady=10)
        
                # Upload Button
                def on_reset_password_button_click():
                    # Get the values from the entries
                    pd = pd_name_entry.get()
                    cpd = cpd_name_entry.get()
                        
                    login_log_text.delete(1.0, tk.END)
                        
                    if pd == cpd and passvalidity(pd) == True :
                        login_log_text.insert(tk.END, "Password valid, Updating Password...")
                        safepword = enc(pd, pd)
                        login_log_text.delete(1.0, tk.END)
                        s3.put_object(Bucket=username, Key='userdata', Body=safepword)
                        login_log_text.insert(tk.END, "Succesfully updated password. Login to continue.")
                        reset_password_window.destroy()
                    elif pd == cpd and passvalidity(pd) == False:
                        login_log_text.delete(1.0, tk.END)
                        login_log_text.insert(tk.END, "Password Invalid, Try again !")
                    else :
                        login_log_text.delete(1.0, tk.END)
                        login_log_text.insert(tk.END, "Passwords didn't match, Try again !")


                    # Close the upload password window
                        

                reset_button = tk.Button(reset_password_window, text="Reset Password", command=on_reset_password_button_click)
                reset_button.grid(row=3, column=0, columnspan=2, pady=10)
                
            reset_password_gui(un, s3)
                
        else :
            login_log_text.delete(1.0, tk.END)
            login_log_text.insert(tk.END, "Verification Failed, Try again !")
                
            
    verify_button = tk.Button(forgot_password_window, text="Proceed for Verification", command=on_forgot_password_button_click)
    verify_button.grid(row=3, column=0, columnspan=2, pady=10)
        

forgot_password_button = tk.Button(login_tab, text="Forgot Password", command= lambda: on_forgot_password_click())
forgot_password_button.grid(row=3, column=1, pady=10)

# Login Log Textbox

login_label = tk.Label(login_tab, text="Login Status")
login_label.grid(row=4, column=0, pady=(100, 120), padx=(150, 10), sticky="w")
login_log_text = tk.Text(login_tab, height=5, width=30, wrap=tk.WORD, fg="red")
login_log_text.grid(row=4, column=1, pady=(20, 40), padx=(10, 80), columnspan=2)

# Signup Tab
signup_tab = ttk.Frame(notebook)
notebook.add(signup_tab, text="   Sign Up   ")  # Rename the tab here

# Labels for Signup Tab
username_label_signup = tk.Label(signup_tab, text="Username:")
username_label_signup.grid(row=0, column=0, pady=(50, 10), padx=(100, 10), sticky="w")

password_label_signup = tk.Label(signup_tab, text="Password:")
password_label_signup.grid(row=1, column=0, pady=10, padx=(100, 10), sticky="w")

confirm_password_label_signup = tk.Label(signup_tab, text="Confirm Password:")
confirm_password_label_signup.grid(row=5, column=0, pady=10, padx=(100, 10), sticky="w")

secret_label_signup = tk.Label(signup_tab, text="Secret:")
secret_label_signup.grid(row=6, column=0, pady=10, padx=(100,0), sticky="w")

default_secret_text = "Enter a secret about you.\nThis will be used to reset your password when you forget it.\nForget this and\nTHAT IS THE END."
username_signup = tk.Entry(signup_tab, width=30)
username_signup.grid(row=0, column=1, pady=(50, 20))

password_signup = tk.Entry(signup_tab, width=30, show="*")
password_signup.grid(row=1, column=1, pady=20)

statement1_label = tk.Label(signup_tab, text="Password must contain >=8 and <=16 letters", fg="gray")
statement1_label.grid(row=2, column=1)

statement2_label = tk.Label(signup_tab, text="Atleast one from each of (0-9), (A-Z)", fg="gray")
statement2_label.grid(row=3, column=1)

statement3_label = tk.Label(signup_tab, text="Atleast one among @, #, $, %, ^, &, *", fg="gray")
statement3_label.grid(row=4, column=1)

confirm_password_signup = tk.Entry(signup_tab, width=30, show="*")
confirm_password_signup.grid(row=5, column=1, pady=20)

secret_signup = tk.Text(signup_tab, height=5, width=30, wrap=tk.WORD, fg='grey')  # Set default text color to grey
secret_signup.insert(tk.END, default_secret_text)
secret_signup.grid(row=6, column=1, pady=(20, 10), padx=(30,30))
secret_signup.bind("<FocusIn>", on_secret_focus_in)
secret_signup.bind("<FocusOut>", on_secret_focus_out)


signup_button = tk.Button(signup_tab, text="Sign Up", command=on_signup_click)
signup_button.grid(row=7, column=1, pady=(30, 170), padx=240)

# Signup Log Textbox

signup_label = tk.Label(signup_tab, text="Registration Status")
signup_label.grid(row=7, column=0, pady=(50, 10), padx=(100, 0), sticky="w")

signup_log_text = tk.Text(signup_tab, height=5, width=30, wrap=tk.WORD, fg="red")
signup_log_text.grid(row=7, column=1, pady=(50, 0), padx=(95, 95), columnspan=2)

# Place the whole 2-tab box at specified coordinates (adjust as needed)
notebook.place(x=660, y=80)

root.mainloop()
