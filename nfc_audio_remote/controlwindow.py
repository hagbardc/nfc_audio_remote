import tkinter

import logging
from socketsender import SocketSender

class ControlWindow(object):

    def __init__(self):
        self.window = tkinter.Tk()
        f1 = tkinter.Frame(self.window, height=50, width=50)
        f1.pack()

        self.infoLabel = tkinter.Label(text = 'Audio Controller')
        self.infoLabel.pack()

        # Album entry space
        self._albumField = tkinter.Entry(self.window)
        self._albumField.pack()
        
        self._playButton = tkinter.Button(self.window, text='Play Album',
                                          command = self._buttonCallback__playAlbum)
        self._playButton.pack()
        
        
        self._stopButton = tkinter.Button(self.window, text='Stop',
                                          command = self._buttonCallback__stop)
        self._stopButton.pack()
        
        self._socketSender = SocketSender()
        
        
    def _buttonCallback__playAlbum(self):
        print('_buttonCallback__playAlbum called')
        albumName = self._albumField.get()
        self._socketSender.send_play(albumName)
        
        
    
    def _buttonCallback__stop(self):
        print('_buttonCallback__stop called')
        
        self._socketSender.send_stop()
        

if __name__ == '__main__':

    c = ControlWindow()
    c.window.mainloop()
