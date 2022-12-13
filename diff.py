import subprocess
import sys


main_branch_name = sys.argv[1]
fetch_result = subprocess.check_output(["git", "fetch", "origin", main_branch_name])
diff_result = str(subprocess.check_output(["git", "diff", f"origin/{main_branch_name}"]))
print(diff_result)