import sys

import pyautogui
import socket
import base64
import json
import time
import os
import glob
from des import *
from PyQt5 import QtCore, QtGui, QtWidgets


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(list)

    def __init__(self, ip, port, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.active_socket = None
        self.ip = ip
        self.port = port
        self.command = 'screen'

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(0)

        def run():
            self.data_connection, address = self.server.accept()
            self.active_socket = self.data_connection

            while True:
                if self.command.split()[0] != 'screen':
                    self.send_json(self.command.split())
                    response = self.receive_json()
                    self.my_signal.emit([response])
                    self.command('screen')
                if self.command.split()[0] == 'screen':
                    self.send_json(self.command.split())
                    response = self.receive_json()
                    self.my_signal.emit([response])

    def send_json(self, data):
        try:
            json_data = json.dumps(data.decode('utf-8'))
        except:
            json_data = json.dumps(data.decode())

        try:
            self.active_socket.send(json_data.encode('utf-8'))
        except ConnectionResetError:
            self.active_socket = None

    def receive_json(self):
        json_data = ''
        while True:
            try:
                if self.active_socket != None:
                    json_data += self.active_socket.recv(1024).decode('utf-8')
                    return json.loads(json_data)
                else:
                    return None
            except ValueError:
                pass


class VNCServer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUI(self)

        self.ip = '127.0.0.1'
        self.port = 4444
        self.thread_handler = MyThread(self.ip, self.port)
        self.thread_handler.start()

        self.thread_handler.mysignal.connect(self.screen_handler)

    def screen_handler(self, screen_value):
        data = ['mouse_left_click', 'mouse_right_click', 'mouse_double_left_click']

        if screen_value[0] not in data:
            decrypt_image = base64.b64decode(screen_value[0])
            with open('2.png', 'wb') as file:
                file.write(decrypt_image)

            image = QtGui.QPixmap('2.png')
            self.ui.label.setPixelMap(image)

    def closeEvent(self, event):
        for file in glob.glob('*.png'):
            try:
                os.remove(file)
            except:
                pass


    def event(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            current_button = event.button()
            if current_button == 1:
                mouse_cord = f'mouse_left_click {event.x()} {event.y()}'
            if current_button == 2:
                mouse_cord = f'mouse_right_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            mouse_cord = f'mouse_double_left_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord
        return QtWidgets.QWidget.event(self, event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_app = VNCServer()
    my_app.show()
    sys.exit(app.exec_())