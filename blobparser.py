
# _________________________________________________________________________________________________

from datetime import datetime
import json
import sys

# _________________________________________________________________________________________________

TIME_STAMP_JS_WIDTH = 13
TIME_STAMP_JS_CONVERT = 1000.0

# _________________________________________________________________________________________________

def parse_human_blob(filename = None,
                     start_timestamp = 0,
                     end_timestamp = sys.maxsize):

    def split_timestamp_and_json(line):
        ptr = 0
        timestamp_str = ''
        while ptr < len(line) and not line[ptr] in '0123456789':
            ptr += 1
        while ptr < len(line) and line[ptr] in '0123456789':
            timestamp_str += line[ptr]
            ptr += 1
        while ptr < len(line) and line[ptr] != '{':
            ptr += 1
        #print line[ptr:]
        blob_json = None#json.loads(line[ptr:])
        return (timestamp_str, blob_json)

    def timestamp_string_to_datetime(timestamp_str):
        return datetime.fromtimestamp(int(timestamp_str) / TIME_STAMP_JS_CONVERT)

    try:
        full_blob_list = []
        with open(filename, 'r') as f:
            next(f)
            for line in f:
                timestamp_str, blob_json = split_timestamp_and_json(line)
                timestamp = None
                if len(timestamp_str) == 0:
                    pass
                elif len(timestamp_str) > TIME_STAMP_JS_WIDTH:
                    timestamp_old = timestamp_string_to_datetime(timestamp_str[:TIME_STAMP_JS_WIDTH])
                    full_blob_list[-1] = (timestamp_old, full_blob_list[-1][1])
                    timestamp = timestamp_string_to_datetime(timestamp_str[TIME_STAMP_JS_WIDTH:])
                    print timestamp_old
                    print timestamp
                    print line
                else:
                    timestamp = datetime.fromtimestamp(int(timestamp_str) / TIME_STAMP_JS_CONVERT)
                full_blob_list.append((timestamp, blob_json))
    except TypeError:
        print '[Error] parse_human_blob: no blob log file to read.'
        return None
    except IOError:
        print '[Error] parse_human_blob: failed to read blob log file.'
        return None

    return None

# _________________________________________________________________________________________________

if __name__ == '__main__':
    temp = parse_human_blob(filename = 'test.log')

# _________________________________________________________________________________________________
