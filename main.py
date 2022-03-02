#!/usr/bin/python3
# Copyright (C) 2022 Gaurav Kedia. All rights reserved.
""" Retrieve Temperature Data """
import logging
import sys
import argparse
import urllib.request as request
import urllib.error
import ast

LOGFILE = '/var/log/tempature.log'


def init_file_logger(logfile='/tmp/main.log', stderr=None):
    """
    Initialize File Logger

    """
    file_format = ('[%(asctime)s %(process)d] %(levelname)s '
                   '(%(module)s:%(lineno)d) %(message)s')
    date_format = '%Y-%m-%dT%H:%M:%S'

    logging.basicConfig(filename=logfile, format=file_format,
                        datefmt=date_format, level=logging.DEBUG)

    if stderr:
        console = logging.StreamHandler()
        logger = logging.getLogger()
        logger.setLevel(stderr)
        logger.addHandler(console)


def get_temp(latitude, longitude):
    """
    Code below will retrieve temperature data

    """
    try:
        uri = "https://api.open-meteo.com/v1/forecast?" + \
                "latitude={latt}&longitude={longt}&hourly=temperature_2m"
        uri = uri.format(latt=latitude, longt=longitude)
        response = request.urlopen(uri)
        data = ast.literal_eval(response.read().decode("UTF-8"))
        if 'error' in data:
            print("Invalid Input, please try again")
            return False
        if data["hourly"]["time"] and data["hourly"]["temperature_2m"]:
            print("{:<15} {:<15} {:<10}".format('Date', 'Time', 'Temperature'))
            for i in range(len(data["hourly"]["temperature_2m"])):
                print("{:<15} {:<15} {:<10}".format(str(data["hourly"]["time"][i].split('T')[0]),
                                                    str(data["hourly"]["time"][i].split('T')[1]),
                                                    str(data["hourly"]["temperature_2m"][i])))
            return True
    except urllib.error.HTTPError as err:
        print("Command failed: %s. See %s for details." % (err, LOGFILE))
        return 1
    except urllib.error.URLError as err:
        print("Command failed: %s. See %s for details." % (err, LOGFILE))
        return 1
    return True


def main():
    """
    Code below will retrieve the latitude and longitude info
    from a place name.

    """
    parser = argparse.ArgumentParser(allow_abbrev=False, conflict_handler='resolve')
    parser.add_argument("--place", type=str, help="Place Name", required=True)
    arguments = parser.parse_args()

    #init_file_logger(logfile=LOGFILE)

    arguments = vars(arguments)
    try:
        uri = "https://geocode.xyz/{place}?json=1"
        uri = uri.format(place=arguments['place'])
        response = request.urlopen(uri)
        data = ast.literal_eval(response.read().decode("UTF-8"))
        if 'error' in data:
            print("Invalid Input, please try again")
        if 'latt' and 'longt' in data:
            if get_temp(data['latt'], data['longt']):
                return 0
    except urllib.error.HTTPError as err:
        print("Command failed: %s. See %s for details." % (err, LOGFILE))
        return 1
    except urllib.error.URLError as err:
        print("Command failed: %s. See %s for details." % (err, LOGFILE))
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as err:
        print("Unexpected exception: %s" % str(err))
        sys.exit(1)
