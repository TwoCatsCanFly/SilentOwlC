import concurrent.futures
import socket
import threading
import logging
import time
import datetime
import string
import random
from tkinter import *
from OwlProt import *
from tkinter.scrolledtext import ScrolledText

logging.basicConfig(filename='main.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

#  кодировка\декодировка сообщений
def enc(msg,type='ascii'):
    return msg.encode(type)
def dec(msg,type='ascii'):
    return msg.decode(type)

#адрес и порт ресивера
reciver_adress = 'localhost'
reciver_port = 9999
sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.settimeout(2.0)


global connection_status
connection_as_client_status = False
connection_as_server_status = False
client_handshake = False

def nickname():
    nickname = input('Choose nickname: ')

def info_msg(txt):
    chat_listbox.insert(END, chat_msg_formatter(txt, None, True))

def connection_as_client(sender):
    global connection_as_client_status
    if connection_as_client_status == False:
        try:
            logging.info(f'Connecting to: {reciver_adress}:{reciver_port}')
            info_msg(f'Попытка соединения с: [{reciver_adress}:{reciver_port}]')
            sender.connect((reciver_adress,reciver_port))
            logging.info('Connection successful')
            info_msg(f'Соединение успешно')
            connection_as_client_status = True
            client_hand(sender)
            return True
        except Exception as err:
            logging.info('Connection fail')
            logging.warning(err)
            print(f'Ошибка при попытке соединения: {err}')
            info_msg(f'Соединение не удалось...')
            connection_as_client_status = False
            return False
    else: info_msg('Соединение уже установлено')

def connection_as_client_func_handler():
    t = threading.Thread(target=connection_as_client, args=[sender])
    t.start()

def chat_msg_formatter(txt,nickname=None,info=False):
    try:
        current_time = datetime.datetime.now()
        msg_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        if info: return f'{msg_time}: {txt}'
        if nickname:
            frm = f'{msg_time} [{nickname}]: {txt}'
            logging.info('Message formatted with nickname')
            return frm
        else:
            rnd_nick = random.choices(string.ascii_uppercase)
            frm = f'{msg_time} [Мистер-{str(rnd_nick[0])}]: {txt}'
            logging.info('Message formatted anonymously')
            return frm

    except Exception as err:
        logging.warning(err)

def msg_receive(size):
    global connection_as_client_status
    if connection_as_client_status:
            try:
                message = sender.recv(size)
                logging.info('Message recived')
                return message
            except Exception as err:
                logging.warning(err)
                print('Error')
                sender.close()
                connection_as_client_status = False

def msg_write():
    while True:
        message = f'{nickname}: {input("")}'
        sender.send(enc(message))

receive_thread = threading.Thread(target=msg_receive)
write_thread = threading.Thread(target=msg_write)

def recive_write_threads_start():
    receive_thread.start()
    write_thread.start()

def write_to_chat():
    inp = input_box.get()
    chat_listbox.insert(END, chat_msg_formatter(inp))
    input_box.delete(0, 'end')

def delete():
    chat_listbox.delete(ANCHOR)

def write_msg():
    pass

def callback(event):
    write_to_chat()

root = Tk()
root.title('SOwlC Client')
root.geometry('500x800')

# Create menu
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label='Соединение',menu=file_menu)
menu_bar.add_command(label='Выход', command=root.quit)

frame_for_chat = LabelFrame(root)
frame_for_chat.pack(fill="x")
frame_for_controls = LabelFrame(root)
frame_for_controls.pack(fill="x")
frame_for_input = LabelFrame(root, text='Ввод')
frame_for_input.pack(fill="x")


global chat_listbox
chat_listbox = Listbox(frame_for_chat,height=40, width=82) # listbox
chat_listbox.pack()

delete_button = Button(frame_for_controls, text='Delete', command=delete)
delete_button.grid(row=0,column=0)

my_button2 = Button(frame_for_controls, text='Test CONNECTION', command=connection_as_client_func_handler)    #lambda: connection(sender))
my_button2.grid(row=0,column=1)

my_button2 = Button(frame_for_controls, text='Test Handshake', command=lambda: client_hand(sender))
my_button2.grid(row=0,column=2)

global input_box
input_box = Entry(frame_for_input,width=70,borderwidth='10')
input_box.grid(row=0,column=0,columnspan=18)
input_box.bind('<Return>',callback)
input_button = Button(frame_for_input, text='Enter',command=write_to_chat)
input_button.grid(row=0,column=20)

root.mainloop()
