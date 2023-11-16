import time
import re
from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMainWindow
import paramiko
from front.main_windows import Ui_MainWindow
from back.work import Worker


class MainWindowBack(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.last = None
        self.setupUi(self)
        self.command = None
        self.setupUi(self)
        self.send_command_console.clicked.connect(self.execute_command)
        self.output_console.setReadOnly(True)
        self.threadpool = QThreadPool()
        self.ssh_client = paramiko.SSHClient()
        self.connect_to_server('10.2.173.136', 22, 'user1', '123')


    def execute_command(self):
        self.command = self.input_console.toPlainText().strip()
        if self.command:

            worker = Worker(self.send_command_terminal)
            worker.signals.result.connect(self.result_connect)
            self.threadpool.start(worker)

    def connect_to_server(self, host, port, username, password):
        try:
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=host, port=port, username=username, password=password,
                                    banner_timeout=200, look_for_keys=False, allow_agent=False)
            self.channel = self.ssh_client.get_transport().open_session()
            self.output_console.append(f"Connected to {host}")
            self.channel.get_pty()
            self.channel.invoke_shell()
            self.output_terminal_run()

        except Exception as e:
            self.output_console.append(f"Connection error: {str(e)}")


    def remove_ansi_escape_codes(self, text):
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)

    def output_terminal_command(self):
        while True:
            if self.channel.recv_ready():
                output = self.channel.recv(4096).decode('utf-8')
                output = self.remove_ansi_escape_codes(output)
                self.output_console.append(self.output_edit(output))
            else:
                break

    def output_terminal_run(self):
        output = self.channel.recv(4096*2).decode('utf-8')
        output = self.remove_ansi_escape_codes(output)
        self.output_console.append(output)

    def send_command_terminal(self):
        self.channel.send((self.command + '\n').encode('utf-8'))
        time.sleep(1)

    def result_connect(self):
        self.output_terminal_command()

    def output_edit(self, output):
        if not self.last:
            self.last = '\n'.join(output.split('\n')[-1:])
            return '\n'.join(output.split('\n')[:-1])
        else:
            return self.last + '\n'.join(output.split('\n')[:-1])


