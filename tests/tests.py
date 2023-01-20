#!/usr/bin/env python3
"""
Author: Audrey Ostrom
Purpose: To test most_active_cookies.py
"""

import os
from subprocess import getstatusoutput, getoutput

import random
from datetime import datetime
from string import ascii_lowercase, ascii_uppercase, digits
from src.most_active_cookie import find_most_active_cookies

PRG = 'src/most_active_cookie.py'
CHARS = ascii_lowercase + ascii_uppercase + digits

# Helper functions
def make_random_date():
    """ Helper function for making random dates """
    return datetime(
        random.randrange(2000,2023),
        random.randrange(1,13),
        random.randrange(1,29),
        random.randrange(0,24),
        random.randrange(0,60)).isoformat()

# Lists we can use to help make log files
cookie_list = [''.join(random.choice(CHARS) for _ in range(10)) for _ in range(20)]
date_list = [make_random_date() for _ in range(40)]


# --------------------------------------------------
def test_exists():
    """Check our source code file exists"""
    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_runnable():
    """Runs using python3"""
    out = getoutput(f'python3 {PRG}')
    assert out.strip() == 'usage: most_active_cookie.py [-h] [-d date] filename\n' \
    'most_active_cookie.py: error: the following arguments are required: filename'


# --------------------------------------------------
def test_executable():
    """Executable gives usage statement without CLI arguments"""
    out = getoutput(PRG)
    assert out.strip() == 'usage: most_active_cookie.py [-h] [-d date] filename\n' \
    'most_active_cookie.py: error: the following arguments are required: filename'


# --------------------------------------------------
def test_usage():
    """Check usage statement is correct"""
    for flag in ['-h', '--help']:
        exit_status, out = getstatusoutput(f'{PRG} {flag}')
        assert exit_status == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_input():
    """Test for user input (return one cookie)"""
    exit_status, out = getstatusoutput(f'{PRG} logfiles/cookie_log.csv -d 2018-12-09')
    assert exit_status == 0
    assert out.strip() == 'AtY0laUfhglK3lC7'

# --------------------------------------------------
def test_multiple_cookies():
    """Tests for user input (return multiple cookies)"""
    exit_status, out = getstatusoutput(f'{PRG} logfiles/cookie_log.csv -d 2018-12-08')
    assert exit_status == 0
    assert out.strip() == 'SAZuXPGUrfbcn5UA\n' \
        '4sMM2LxV07bPJzwf\n' \
        'fbcn5UAVanZf6UtG'

def test_bad_date():
    """Tests for bad dates not found in log file"""
    exit_status, out = getstatusoutput(f'{PRG} logfiles/cookie_log.csv -d 2022-12-25')
    assert exit_status == 1
    assert out.strip() == 'No cookies found for given day'

def test_bad_file():
    """Tests for file that doesn't exist"""
    not_real_file = 'logfiles/noexist.csv'
    exit_status, out = getstatusoutput(f"{PRG} {not_real_file} -d 2022-12-25")
    assert exit_status == 1
    assert out.strip() == f"No such file or directory: '{not_real_file}'"

# --------------------------------------------------
def test_basic_random():
    """Tests function find_most_active_cookies returns one cookie"""
    outfile =  open("logfiles/tests_basic.csv", "w+", encoding="utf-8")
    for _ in range(6):
        outfile.write(f"{cookie_list[0]},{'2018-12-09T14:19:00'}\n")
    for _ in range(4):
        outfile.write(f"{cookie_list[random.randrange(0, 10)]},{make_random_date()}\n")
    outfile.flush()
    outfile.seek(0)
    result = list(find_most_active_cookies(outfile, '2018-12-09'))
    assert result == [cookie_list[0]]

def test_multiple_random():
    """tests function find_most_active_cookies returns multiple cookies"""
    outfile = open("logfiles/tests_multiple.csv", "w+", encoding="utf-8")
    for _ in range(3):
        outfile.write(f"{cookie_list[0]},{date_list[0]}\n")
        outfile.write(f"{cookie_list[1]},{date_list[0]}\n")
        outfile.write(f"{cookie_list[2]},{date_list[0]}\n")
    outfile.write(f"{cookie_list[random.randrange(0, 10)]},{make_random_date()}\n")
    outfile.flush()
    outfile.seek(0)
    stripped_date = (date_list[0].split('T'))[0]
    result = list(find_most_active_cookies(outfile, stripped_date))
    assert result == cookie_list[0:3]
