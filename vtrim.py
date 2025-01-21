#!/usr/bin/env python3

import yaml
import argparse
import sys
import re
from datetime import datetime, timedelta
import os
import subprocess


# Colours.  :)
class ansi:
  BLUE      = '\033[94m'
  CYAN      = '\033[96m'
  GREEN     = '\033[92m'
  YELLOW    = '\033[93m'
  RED       = '\033[91m'
  END       = '\033[0m'
  BOLD      = '\033[1m'
  UNDERLINE = '\033[4m'

# Get input yaml file name from commandline.
parser = argparse.ArgumentParser( sys.argv[0] )
parser.add_argument( 'yaml_file', help='Specify a yaml file containing the cut list.' )
yaml_file = parser.parse_args().yaml_file

# Parse yaml.
with open( yaml_file, 'r' ) as stream:
  cuts = yaml.safe_load( stream )

# Loop through the input files and then the cuts for each input file.
for record in cuts:
  for cut in record['cuts']:

    # Set out input filename.
    infile = record['input']

    # Get the cut range and convert to a start and duration for ffmpeg.  When using ffmpeg
    # the end ts is referenced to the start timestamp of the output video.  The workaround
    # is to use copyts, but then we need an additional step to get sensible timestamps in
    # the output video.
    ( start, end ) = re.split( r'\s*-\s*', cut['range'] )
    sec = int( ( datetime.strptime( end, '%M:%S') - datetime.strptime( start, '%M:%S' ) ).total_seconds() )

    # Get the input filename and extension components and build output filename with cut details.
    ( base, ext ) = os.path.splitext( infile )
    outfile = f"{base}_{start}-{end}__{cut['output']}{ext}"

    cmd = [ 'ffmpeg', '-ss', start, '-i', infile, '-t', str( sec ), '-c', 'copy', outfile ]
    print( f"\n\n{ansi.GREEN}{ansi.BOLD}======={ansi.YELLOW}{ansi.BOLD}>{ansi.CYAN} {' '.join( cmd )}{ansi.END}" )
    subprocess.run( cmd )
