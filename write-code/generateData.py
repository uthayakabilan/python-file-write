import sys
import os

# path to the root log file
directory_path = (
    "/Users/kabil/Desktop/Files/Playground/python-file-write/cx-health-monitor/"
)
file_path = os.path.join(directory_path, "log_file.csv")

if os.path.exists(directory_path):
    f = open(file_path, "w")
    # Log file is created to store the data. Log file will be automatically removed once the data is moved
    try:
        f.write("Hello from the image: {}".format(sys.argv[1]))
    finally:
        f.close()
else:
    print(
        "Path not found to write the data, make sure the directory and file exixts to write the data"
    )
