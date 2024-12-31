import msvcrt
import time

def maskpass(prompt):
    input_string = ""
    print(prompt, end='', flush=True)

    while True:
        char = msvcrt.getch().decode('utf-8')

        if char == '\r' or char == '\n':
            break
        elif char == '\b':  # Backspace
            if input_string:
                input_string = input_string[:-1]
                print('\b \b', end='', flush=True)  # Clear the character
        else:
            print(char, end='', flush=True)
            time.sleep(0.2)
            print('\b*', end='', flush=True)
            input_string += char
            
    print("")
            
    return input_string
