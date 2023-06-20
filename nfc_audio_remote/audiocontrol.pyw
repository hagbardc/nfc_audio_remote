from controlwindow import ControlWindow


# TODO: You can get rid of this global by registering the autocomplete selection event AFTER the creation of 
# the autocomplete object.  That way we can create the ControlWindow, and then do the registering of the 
# selection event via the handle to that ControlWindow (e.g. c._autocomplete.selection = _selectionCallback)
# sort of thing. 
global c
c = None
def _selectionCallback(itemSelected):
    """ Method for registering with the autocomplete widget.
    
    Args:
        itemSelected (dict): Dict of {'artist': str, 'album': str } representing the album selected
    """
    print('Selection callback: {0}'.format(itemSelected))
    c.playAlbum(albumName=itemSelected['album'], artistName=itemSelected['artist'])


c = ControlWindow(_selectionCallback)
c.window.mainloop()
