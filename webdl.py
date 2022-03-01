import os
import json
import subprocess
import argparse
import sys
import pyfiglet
from rich import print
from typing import DefaultDict

title = pyfiglet.figlet_format('WEBDL Script', font='slant')
print(f'[magenta]{title}[/magenta]')
print("by parnex")
print("Required files : yt-dlp.exe, mkvmerge.exe, mp4decrypt.exe, aria2c.exe\n")

arguments = argparse.ArgumentParser()
# arguments.add_argument("-m", "--video-link", dest="mpd", help="MPD url")
arguments.add_argument("-o", '--output', dest="output", help="Specify output file name with no extension", required=True)
arguments.add_argument("-id", dest="id", action='store_true', help="use if you want to manually enter video and audio id.")
arguments.add_argument("-s", dest="subtitle", help="enter subtitle url")
arguments.add_argument("-k", dest="key", help="Enter Keys")
arguments.add_argument("-d", dest="delenc", action='store_true', help="Delete encoded AND JSON FILE upon completion")
args = arguments.parse_args()

mpd_url = args.mpd
keys = args.key
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)

youtubedlexe = dirPath + '/binaries/yt-dlp.exe'
aria2cexe = dirPath + '/binaries/aria2c.exe'
mp4decryptexe = dirPath + '/binaries/mp4decrypt_new.exe'
mkvmergeexe = dirPath + '/binaries/mkvmerge.exe'
SubtitleEditexe = dirPath + '/binaries/SubtitleEdit.exe'

# mpdurl = str(args.mpd)
output = str(args.output)
subtitle = str(args.subtitle)

if args.id:
    print(f'Selected MPD : {mpd_url}\n')    
    subprocess.run([youtubedlexe, '-k','--referer','https://www.hotstar.com/in','--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', '--allow-unplayable-formats', '--no-check-certificate','--cookies-from-browser' ,'chrome','-F', mpd_url])

    vid_id = input("\nEnter Video ID : ")
    audio_id = input("Enter Audio ID : ")
    subprocess.run([youtubedlexe, '-k', '--allow-unplayable-formats','--referer','https://www.hotstar.com/in', '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', '--no-check-certificate', '-f', audio_id, '--fixup', 'never', mpd_url, '--audio-multistreams', '-o', 'encrypted.m4a', '--external-downloader', aria2cexe, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
    subprocess.run([youtubedlexe, '-k', '--allow-unplayable-formats','--referer','https://www.hotstar.com/in','--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36','--no-check-certificate', '-f', vid_id, '--fixup', 'never', mpd_url, '-o', 'encrypted.mp4', '--external-downloader', aria2cexe, '--external-downloader-args', '-x 16 -s 16 -k 1M'])   

else:
    print(f'Selected MPD : {mpd_url}\n')
    subprocess.run([youtubedlexe, '-k','--referer','https://www.hotstar.com/in','--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36, '--allow-unplayable-formats', '--no-check-certificate', '-f', 'ba', '--fixup', 'never', json_mpd_url, '-o', 'encrypted.m4a', '--external-downloader', aria2cexe, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
    subprocess.run([youtubedlexe, '-k','--referer','https://www.hotstar.com/in','--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36, '--allow-unplayable-formats', '--no-check-certificate', '-f', 'bv', '--fixup', 'never', json_mpd_url, '-o', 'encrypted.mp4', '--external-downloader', aria2cexe, '--external-downloader-args', '-x 16 -s 16 -k 1M'])    


print("\nDecrypting .....")
subprocess.run(f'{mp4decryptexe} --show-progress {keys} encrypted.m4a decrypted.m4a', shell=True)
subprocess.run(f'{mp4decryptexe} --show-progress {keys} encrypted.mp4 decrypted..mp4', shell=True)


if args.subtitle:
    subprocess.run(f'{aria2cexe} {subtitle}', shell=True)
    os.system('ren *.xml en.xml')
    subprocess.run(f'{SubtitleEditexe} /convert en.xml srt', shell=True) 
    print("Merging .....")
    subprocess.run([mkvmergeexe, '--ui-language' ,'en', '--output', output +'.mkv', '--language', '0:eng', '--default-track', '0:yes', '--compression', '0:none', 'decrypted.mp4', '--language', '0:eng', '--default-track', '0:yes', '--compression' ,'0:none', 'decrypted.m4a','--language', '0:eng','--track-order', '0:0,1:0,2:0,3:0,4:0', 'en.srt'])
    print("\nAll Done .....")
if args.delenc:
    delete_choice = 1
    if os.path.isfile(output + ".mkv"):
        os.remove(keyfile)
else:
    print("\nDo you want to delete the Encrypted Files : Press 1 for yes , 2 for no")
    delete_choice = int(input("Enter Response : "))

if delete_choice == 1:
    os.remove("encrypted.m4a")
    os.remove("encrypted.mp4")
    os.remove("decrypted.m4a")
    os.remove("decrypted.mp4")
    try:    
        os.remove("en.srt")
    except:
        pass
else:
    pass
