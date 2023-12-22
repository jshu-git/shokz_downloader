a simple python program to download youtube playlists/songs asynchronously onto a Shokz device (i.e. the [Shokz OpenSwim](https://shokz.com/products/openswim))


#### Setup
```
pip install -r requirements.txt
python main.py -d <downloads folder> -n <name> -u <url> -s <Shokz path>
```

#### Usage
```
usage: main.py [-h] [-d DOWNLOADS] -n NAME -u URL [-s SHOKZ]

description: this script downloads .mp3 files from a youtube playlist and copies them to a folder. if you provide a Shokz path, it will copy the files to the device (in order)

options:
  -h,           --help                show this help message and exit
  -d DOWNLOADS, --downloads DOWNLOADS the path to a downloads folder. defaults to ~/Downloads
  -n NAME,      --name      NAME      the desired name of the downloaded folder, i.e. "Daniel Caesar - Freudian"
  -u URL,       --url       URL       the url of a youtube playlist, i.e. https://youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf
  -s SHOKZ,     --shokz     SHOKZ     the path to a Shokz device mounted on the machine, i.e. /Volumes/OpenSwim

example usage: python main.py -n "Daniel Caesar - Freudian" -u https://www.youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf -s /Volumes/OpenSwim
```

#### some notes
- include quotes if values have spaces
- the file names are prepended with an index to identify the order of the files
  - this is later used to copy the files over in order, see [How to list the track order on OpenSwim](https://intl.help.shokz.com/s/article/How-to-list-the-track-order-on-OpenSwim-formerly-Xtrainerz-17) for why
- sometimes, the API used to download a youtube link fails
  - if this happens, the program will ask to input a different link to try
  - for example, https://www.youtube.com/watch?v=sQgLiBiv26U will not download for some reason, but https://www.youtube.com/watch?v=gb1SQ2vc-5o will
- special characters in file names are removed to avoid issues when saving