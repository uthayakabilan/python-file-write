# !/usr/bin/env python
import os
import sys
from analysis import get_lowest_value

# from datetime import date
# Import tiem for current date in python 2
import time

# Base ht command, format image_name with specified image
base_cmd = "/usr/bin/python3 /Users/kabil/Desktop/Files/Playground/python-file-write/write-code/generateData.py {rsvn_id} -i {image_name}"
# Base directory
base_dir = "/Users/kabil/Desktop/Files/Playground/python-file-write/cx-health-monitor/"
# Base directory of the main log file
base_log_file_dir = "/Users/kabil/Desktop/Files/Playground/python-file-write/cx-health-monitor/log_file.csv"
# Current_date used instead of date.today() for python2
current_date = time.strftime("%Y-%m-%d")


# Function to create base directory if it does not exixts
def check_base_dir():
    if os.path.exists(base_dir):
        return True
    else:
        try:
            # os.makedirs(base_dir, exist_ok=True)
            try:
                os.makedirs(base_dir)
            except:
                pass
            return True
        except:
            return False


def wait_till_file(path, timer=3600, interval=60):
    if (timer <= 0):
        print("timer ended")
        return False
    print("timer remaining.. ", timer)
    print("retrying in.. ", interval)
    if (os.path.exists(path)):
        print("Path exists ... ")
        time.sleep(60)
        print("File found")
        return True
    else:
        time.sleep(interval)
        return wait_till_file(path, timer-interval, interval)


# utility function to run the ht command to generate the data with the specified image name
def generate_data(image, rsvn_id=False):
    if rsvn_id:
        id = "-rsvnId " + rsvn_id
        ht_cmd = base_cmd.format(image_name=image, rsvn_id=id)
    else:
        ht_cmd = base_cmd.format(image_name=image, rsvn_id="")
    print(ht_cmd)
    os.system(ht_cmd)


# utility function to copy contents from source to destination
def read_and_copy(
    dest_dir, dest_file, mode="w", source_file=base_log_file_dir, delete_source=False
):
    if wait_till_file(source_file):
        if os.path.exists(dest_dir):
            open_source_file = open(source_file, "r")
            open_dest_file = open(dest_file, mode)
            for line in open_source_file:
                open_dest_file.write(line)
            open_source_file.close()
            open_dest_file.close()
            if delete_source:
                time.sleep(60)
                print("Source file deleted")
                os.remove(source_file)
        else:
            print(
                "Destination does not exist. Please check the path to the destination directory"
            )
    else:
        print("Source file does not exist. Please check the path to the source file")


def baseline():
    dest_dir = os.path.join(base_dir, "Multicast",
                            "Baseline", "XX_10_12_0001AJ")
    # os.makedirs(dest_dir, exist_ok=True)
    try:
        os.makedirs(dest_dir)
    except:
        pass
    # dest_file = os.path.join(dest_dir, "baseline_{}.csv".format(date.today()))
    dest_file = os.path.join(dest_dir, "baseline_{}.csv".format(current_date))
    read_and_copy(dest_dir, dest_file, "w", delete_source=True)
    update_build_baseline()


def update_baseline():
    dest_dir = os.path.join(base_dir, "Multicast",
                            "Baseline", "BaselinedValues")
    # os.makedirs(dest_dir, exist_ok=True)
    try:
        os.makedirs(dest_dir)
    except:
        pass
    dest_file = os.path.join(dest_dir, "baselined_values.csv")
    read_and_copy(dest_dir, dest_file, "w")


def update_build_baseline(build):
    dest_dir = os.path.join(
        base_dir, "Multicast", "Baseline", "XX_10_12_0001AJ", "BaselinedValue"
    )
    try:
        os.makedirs(dest_dir)
    except:
        pass
    dest_file = os.path.join(dest_dir, "baselined_10_12.csv")
    # get lowest value
    lowest_file_dir = os.path.join(
        base_dir, "Multicast", "Baseline", "XX_10_12_0001AJ")
    source_file = get_lowest_value(lowest_file_dir)
    if source_file == "no file found":
        print("No file found in: ", lowest_file_dir)
    else:
        read_and_copy(dest_dir, dest_file, "w", source_file=source_file)


def test_run(baseline_version, build):
    dest_dir = os.path.join(base_dir, "Multicast",
                            "TestRun", "XX_10_12_1000BD")
    # os.makedirs(dest_dir, exist_ok=True)
    try:
        os.makedirs(dest_dir)
    except:
        pass
    # dest_file = os.path.join(dest_dir, "testrun_{}.csv".format(date.today()))
    dest_file = os.path.join(dest_dir, "testrun_{}.csv".format(current_date))
    # Compare functionality
    read_and_copy(dest_dir, dest_file, "w")
    print(baseline_version, build)


def default_run():
    dest_dir = os.path.join(base_dir, "Multicast",
                            "TestRun", "XX_10_12_1000BD")
    # os.makedirs(dest_dir, exist_ok=True)
    try:
        os.makedirs(dest_dir)
    except:
        pass
    # dest_file = os.path.join(dest_dir, "testrun_{}.csv".format(date.today()))
    dest_file = os.path.join(dest_dir, "testrun_{}.csv".format(current_date))
    read_and_copy(dest_dir, dest_file, "w")


def remove_rsvn_id(args):
    is_rsvn = False
    rsvn_index = 0
    arg_list = args
    for x in range(0, len(args)):
        if "-rsvnId" in args[x]:
            is_rsvn = True
            rsvn_index = x
    if is_rsvn:
        arg_list = args[:rsvn_index]
    return arg_list, is_rsvn, args[rsvn_index + 1]


def run_build(args):
    if len(args) > 2 and args[1] == "-i":
        args, is_rsvn, rsvn_id = remove_rsvn_id(args)
        print(args, is_rsvn, rsvn_id)
        # Extracts image name from the runtime
        image = args[2]
        print(image)
        if is_rsvn:
            generate_data(image, rsvn_id)
        else:
            generate_data(image)
        if len(args) > 3:
            # Extracts run mode from the runtime and compares with the conditions
            run_mode = args[3]
            if run_mode == "baseline":
                baseline()
            elif run_mode == "update-baseline":
                if len(args) > 4:
                    build = args[4]
                    update_build_baseline(build)
                else:
                    update_baseline()
            elif run_mode == "testrun":
                if len(args) > 5:
                    # Extracts baseline version to be comapred
                    baseline_version = args[4]
                    build = args[5]
                    print("test_run mode with values ",
                          baseline_version, build)
                    test_run(baseline_version, build)
                else:
                    print("Enter the correct test run built")
            else:
                print("Invalid run mode")
        else:
            # Executes when no run mode is specified, only image is specified with the -i flag
            default_run()
    else:
        print("Invalid command. Please specify the image file using -i flag")


# Main function/Starting point for execution
def run():
    if check_base_dir():
        run_build(sys.argv)
    else:
        print("Unable to find/create/permission denied for the base directory")


run()
