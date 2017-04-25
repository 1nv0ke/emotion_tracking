
from timestamp import get_timestamp_from_irb_file
import pickle

IRB_FILE_PREFIX = ''
IRB_FILE_SUFFIX = '.irb'
IRB_FILE_NUM_START = 1
IRB_FILE_NUM_WIDTH = 4

IMAGE_FILE_SUFFIX = '.jpg'

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
            irb_file_name = IRB_FILE_PREFIX + str(irb_file_num).zfill(IRB_FILE_NUM_WIDTH) + IRB_FILE_SUFFIX
            timestamp = get_timestamp_from_irb_file(irb_file_name)
        except IOError:
            break
        img_file_name = img_file_prefix + str(img_file_num).zfill(img_file_num_width) + img_file_suffix
        parsed.append((timestamp, img_file_name))
        irb_file_num += 1
        img_file_num += 1
    
    print "%d timestamp(s) extracted." % (irb_file_num - IRB_FILE_NUM_START)

    if pickled_file != None:
        with open(pickled_file + '.pickle', 'wb') as handle:
            pickle.dump(parsed, handle, protocol = pickle.HIGHEST_PROTOCOL)
    
    return parsed

# ___
if __name__ == '__main__':
    print parse_irb_to_csv(irb_path= '',
                           img_file_prefix = 'seq_04212017_',
                           img_file_num_start = 240,
                           pickled_file = 'timestamps')
