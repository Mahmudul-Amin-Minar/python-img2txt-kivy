import pytesseract
import pyperclip
import sqlite3
import tkinter as tk

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import MWETokenizer

from functools import partial
import kivy.resources
from kivy.app import App
from kivy.core import clipboard
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.uix.button import Button 
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen 
try:
    from PIL import Image
except ImportError:
    import Image

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    

    def img(self, path, filename):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

        img = Image.open(str(filename[0]))
        self.text = pytesseract.image_to_string(img, lang='eng')
        self.copy()
        self.cancel()

    def copy(self):
        return pyperclip.copy(self.text)

    def show_result(self):
        layout = BoxLayout(orientation='horizontal')
        closeButton = Button(text = "Close", size_hint=(0.2,0.1))
        showButton = Button(text = "Words", size_hint=(0.2,0.1))
        showPhrase = Button(text = "Phrases", size_hint=(0.2,0.1))
        content = TextInput(text=self.text)

        layout.add_widget(closeButton)
        layout.add_widget(content)
        layout.add_widget(showButton)
        layout.add_widget(showPhrase)
        
        self._popup = Popup(title="Here is the text from image", content=layout, size_hint=(1, 1))
        self._popup.open()
        closeButton.bind(on_press =self._popup.dismiss)
        showButton.bind(on_release=lambda a:self.show_word_meaning())
        showPhrase.bind(on_release=lambda a:self.show_phrases_meaning())

    
    def show_word_meaning(self):

        ps = PorterStemmer()
        wl = WordNetLemmatizer()
        stop_words = set(stopwords.words("english"))

        example_para = self.text
        words = word_tokenize(example_para)

        filtered_pos = ['NN','VB','JJ','RB'] # word will included under this category
        # NN noun, singular ‘desk’
        # VB verb, base form take
        # JJ adjective ‘big’
        # RB adverb very, silently,

        a_word  = [] # wordList without filler word
        for w in words:
            if w not in stop_words:
                a_word.append(w)

        tags = nltk.pos_tag(a_word) # words with POS tags

        b_word = []
        for w in tags:
            if w[1] in filtered_pos:
                b_word.append(wl.lemmatize(w[0])) # stemed word made->make

        conn = sqlite3.connect("word.db")
        curr = conn.cursor()

        word_meaning = set()

        for w in b_word:

            word = w.lower().strip()
            try:
                curr.execute("SELECT en_word, bn_word FROM wordlist WHERE LOWER(en_word)=?", (word,))
            except:
                continue

            # fetch all the data from the database file
            rows = curr.fetchall()

            for r in rows:
                if len(r) > 0:
                    word_meaning.add(r)
        
        conn.close()

        root = tk.Tk()
        root.title('Word Meanings')
        root.geometry("800x500") #You want the size of the app to be 500x500
        root.resizable(0, 0)

        T = tk.Text(root, bg='#DEDEDE', fg='black', font=("Helvetica", 16)) 
        T.pack()

        for word in word_meaning:
            T.insert(tk.INSERT, f'{word[0]}:   {word[1]}\n') 
        
        root.mainloop()

    def show_phrases_meaning(self):
        phrases = []
        ph_token = MWETokenizer([
            ("yellow", "dog"), ("without", "fail"), 
            ("worthy", "of"), ("with", "a", "view", "to"), 
            ("well", "up"), ("well", "to", "do"), 
            ("well", "off"), ("victim", "of"), 
            ("under", "age"), ("upper", "hand"), 
            ("up", "to"), ("up", "to", "date"), 
            ("ups", "and", "downs"), ("to", "the", "back", "bone"), 
            ("to", "the", "point"), ("to", "the", "utmost"), 
            ("to", "the", "brim"), ("to", "go", "to", "the", "dogs"), 
            ("through", "and", "through"), ("silver", "tongue"), 
            ("subject", "to"), ("sine", "die"), 
            ("shoulder", "to", "shoulder"), ("short", "cut"), 
            ("stand", "by"), ("set", "fire", "to"), 
            ("see", "the", "light"), ("safe", "and", "sound"), 
            ("run", "a", "risk"), ("right", "and", "left"), 
            ("rise", "and", "fall"), ("take", "after"), 
            ("take", "heart"), ("step", "by", "step"), 
            ("summer", "friends"), ("strike", "work"), 
            ("so", "and", "so"), ("slow", "and", "steady"), 
            ("slow", "coach"), ("slip", "of", "tongue"), ("cats", "and", "dogs")])
        
        # Use tokenize method 
        contain_phrase = ph_token.tokenize(self.text.split())

        for phrase in contain_phrase:
            if '_' in phrase:
                ph = phrase.split('_')
                p = ' '.join(ph)
                phrases.append(p)

        phrases_meaning = set()

        conn = sqlite3.connect("phrases.db")
        curr = conn.cursor()

        for p in phrases:
            ph_mean = p.lower().strip()
            try:
                curr.execute("SELECT * FROM phrases WHERE LOWER(phrase)=?", (ph_mean,))
            except:
                continue
            # fetch all the data from the database file
            rows = curr.fetchall()

            for r in rows:
                if len(r) > 0:
                    phrases_meaning.add(r)
        
        conn.close()

        root = tk.Tk()
        root.title('Phrases Meanings')
        root.geometry("800x500") #You want the size of the app to be 500x500
        root.resizable(0, 0)

        T = tk.Text(root, bg='#DEDEDE', fg='black', font=("Helvetica", 16)) 
        T.pack()
        if len(phrases_meaning)>0:
            for phrase in phrases_meaning:
                T.insert(tk.INSERT, f'{phrase[0]}:  ({phrase[1]}):  {phrase[2]}\n\n')
        else:
            T.insert(tk.INSERT, "\nEither there is no phrase or we don't have that much data.\n")
        
        root.mainloop()


class Root(Screen):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def show_load_list(self):
        content = LoadDialog(load=self.load_list, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load a file list", content=content, size_hint=(1, 1))
        self._popup.open()

    def load_list(self, path, filename):
        pass

    def dismiss_popup(self):
        self._popup.dismiss()

    def save_w(self, word, bn, eng_syn, bn_syn, root):

        word = (word.get()).strip()
        bn = (bn.get()).strip()
        eng_syn = (eng_syn.get()).strip()
        bn_syn = (bn_syn.get()).strip()

        labelResult = tk.Label(root)
        
        if len(word) == 0:
            word = ''
        if len(bn) == 0:
            bn = ''
        if len(eng_syn) == 0:
            eng_syn = ''
        if len(bn_syn) == 0:
            bn_syn = ''

        conn = sqlite3.connect("word.db")
        curr = conn.cursor()

        # using ? mark placeholder to insert data
        if len(word) == 0 and len(bn) == 0 and len(eng_syn) == 0 and len(bn_syn) == 0:
            result = "Please fill at least Main word & Bangla meaning. :)"
            labelResult.config(text=f'{result}', fg='red')
        else:
            curr.execute("INSERT INTO wordlist VALUES (?, ?, ?, ?)", (word, bn, eng_syn, bn_syn))
            conn.commit()
            conn.close()

            result = 'Success..!!!'
            labelResult.config(text=f'{result}', fg='green')

        labelResult.grid(row=9, column=2)

    def add_new_word(self):
        large_font = ('Verdana',20)

        root = tk.Tk()

        root.geometry("500x400") #You want the size of the app to be 500x500
        root.resizable(0, 0)
        root.title('Add New Word')

        word = tk.StringVar()
        bn = tk.StringVar()
        eng_syn = tk.StringVar()
        bn_syn = tk.StringVar()

        labelword = tk.Label(root, text="Main Word").grid(row=1, column=0)
        labelbn = tk.Label(root, text="Bangla Meaning").grid(row=2, column=0)  
        labeleng_syn = tk.Label(root, text="English Synonym").grid(row=3, column=0)  
        labelbn_syn = tk.Label(root, text="Bangla Synonym").grid(row=4, column=0)  


        entryWord = tk.Entry(root, textvariable=word, font=large_font).grid(row=1, column=2, padx=10, pady=10)
        entryBn = tk.Entry(root, textvariable=bn, font=large_font).grid(row=2, column=2, padx=10, pady=10)
        entryEng_syn = tk.Entry(root, textvariable=eng_syn, font=large_font).grid(row=3, column=2, padx=10, pady=10)
        entryBn_syn = tk.Entry(root, textvariable=bn_syn, font=large_font).grid(row=4, column=2, padx=10, pady=10)

        save = partial(self.save_w, word, bn, eng_syn, bn_syn, root)
        buttonCal = tk.Button(root, text="Save", command=save, activebackground = "green", activeforeground = "white", font=large_font).grid(row=8, column=2, padx=10, pady=10)

        root.mainloop()


class SearchWindow(Screen):
    output = ObjectProperty(None)
    text_field = ObjectProperty(None)
      
    
    def find_word(self, w):
        word = w.text.lower().strip()
        conn = sqlite3.connect("word.db")
        conn2 = sqlite3.connect("phrases.db")
    
        curr = conn.cursor()
        curr2 = conn2.cursor()
        curr.execute("SELECT * FROM wordlist WHERE LOWER(en_word)=?", (word,))
        curr2.execute("SELECT * FROM phrases WHERE LOWER(phrase)=?", (word,))

        # fetch all the data from the database file
        rows = curr.fetchall()
        rows2 = curr2.fetchall()
        
        conn.close()
        conn2.close()

        self.text_field.text = ''
    
        root = tk.Tk()
        root.title('Find word')
        root.geometry("800x500") #You want the size of the app to be 500x500
        root.resizable(0, 0)

        main_word = f'Main Word:\n{word}\n\n'
        T = tk.Text(root, bg='#DEDEDE', fg='black', font=("Helvetica", 16)) 
        T.pack()

        if len(rows)>0:
            bn_meaning = 'Bangla Meaning:\n' + rows[0][1] + '\n\n\n'
            en_syns = 'English Synonyms:\n'+ rows[0][2] + '\n\n\n'
            bn_syns = 'Bangla Synonyms:\n' + rows[0][3] + '\n\n\n'
            T.insert(tk.INSERT, main_word) 
            T.insert(tk.END, bn_meaning)
            T.insert(tk.END, en_syns)
            T.insert(tk.END, bn_syns)

        elif len(rows2)>0:
            bn_meaning = 'Bangla Meaning:\n' + rows2[0][1] + '\n\n\n'
            en_sent = 'Example Sentence:\n'+ rows2[0][2] + '\n\n\n'
            T.insert(tk.INSERT, main_word)
            T.insert(tk.END, bn_meaning)
            T.insert(tk.END, en_sent)

        else:
            T.insert(tk.INSERT, main_word)
            T.insert(tk.END, "No definition found. We will add it soon.")

        root.mainloop()

class SearchResultWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("ocr.kv")
sm = WindowManager()
screens = [SearchWindow(name='search'), SearchResultWindow(name='search_result'), Root(name='main')]
for screen in screens:
    sm.add_widget(screen)

sm.current = 'main'

class LoadDialogApp(App):
        
    def build(self):
        return sm

if __name__ == '__main__':
    from kivy.core.window import Window
    Window.clearcolor = (.9, .8, .7, 1)
    LoadDialogApp().run()