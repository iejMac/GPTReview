import subprocess

fetch_result = subprocess.check_output(["git", "fetch", "origin", "master"])
diff_result = str(subprocess.check_output(["git", "diff", "origin/master"]))
print(diff_result)