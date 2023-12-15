import json
import time
import re
from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMainWindow
import paramiko
from front.main_windows import Ui_MainWindow
from back.work import Worker
from back.callback_mqtt import CallbackMQTT
from PyQt6.QtGui import QColor


class MainWindowBack(QMainWindow, Ui_MainWindow):
    def __init__(self, mqttc):
        super().__init__()
        self.address_dgu = None
        self.command_dgu = None
        self.last = None
        self.setupUi(self)
        self.command_console = None
        self.setupUi(self)
        # self.change_color()
        self.send_command_console.clicked.connect(self.execute_command_console)
        self.pushCommandDGU.clicked.connect(self.execute_command_dgu)

        self.output_console.setReadOnly(True)
        self.threadpool = QThreadPool()
        self.ssh_client = paramiko.SSHClient()
        self.connect_to_server('10.2.173.183', 22, 'user1', '123')
        self.change_color()
        self.mqttc = CallbackMQTT(mqttc)
        self.run_method_mqtt_callback()

    def execute_command_console(self):
        self.command_console = self.input_console.toPlainText().strip()
        if self.command_console:
            worker = Worker(self.send_command_terminal)
            worker.signals.result.connect(self.result_connect)
            self.threadpool.start(worker)

    def execute_command_dgu(self):
        self.command_dgu = self.comboBox_type_command.currentText()
        self.address_dgu = self.lineEdit_adress.text()
        self.slave_dgu = self.lineEdit_slave.text()
        self.value_dgu = self.lineEdit_value.text()

        msg = json.dumps({"command": self.command_dgu,
                          "address_dgu": self.address_dgu,
                          "slave_dgu": self.slave_dgu,
                          "value_dgu": self.value_dgu})

        self.mqttc.publish_data("mpei/commands_operator/diesel", msg)

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
        output = self.channel.recv(4096 * 2).decode('utf-8')
        output = self.remove_ansi_escape_codes(output)
        self.output_console.append(output)

    def send_command_terminal(self):
        self.channel.send((self.command_console + '\n').encode('utf-8'))
        time.sleep(1)

    def result_connect(self):
        self.output_terminal_command()

    def output_edit(self, output):
        if not self.last:
            self.last = '\n'.join(output.split('\n')[-1:])
            return '\n'.join(output.split('\n')[:-1])
        else:
            return self.last + '\n'.join(output.split('\n')[:-1])

    def run_method_mqtt_callback(self):
        self.mqttc.callback_data("mpei/Emulator_('10.2.173.233', 8462)/Current", self.d_c_1)
        self.mqttc.callback_data("mpei/Emulator_('10.2.173.233', 8462)/Volt", self.d_u_1)
        self.mqttc.callback_data("mpei/Emulator_('10.2.173.233', 8462)/Power", self.d_p_1)

        self.mqttc.callback_data("mpei/Emulator_('10.2.173.234', 8462)/Current", self.d_c_2)
        self.mqttc.callback_data("mpei/Emulator_('10.2.173.234', 8462)/Volt", self.d_u_2)
        self.mqttc.callback_data("mpei/Emulator_('10.2.173.234', 8462)/Power", self.d_p_2)

        self.mqttc.callback_data("mpei/Victron/PV_battery_voltage", self.d_u_3)
        self.mqttc.callback_data("mpei/Victron/PV_power", self.d_p_3)
        self.mqttc.callback_data("mpei/Victron/Frequency_L1", self.d_f_a_3)
        self.mqttc.callback_data("mpei/Victron/Frequency_L2", self.d_f_b_3)
        self.mqttc.callback_data("mpei/Victron/Frequency_L3", self.d_f_c_3)
        self.mqttc.callback_data("mpei/Victron/PV_battery_current", self.d_c_3)

    def change_color(self):
        self.d_c_1.setStyleSheet("QLCDNumber { color: green; }")
        self.d_u_1.setStyleSheet("QLCDNumber { color: green; }")
        self.d_p_1.setStyleSheet("QLCDNumber { color: green; }")
        self.d_c_2.setStyleSheet("QLCDNumber { color: green; }")
        self.d_u_2.setStyleSheet("QLCDNumber { color: green; }")
        self.d_p_2.setStyleSheet("QLCDNumber { color: green; }")

        self.d_u_3.setStyleSheet("QLCDNumber { color: green; }")
        self.d_p_3.setStyleSheet("QLCDNumber { color: green; }")
        self.d_f_a_3.setStyleSheet("QLCDNumber { color: green; }")
        self.d_f_b_3.setStyleSheet("QLCDNumber { color: green; }")
        self.d_f_c_3.setStyleSheet("QLCDNumber { color: green; }")
        self.d_c_3.setStyleSheet("QLCDNumber { color: green; }")
