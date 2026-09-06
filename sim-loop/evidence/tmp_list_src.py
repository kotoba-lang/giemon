import os
root = "/Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon"
out = []
for sub in ["src", "test"]:
    for dirpath, dirs, files in os.walk(os.path.join(root, sub)):
        for f in files:
            out.append(os.path.relpath(os.path.join(dirpath, f), root))
with open("/tmp/src_list.txt", "w") as fh:
    fh.write("\n".join(sorted(out)))
print(len(out))
