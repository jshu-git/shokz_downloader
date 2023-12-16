
a simple python program to download youtube playlists/songs asynchronously onto a device (i.e. the [Shokz OpenSwim](https://shokz.com/products/openswim))


#### Getting Started
```
pip install -r requirements.txt
python main.py -d <downloads folder> -n <name> -u <url>
```

#### General Usage (`main.py`):
```
usage: main.py [-h] [-d DOWNLOADS] -n NAME -u URL [-s SHOKZ]

description: this script downloads .mp3 file(s) from a youtube playlist/link and copies them to a folder. if you have a Shokz device, it will copy the files to the device (in order)

options:
  -h,           --help                show this help message and exit
  -d DOWNLOADS, --downloads DOWNLOADS the path to a downloads folder. defaults to ~/Downloads
  -n NAME,      --name      NAME      the desired name of the downloaded folder, i.e. "Daniel Caesar - Freudian"
  -u URL,       --url       URL       the url of a youtube playlist or link, i.e. https://youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf
  -s SHOKZ,     --shokz     SHOKZ     the path to the Shokz device mounted on the machine, i.e. /Volumes/OpenSwim

example usage: python main.py -n "Daniel Caesar - Freudian" -u https://www.youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf -s /Volumes/OpenSwim
```

#### "just copy" (`just_copy.py`):
```
usage: just_copy.py [-h] -f FOLDER -s SHOKZ

description: this script copies .mp3 file(s) from a folder to a Shokz device

options:
  -h,        --help          show this help message and exit
  -f FOLDER, --folder FOLDER the path to a folder with .mp3 files to copy, i.e. ~/Desktop/Songs
  -s SHOKZ,  --shokz  SHOKZ  the path to the Shokz folder mounted on the machine, i.e. /Volumes/OpenSwim

example usage: python just_copy.py -f ~/Desktop/Songs -s /Volumes/OpenSwim
```

note: include quotes if values have spaces