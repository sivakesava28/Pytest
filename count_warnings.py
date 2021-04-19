import os
import sys

def get_warning_count(lines):
    wcount = 0
    for line in lines:
        if (line.find("warning") >= 0):
            wcount += 1;
        #line = line.lstrip().rstrip()
        #print line.split(":")[4].lstrip()
        

    return wcount

def get_warn_count_by_file(log_file):
    try:
        fd = open(log_file, "r")
    except IOError:
        print("Error: Open failed", log_file)
        return 0

    lines = fd.readlines()
    fd.close()
    #print(lines)
    wcount = get_warning_count(lines)

    return wcount

def is_build_promoted(warn_count_by_file):

    old_warn_count = warn_count_by_file[0][1]
    cur_warn_count = warn_count_by_file[1][1]

    if (old_warn_count != 0 and cur_warn_count != 0 and cur_warn_count > old_warn_count):
        print("""*** New warnings are introduced in current build, can't be promoted  """)
        print("""*** Old     Warning count %s:%d """ % (warn_count_by_file[0][0], old_warn_count))
        print("""*** Current Warning count %s:%d """ % (warn_count_by_file[1][0], cur_warn_count))
        return -1
    else:
        print(""" build promoted """)
        print("""*** Old     Warning count %s:%d """ % (warn_count_by_file[0][0], old_warn_count))
        print("""*** Current Warning count %s:%d """ % (warn_count_by_file[1][0], cur_warn_count))
        return 0
    
def is_valid_aruguments(argv):
    if(len(argv) < 3) or (len(argv)>=4):
        print("Error: Invalid/Insufficient arguments")
        print("Usage: count_warnings.py <current log file> <old log file>")
        print("")
        return False
    return True

def main(argv):
    warn_count_by_file = []

    if (is_valid_aruguments(argv) == False):
        exit(1)

    for count, args in enumerate(list(argv)[1:]):
        wcount = get_warn_count_by_file(args)
        warn_count_by_file.append([args, wcount])
        #print(args,wcount)
        #print(warn_count_by_file)
    if (is_build_promoted(warn_count_by_file) < 0):
        print("Build CAN'T be promoted")
        return False
    else:
        print("Build Promoted")
        return True

if (__name__ == "__main__"):
    main(sys.argv)

