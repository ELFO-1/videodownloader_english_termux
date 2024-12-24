# videodownloader_english_termux
videodownloader for termux

to use myvideodownloader in termux you need python 3, the latest yt-dlp and ffmpeg

u need termux installed 
give storage access and need this things :

pkg update && pkg upgrade
pkg install python
pkg install ffmpeg
pip install yt-dlp

install new yt-dlp
python3 -m pip install -U yt-dlp

I have the python file and the cookies.txt 
in the folder downloads/videodownloader 
that is also the download directory 
where the videos are saved 
to copy them into the termux directory
execute or adapt the following commands

cd ~/storage/downloads/videodownloader

cp cookies.txt ~/.config/ytdownloader

cp myvideodownloader.py ~

when asked for cookies file 
enter the following path  :
 /data/data/com.termux/files/home/.config/ytdownloader/cookies.txt
