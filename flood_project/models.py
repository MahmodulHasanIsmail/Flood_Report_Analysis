#main class "FloodReport" ache (OOP part)

SEVERITY_LEVELS = ("Low", "Medium", "High", "Critical")


class FloodReport:
    #Ekta flood report er data ebong tar severity hishab kore

    def __init__(self, report_id, district, date, water_level,
                 affected_people, houses_damaged):
        self.report_id = report_id              # string, jemon "R001"
        self.district = district                # string
        self.date = date                        # string "YYYY-MM-DD"
        self.water_level = water_level          # float (meter)
        self.affected_people = affected_people  # int
        self.houses_damaged = houses_damaged    # int
        self.severity = self.calculate_severity()

    def calculate_severity(self):
        if self.water_level >= 4:
            return SEVERITY_LEVELS[3]   # 
        elif self.water_level >= 3:
            return SEVERITY_LEVELS[2]   
        elif self.water_level >= 2:
            return SEVERITY_LEVELS[1]  
        else:
            return SEVERITY_LEVELS[0]   

    def to_dict(self):
        #Record ke dictionary te convert kore (file e save korar jonno
        return {
            "report_id": self.report_id,
            "district": self.district,
            "date": self.date,
            "water_level": self.water_level,
            "affected_people": self.affected_people,
            "houses_damaged": self.houses_damaged,
        }
    def to_row(self):
        #Table e dekhanor jonno tuple.
        return (self.report_id, self.district, self.date, self.water_level,
                self.affected_people, self.houses_damaged, self.severity)
