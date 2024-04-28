# This is an encryption program inspired by the german Enigma encoding machine from WWII
# the program traces the inputted letters through 3 "rotor" lists, changing the output slightly each time
# via "offsets" (meant to mimic the turning of the Enigma machine's dials) this process can be reversed when the cipher
# is known to decrypt the message
# the cipher is used to set unique starting offsets to provide a unique encryption
# currently only supports the lowercase alphabet, numbers 1-10, and the special characters "." and "\n"

# --imports--

import random as r
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import pyperclip


# --functions--

def cipher(text):  # converts cipher into applicable rotor offsets
    global offsets
    offsets = []
    for i in range(3):
        offsets.append(int(text[1] + text[-1]) % rotor_len)
        text = text[1:-1]


def encode(text_in, code):  # takes text and cipher, returns encoded text
    cipher(code)  # called to apply rotor offsets
    text_out = ''
    for u, letter in enumerate(text_in):
        if letter == '_':
            letter = ' '
        if letter == '\n':  # switching newline to "_" for encoding
            letter = '_'
        temp_letter = letter.lower()
        for i, offset in enumerate(offsets):  # chaining through rotors to encode
            index = (rotors[0].index(temp_letter) + offset) % rotor_len
            temp_letter = rotors[i + 1][index]
        offsets[0] = (offsets[0] + 1) % rotor_len  # upping offsets to provide a unique per letter code
        if (u % 3) == 0:
            offsets[1] = (offsets[1] + 1) % rotor_len
        if (u % 9) == 0:
            offsets[2] = (offsets[2] + 1) % rotor_len
        text_out += temp_letter
    return text_out


def decode(text_in, code):  # takes encoded text and cipher, returns decoded text
    cipher(code)  # called to apply rotor offsets
    text_out = ''
    if text_in[-1] == '\n':  # removes trailing newlines
        text_in = text_in[:-1]
    for u, letter in enumerate(text_in):
        temp_letter = letter.lower()
        for i in [3, 2, 1]:  # chaining through rotors in reverse to decode
            index = (rotors[i].index(temp_letter) - offsets[i - 1])
            if index < 0:
                index = rotor_len + index
            temp_letter = rotors[0][index]
        offsets[0] = (offsets[0] + 1) % rotor_len  # mimicking encoding sequence
        if (u % 3) == 0:
            offsets[1] = (offsets[1] + 1) % rotor_len
        if (u % 9) == 0:
            offsets[2] = (offsets[2] + 1) % rotor_len
        if temp_letter == '_':  # switches "_" back to newline after decoding
            temp_letter = '\n'
        text_out += temp_letter
    return text_out


def GUI_encode():  # call from the GUI button "Encode"
    global filename
    if len(cipher_entry.get()) == 6:
        if file_loaded:  # file encoding
            file = open(filename, 'r')
            if (filename[-12:-4] == ' DECODED') or (filename[-12:-4] == ' ENCODED'):
                cutoff = -12
            else:
                cutoff = -4
            filename = filename[:cutoff] + ' ENCODED' + filename[-4:]
            file_text = file.read()
            file_out = open(f"{filename}", 'w')
            file_out.write(encode(file_text, cipher_entry.get()))
            text_exit.config(state='normal')
            text_exit.delete('1.0', 'end')
            text_exit.insert('1.0', f'Output written to:\n{filename}')
            text_exit.config(state='disabled')
        elif len(text_entry.get('1.0', 'end')) > 1:  # 8 = 6 cipher digits + newline char + one input char
            text_exit.config(state='normal')
            text_exit.delete('1.0', 'end')
            text_exit.insert('1.0', encode(text_entry.get('1.0', 'end-1c'), cipher_entry.get()))
            text_exit.config(state='disabled')
    else:
        messagebox.showerror('Error', 'Cipher Needed')


def GUI_decode():  # call from GUI button "Decode"
    global filename
    if len(cipher_entry.get()) == 6:
        if file_loaded:  # file decoding
            file = open(filename, 'r')
            file_text = file.read()
            if (filename[-12:-4] == ' DECODED') or (filename[-12:-4] == ' ENCODED'):
                cutoff = -12
            else:
                cutoff = -4
            filename = filename[:cutoff] + ' DECODED' + filename[-4:]
            file_out = open(f"{filename}", 'w')
            file_out.write(decode(file_text, cipher_entry.get()))
            text_exit.config(state='normal')
            text_exit.delete('1.0', 'end')
            text_exit.insert('1.0', f'Output written to:\n{filename}')
            text_exit.config(state='disabled')
        elif len(text_entry.get('1.0', 'end')) > 1:  # 8 = 6 cipher digits + newline char + one input char
            text_exit.config(state='normal')
            text_exit.delete('1.0', 'end')
            text_exit.insert('1.0', decode(text_entry.get('1.0', 'end-1c'), cipher_entry.get()))
            text_exit.config(state='disabled')
    else:
        messagebox.showerror('Error', 'Cipher Needed')


def rand_cipher():  # call from the GUI button "Random"
    cipher_entry.delete(0, 'end')
    cipher_entry.insert(1, str(r.randint(100000, 999999)))  # magic numbers represent range of 6-digit numbers


def clear():  # clears file variables and text entries (besides cipher)
    global filename, file_loaded
    text_entry.config(state='normal')
    text_entry.delete('1.0', 'end')
    text_exit.config(state='normal')
    text_exit.delete('1.0', 'end')
    text_exit.config(state='disabled')
    filename = ''
    file_loaded = False


def load_file():  # prompts file explorer, saves return to "filename"
    global file_loaded, filename
    clear()
    filename = fd.askopenfilename()
    if filename != '':
        text_entry.insert('1.0', f"File loaded:\n{filename}")
        text_entry.config(state='disabled')
        file_loaded = True


def clipboard():  # copies "cipher | output" to clipboard
    pyperclip.copy(text_exit.get("1.0", "end"))


# --definitions--
rotor = list('_ .abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-=+{}[]/?>,<;:`~')
rotor.append('"')
rotor.append("'")
rotors = [rotor, rotor, rotor, rotor]
rotor_len = len(rotors[0])
offsets = []
filename = ''
file_loaded = False

# --GUI--
# color definitions
background = '#1c1b18'
text_bg = '#302f2c'
code_button_bg = 'blue'
ui_button_bg = 'green'

# setting up GUI elements

window = tk.Tk()
window.title('Enigma')
window.config(bg=background)

frame1 = tk.Frame(width=1, bg=background)
frame2 = tk.Frame(width=1, bg=background)

label1 = tk.Label(text="6-digit cipher: ", fg='white', bg=background)
label2 = tk.Label(text="Input", fg='white', bg=background)
label3 = tk.Label(frame2, text='Output', fg='white', bg=background)

cipher_entry = tk.Entry(frame1, width=7, fg='white', bg=text_bg)
text_entry = tk.Text(width=26, height=4, fg='white', bg=text_bg)
text_exit = tk.Text(width=26, height=4, state='disabled', fg='white', bg=text_bg)

encode_button = tk.Button(text='Encode', bg='blue', fg='white', command=GUI_encode)
decode_button = tk.Button(text='Decode', bg='blue', fg='white', command=GUI_decode)
random_button = tk.Button(frame1, text='Random', fg='white', bg=ui_button_bg, command=rand_cipher)
clear_button = tk.Button(text='Clear', fg='white', bg=ui_button_bg, command=clear)
file_button = tk.Button(frame1, text='File', command=load_file)
copy_button = tk.Button(frame2, text='Copy', height=1, command=clipboard)

# packing GUI elements
label1.pack()
frame1.pack()
file_button.pack(side='left')
cipher_entry.pack(side='left', padx=20)
random_button.pack(side='right')
label2.pack()
text_entry.pack(padx=5)
frame2.pack()
copy_button.pack(side='right', padx=10, pady=5)
label3.pack(side='left')
text_exit.pack()
encode_button.pack(side='left', padx=15, pady=5)
decode_button.pack(side='right', padx=15, pady=5)
clear_button.pack(pady=5)
'''
error = False
while not error:
    phrase = ''
    for i in range(r.randint(1,12)):
        letter = rotor[r.randint(0, rotor_len-1)]
        while letter == '_':
            letter = rotor[r.randint(0, rotor_len - 1)]
        phrase += letter
    code = str(r.randint(100000, 999999))
    encoded = encode(phrase, code)
    if decode(encoded, code) == phrase:
        result = 'matches'
    else:
        result = '!!! does not match !!!'
        error = True
    print(f'{result}\nPhrase:{phrase}\nCode:{code}')
'''
window.mainloop()
