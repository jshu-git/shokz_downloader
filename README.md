a simple program to download spotify albums onto a Shokz device (i.e. the [Shokz OpenSwim](https://shokz.com/products/openswim))

### Why?

The goal of this program is to simplify downloading albums and transmitting them sequentially to the device to preserve track order.

I usually listen to albums from start to finish. However, the Shokz OpenSwim device can't smartly detect track order. In short, the order is based on file transmission time. When simply dragging and dropping files onto the device, the order they "finish" is random, resulting in a different track order when playing them on the device. See [How to list the track order on OpenSwim](https://intl.help.shokz.com/s/article/How-to-list-the-track-order-on-OpenSwim-formerly-Xtrainerz-17) for more info.

Note: I'm aware of [this article](https://en.help.shokz.com/s/get-article?urlName=how-to-list-tracks-order-EN). However, after trying the steps in it, the track order is still (seemingly) random.

#### Setup

```
git clone https://github.com/jshu-git/shokz_downloader.git
cd shokz_downloader
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Usage

```
python main.py -n "name" -l "link" -d /Volumes/OpenSwim/

example: python main.py -n "Daniel Caesar - Freudian" -l "https://open.spotify.com/album/3xybjP7r2VsWzwvDQipdM0" -d /Volumes/OpenSwim
```

### Demo

https://github.com/jshu-git/shokz_downloader/assets/41213299/9f162609-9501-44dd-9476-86ab8a5d1e6f

Note: For demo purposes, I downloaded the album to my Desktop, but in practice it should be to the location of your device.

#### Notes

- Enclose values in quotes (if they have spaces)
- The file names are prepended with an index to identify the order of the files, which is used to copy them to the device in order
- Sometimes, a download will fail. Currently, there is no mechanism to retry, so you will have to delete the folder off of the device and retry

#### TODO

- [] add support for playlists
- [] smart retry when a download fails
