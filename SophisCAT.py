import sys
import base64
import os
import random
import string

if len(sys.argv) != 2:
    print("usage: python3 SophisCAT.py <file>")
    sys.exit(1)

infile = sys.argv[1]
if not os.path.isfile(infile):
    print("file not found")
    sys.exit(1)

with open(infile, "rb") as f:
    data = f.read()

b64 = base64.b64encode(data).decode("ascii")
basename = os.path.splitext(os.path.basename(infile))[0]
outfile = basename + ".py"
orig_name = os.path.basename(infile)

print('Include subprocess.Popen(["' + orig_name + '"]) in the generated code? (y/n)')
ans = input().strip().lower()
include_pop = ans in ("y", "yes")

def rand_var():
    return "".join(random.choices(string.ascii_letters, k=random.randint(6, 12)))

v1 = rand_var()
v2 = rand_var()
while v2 == v1:
    v2 = rand_var()

code = "import base64, subprocess, sys, os\n"
code += v1 + ' = "' + b64 + '"\n'
code += v2 + " = base64.b64decode(" + v1 + ")\n"
code += 'with open("' + orig_name + '","wb") as f:\n'
code += "    f.write(" + v2 + ")\n"
if include_pop:
    code += 'subprocess.Popen(["' + orig_name + '"])\n'
# Up i was fucking acting delulu i written when i was half asleeo so it did this shit and ran itself
with open(outfile, "w") as f:
    f.write(code)

print("Created " + outfile)
