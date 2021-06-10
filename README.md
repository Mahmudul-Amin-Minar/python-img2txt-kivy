# Extracting Text from Image (OCR)
Image Processing is now a day’s considered to be a favorite topic in the IT industry. It is
a field under Digital Signal Processing. One of its major applications is Optical Character
Recognition (OCR). When the object to be matched is presented then our brains or in
general recognition system starts extracting the important features of the object that
includes color, depth, shape and size. These features are stored in the part of the memory.
Now the brain starts finding the closest match for these extracted features in the whole
collection of objects, which is already stored in it. This we can refer as standard library.
When it finds the match then it gives the matched object or signal from the standard
library as the final result. For humans character recognition seems to be simple task but
to make a computer analyze and finally correctly recognize a character is a difficult task.
OCR is one such technique that gives the power of vision to the computer to extract data
from images and find important data from it and make it computer editable.

# Extracting Text from Image (OCR)
Extracting Text from Image (OCR) using [PyTesseract](https://pypi.org/project/pytesseract/) and [Kivy Framework](https://kivy.org/#home).

## Home Window

This is the main window of the application. All functionality can be accessed from the
home.
There are 3 option:
1. Upload an image(for OCR).
2. Search Word/Phrase(for Bangla meanings).
3. Add New Word(for adding new words to database).

![Home Window](https://github.com/Mahmudul-Amin-Minar/python-img2txt-kivy/blob/master/images/1.PNG)

## Image File Insert

We can upload an image file for character recognition from that image. In figure 4.2 is
shown how to select our desired file.

![Image File Insert](https://github.com/Mahmudul-Amin-Minar/python-img2txt-kivy/blob/master/images/2.PNG)

## Extracted Text from Image

After selection an image we can see the text from that image file. This is done by our
tesseract OCR engine.

![Extracted Text from Image](https://github.com/Mahmudul-Amin-Minar/python-img2txt-kivy/blob/master/images/3.PNG)

## Bangla Word Meaning

We can also see the Bangla meanings of each word that has been recognized from the
image that is shown in the figure.

![Bangla Word Meaning](https://github.com/Mahmudul-Amin-Minar/python-img2txt-kivy/blob/master/images/4.PNG)

## Phrases Detection and Bangla Meaning

The system can also detects phrases and idioms from any given text input or image file
containing text. It also show those phrase and idioms with Bangla meaniongs.

![Phrases Detection and Bangla Meaning](https://github.com/Mahmudul-Amin-Minar/python-img2txt-kivy/blob/master/images/5.PNG)

## Word Search

Word input for searching is shown in the below picture.

![Word Search](https://github.com/Mahmudul-Amin-Minar/python-img2txt-kivy/blob/master/images/6.PNG)

## Word Information

The picture in the below shows the Bangla word meaning that was search as well as
English and Bangla synonyms.

![Word Information](https://github.com/Mahmudul-Amin-Minar/python-img2txt-kivy/blob/master/images/7.PNG)

## Adding New Word

We can also add new word in the database. This is Add new word window.

![Adding New Word](https://github.com/Mahmudul-Amin-Minar/python-img2txt-kivy/blob/master/images/8.PNG)
