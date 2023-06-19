"""
Inspired by http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
Changes:
    - Fixed AttributeError: 'AutocompleteEntry' object has no attribute 'listbox'
    - Fixed scrolling listbox
    - Case-insensitive search
    - Added focus to entry field
    - Custom listbox length, listbox width matches entry field width
    - Custom matches function
"""

from tkinter import *
import re

class AutocompleteEntry(Entry):
    def __init__(self, autocompleteList, *args, **kwargs):

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)
                
            self.matchesFunction = matches

        if 'selectionCallback' in kwargs:
            self._selectionCallback = kwargs['selectionCallback']
            del kwargs['selectionCallback']
        else:
            self._selectionCallback = None
        
        Entry.__init__(self, *args, **kwargs)
        self.focus()

        #self.autocompleteList = [ w["name"] for w in autocompleteList ]
        # Here, autocompleteList is a list of dict objects {album['artist'], album['album']}
        # we want to create a lookup table that allows us to get access to each element on a select operation

        aclist = []  # list for the autocomplete entry box
        self.albumList = {}  # new dict object, { 'artist - album':  {album['artist'], album['album']} }
        for album in autocompleteList:
            print('==> {0}'.format(album))
            lookupStr = '{0} - {1}'.format(album['artist'], album['album'])
            aclist.append(lookupStr)
            self.albumList[lookupStr] = album

        self.autocompleteList = aclist

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        
        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            wordsWithPayload = self.comparison()
            if wordsWithPayload:
                if not self.listboxUp:
                    self.listbox = Listbox(width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                
                self.listbox.delete(0, END)
                for w in wordsWithPayload:
                    self.listbox.insert(END,w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False
        print(self.listbox.curselection())

    def selection(self, event):
        chosenString = None
        if self.listboxUp:
            self.var.set(self.listbox.get(ACTIVE))
            print('==> {0}'.format(self.listbox.get(ACTIVE)))
            chosenString = '{0}'.format(self.listbox.get(ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)


        print('chosenString is {0}'.format(chosenString))
        if chosenString:
            self._selectionCallback(self.albumList[chosenString])

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
                
            if index != '0':                
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)
                
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
                print("movedown: {0}".format(self.listbox.curselection()))
                
            if index != END:                        
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)
                
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index) 

    def comparison(self):
        return [ w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w) ]

if __name__ == '__main__':
    import json
    f = open('data/albumlist.json', mode='r')
    album_json = f.read()
    f.close()
    albumlist = json.loads(album_json)
    aclist = []
    for album in albumlist:
        aclist.append('{0} - {1}'.format(album['artist'], album['album']))

    def matches(fieldValue, acListEntry):
        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
        return re.match(pattern, acListEntry)

    def matches_internal(fieldValue, acListEntry):
        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
        return re.search(pattern, acListEntry)
    
    root = Tk()
    entry = AutocompleteEntry(albumlist, root, listboxLength=20, width=32, matchesFunction=matches_internal)
    entry.grid(row=0, column=0)    
    Button(text='Python').grid(column=0)
    Button(text='Tkinter').grid(column=0)
    Button(text='Regular Expressions').grid(column=0)
    Button(text='Fixed bugs').grid(column=0)
    Button(text='New features').grid(column=0)
    Button(text='Check code comments').grid(column=0)
    root.mainloop()
