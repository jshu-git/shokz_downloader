from sys      import stderr, exit
from argparse import ArgumentParser

class Parser(ArgumentParser):
    def error(self, message):
        stderr.write('error: %s\n' % message)
        self.print_help()
        exit(2)

def parse():
    parser = Parser(description = 'description: this script downloads .mp3 file(s) from a youtube playlist/link and copies them to a folder. if you have a Shokz device, it will copy the files to the device (in order)',
                    epilog      = 'example usage: python main.py -n "Daniel Caesar - Freudian" -u https://www.youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf')

    parser.add_argument('-d', '--downloads', default  = '~/Downloads', help = 'the path to a downloads folder. defaults to ~/Downloads')
    parser.add_argument('-n', '--name',      required = True,          help = 'the desired name of the downloaded folder, i.e. "Daniel Caesar - Freudian"')
    parser.add_argument('-u', '--url',       required = True,          help = 'the url of a youtube playlist or link, i.e. https://youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf')
    parser.add_argument('-s', '--shokz',                               help = 'the path to the Shokz device mounted on the machine, i.e. /Volumes/OpenSwim')

    args = parser.parse_args()
    return args