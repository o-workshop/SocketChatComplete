from tkinter import *
import socket
import threading

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
BG_COLOR_INPUT = "#2C3E50"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:
    def __init__(self):
        self.host = 'chat.ousmane.me'
        self.port = 1234
        self.username = ''
        self.create_connection()

        # Top level widget
        self.window = Tk()
        self._setup_login_window()

    def run(self):
        self.window.mainloop()

    def create_connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect((self.host, self.port))
        except:
            print("couldn't connect to server")

    def handle_messages(self):
        while True:
            msg = self.client.recv(1204).decode()
            msg = f'{msg}\n\n'
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg)
            self.text_widget.configure(state=DISABLED)

            self.text_widget.see(END)

    def _setup_login_window(self):
        self.window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=200)

        self.pls = Label(self.login, text="Please enter your name to join the chat", justify=CENTER, font=FONT_BOLD)
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.name_label = Label(self.login, text="Name: ", font=FONT)
        self.name_label.place(relheight=0.2, relx=0.1, rely=0.2)

        self.name_input = Entry(self.login, font=FONT)
        self.name_input.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)

        self.name_input.focus()

        self.join_button = Button(self.login, text="Join Chat", font=FONT_BOLD,
                                  command=lambda: self.join_chat(self.name_input.get()))
        self.join_button.place(relx=0.4, rely=0.55)


    def _setup_main_window(self):
        self.window.deiconify()
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # text widget
        self.text_widget = Text(self.window, width=20, height = 2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message input(entry) box
        self.msg_entry = Entry(bottom_label, bg=BG_COLOR_INPUT, fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.11)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()

    def join_chat(self, name):
        print("Your name is: ", name)
        self.username = name
        self.client.send(self.username.encode())
        self.login.destroy()
        self._setup_main_window()

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        print("The text in there is: ", msg)
        self.client.send(msg.encode())
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


app = ChatApplication()
app.run()