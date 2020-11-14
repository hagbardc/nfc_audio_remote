import socket
import json
import copy

class SocketSender(object):
    def __init__(self, host = '192.168.1.253', port = 32413):
        self.host = host
        self.port = port

        self._templatePayload = { 'source': 'remote', 'event': None, 'data': {} }

    def _send_message(self, message):

        messageToSend = message
        if type(message) is dict:
            messageToSend = json.dumps(message)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(messageToSend.encode('utf-8'))

    def send_stop(self):
        dict_to_send = copy.copy(self._templatePayload)

        dict_to_send['event'] = 'stop'
        str_to_send = json.dumps(dict_to_send)
        self._send_message(str_to_send)

    def send_start_album(self, album, artist=None):
        dict_to_send = copy.copy(self._templatePayload)
        dict_to_send['source'] = 'plex'

        dict_to_send['event'] = 'start'
        albumDict = {'album': album}

        if artist:
            albumDict['artist'] = artist
            
        dict_to_send['data'] = albumDict
        self._send_message(dict_to_send)

    def send_forward(self):
        dict_to_send = copy.copy(self._templatePayload)
        dict_to_send['event'] = 'forward'
        self._send_message(dict_to_send)
        
    def send_pause(self):
        dict_to_send = copy.copy(self._templatePayload)
        dict_to_send['event'] = 'pause'
        self._send_message(dict_to_send)
        
    def send_previous(self):
        dict_to_send = copy.copy(self._templatePayload)
        dict_to_send['event'] = 'previous'
        self._send_message(dict_to_send)

    def send_volume_update(self, volume):
        dict_to_send = copy.copy(self._templatePayload)
        dict_to_send['event'] = 'setVolume'
        dict_to_send['data'] = {'volume': int(volume)}
        self._send_message(dict_to_send)
        
