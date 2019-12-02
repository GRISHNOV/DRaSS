import argparse
import sys
import io
from passporteye import read_mrz


def recognize_data(data):
    mrz = read_mrz(data, extra_cmdline_params='--oem 0')
    recogn_data = mrz.to_dict()
    print(recogn_data)


def main():
    parser = argparse.ArgumentParser(description='Function for recognition of passport and cards')
    parser.add_argument('infile', type=argparse.FileType('rb'), help='input file with text for recognition')
    # parser.add_argument('-o', '--outfile', metavar='outfile', type=argparse.FileType('w'), default=open('a.out', 'w'), help='output file with recognition text')
    #parser.add_argument('-t', '--test', action='store_true', help='provide testing this function')
    # subparsers = parser.add_subparsers('-t', '--test', help='provide testing this function')

    args = parser.parse_args()

    print(args.infile)
    # print(args.outfile)

    recognize_data(args.infile)


if __name__=="__main__":
    main()
