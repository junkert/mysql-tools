#!/usr/bin/env python3

import argparse
import getpass
import time
import MySQLdb
from datetime import datetime
from pprint import pprint

def parse_args():
    ap = argparse.ArgumentParser(
        description=(
            "Prints out the MySQL full process list as well as InnoDB status when threads hit --max-threads"
        )
    )

    ap.add_argument(
        "-U",
        "--user",
        dest="user",
        metavar="user",
        required=True,
        help="MySQL username with admin privileges")

    ap.add_argument(
        "-H",
        "--host",
        dest="host_name",
        metavar="host_name",
        required=True,
        help="MySQL hostname")

    ap.add_argument(
        "-P",
        "--port",
        dest="port",
        metavar="port",
        default=3306,
        help="MySQL port")

    ap.add_argument(
        "-T",
        "--max-threads",
        dest="max_threads",
        metavar="max_threads",
        required=True,
        help="Maximum threads to allow before printing out the full process list and InnoDB status")
    return ap.parse_args()


def get_full_process_list(cursor):
    cursor.execute("SHOW FULL PROCESSLIST")
    return cursor.fetchall()

def get_innodb_status(cursor):
    cursor.execute("SHOW ENGINE INNODB STATUS")
    return cursor.fetchall()


def print_time():
    currentDateAndTime = datetime.now()
    # Output: 2022-03-19 10:05:39.482383
    print("Date & Time: ", currentDateAndTime.isoformat())


def main(args):
    password = getpass.getpass("Password: ")
    sess = MySQLdb.connect(
        user=args.user,
        password=password,
        host=args.host_name,
        port=args.port,
        database='mysql'
    )

    cursor = sess.cursor()
    while True:
        process_list = get_full_process_list(cursor)

        if len(process_list) > int(args.max_threads):

            # Grab status right away, so we are as close as possible to the time
            # when we ran the full process list query
            innodb_status = get_innodb_status(cursor)

            print("=" * 120)
            print_time()
            print("")
            print("Full process list:")
            print("=" * 20)
            for row in process_list:
                print(f"{row[0]}\t | {row[1]}\t | {row[2]}\t | {row[3]}\t | {row[4]}\t | {row[5]}\t | {row[6]}\t | {row[7]}")
            print("")
            print("=" * 20)
            print("InnoDB status:")
            pprint(innodb_status)
            for row in innodb_status:
                for col in row:
                    print(col)
            print("")
            print("")
        time.sleep(1)

if __name__ == "__main__":
    exit(main(parse_args()))
