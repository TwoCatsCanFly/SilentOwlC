import concurrent.futures
import socket
import threading
from tkinter import *

'''

SOwl v1
------!hi---------->
<-----!hi_ans-------
------!my_nick----->
<-----!my_nick------
|-----exchange-----|
------!disconnect-->
|-----disconnect---|

'''
#  кодировка\декодировка сообщений
def enc(msg,type='ascii'):
    return msg.encode(type)
def dec(msg,type='ascii'):
    return msg.decode(type)

# словарь протокола
sowl_v1 = {'!hi':39847325,
           '!hi_ans':29574274,
           '!my_nick':65733473,
           '!disconnect':40453295,}

#адрес и порт ресивера
reciver_adress = 'localhost'
reciver_port = 9999
sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def nickname():
    nickname = input('Choose nickname: ')

def connection():
    sender.connect((reciver_adress,reciver_port))

def msg_receive():
    while True:
        try:
            message = sender.recv(1024)
            message_dec = dec(message)
            if message_dec == 'NICK':
                sender.send(enc(nickname))
            else:
                print(message_dec)
        except:
            print('Error')
            sender.close()
            break

def msg_write():
    while True:
        message = f'{nickname}: {input("")}'
        sender.send(enc(message))


receive_thread = threading.Thread(target=msg_receive)
write_thread = threading.Thread(target=msg_write)

def recive_write_threads_start():
    receive_thread.start()
    write_thread.start()




root = Tk()
root.title('SOwlC Client')
root.geometry('500x800')

# Create menu
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label='Соединение',menu=file_menu)
menu_bar.add_command(label='Выход', command=root.quit)

frame_for_label = LabelFrame(root, text='Чат', padx=15, pady=15, width=20)
frame_for_label.pack(padx=10, pady=10 )

# Текст

# myLabel = Label(frame_for_label, text='Hello worldooooooooooooooooooooo').pack()
# myLabel2 = Label(frame_for_label, text='TKInter').pack()
# myLabel3 = Label(frame_for_label, text='hello mr. Freeman').pack()

chat_listbox = Listbox(frame_for_label) # listbox
chat_listbox.pack()

chat_listbox.insert(END,'TI PIDOR!') # add to listbox
chat_listbox.insert(END,'NYET, TI!!')

my_list = ['one','two','three']
for i in my_list: chat_listbox.insert(END,i)

def delete():
    chat_listbox.delete(ANCHOR)


my_button = Button(frame_for_label, text='Delete', command=delete)
my_button.pack()

root.mainloop()
