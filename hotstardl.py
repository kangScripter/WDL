import os
import subprocess

print("HOTSTAR DOWNLOADER")
print("by TEJ")

currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)



ytdlp = dirPath + '/binaries/yt-dlp.exe'
aria2c = dirPath + '/binaries/aria2c.exe'

link = input("ENTER HOTSTAR LINK: ")
subprocess.run([ytdlp, '-F', link])
   
  
res = input("ENTER RESOULUTION: ")
subprocess.run([ytdlp, '-f', res, link, '--remux-video', 'mkv', '--merge-output-format', 'mkv', '--no-warnings', '--audio-quality', '128', '--downloader-args', 'aria2c'])
