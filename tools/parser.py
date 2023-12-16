from sys      import stderr, exit
from os       import path
from argparse import ArgumentParser

class Parser(ArgumentParser):
    def error(self, message):
        stderr.write('error: %s\n' % message)
        self.print_help()
        exit(2)

def parse():
    parser = Parser(epilog='example usage: python main.py -d ~/Desktop -n "Daniel Caesar - Freudian" -u https://www.youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf')

    parser.add_argument('-d', '--downloads', default  = path.expanduser('~/Downloads'), help = 'the path to your downloads folder. defaults to ~/Downloads')
    parser.add_argument('-n', '--name',      required = True,                           help = 'the desired name of the downloaded folder, i.e. Daniel Caesar - Freudian')
    parser.add_argument('-u', '--url',       required = True,                           help = 'the url of the playlist, i.e. https://youtube.com/playlist?list=PLDCdjwiC90THbJ4KUiy2bzku9hMAZG3vf')

    args = parser.parse_args()
    return args