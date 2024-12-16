import pandas as pd


class DiscountedCashFlow:
    def __init__(self, 
                 income_statements: pd.DataFrame, 
                 balance_sheets: pd.DataFrame, 
                 cash_flow_statements: pd.DataFrame):
        self.income_statements = self.select_income_statement(income_statements)
        self.balance_sheets = self.select_balance_sheet(balance_sheets)
        self.cash_flow_statements = self.select_cash_flow_statement(cash_flow_statements)

        self.wacc = None
        self.growth_rate = None

    def set_wacc(self, wacc: float):
        if wacc < 0 or wacc > 1:
            raise ValueError("Weighted average cost of capital must be between 0 and 1.")
        self.wacc = wacc

    def set_growth_rate(self, growth_rate: float):
        if growth_rate < 0 or growth_rate > 1:
            raise ValueError("Growth rate must be between 0 and 1.")
        self.growth_rate = growth_rate

    @staticmethod
    def select_income_statement(income_statement: pd.DataFrame) -> pd.DataFrame:
        # Select `revenues` and `cogs`, `operating_expenses` and `gross_profit`
        return income_statement[['revenues', 'cogs', 'operating_expenses', 'gross_profit']]

    @staticmethod
    def select_balance_sheet(balance_sheet: pd.DataFrame) -> pd.DataFrame:
        # Select `accounts_receivable`, `inventory`, `accounts_payable`, `current_liabilities`, `fixed_assets`, and `current_assets`
        return balance_sheet[['accounts_receivable', 'inventory', 'accounts_payable', 'current_liabilities', 'fixed_assets', 'current_assets']]

    @staticmethod
    def select_cash_flow_statement(cash_flow_statement: pd.DataFrame) -> pd.DataFrame:
        # Select `net_cash_flow` for validation purposes.
        return cash_flow_statement[['net_cash_flow']]
    
    def cogs_ratio(self, std_multiplier: float = 1.5) -> pd.DataFrame:
        # COGS / Revenues
        cogs_ratio = self.income_statements['cogs'] / self.income_statements['revenues']
        
        # Calculate mean and std
        mean = cogs_ratio.mean()
        std = cogs_ratio.std()
        
        # Drop values outside 1.5 std
        cogs_ratio = cogs_ratio[abs(cogs_ratio - mean) <= std * std_multiplier].mean()
        return cogs_ratio

    def operating_expenses_ratio(self, std_multiplier: float = 1.5) -> pd.DataFrame:
        # Operating Expenses / Revenues
        operating_expenses_ratio = self.income_statements['operating_expenses'] / self.income_statements['revenues']
        
        # Calculate mean and std
        mean = operating_expenses_ratio.mean()
        std = operating_expenses_ratio.std()
        
        # Drop values outside 1.5 std
        operating_expenses_ratio = operating_expenses_ratio[abs(operating_expenses_ratio - mean) <= std * std_multiplier].mean()
        return operating_expenses_ratio

    def change_in_net_working_capital(self, std_multiplier: float = 1.5) -> pd.DataFrame:
        nwc = self.balance_sheets['current_assets'] - self.balance_sheets['current_liabilities']
        nwc_delta = nwc.diff().dropna()
        
        # Calculate mean and std
        mean = nwc_delta.mean()
        std = nwc_delta.std()
        
        # Drop values outside 1.5 std
        nwc_delta = nwc_delta[abs(nwc_delta - mean) <= std * std_multiplier].mean()
        return nwc_delta

    def calculate_free_cash_flow(self) -> pd.DataFrame:
        # Calculate EBIT (Earning Before Interest and Taxes)
        # If available Tax rate + Depreciation and amortization
        ebit = self.income_statements['gross_profit'] - self.income_statements['operating_expenses']

        # Approximate CAPEX
        # CapEx is the outflow of cash spent on fixed assets
        capex = -self.balance_sheets['fixed_assets'].diff().dropna()
        
        # Net Working Capital Changes
        nwc_change = self.change_in_net_working_capital()
        
        # Free Cash Flow Calculation
        fcf = ebit + capex - nwc_change
        
        # Prepare Output
        fcf_df = pd.DataFrame({
            "EBIT": ebit,
            "EBIT_after_Tax": ebit,
            "CapEx": capex,
            "Change_in_NWC": nwc_change,
            "Free_Cash_Flow": fcf
        })
        return fcf_df
