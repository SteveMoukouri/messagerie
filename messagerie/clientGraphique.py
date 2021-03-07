import tkinter as tk
from tkinter import ttk
from client import Client
from tkinter import scrolledtext


class clientGraphique(tk.Tk):
     
    def __init__(self, *args, **kwargs): 
         
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}  
        for F in (StartPage, Dialog):
  
            frame = F(container, self)
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    def pass_data_dialog(self, text):
        self.frames[self.pages[1]].get_text(text)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Messagerie config:").grid(row = 0, column = 0)
        tk.Label(self, text = "username:").grid(row = 1, column = 0)
        tk.Label(self, text = "server:").grid(row = 2, column = 0)
        tk.Label(self, text = "port:").grid(row = 3, column = 0)

        self.entryUsername = tk.Entry(self)
        self.entryUsername.grid(row = 1, column = 1)
        self.entryServer = tk.Entry(self)
        self.entryServer.grid(row = 2, column = 1)
        self.entryPort = tk.Entry(self)
        self.entryPort.grid(row = 3, column = 1)
        button = tk.Button(self, text="validate", command=self.validateConfig)
        button.grid(row = 4, column = 0, columnspan=2)
        
    def validateConfig(self):
        self.send_text({'username':self.entryUsername.get(),'server':self.entryServer.get(),'port':int(self.entryPort.get())})

    def send_text(self, text):
        self.controller.frames[Dialog].set_data(text)
        self.controller.show_frame(Dialog)

class Dialog(tk.Frame):
    def __init__(self, parent, controller):
        username = ""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.st = scrolledtext.ScrolledText(self, state='disabled')
        self.st.configure(font='TkFixedFont')
        self.st.grid(column=0, row=1, sticky='w', columnspan=4)
        self.st.insert(tk.END,"j'ecris")
        self.msg_entry = ttk.Entry(self)
        self.msg_entry.grid(column=3, row=2,sticky="NSEW")
        btn_column = ttk.Button(self, text="Send", command=lambda: self.send_msg({'msg': self.msg_entry.get()}))
        btn_column.grid(column=3)
    

    def set_data(self, data):
        self.client = Client(data['username'], data['server'], data['port'])
        self.username = data['username']
        self.client.listen()

    def send_msg(self, data):
        self.client.send(data['msg'])
        self.client.listen()
        self.client.handle_msg(data['msg']) 
        self.handle(data)

    def handle(self, data):
        self.st.configure(state='normal')
        self.st.insert(tk.END,self.username + " : " + data['msg'] + '\n')
        self.st.configure(state='disabled')



if __name__ == "__main__":
    app = clientGraphique()
    app.mainloop()