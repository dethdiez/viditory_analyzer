from subprocess import call
import hashlib

f = open("example1.json", "w")
call (["ffprobe","-i","example1.mp4","-print_format","json","-show_streams","-show_format","-show_data","-hide_banner"], stdout=f)
 
hasher = hashlib.md5()
with open('example1.mp4', 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
print(hasher.hexdigest())
