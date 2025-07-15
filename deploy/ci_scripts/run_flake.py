import subprocess
import sys

import requests
from utils.args_parser import get_args

args = get_args(sys.argv)
headers = {
    "PRIVATE-TOKEN": args.get("token"),
    "Content-Type": "application/x-www-form-urlencoded",
}
response = requests.get(
    f'{args.get("url")}/api/v4/projects/{args.get("project_id")}/merge_requests/{args.get("merge_request_id")}/changes',
    headers=headers,
)
files_in_mr = [
    file_name.get("new_path", "")
    for file_name in response.json().get("changes", [])
    if file_name.get("new_path", "").endswith(".py")
]
if files_in_mr:
    result = subprocess.run(
        "flake8 --config=app/setup.cfg " + " ".join(files_in_mr),
        shell=True,
        text=True,
        capture_output=True,
    )
    print(result.stdout)
    print(result.stderr)
    with open("flake8label.txt", "w+") as f:
        if result.returncode == 0:
            f.write("flake8-passed")
        else:
            f.write("flake8-failed")
