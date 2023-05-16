import os
import sys
from datetime import date

# Base ht command, format image_name with specified image
base_cmd = "/usr/bin/python3 /Users/kabil/Desktop/Files/Playground/python-file-write/write-code/generateData.py {image_name}"
# Base directory
base_dir = "/Users/kabil/Desktop/Files/Playground/python-file-write/cx-health-monitor/"
# Base directory of the root log file
base_log_file_dir = "/Users/kabil/Desktop/Files/Playground/python-file-write/cx-health-monitor/log_file.csv"


# utility function to run the ht command to generate the data with the specified image name
def generateData(image):
    ht_cmd = base_cmd.format(image_name=image)
    os.system(ht_cmd)


# utility function to copy contents from source to destination
def readAndCopy(dest_dir, dest_file, mode="w", source_file=base_log_file_dir):
    if os.path.exists(source_file):
        if os.path.exists(dest_dir):
            sourceFile = open(source_file, "r")
            destFile = open(dest_file, mode)
            for line in sourceFile:
                destFile.write(line)
            sourceFile.close()
            destFile.close()
            os.remove(source_file)
            # Log file removed after copying the data
        else:
            print(
                "Destination does not exist. Please check the path to the destination directory"
            )
    else:
        print("Source file does not exist. Please check the path to the source file")


def baseLine():
    dest_dir = os.path.join(base_dir, "Multicast", "Baseline", "XX_10_12_0001AJ")
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, "baseline_{}.csv".format(date.today()))
    readAndCopy(dest_dir, dest_file, "w")


def updateBaseLine():
    dest_dir = os.path.join(base_dir, "Multicast", "Baseline", "BaselinedValues")
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, "baselined_values.csv")
    readAndCopy(dest_dir, dest_file, "w")


def testRun(baseline_version, build):
    dest_dir = os.path.join(base_dir, "Multicast", "TestRun", "XX_10_12_1000BD")
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, "testrun_{}.csv".format(date.today()))
    # Compare functionality
    readAndCopy(dest_dir, dest_file, "w")
    print(baseline_version, build)


def defaultRun():
    dest_dir = os.path.join(base_dir, "Multicast", "TestRun", "XX_10_12_1000BD")
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, "testrun_{}.csv".format(date.today()))
    readAndCopy(dest_dir, dest_file, "w")


if len(sys.argv) > 2 and sys.argv[1] == "-i":
    # Extracts image name from the runtime
    image = sys.argv[2]
    generateData(image)
    if len(sys.argv) > 3:
        # Extracts run mode from the runtime and compares with the conditions
        run_mode = sys.argv[3]
        if run_mode == "baseline":
            baseLine()
        elif run_mode == "update-baseline":
            updateBaseLine()
        elif run_mode == "testrun":
            if len(sys.argv) > 5:
                # Extracts baseline version to be comapred
                baseline_version = sys.argv[4]
                build = sys.argv[5]
                print("test_run mode with values ", baseline_version, build)
                testRun(baseline_version, build)
            else:
                print("Enter the correct test run built")
        else:
            print("Invalid run mode")
    else:
        # Executes when no run mode is specified, only image is specified with the -i flag
        defaultRun()
else:
    print("Invalid command. Please specify the image file using -i flag")
