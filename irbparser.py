
# _________________________________________________________________________________________________

from datetime import datetime
import sys
import pickle

# _________________________________________________________________________________________________

IRB_FILE_PREFIX = ''
IRB_FILE_SUFFIX = '.irb'
IRB_FILE_NUM_START = 1
IRB_FILE_NUM_WIDTH = 4

IMAGE_FILE_SUFFIX = '.jpg'

FILE_IRB_TIMESTAMP_OFFSET = 0x07F8
FILE_IRB_TIMESTAMP_LENGTH = 5

# Don't forget to change the date here!
CURRENT_YEAR = 2017
CURRENT_MONTH = 4
CURRNET_DAY = 28

# _________________________________________________________________________________________________

def parse_timestamp(timestamp):
    time_min = 0xC000000000
    time_max = 0xFFFFFFFFFF
    time_day = 24 * 3600 * 1000
    unit = 0.5 * (time_max - time_min) / time_day
    diff = timestamp - time_min + 1
    curr_ms = int(diff / unit)
    curr_hour = curr_ms / 1000 / 3600
    curr_ms -= curr_hour * 1000 * 3600
    curr_min = curr_ms / 1000 / 60
    curr_ms -= curr_min * 1000 * 60
    curr_sec = curr_ms / 1000
    curr_ms -= curr_sec * 1000
    curr_us = curr_ms * 1000
    
    # We got negative hour for some file, while numbers in other field are correct
    # So we added this line to fix it
    curr_hour = curr_hour % 24

    return datetime(CURRENT_YEAR, CURRENT_MONTH, CURRNET_DAY, curr_hour, curr_min, curr_sec, curr_us)

def get_timestamp_from_irb_file(filename):
    f = open(filename, 'rb')
    f.seek(FILE_IRB_TIMESTAMP_OFFSET, 0)
    timestamp = long()
    for i in range(FILE_IRB_TIMESTAMP_LENGTH):
        timestamp = long(ord(f.read(1)) << (8*i)) + timestamp
    f.close()
    return parse_timestamp(timestamp)

# _________________________________________________________________________________________________

def parse_irb_to_csv(irb_path = '',
                     img_file_prefix = '',
                     img_file_num_start = 1,
                     img_file_num_width = 4,
                     img_file_suffix = '.jpg',
                     pickled_file = None):

    irb_file_num = IRB_FILE_NUM_START
    img_file_num = img_file_num_start
    parsed = []

    while True:
        try:
            irb_file_name = irb_path + IRB_FILE_PREFIX + str(irb_file_num).zfill(IRB_FILE_NUM_WIDTH) + IRB_FILE_SUFFIX
            timestamp = get_timestamp_from_irb_file(irb_file_name)
        except IOError:
            break
        img_file_name = img_file_prefix + str(img_file_num).zfill(img_file_num_width) + img_file_suffix
        parsed.append((timestamp, img_file_name))
        irb_file_num += 1
        img_file_num += 1
    
    print "%d timestamp(s) extracted." % (irb_file_num - IRB_FILE_NUM_START)

    if pickled_file != None:
        with open(pickled_file, 'wb') as handle:
            pickle.dump(parsed, handle, protocol = pickle.HIGHEST_PROTOCOL)
    
    return parsed

# _________________________________________________________________________________________________

if __name__ == '__main__':
    print parse_irb_to_csv(irb_path = sys.argv[1],
                           img_file_prefix = sys.argv[2],
                           img_file_num_start = int(sys.argv[3]),
                           pickled_file = sys.argv[4])

# _________________________________________________________________________________________________
