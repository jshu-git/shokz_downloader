a simple python program to download youtube playlists/songs asynchronously onto a Shokz device (i.e. the [Shokz OpenSwim](https://shokz.com/products/openswim))


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
  -s SHOKZ,     --shokz     SHOKZ     the path to a Shokz device mounted on the machine, i.e. /Volumes/OpenSwim

example usage: python main.py -n "Daniel Caesar - Freudian" -u https://www.youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf -s /Volumes/OpenSwim
```

#### some notes:
- include quotes if values have spaces
- the file names are prepended with an index (if it was a playlist download) to identify the order of the files
  - this is later used to copy the files in order, see [How to list the track order on OpenSwim](https://intl.help.shokz.com/s/article/How-to-list-the-track-order-on-OpenSwim-formerly-Xtrainerz-17) for why
  - this does not apply for single link downloads
- there is also a `just_copy.py` script
  - `python just_copy.py -f <folder> -s <shokz device>`
  - this is useful if (1) you already have .mp3 files **AND** (2) you want to copy them in a certain order to a Shokz device
    - you will need to prepend the file names with an index (i.e. `1 - song.mp3`, `2 - song.mp3`, etc.) in order for the files to be copied in order
    - if you don't care about the order, don't bother running this script and just drag and drop the files onto the device