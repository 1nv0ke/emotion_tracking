# _________________________________________________________________________________________________

from datetime import datetime
import sys
import pickle

# _________________________________________________________________________________________________

def combine(left_file, right_file, id_in, out_pickle):
    with open(left_file, 'rb') as f:
        left_list = pickle.load(f)
    
    with open(right_file, 'rb') as f:
        right_list = pickle.load(f)

    total_number = len(left_list) + len(right_list)

    comb_list = []
    
    for x in left_list:
        if (x[1] > 0.0):
            comb_list.append(x)

    for x in right_list:
        if (x[1] > 0.0):
            comb_list.append(x)
    
    comb_list_sort = sorted(comb_list, key=lambda x: x[0])

    # handle duplicates
    output = []
    seen_date = []
    for x in comb_list_sort:
        if x[0] not in seen_date:
            output.append(x)
            seen_date.append(x[0])        
        else:
            temp = output[-1]
            output.remove(temp)
            temp = (temp[0], (x[1] + temp[1]) / 2.0)
            output.append(temp)

    output = [(x[0], id_in, x[1]) for x in output]
    result_number = len(output)

    with open(out_pickle, 'wb') as f:
       pickle.dump(output ,f)    
    
    return total_number, result_number

# _________________________________________________________________________________________________

if __name__ == '__main__':
    left_pickle = sys.argv[1]
    right_pickle = sys.argv[2]
    id_in = int(sys.argv[3])
    outname = sys.argv[4]
    
    total_num, res_num = combine(left_pickle, right_pickle, id_in, outname);

    print "Before: %d datapoints\nAfter: %d datapoints" % (total_num, res_num)

# _________________________________________________________________________________________________

