import json
from Interface.interface import InterfaceCallback

interface = InterfaceCallback


class CallbackMQTT(InterfaceCallback):

    def __init__(self, mqttc):
        self.terminal = None
        self.data = None
        self.mqttc = mqttc

    def callback_data(self, topic, display):
        self.mqttc.message_callback_add(topic, lambda client, userdata, data: self.get_data(data, display))

    def get_data(self, data, display):
        parsed_data = json.loads(data.payload.decode("utf-8", "ignore"))
        data = round(float(list(parsed_data.values())[0]), 2)
        display.display(data*100+1)

    def validate_data(self, data):
        pass
