from pathlib import Path
from collections import defaultdict

here = Path(__file__).parent
lines = Path(here/"07.txt").read_text().splitlines()

# keep track of current directory as an array where each successive element is a sub-directory e.g ['/', 'a', 'e']
curr_dir = ['/']

# keep a map of the total size of each directory where each key is a string representation of the path ['//a/e']
dir_sizes = defaultdict(int)

for line in lines:
    parts = line.split()
    if parts[0] == '$':  # $ <cd OR ls> <args>
        if parts[1] == 'cd':  
            if parts[2] == '..':
                curr_dir.pop()
            elif parts[2] == '/':
                curr_dir = curr_dir[:1]
            else:
                curr_dir.append(parts[2])
    else:
        if not parts[0] == "dir":  # dir <dir_name> OR <file_size> <file_name>
            # increase the total size of the current directory and all its parent directories by the file size
            for i in range(len(curr_dir)):
                dir_path = '/'.join(curr_dir[:i+1])
                dir_sizes[dir_path] += int(parts[0])

print(f"Part 1: {sum(size for size in dir_sizes.values() if size < 100000)}")

total_size = 70000000
unused_space = total_size - dir_sizes['/']
needed_size = 30000000
min_to_delete_size = needed_size - unused_space

for size in sorted(dir_sizes.values()):
    if size >= min_to_delete_size:
        print(f"Part 2: {size}")
        break
