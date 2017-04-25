
FILE_IRB_TIMESTAMP_OFFSET = 0x07F8
FILE_IRB_TIMESTAMP_LENGTH = 5

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
    return (curr_hour, curr_min, curr_sec, curr_ms)

def get_timestamp_from_irb_file(filename):
    f = open(filename, 'rb')
    f.seek(FILE_IRB_TIMESTAMP_OFFSET, 0)
    timestamp = long()
    for i in range(FILE_IRB_TIMESTAMP_LENGTH):
        timestamp = long(ord(f.read(1)) << (8*i)) + timestamp
    f.close()
    return parse_timestamp(timestamp)

if __name__ == '__main__':
    print get_timestamp_from_irb_file('00_00_00_001.irb')
    print get_timestamp_from_irb_file('00_00_00_002.irb')
    print get_timestamp_from_irb_file('18_58_11_104.irb')
