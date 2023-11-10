import tkinter as tk
import time
import socket
import threading

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-topmost', True)
        self.server_ip = socket.gethostbyname(socket.gethostname())
        print(f"Серверный IP-адрес: {self.server_ip}")

        window_width = 150
        window_height = 80
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - window_width
        y = 0
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        #self.root.geometry("150x80")
        self.root.wm_attributes("-toolwindow", 1)
        self.root.wm_attributes("-disabled", 0)
        self.root.resizable(width=False, height=False)



        self.root.title("Таймер")

        self.timer_duration = 60  # Длительность по умолчанию в секундах
        self.time_left = 0
        self.is_running = False

        self.label = tk.Label(root, text="Таймер", font=("Helvetica", 24))
        self.label.pack(padx=20, pady=20)

        self.start_button = tk.Button(root, text="Старт", command=self.start_timer)
        self.stop_button = tk.Button(root, text="Стоп", command=self.stop_timer)

        self.start_button.pack()
        self.stop_button.pack()
        self.stop_button.config(state=tk.DISABLED)

        # Создаем серверный сокет для удаленного управления
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1", 12345))  # Привяжите сокет к конкретному адресу и порту
        self.server_socket.listen(5)  # Ожидаем соединений от клиентов

        self.client_socket = None
        self.running = True

        # Запускаем отдельный поток для обработки клиентских запросов
        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.start()

        # Устанавливаем обработчик события закрытия окна
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_timer_duration(self, duration):
        try:
            duration = int(duration)
            if duration > 0:
                self.timer_duration = duration
                print(f"Длительность таймера установлена на {self.timer_duration} секунд.")
            else:
                print("Недопустимая длительность таймера.")
        except ValueError:
            print("Недопустимое значение длительности таймера.")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.time_left = self.timer_duration
            self.update_timer()

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.is_running and self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.label.config(text=f"{minutes}:{seconds:02}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.is_running and self.time_left == 0:
            self.label.config(text="Время!")
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def accept_connections(self):
        try:
            while self.running:
                self.client_socket, client_address = self.server_socket.accept()
                print(f"Соединение от {client_address} установлено.")
                client_thread = threading.Thread(target=self.handle_client, args=(self.client_socket,))
                client_thread.start()
        except Exception as e:
            print(f"Ошибка при установлении соединения: {str(e)}")

    def handle_client(self, client_socket):
        try:
            while self.running:
                data = client_socket.recv(1024).decode()
                if data == "start":
                    self.start_timer()
                elif data == "stop":
                    self.stop_timer()
                elif data.startswith("set_timer"):
                    _, duration = data.split()
                    self.set_timer_duration(duration)
                else:
                    print(f"Неизвестная команда от клиента: {data}")
        except Exception as e:
            print(f"Ошибка при обработке команды от клиента: {str(e)}")
        finally:
            client_socket.close()

    def on_closing(self):
        self.running = False
        self.server_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
