# To handle dates, we need the datetime and relativedelta modules.
# You might need to install python-dateutil: pip install python-dateutil
from datetime import date
from dateutil.relativedelta import relativedelta

class LongTermDeferredExpense:
    """
    A class to represent and manage a long-term deferred expense.
    It handles the initial setup and periodic amortization.
    """
    def __init__(self, name: str, total_cost: float, amortization_period_months: int, start_date: date):
        """
        Initializes the deferred expense asset.
        
        Args:
            name (str): The name of the expense (e.g., "Office Renovation").
            total_cost (float): The total initial cost of the expense.
            amortization_period_months (int): The total number of months over which to amortize.
            start_date (date): The date when the amortization begins.
        """
        if amortization_period_months <= 0:
            raise ValueError("Amortization period must be greater than zero.")
            
        self.name = name
        self.total_cost = total_cost
        self.amortization_period_months = amortization_period_months
        self.start_date = start_date
        
        # This is the current value of the asset on the balance sheet.
        # It starts with the total cost.
        self.book_value = total_cost
        
        # Calculate the fixed monthly amortization amount.
        # We round to 2 decimal places for currency.
        self.monthly_amortization_amount = round(total_cost / amortization_period_months, 2)
        
        # A list to keep a record of all amortization transactions.
        self.amortization_history = []
        
        print(f"--- 初始确认：新增长期待摊费用 ---")
        print(f"费用名称: {self.name}")
        print(f"总成本: {self.total_cost:,.2f} 元")
        print(f"摊销期: {self.amortization_period_months} 个月")
        print(f"每月摊销额: {self.monthly_amortization_amount:,.2f} 元")
        print("会计分录 (Journal Entry):")
        print(f"  借 (Debit): 长期待摊费用 - {self.name}  {self.total_cost:,.2f}")
        print(f"  贷 (Credit): 银行存款  {self.total_cost:,.2f}")
        print("-" * 40)

    def amortize_for_period(self, amortization_date: date):
        """
        Performs the amortization for a single period (typically a month).
        This simulates the monthly accounting entry.
        
        Args:
            amortization_date (date): The date of the current amortization period.
        """
        if self.book_value <= 0:
            print(f"({amortization_date.strftime('%Y-%m-%d')}) {self.name} 已全额摊销完毕。")
            return
            
        # Determine the amount to amortize.
        # This handles the final month, which might have a slightly different amount due to rounding.
        amount_to_amortize = min(self.book_value, self.monthly_amortization_amount)
        
        # Decrease the book value of the asset.
        self.book_value -= amount_to_amortize
        
        # Record the transaction.
        transaction = {
            "date": amortization_date,
            "amortized_amount": amount_to_amortize,
            "remaining_book_value": self.book_value
        }
        self.amortization_history.append(transaction)
        
        # Print the journal entry for the current period's amortization.
        print(f"--- {amortization_date.strftime('%Y年%m月')} 摊销 ---")
        print("会计分录 (Journal Entry):")
        print(f"  借 (Debit): 管理费用  {amount_to_amortize:,.2f}")
        print(f"  贷 (Credit): 长期待摊费用 - {self.name}  {amount_to_amortize:,.2f}")
        self.get_status()

    def get_status(self):
        """
        Prints the current status of the deferred expense.
        """
        print(f"当前剩余账面价值 (Book Value): {self.book_value:,.2f} 元")
        print("-" * 40)

# main function is the entry point of the program
def main():
    print("Hello from myproject!")
    # Process of making correct accounting treatment on long-term pre-paid expenses
    # --- 模拟实验开始 (Simulation Starts Here) ---

    # 1. 定义实验参数
    # Define parameters for the experiment.
    expense_name = "办公室装修费"
    cost = 120000.00
    period_in_years = 5
    period_in_months = period_in_years * 12
    simulation_start_date = date(2025, 1, 1)

    # 2. 初始确认：创建长期待摊费用资产
    # Initial Recognition: Create the long-term deferred expense asset.
    renovation_expense = LongTermDeferredExpense(
        name=expense_name,
        total_cost=cost,
        amortization_period_months=period_in_months,
        start_date=simulation_start_date
    )

    # 3. 模拟随时间推移的每月摊销过程
    # Simulation: Loop through time to perform monthly amortization.
    # We will simulate for the entire period + 2 extra months to show it's fully amortized.
    print("\n>>> 开始模拟每月摊销过程...\n")
    current_date = simulation_start_date
    for month_num in range(period_in_months + 2):
        # For the first month, the date is the start date. For subsequent months, add one month.
        if month_num > 0:
            current_date += relativedelta(months=1)
        
        # Perform amortization for the current simulated month.
        renovation_expense.amortize_for_period(current_date)

    # 4. 最终状态
    # Final status check.
    print("\n>>> 模拟结束，查看最终摊销历史记录。")
    total_amortized = sum(t['amortized_amount'] for t in renovation_expense.amortization_history)
    print(f"总计摊销金额: {total_amortized:,.2f} 元")
    print(f"最终剩余账面价值: {renovation_expense.book_value:,.2f} 元")


if __name__ == "__main__":
    main()
