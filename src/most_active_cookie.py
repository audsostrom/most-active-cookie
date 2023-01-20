#!/usr/bin/env python3
"""
Author: Audrey Ostrom
Purpose: Process a given log file and return the most active
cookie for specified day
"""

import sys
import argparse

def find_most_active_cookies(input_file, input_date):
    """Creates dictionary of cookies and finds most frequent cookie on specific day"""
    cookie_dict = {}
    max_freq = 1
    # read each line of input file
    for line in input_file:
    # create edge list from remaining lines
        [current_cookie, current_time_stamp] = line.split(',')
        date = current_time_stamp.split('T')[0]
        if date == input_date:
            if current_cookie in cookie_dict:
                cookie_dict[current_cookie] += 1
                if cookie_dict[current_cookie] > max_freq:
                    max_freq = cookie_dict[current_cookie]
            else:
                cookie_dict[current_cookie] = 1
    # no matches in log file for date
    if len(cookie_dict) == 0:
        sys.exit('No cookies found for given day')
    # yield all most frequently active cookies
    for key, value in cookie_dict.items():
        if value == max_freq:
            yield key

def cli_arg_parse():
    """Gets command-line inputs from user for log file and date"""
    parsed_cli = argparse.ArgumentParser(description='Find most active cookie on \
        given day from log file')
    parsed_cli.add_argument('filename', help='log file to read')
    parsed_cli.add_argument('-d', '--date', metavar='date', help='date for searching for cookies')
    return parsed_cli.parse_args()

# ------------------------------------------------------------------------------
# main()
# ------------------------------------------------------------------------------
def main():
    """main function that takes in two user-specified command line arguments"""
    try:
        arguments = cli_arg_parse()
        check_date = arguments.date
        infile = open(arguments.filename, "r", encoding="utf-8")
        # print all most frequent cookies on a given day
        for cookie in find_most_active_cookies(infile, check_date):
            print(cookie)
    # input file doesn't exist
    except FileNotFoundError:
        sys.exit(f"No such file or directory: '{arguments.filename}'")

if __name__ == "__main__":
    main()
