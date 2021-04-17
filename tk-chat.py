from tkinter import *
import socket
import threading

# TkInter makes the widgets look native on every platform, very limited and old but will get the job done
# Included with standard Linux, Windows, and OSX installs of Python
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
BG_COLOR_INPUT = "#2C3E50"
TEXT_COLOR = "#EAECEE"  # Almost white

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatApplication:
    def __init__(self):
        self.host = 'chat.ousmane.me'
        self.port = 1234
        self.username = ''
        self.create_connection()

        # Top level widget of TK
        self.window = Tk()
        self._setup_login_window()

    def run(self):
        self.window.mainloop()

    def create_connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect((self.host, self.port))

        except:
            print("Couldn't connect to server")

    def handle_messages(self):
        while True:
            message = self.client.recv(1204).decode()
            self.text_widget.config(state=NORMAL)
            self.text_widget.insert(END, message + "\n\n")

            self.text_widget.config(state=DISABLED)
            self.text_widget.see(END)

    def _setup_login_window(self):
        self.window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        # Don't let the user resize the window
        self.login.resizable(width=False, height=False)
        # Set the width and height
        self.login.configure(width=400, height=200)
        # Create the login label
        # (We're adding it to the Login level so when the level is destroyed, everything in it is also destroyed
        self.pls = Label(self.login,
                         text="Please enter your name to join the chat",
                         justify=CENTER,
                         font=FONT_BOLD)

        # rel does it as a fraction of the parent widget, so this is 15% of the height of the parent
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)
        # create a Label
        self.name_label = Label(self.login, text="Name: ", font=FONT)
        # place the label
        self.name_label.place(relheight=0.2, relx=0.1, rely=0.2)

        # create a entry box for (Just a single line textbox)
        self.name_input = Entry(self.login, font=FONT)

        self.name_input.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)

        # set the focus of the cursor to the textbox (same as if we clicked on it in the first place)
        self.name_input.focus()

        # create a join button along with an action when it's clicked
        self.joinButton = Button(self.login, text="Join Chat", font=FONT_BOLD,
                                 command=lambda: self.join_chat(self.name_input.get()))

        self.joinButton.place(relx=0.4, rely=0.55)

    def _setup_main_window(self):
        self.window.deiconify()
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider (We're not going to need this again outside of this function
        # so we don't need to assign it to the class using self.
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        # Takes up majority of the window with almost 75%
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        # When you hover above it, it changes the cursor to arrow
        # We disable it because we only want to add text from the
        # program, not the user, and when we hover we see the arrow cursor
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg=BG_COLOR_INPUT, fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()

    def join_chat(self, name):
        print("Name: ", name)
        self.client.send(name.encode())
        self.login.destroy()
        self._setup_main_window()

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self.client.send(msg.encode())
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        # delete means where are we starting and where are we ending
        # we're deleting from 0 (first) to end so the whole thing
        self.msg_entry.delete(0, END)
        msg = f"{sender}: {msg}\n\n"
        # remember we have the text widget disabled so to send a message, we have to disable it
        # add our message
        # then disable it
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg)
        self.text_widget.configure(state=DISABLED)

        # set the cursor back to the ending so next time we input something it goes there
        self.text_widget.see(END)


if __name__ == "__main__":
    app = ChatApplication()
    app.run()
