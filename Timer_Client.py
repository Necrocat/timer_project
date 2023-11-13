import tkinter as tk
import socket

class TimerClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Клиент Таймера")
        self.root.geometry("345x170")
        self.root.resizable(width=False, height=False)



        self.server_ip = tk.StringVar()
        self.server_port = tk.IntVar()
        self.timer_duration = tk.StringVar()
        self.timer_duration.set("1200")  # Значение таймера по умолчанию (1200 секунд = 20 минут)

        self.server_ip_label = tk.Label(root, text="IP-адрес сервера:")
        #self.server_ip_label.pack()
        self.server_ip_label.place(x=5, y=5)

        self.server_ip_entry = tk.Entry(root, textvariable=self.server_ip)
        self.server_ip_entry.place(x=110,y=8)
        #self.server_ip_entry.pack()

        self.server_port_label = tk.Label(root, text="Порт сервера:")
        self.server_port.set("12345")
        self.server_port_label.place(x=5,y=35)
        #self.server_port_label.pack()

        self.server_port_entry = tk.Entry(root, textvariable=self.server_port)
        self.server_port_entry.place(x=110,y=35)
        #self.server_port_entry.pack()

        self.set_timer_label = tk.Label(root, text="Set Timer (sec):")
        #self.set_timer_label.pack()
        self.set_timer_label.place(x=5,y=70)

        self.timer_duration_entry = tk.Entry(root, textvariable=self.timer_duration)
        self.timer_duration_entry.place(x=110,y=70)
        #self.timer_duration_entry.pack()

        self.set_timer_button = tk.Button(root, text="Set Timer", command=self.set_timer, width=12)
        self.set_timer_button.place(x=240,y=68)
        #self.set_timer_button.pack()

        self.connect_button = tk.Button(root, text="Подключиться", command=self.connect_to_server, height=3)
        self.connect_button.place(x=240,y=4)
        #self.connect_button.pack()

        self.start_button = tk.Button(root, text="Старт", command=self.start_timer, height=3, width=20)
        self.start_button.place(x=5,y=100)
        #self.start_button.pack()
        self.start_button.config(state=tk.DISABLED)

        self.stop_button = tk.Button(root, text="Стоп", command=self.stop_timer, height=3, width=20)
        self.stop_button.place(x=184,y=100)
        #self.stop_button.pack()
        self.stop_button.config(state=tk.DISABLED)



        self.client_socket = None

    def connect_to_server(self):
        try:
            server_ip = self.server_ip.get()
            server_port = self.server_port.get()
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, server_port))
            print("Соединение с сервером установлено.")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
        except Exception as e:
            print(f"Ошибка при подключении к серверу: {str(e)}")

    def start_timer(self):
        if self.client_socket:
            self.client_socket.send("start".encode())

    def stop_timer(self):
        if self.client_socket:
            self.client_socket.send("stop".encode())

    def set_timer(self):
        if self.client_socket:
            duration = self.timer_duration.get()
            if duration.isdigit() and int(duration) > 0:
                command = f"set_timer {duration}"
                self.client_socket.send(command.encode())
                print(f"Таймер установлен на {duration} секунд.")
            else:
                print("Недопустимое значение таймера.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerClientApp(root)
    root.mainloop()
