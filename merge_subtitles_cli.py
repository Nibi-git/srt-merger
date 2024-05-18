import sys  # input arguments
import getopt  # to raise error in case of incorrect arguments
from srtmergecommon import do_merge

def main(argv):
    # Parse arguments
    primary_path = ''
    secondary_path = ''
    try:
        opts, args = getopt.getopt(
            argv, "hp:s:", ["primary-path=", "secondary-path="])
    except getopt.GetoptError:
        print ('merge_subtitles.py -p <primary_path>'
               '-s <secondary_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print ('merge_subtitles.py -p <primary_path>'
                   ' -s <secondary_path>')
            sys.exit()
        elif opt in ("-p", "--primary-path"):
            primary_path = arg
        elif opt in ("-s", "--secondary-path"):
            secondary_path = arg

    # Write merged to file
    merged_path = primary_path.replace('.srt', '.merged.srt')

    do_merge(primary_path,
            '{\\an1}',
            '#FFFF00',
            secondary_path,
            '{\\an3}',
            '#FFFFFF',
            merged_path)

if __name__ == "__main__":
    main(sys.argv[1:])
