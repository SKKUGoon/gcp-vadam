import pandas as pd


class FilingDataContainer:
    def __init__(self):
        self.dates = list()
        self.income_statements = list()
        self.balance_sheets = list()
        self.cash_flow_statements = list()

    def set_date(self, date):
        self.dates.append(date)

    def insert_income_statement(self, income_statement, date):
        data = self.parse_income_statement_data(income_statement, date)
        self.income_statements.append(data)

    def insert_balance_sheet(self, balance_sheet, date):
        data = self.parse_balance_sheet_data(balance_sheet, date)
        self.balance_sheets.append(data)

    def insert_cash_flow_statement(self, cash_flow_statement, date):
        data = self.parse_cash_flow_statement_data(cash_flow_statement, date)
        self.cash_flow_statements.append(data)

    def get_data(self):
        income_statements = self.merge_data(*self.income_statements)
        balance_sheets = self.merge_data(*self.balance_sheets)
        cash_flow_statements = self.merge_data(*self.cash_flow_statements)

        # income_statements = pd.DataFrame(income_statements, index=self.dates)
        # balance_sheets = pd.DataFrame(balance_sheets, index=self.dates)
        # cash_flow_statements = pd.DataFrame(cash_flow_statements, index=self.dates)

        return income_statements, balance_sheets, cash_flow_statements, self.dates

    @staticmethod
    def parse_income_statement_data(income_statement, date):
        return {
            "basic_earnings_per_share": {date: income_statement.basic_earnings_per_share.value if income_statement.basic_earnings_per_share is not None else None},
            "revenues": {date: income_statement.revenues.value if income_statement.revenues is not None else None},
            "cogs": {date: income_statement.cost_of_revenue.value if income_statement.cost_of_revenue is not None else None},
            "gross_profit": {date: income_statement.gross_profit.value if income_statement.gross_profit is not None else None},
            "operating_expenses": {date: income_statement.operating_expenses.value if income_statement.operating_expenses is not None else None},
        }

    @staticmethod
    def parse_balance_sheet_data(balance_sheet, date):
        return {k: {date: v.value} for k, v in balance_sheet.items()}

    @staticmethod
    def parse_cash_flow_statement_data(cash_flow_statement, date):
        return {
            "exchange_gains_losses": {date: cash_flow_statement.exchange_gains_losses.value if cash_flow_statement.exchange_gains_losses is not None else None},
            "net_cash_flow": {date: cash_flow_statement.net_cash_flow.value if cash_flow_statement.net_cash_flow is not None else None},
            "net_cash_flow_from_financing_activities": {date: cash_flow_statement.net_cash_flow_from_financing_activities.value if cash_flow_statement.net_cash_flow_from_financing_activities is not None else None},
        }

    @staticmethod
    def merge_data(*data):
        container = {k: {} for k in data[0].keys()}
        for d in data:
            for k, v in d.items():
                container[k].update(v)
        return container
