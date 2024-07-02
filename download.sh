if [ -z "$1" ]; then
	echo "specify album/playlist name"
	exit 1
fi
if [ -z "$2" ]; then
	echo "specify link"
	exit 1
fi
DEST=~/Desktop/"$1"
mkdir "$DEST"
cd "$DEST"
spotdl download $2
