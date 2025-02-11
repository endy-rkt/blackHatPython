#!/bin/python3
from pathlib import Path
import argparse

#create a parser by instanciating ArgumentParser
#you can leave at default
parser = argparse.ArgumentParser(
    prog='',
    usage=None,
    description=None,
    add_help=True
)

#add args and opt
parser.add_argument("path")

# parse the input arguments and get a Namespace object that contains all the user’s arguments
args = parser.parse_args()

print(f"{args}")

targetDir = Path(args.path)

if not targetDir.exists():
    print("The target dir doesn`t exist.")
    raise SystemExit(1)

for entry in targetDir.iterdir():
    print(entry.name)
