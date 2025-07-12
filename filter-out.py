#! /usr/bin/python3

import re
import sys

regexps = []
for a in sys.argv[1:]:
    try: regexps.append(re.compile(a))
    except Exception as e:
        sys.stderr.write("compiling regexp %s failed - %s\n" % (a, e))
        sys.exit(2)

print_lines = False
for line in sys.stdin:
    if line.startswith("---"):
        print_lines, split = True, line.split(" ", 4)
        if len(split) > 3:
            url = split[3 if split[1] == "REQUEST" else 2].lstrip("[").rstrip("]")
            for r in regexps:
                if r.search(url):
                    print_lines = False
                    break
    if print_lines:
        sys.stdout.write(line)
