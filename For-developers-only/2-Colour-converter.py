#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob, os, errno
from PIL import Image
import PIL.ImageOps

"""
Python converter for converting png, jpeg and bmp to usable .bmp files which
can be used by the E-Paper display. Currently, any image will be converted
to pure white and pure black pixels, without any shades of grey, just as the
displays expects them to be.

Tested and confired to work

Copyright by Ace-Laboratory
"""
#--------------only change the following two lines-----------------#
input_folder = '/home/pi/conversion/input/'
output_folder = '/home/pi/conversion/output/'
#-----------------no need to change anything below----------------#

os.chdir(input_folder)

""" Creating lists with filenames first"""

pngs = []
for files in glob.glob("*.png"):
    print('found this png: '+ os.path.splitext(os.path.basename(files))[0])
    pngs.append(os.path.splitext(os.path.basename(files))[0])

bmps = []
for files in glob.glob("*.bmp"):
    print('found this bmp: ' files)
    bmps.append(files)

jpegs= []
for files in glob.glob("*.jpeg"):
    print('found this jpeg: '+ os.path.splitext(os.path.basename(files))[0])
    jpegs.append(os.path.splitext(os.path.basename(files))[0])

print('converting the images now')


"""Some variables first. It's required for reducing colours"""
thresh = 126 # any value below 127 works.
fn = lambda x : 255 if x > thresh else 0

""" Conversion is done in two steps:
1) Converting the file from .png or .jpeg .bmp to a greyscale .bmp
2) Inverting the colours and rotating the image 90° anticlockwise
"""


""" Step 1 conversion for png files"""
if not os.path.exists(input_folder+'pngs/'):
    print('temporary png folder does not exist, creating now...')
    os.makedirs(input_folder+'pngs/')

print("attempting to convert pngs now...")
for files in pngs:
    png=Image.open(input_folder+files+".png")
    png.load()
    background = Image.new("RGB", png.size, (255, 255, 255)) #removing alpha channel
    background.paste(png, mask=png.split()[3]) #removing alpha channel
    background.convert('L').point(fn, mode='1').save((input_folder+'pngs/'+files+'.bmp'), 'BMP', quality=90)

""" Step 2 conversion for png files"""
png_bmp = []
os.chdir(input_folder+'pngs/')
for files in glob.glob("*.bmp"):
    png_bmp.append(files)
for files in png_bmp:
    (PIL.ImageOps.invert((Image.open(input_folder+'pngs/'+files).rotate(-90, expand=True)).convert('L'))).save(output_folder+files)
print("All png files have been converted.")


os.chdir(input_folder)

""" Step 1 conversion for jpeg files"""
if not os.path.exists(input_folder+'jpegs/'):
    print('temporary jpeg folder does not exist, creating now...')
    os.makedirs(input_folder+'jpegs/')

print("attempting to convert jpeg now...")

for files in jpegs:
    (Image.open(input_folder+files+".jpeg").convert('L').point(fn, mode='1').save((input_folder+'jpegs/'+files+".bmp"), 'BMP', quality=90))

""" Step 2 conversion for jpeg files"""

jpeg_bmp = []
os.chdir(input_folder+'jpegs/')
for files in glob.glob("*.bmp"):
    print('These :'+files)
    jpeg_bmp.append(files)
for files in jpeg_bmp:
    (PIL.ImageOps.invert((Image.open(input_folder+'jpegs/'+files).rotate(-90, expand=True)).convert('L'))).save(output_folder+files)


""" Step 1 & 2 conversion for bmp files"""
for files in bmps:
    PIL.ImageOps.invert(Image.open(input_folder+files+".bmp").convert('L').point(fn, mode='1')).rotate(-90, expand=True).save((output_folder+files), 'BMP', quality=90)

print('All done')
