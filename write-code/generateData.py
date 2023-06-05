import sys
import os

# path to the root log file
directory_path = (
    "/Users/kabil/Desktop/Files/Playground/python-file-write/cx-health-monitor/"
)
file_path = os.path.join(directory_path, "log_file.csv")

if os.path.exists(directory_path):
    pass
else:
    print(
        "Path not found to write the data, make sure the directory and file exixts to write the data"
    )
