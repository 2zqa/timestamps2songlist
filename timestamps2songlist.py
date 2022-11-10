from datetime import datetime
from itertools import pairwise
import logging
import sys
import os

# === Functions ===
def calc_timestamp_diff(time_string1, time_string2):
    t1 = datetime.strptime(time_string1, "%M:%S")
    t2 = datetime.strptime(time_string2, "%M:%S")
    # print("diff:",str(t2-t1))
    return str(t2 - t1)[2:]

def get_song_info(line):
    timestamp, song = line.split(" ", 1)
    artist, song_name = song.strip().split(" - ", 1)
    return (timestamp, artist, song_name)

def format_line(index, line, next_timestamp):
    timestamp, artist, song_name = get_song_info(line)
    song_length = calc_timestamp_diff(timestamp, next_timestamp)

    logging.debug(f"DEBUG: {next_timestamp} - {timestamp} equals {song_length}")

    return f"{index}. {song_name} - {artist} ({song_length})"

# === Main ===
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_path = ""
duration_of_medium = ""
if len(sys.argv) == 3:
    duration_of_medium = sys.argv[1]
    if not ":" in duration_of_medium:
        print("Please enter a valid duration")
        exit(1)
    file_path = sys.argv[2]
    if not os.path.isfile(file_path):
        print(file_path, "does not exist")
        exit(1)
elif len(sys.argv) == 1:
    while True:
        duration_of_medium = input("Enter video duration: ")
        if not duration_of_medium:
            print("Please enter a duration")
        elif not ":" in duration_of_medium:
            print("Please enter a valid duration")
        else:
            break

    while True:
        file_path = input("Enter path: ")
        if not file_path:
            print("Please enter a file path")
        elif not os.path.isfile(file_path):
            print("file \"" + file_path + "\" does not exist")
        else:
            break
else:
    print("Usage: timestamps2songlist.py <total medium duration> [filepath]")
    exit(1)

lines_to_be_printed = []
with open(file_path) as lines:
    for index, (line, next_line) in enumerate(pairwise(lines), start=1):
        # Skip empty lines and lines starting with a number sign (#)
        if line.startswith("#") or not line.strip():
            continue
        next_timestamp = get_song_info(next_line)[0]
        lines_to_be_printed.append(format_line(index, line, next_timestamp))
    
    # Variable next_line is still preserved from the for-loop. Scope in python be tripping.
    index += 1
    lines_to_be_printed.append(format_line(index, next_line, duration_of_medium))

print("\n".join(lines_to_be_printed))