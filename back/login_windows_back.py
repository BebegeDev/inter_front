import time
from datetime import datetime
from utils.create_file_and_path import Util
import paho.mqtt.client as mqtt


class UiAutoWindowBack:

    def __init__(self):

        self.connected_user = None
        self.list_connections_y = ["Авторизация успешна", "Успешное подключения к серверу MQTT"]
        self.list_connections_n = ["Авторизация неуспешна", "Ошибка подключения к серверу MQTT"]
        self.message = None
        self.auto_user = False

    @staticmethod
    def get_date():
        current_datetime = datetime.now()
        return current_datetime.strftime("%H:%M:%S")


    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected_user = True
            print("Подключение к MQTT СЕРВЕРУ прошло успешно")
            print("------------------------------------------------------------------")
            client.subscribe('#')
            self.message = f'{self.list_connections_y[0]} {self.get_date()}'
        else:
            print("Ошибка при подключении к MQTT СЕРВЕРУ")
            self.connected_user = False
            self.mqttc.disconnect()
            self.message = f'{self.list_connections_n[0]} {self.get_date()}'


    def connection(self, user, password, name='setting.ini'):
        if self.connected_user:
            print("Уже подключено, не требуется повторного подключения.")
            return True

        config = Util().config_pars(name)

        host = config["MQTT"]["MQTT_HOST"]
        port = int(config["MQTT"]["MQTT_PORT"])
        interval = int(config["MQTT"]["MQTT_KEEPALIVE_INTERVAL"])
        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(username=user, password=password)
        self.mqttc.on_connect = self.on_connect
        try:
            result = self.mqttc.connect(host, port, interval)
            if result == 0:  # 0 indicates success in connecting
                self.mqttc.loop_start()
            else:
                print(f"Ошибка при подключении к MQTT СЕРВЕРУ. Код возврата: {result}")
                self.message = f'{self.list_connections_n[1]} {self.get_date()}'
                return False
        except Exception as e:
            self.message = f'{self.list_connections_n[1]} {self.get_date()}'
            print(f"Произошла ошибка при подключении к MQTT СЕРВЕРУ: {e}")
            return False
        time.sleep(1)
        return self.connected_user


