from wand.image import image
with Image(filename='2018-01-02 13-27-44_1514911110606.JPG') as img:
    print ('width = ', img.width)
    print ('height = ', img.height)