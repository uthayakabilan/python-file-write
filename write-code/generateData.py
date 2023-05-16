import sys
import os

# path to the root log file
root_dir = "/Users/kabil/Desktop/Files/Playground/python-file-write/cx-health-monitor/"

if os.path.exists(root_dir):
    log_file = os.path.join(root_dir, "log_file.csv")
    f = open(log_file, "w")
    # Log file is created to store the data. Log file will be automatically removed once the data is moved
    try:
        f.write("Hello from the image: {}".format(sys.argv[1]))
    finally:
        f.close()
else:
    print(
        "Path not found to write the data, make sure the directory and file exixts to write the data"
    )
