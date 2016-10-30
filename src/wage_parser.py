'''
Created on Oct 28, 2016

@author: petteri.raisanen
'''

import csv
import os
from operator import attrgetter

BASE_HOURLY_RATE_CENTS = 375
EVENING_EXTRA_RATE_CENTS = 115

EVENING_WORK_START_HOUR = 18
EVENING_WORK_END_HOUR = 6
NORMAL_WORKING_HOURS = 8

def calculate_overtime_hours(hours):
    return max(hours - NORMAL_WORKING_HOURS, 0);

def calculate_hours(start, end):
    if end <= start:
        # burning the midnight candle at night shift
        hours = (24 - start) + end
        evening_hours = min(24 - EVENING_WORK_START_HOUR, 24 - start) + min(end, EVENING_WORK_END_HOUR)
    else:
        hours = (end - start)
        evening_hours = max(end - EVENING_WORK_START_HOUR, 0)

    overtime_hours = calculate_overtime_hours(hours)
    if overtime_hours:
        evening_hours = 0

    return (hours, evening_hours, overtime_hours)

# Converts 11:30, 02:00 type of times into a normalized form,
# e.g. 11.5, 2.0 etc. that are good enough for hour calculation purposes.
#LIMITATION: This will not really work if there are times that are not at 30 minute precisions.
def normalize_time(time):
    parts = time.split(":")

    hours = int(parts[0])

    if (hours < 0):
        raise ValueError("Hours cannot be negative!")

    if len(parts) > 1:
        minutes = float(parts[1])
        hours += minutes / 60.0

    if (hours >= 24):
        raise ValueError("Hours must be smaller than 24!")

    return hours

# The same date may have multiple entries, here we combine them first:
def normalize_hours(raw_hours):
    normalized = []

    current_date = None
    for hours in sorted(raw_hours, key=attrgetter("date")):
        if hours.date != current_date:
            normalized.append(hours)

            current_date = hours.date
        else:
            normalized[-1].add_hours(hours)

    return normalized

def calculate_overtime_pay(overtime_hours):
    pay = overtime_hours * 0.25 * BASE_HOURLY_RATE_CENTS
    if (pay > 2):
        pay += (overtime_hours - 2) * 0.25 * BASE_HOURLY_RATE_CENTS

    if (pay > 4):
        pay += (overtime_hours - 4) * 0.50 * BASE_HOURLY_RATE_CENTS

    return pay

class Hours(object):

    def __init__(self, date, start, end):
        self.date = date
        (self.hours, self.evening_hours, self.overtime_hours) = calculate_hours(normalize_time(start), normalize_time(end))

    def to_dollars(self):

        cents = self.hours * BASE_HOURLY_RATE_CENTS
        cents += self.evening_hours * EVENING_EXTRA_RATE_CENTS
        cents += calculate_overtime_pay(self.overtime_hours)

        return cents / 100.00

    def add_hours(self, other):
        self.hours += other.hours
        self.evening_hours += other.evening_hours

        # This is a little complicated: if our total hours go over the overtime limit, we need to recalculate the lot:
        self.overtime_hours = calculate_overtime_hours(self.hours)
        # And if we got any, evening hours become irrelevant
        if self.overtime_hours:
            self.evening_hours = 0

class MonthlyWage(object):
    def __init__(self, person_id, name, wage):
        self.person_id = person_id
        self.name = name
        self.wage = wage


def parse_month(date_str):
    # 12.3.2014
    comps = date_str.strip().split(".")
    if len(comps) != 3:
        raise ValueError("Invalid date %s" % date_str)

    # we do't the day
    month = int(comps[1])
    year = int(comps[2])

    return (month, year)

class WageParser(object):
    def __init__(self, in_file):
        if os.path.exists(in_file):
            self.in_file = in_file
        else:
            raise Exception("File %s not found." % in_file)

        self.persons = {}
        self.hours = {}
        self.__month = None

    def validate_and_set_month(self, date):
        month = parse_month(date)
        if not self.__month:
            self.__month = month

        if self.__month != month:
            raise Exception("The CSV should only contain entries for one month!")

    def __parse_csv(self):
        with open(self.in_file) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                name = row["Person Name"]
                person_id = row["Person ID"]

                if person_id not in self.persons:
                    self.persons[person_id] = name

                if person_id not in self.hours:
                    self.hours[person_id] = []

                date = row["Date"]
                self.validate_and_set_month(date)

                self.hours[person_id].append(Hours(date, row["Start"], row["End"]))

    def __calculate_wages(self):
        monthly_wages = []

        for person_id in sorted(self.persons.keys()):
            for hours in normalize_hours(self.hours[person_id]):
                print(person_id, hours.date, hours.hours, hours.evening_hours, hours.overtime_hours, hours.to_dollars())
            daily_wages = map(lambda hours: hours.to_dollars(), normalize_hours(self.hours[person_id]))

            monthly_wage = 0.0
            for daily_wage in daily_wages:
                monthly_wage += daily_wage

            monthly_wages.append(MonthlyWage(person_id, self.persons[person_id], monthly_wage))

        return monthly_wages

    def parse(self):
        self.__parse_csv()
        return self.__calculate_wages() 
    
    def month(self):
        return self.__month