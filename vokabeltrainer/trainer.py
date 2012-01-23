#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk, cPickle
from random import choice
from trainer_base  import Trainer

class VokabelTrainer(object, Trainer):

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("trainer.ui")
        self.builder.connect_signals(self)
        self.load()
        self.builder.get_object('show').set_active(True)
        self.builder.get_object('show_all').set_active(True)
        
    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
    
    def quit(self):
        self.save()
        gtk.main_quit()
        

    def on_trainer_destroy(self, *args):
        self.quit()
          
    def word(self, *args):
        try:
            magic = choice(self.register.keys())
        except IndexError:
            magic = 'Kartei ist leer!'
        self.builder.get_object('suggestion').set_text('')
        self.builder.get_object('question').set_text(magic)
        
    def on_easy_clicked(self, *args):
        self.register = self.easy
        self.word()
        
    def on_middle_clicked(self, *args):
        self.register = self.middle
        self.word()
        
    def on_hard_clicked(self, *args):
        self.register = self.hard
        self.word()       
     
    def on_enter_clicked(self, *args):
        question = self.builder.get_object('question').get_text()
        sug = self.builder.get_object('suggestion').get_text()
        try:
            if sug == self.register[question]:
                answer = 'richtig!' 
                self.move(question)
            else:
                answer = 'richtig wäre "%s"' % self.register[question]
        except:
            answer = 'Sie ist wirklich leer!'
        self.builder.get_object('answer').set_text(answer)
        self.word()

    def on_edit_clicked(self, *args):
        self.builder.get_object('secound_window').show()
      
    def on_close_clicked(self, *args):
        self.builder.get_object('secound_window').hide()      
    
    def on_show_toggled(self, *args): 
        if self.builder.get_object('show').get_active():
            self.builder.get_object('zeigen').show_all()
        else:
            self.builder.get_object('zeigen').hide_all()
    
    def on_add_toggled(self, *args): 
        if self.builder.get_object('add').get_active():
            self.builder.get_object('hinzufuegen').show_all()
        else:
            self.builder.get_object('hinzufuegen').hide_all() 
    
    def on_delete_toggled(self, *args): 
        if self.builder.get_object('delete').get_active():
            self.builder.get_object('loeschen').show_all()
        else:
            self.builder.get_object('loeschen').hide_all()
    
    def text(self, register, *args):
        words = ''
        if register == 'show_all':
            all = self.easy
            all.update(self.middle)
            all.update(self.hard)
            for k,v in all.iteritems():
                words += '%s : %s\n' % (k, v)       
        elif register == 'show_easy':
            for k,v in self.easy.iteritems():
                words += '%s : %s\n' % (k, v)       
        elif register == 'show_middle':
            for k,v in self.middle.iteritems():
                words += '%s : %s\n' % (k, v)       
        elif register == 'show_hard':
            for k,v in self.hard.iteritems():
                words += '%s : %s\n' % (k, v)       
        else:
            words = self.log
        self.builder.get_object('textbuffer').set_text(words)
        
    def on_show_all_toggled(self, *args):
        if self.builder.get_object('show_all').get_active():
            self.text('show_all')
        
    def on_show_easy_toggled(self, *args):
        if self.builder.get_object('show_easy').get_active():
            self.text('show_easy')     
        
    def on_show_middle_toggled(self, *args):
        if self.builder.get_object('show_middle').get_active():
            self.text('show_middle')
            
    def on_show_hard_toggled(self, *args):
        if self.builder.get_object('show_hard').get_active():
            self.text('show_hard')    

    def on_history_toggled(self, *args):
        if self.builder.get_object('history').get_active():
            self.text('history')    
           
    def on_done_clicked(self, *args):
        de = self.builder.get_object('german').get_text()
        en = self.builder.get_object('english').get_text()
        self.hard[de] = en
        self.builder.get_object('german').set_text('')
        self.builder.get_object('english').set_text('')

    def on_del_clicked(self, *args):
        garbage = self.builder.get_object('trash').get_text()
        
        if garbage in self.easy: 
            del self.easy[garbage]
            self.builder.get_object('trash_result').set_text('löschen erfolgreich') 
        elif garbage in self.middle:
            del self.middle[garbage]
            self.builder.get_object('trash_result').set_text('löschen erfolgreich')
        elif garbage in self.hard:
            del self.hard[garbage]
            self.builder.get_object('trash_result').set_text('löschen erfolgreich')
        else:
            self.builder.get_object('trash_result').set_text('dieses Wort gab es nie')
        self.builder.get_object('trash').set_text('')
        
if __name__ == '__main__':
    app = VokabelTrainer()
    app.run()
