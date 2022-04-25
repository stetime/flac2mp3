import os
import argparse
import fnmatch
from subprocess import call
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--quality", help="quality (cbr, vbr)")
parser.add_argument("--input", help="input path to flacs")
parser.add_argument("--output", help="output path to mp3s")
args = parser.parse_args()

path = args.input if args.input else '.'
output = args.output if args.output else '.'

if args.quality == 'vbr':
    quality_prefix = '-q:a'
    quality = "0"
else:
    quality_prefix = '-b:a'
    quality = '320k'


def get_encoder_path():
    pathenv = os.getenv('PATH').split(':')
    for path in pathenv:
        if os.path.isfile(os.path.join(path, 'ffmpeg')):
            return os.path.join(path, 'ffmpeg')

# TODO: in absence of working ffmpeg install, use lame/flac instead.


def enumerate_files(flacpath):
    input_flacs = [os.path.join(path, file) for file in os.listdir(
        flacpath) if fnmatch.fnmatch(file, '*.flac')]
    return input_flacs


input = enumerate_files(path)

if input:
    for file in input:
        output_filename = f"{Path(file).stem}.mp3"
        print(os.path.join(output, output_filename))
        call([get_encoder_path(), '-i', file,
             quality_prefix, quality, output_filename])
