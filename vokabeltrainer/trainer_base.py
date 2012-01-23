#!/usr/bin/env python
#coding: utf-8
import cPickle, time, sys
from random import choice

class Trainer():
    def __init__(self):
        self.load()
        self.register = self.hard
        self.tools  = {'':'train()', '!':'help()', '+':'add()', '-':'delete()',\
                             ':':'show()', '1':'chooser(1)', '2':'chooser(2)',\
                            '3':'chooser(3)', '#':'history()', '...':'exit()'} 
        self.mode = 'self.train()'
        print 'welcome'.center(80, '-'), '\nfor help print "!"\n'

    def load(self):
        try:
            f = file('easywords.data')
            self.easy = cPickle.load(f)
        except IOError:
            self.easy = {}
        try:
            f = file('middlewords.data')
            self.middle = cPickle.load(f)
        except IOError:
            self.middle = {}
        try:
            f = file('hardwords.data')
            self.hard = cPickle.load(f)
        except IOError:
            self.hard = {}
        self.log = ''
        try:
            f = file('log.txt')
            for line in f:
                self.log += line
        except IOError:
            self.log  += 'history of your learning-process:\n'

    def save(self):
        f = file('easywords.data', 'w')
        cPickle.dump(self.easy, f)
        f.close()
        f = file('middlewords.data', 'w')
        cPickle.dump(self.middle, f)
        f.close()
        f = file('hardwords.data', 'w')
        cPickle.dump(self.hard, f)
        f.close()        
          
    def help(self):
        print 5*'_', '\nhelp:\nfor to go back to the learning-mode\n\
write nothing and press <enter>\n+ for adding a new word\n\
- for deleting a word\n: for showing words\n# for history\n\
"..." for closeing the trainer\n\
1 for easy, 2 for middle or 3 for hard\n'
        self.mode = 'self.train()'

    def run(self):
        while True:
            exec self.mode

    def exit(self):
        print 'good bye!'.center(80, '-')
        sys.exit()

    def train(self):
        try:
            german = choice(self.register.keys())
        except IndexError:
            print 'register is empty. please add some words.'
            self.mode = 'self.add()'
        else:
            print 'german:', german
            suggestion = raw_input('english: ')
            train_tools = self.tools.keys()[1:]
            if suggestion in train_tools:
                self.mode = 'self.%s' %  self.tools[suggestion]
            else:
                if suggestion == self.register[german]:
                    print 'good!\n'
                    self.move(german)
                else:
                    print 'right would be', self.register[german], '\n', 20*'_'

    def move(self, german):
        if self.register == self.easy:
            word = self.register.pop(german) 
            line = '\n',time.strftime("%d.%m.%Y um %H:%M:%S Uhr")\
                          , ' - ', german, ' : ', word
            for element in line:
                self.log += element
            f = open('log.txt', 'w')
            f.write(self.log)
            f.close
        elif self.register == self.hard:
            word = self.register.pop(german)     
            self.middle[german] = word
        elif self.register == self.middle:
            word = self.register.pop(german) 
            self.easy[german] = word
        self.save()

    def add(self):
        print 12*'_', '\nadd new words'
        german = raw_input('german: ')
        if german in self.tools.keys():
            self.mode = 'self.%s' %  self.tools[german]
        else:
            english = raw_input('english: ')
            if english in self.tools.keys():
                self.mode = 'self.%s' %  self.tools[english]
            else:
                self.hard[german] = english
                print 'done!'
                self.save()

    def delete(self):
        print 12*'_', '\ndelete words'
        german = raw_input('german: ')
        if german in self.tools.keys():
            self.mode = 'self.%s' %  self.tools[german]
        else:
            all = [self.hard, self.easy, self.middle]
            for x in all:
                if german in x:
                    del x[german]
                    self.save()
                    print 'done!'

    def show(self):
        if self.register == self.hard:
            print 11*'_', '\nhard words:'
        elif self.register == self.middle:
            print 13*'_', '\nmiddle words:'
        elif self.register == self.easy:
            print 11*'_', '\neasy words:'
        if len(self.register) > 0:        
            for ger, eng in self.register.iteritems():
                print '%s : %s' %(ger, eng)
        else:
            print 'empty register!'
        print
        self.mode = 'self.train()'

    def chooser(self, number):
        if number == 3:
            self.register = self.hard
            print 'register -> hard'
        elif number == 2:
            self.register = self.middle
            print 'register -> middle'            
        elif number == 1:
            self.register = self.easy
            print 'register -> easy'
        self.mode = 'self.train()'
    
    def history(self):
        print self.log, '\n'
        self.mode = 'self.train()'

if __name__ == '__main__':
    learn = Trainer()
    learn.run()
