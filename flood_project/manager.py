# Ei file e FloodManager class ache: add, delete, update, search, analysis

from datetime import datetime

import numpy as np  

from models import FloodReport


def validate_report(report_id, district, date, water_level,
                    affected_people, houses_damaged):
    #"""Input check kore. Bhul thakle ValueError dey, thik thakle FloodReport object dey."""
    report_id = report_id.strip()
    district = district.strip()
    date = date.strip()


    if report_id == "":
        raise ValueError("Report id needed")
    if district == "":
        raise ValueError("District must be filled")
    if date == "":
        raise ValueError("Date can't be null")

    # Date format check
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date formate must be in YYYY-MM-DD ")

    # Number check
    try:
        water_level = float(water_level)
        affected_people = int(affected_people)
        houses_damaged = int(houses_damaged)
    except ValueError:
        raise ValueError("Water level, Affected People, Houses Damaged "
                         "must be in integer number .")

    # Out of range check
    if water_level < 0 or water_level > 20:
        raise ValueError("Water level must be in between 0 to 20")
    if affected_people < 0 or houses_damaged < 0:
        raise ValueError("negative value not allowed.")

    return FloodReport(report_id, district.title(), date, water_level,
                       affected_people, houses_damaged)


class FloodManager:

    def __init__(self):
        self.reports = []  
        self.used_ids = set() 


    def add_report(self, report_id, district, date, water_level,
                   affected_people, houses_damaged):
        report = validate_report(report_id, district, date, water_level,
                                 affected_people, houses_damaged)
        if report.report_id in self.used_ids:
            raise ValueError("Ei ID age thekei ache: " + report.report_id)
        self.reports.append(report)
        self.used_ids.add(report.report_id)  #set doesnt support append 

    def find_index(self, report_id):
        for i in range(len(self.reports)):
            if self.reports[i].report_id == report_id:
                return i
        return -1

    def update_report(self, report_id, district, date, water_level,
                      affected_people, houses_damaged):
        index = self.find_index(report_id.strip())
        if index == -1:
            raise ValueError("Report not found " + report_id)
        new_report = validate_report(report_id, district, date, water_level,
                                     affected_people, houses_damaged)
        self.reports[index] = new_report

    def delete_report(self, report_id):
        index = self.find_index(report_id)
        if index == -1:
            raise ValueError("Report not found " + report_id)
        self.reports.pop(index)
        self.used_ids.discard(report_id)

    def search_by_district(self, text):
        text = text.strip().lower()
        return [r for r in self.reports if text in r.district.lower()]

    # ---------- Analysis (NumPy) ----------
    def analyze(self):
        if len(self.reports) == 0:
            return None

        levels = []
        total_affected = 0
        total_houses = 0
        district_totals = {}
        severity_count = {}

        for r in self.reports:
            levels.append(r.water_level)
            total_affected = total_affected + r.affected_people
            total_houses = total_houses + r.houses_damaged

            if r.district in district_totals:
                district_totals[r.district] = district_totals[r.district] + r.affected_people
            else:
                district_totals[r.district] = r.affected_people

            if r.severity in severity_count:
                severity_count[r.severity] = severity_count[r.severity] + 1
            else:
                severity_count[r.severity] = 1

        worst_district = ""
        highest = -1
        for district in district_totals:
            if district_totals[district] > highest:
                highest = district_totals[district]
                worst_district = district

        return {
            "total_reports": len(self.reports),
            "avg_level": float(np.mean(levels)),
            "max_level": float(np.max(levels)),
            "total_affected": total_affected,
            "total_houses": total_houses,
            "district_totals": district_totals,
            "severity_count": severity_count,
            "worst_district": worst_district,
        }
