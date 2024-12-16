from datetime import datetime
from typing import List
import pandas as pd

class DateIndex:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
    
    def generate_monthly_index(self) -> List[datetime]:
        # Returns the list of end of the month within the date range
        dates = pd.date_range(
            start=self.start_date.replace(day=1),
            end=self.end_date,
            freq='M'  # Month End
        )
        return dates.to_list()

    def generate_quarterly_index(self) -> List[datetime]:
        # Returns the list of end of the quarter date within the date range
        dates = pd.date_range(
            start=self.start_date.replace(day=1),
            end=self.end_date,
            freq='Q'  # Quarter End
        )
        return dates.to_list()

    def generate_yearly_index(self) -> List[datetime]:
        # Returns the list of end of the year date within the date range
        dates = pd.date_range(
            start=self.start_date.replace(month=1, day=1),
            end=self.end_date,
            freq='A'  # Year End
        )
        return dates.to_list()