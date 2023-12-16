a simple python program to download youtube playlists/songs asynchronously (i.e. for the [Shokz OpenSwim](https://shokz.com/products/openswim))

```shell
pip install -r requirements.txt
python main.py -n <name> -u <url>
```

```text
usage: main.py [-h] [-d DOWNLOADS] -n NAME -u URL

options:
  -h,           --help                show this help message and exit
  -d DOWNLOADS, --downloads DOWNLOADS the path to your downloads folder. defaults to ~/Downloads
  -n NAME,      --name NAME           the desired name of the downloaded folder, i.e. "Daniel Caesar - Freudian"
  -u URL,       --url URL             the url of a youtube playlist or link, i.e. https://youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf

example usage: python main.py -n "Daniel Caesar - Freudian" -u https://www.youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf
```
note: include quotes if values have spaces