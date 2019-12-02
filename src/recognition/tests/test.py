#!/usr/bin/python3

import argparse
import sys

parser = argparse.ArgumentParser(description='Function for encrypt data from file due AES')
parser.add_argument('infile', type=argparse.FileType('r'), help='input file with text for encryption')
parser.add_argument('key', type=str, help='key for encryption in AES')
parser.add_argument('-o', '--outfile', metavar='outfile', type=argparse.FileType('w'), default=open('a.out', 'w'), help='output file with crypto text')
#parser.add_argument('-t', '--test', action='store_true', help='provide testing this function')

# subparsers = parser.add_subparsers('-t', '--test', help='provide testing this function')

# parser_a = subparsers.add_parser('-t', help='a help')
# parser_a.add_argument('bar', type=int, help='bar help')

args = parser.parse_args()

print(args.infile)
print(args.outfile)