import tkinter
import tkinter.ttk

import logging
from socketsender import SocketSender

class ImageButton:
    """button1 = Button("Testo", "4ce", 0, 0)"""
    def __init__(self, root, text, command, row, column, image=""):
        
        image2 = tkinter.PhotoImage(file=image)
        image3 = image2.subsample(1, 1)
        self.button = tkinter.ttk.Button(
            root,
            text=text,
            image=image3,
            compound = tkinter.LEFT,
            command=command)

        self.button.grid(row=row, column=column, sticky=tkinter.NW, pady=0)
        self.button.image = image3



class ControlWindow(object):

    def __init__(self):
        self.window = tkinter.Tk()
        #f1 = tkinter.Frame(self.window, height=50, width=100)
        #f1.pack()
        


        self._infoLabel = tkinter.Label(text = 'NFCAudioServer Controller')
        self._volumeLabel = tkinter.Label(text = 'Vol')

        # Album entry space
        self._albumField = tkinter.Entry(self.window)
        
        
        self._infoLabel.grid(row=0)
        
        self._albumField.grid(row=3, column=0)


        self._playButton = ImageButton(   self.window, text='Play Album',
                                          command = self._buttonCallback__playAlbum,
                                          row=3, column=1
                                          )

        self._pauseButton = ImageButton(   self.window, text='Pause',
                                          command = self._buttonCallback__pause,
                                          row=1, column=1, image='images/play-50px.png'
                                          )
                                          
        self._backButton = ImageButton(   self.window, text='Back',
                                          command = self._buttonCallback__previous,
                                          row=1, column=0, image='images/rewind-50px.png'
                                          )
        self._forwardButton = ImageButton(   self.window, text='Fwd',
                                          command = self._buttonCallback__forward,
                                          row=1, column=2, image='images/fast-forward-50px.png'
                                          )


        self._volumeLabel.grid(row=0, column=3, padx=(20, 10))
                      
        self._volumeSlider = tkinter.Scale( self.window,
                                            command = self._scaleCallback__volume,
                                            to=0, from_=100, resolution=5)
        self._volumeSlider.set(75)
        self._volumeSlider.grid(row=1, rowspan=3, column=3)
        self._volumeUpdateJob = None

        self._socketSender = SocketSender()
        
        
    def _layout_widgets(self):
        self._infoLabel.grid(row=0)
        self._albumField.grid(row=0)
        
        self._backButton.grid(row=1, column=0)
        self._stopButton.grid(row=1, column=1)
        self._forwardButton.grid(row=1, column=2)
        
        self._albumField.grid(row=2, column=0)
        self._playButton.grid(row=2, column=1)
        
        
    def _buttonCallback__playAlbum(self):
        print('_buttonCallback__playAlbum called')
        albumName = self._albumField.get()
        self._socketSender.send_start_album(albumName)
        
        
    def _buttonCallback__pause(self):
        print('_buttonCallback__pause called')
        self._socketSender.send_pause()
        
    def _buttonCallback__previous(self):
        print('_buttonCallback__previous called')
        self._socketSender.send_previous()

    def _buttonCallback__forward(self):
        print('_buttonCallback__forward called')
        self._socketSender.send_forward()
    
    def _scaleCallback__volume(self, volumeValue):

        if not self._volumeUpdateJob:
            self._volumeUpdateJob = 1
            self.window.after(500, self._sendVolumeUpdate(volumeValue))
            return
        
        self.window.after_cancel(self._volumeUpdateJob)
        self._volumeUpdateJob += 1
        self.window.after(500, self._sendVolumeUpdate(volumeValue))
        
    def _sendVolumeUpdate(self, volumeValue):
        
        print('_sendVolumeUpdate called with {0}, job {1}'.
                format(volumeValue, self._volumeUpdateJob))
        
        self._volumeUpdateJob = None
        
        

if __name__ == '__main__':

    c = ControlWindow()
    c.window.mainloop()
