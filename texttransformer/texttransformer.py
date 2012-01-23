#!/usr/bin/env python
# coding: utf-8
import gtk
import random
import os

class TextEffects(object):
    def __init__(self, text):
        self.text = text

    def alphabet_soup(self):
        s = [os.linesep, [os.linesep], ' ', [' '], '.', ['.'], '(', ['('], \
             ')', [')'], ':', [':'], ';', [';'], '-', ['-']]
        i = []
        for c in self.text:
            i.append(c)
        n = 2
        i.insert(1, [i.pop(1)])        
        while n < (len(i)-1):
            if i[n] == '\xc3':
                i.insert(n, i.pop(n)+i.pop(n))
            if s.count(i[n+1]) > 0:
                i[n] = list(i[n])
                n += 1
            elif s.count(i[n]) > 0:
                i[n] = list(i[n])
                n += 1
            elif s.count(i[n-1]) > 0:
                i[n] = list(i[n])
                n +=1
            elif s.count(i[n-2]) > 0:
                i[n] = list(i[n])
                n +=1
            else:
                i[n-1].append(i.pop(n))
        
        i[0], i[-1] = list(i[0]), list(i[-1])
        j = []
        for c in i:
            random.shuffle(c)
            j.extend(c)
        newText = ''.join(j)    
        return newText

        
    def roller_caster(self):
        n = 0
        newText = ""
        for element in self.text:
            if n & 1 is 1:
                newText += self.text[n].upper()
                n += 1
            else:
                newText += self.text[n].lower()      
                n += 1
        return newText

class TextTransformer(object):
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("texttransformer.ui")
        self.builder.connect_signals(self)

    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
    
    def quit(self):
        gtk.main_quit()


    def on_window1_destroy(self, *args):
        self.quit()

    
    def on_alphabetsoup_clicked(self, *args):
        text = self.builder.get_object('entry1').get_text()
        text = TextEffects(text)
        self.builder.get_object('entry2').set_text(text.alphabet_soup())
    
    def on_rollercaster_clicked(self, *args):        
        text = self.builder.get_object('entry1').get_text()
        text = TextEffects(text)
        self.builder.get_object('entry2').set_text(text.roller_caster())

                     
if __name__ == '__main__':
    app = TextTransformer()
    app.run()
