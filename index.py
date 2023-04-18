import subprocess
import sys

action = sys.argv[1]
sub_domain = sys.argv[2]
repo_name = sys.argv[3]

if action == "add":
    subprocess.run(["python3", "add-link.py", sub_domain, repo_name])
elif action == "remove":
    subprocess.run(["python3", "remove-link.py", sub_domain, repo_name])
else:
    print("You must specify an action (add or remove)")
    sys.exit(1)