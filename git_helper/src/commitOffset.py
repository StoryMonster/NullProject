import sys


def search_commit(commit_id, offset):
    act_find_specific_commit = False
    while True:
        try:
            line = raw_input()
        except EOFError:
            print "Error: Cannot find the specific commit"
            break
        if line.find("commit ") != -1:
            if act_find_specific_commit == True:
                offset += 1
                if offset == 0:
                    print "\033[40;33m{}\033[0m".format(line)
                    break
            else:
                commit = line.split()[1]
                if commit.find(commit_id) == 0:
                    act_find_specific_commit = True


if __name__ == '__main__':
    assert len(sys.argv) == 3, "Error: Unknown action"
    commit_id = sys.argv[2]
    assert len(commit_id) >= 7, "Error: The length of commit id should larger than 7"
    offset = int(sys.argv[1])
    assert offset < 0, "Error: Can only support find commid id before the specific commit"
    search_commit(commit_id, offset)
