
from decimal import *


class Category:
    """Instantiate objects based on budget categories."""
    
    def __init__(self, category:str):
        """Initialize the class.

        Args:
            category (_str): name of budget category
        """
        self.name = category
        self.amount = 0
        self.ledger = list()
        
    def __repr__(self):
        """Print formatting for class."""
        ledger_print = ""
        for item in self.ledger:
            amount = item['amount']
            description = item['description'][0:23]
            
            ledger_entry = f"{description:<23}{amount:>-7.2f}\n"
            ledger_print += ledger_entry
                
        total = f"Total: {self.amount}"
        r = f"{self.name:*^30}\n{ledger_print}{total}"
        return r
    
    def deposit(self, amount: int, description: str = ''):
        """Record deposits into category.

        Args:
            amount (int): amount deposited
            description (str, optional): Description. Defaults to ''.
        """
        self.amount += amount
        deposit_dict = {"amount": amount,"description": description}
        self.ledger.append(deposit_dict)

    def withdraw(self, amount: int, description: str = '') -> bool:
        """Record withdrawals from account.

        Args:
            amount (int): amount withdrawn
            description (str, optional): _description_. Defaults to ''.

        Returns (bool):
            True: withdrawal successful
            False: withdrawal failed
        """
        status = self.check_funds(amount)
        
        if amount >= 1000:
            return False
        
        elif status == True:
            self.amount -= amount
            withdraw_dict = {"amount": -amount, "description": description}
            self.ledger.append(withdraw_dict)
            return True
        
        else:
            return False   
    
    def get_balance(self):
        """Balance of budget category."""
        return self.amount
    
    def transfer(self, amount: int, category: object) -> bool:
        """Transfer from one budget category to another.

        Args:
            amount (int): amount transferred
            category (object): Receiving budget category

        Returns (bool):
            True: Transfer successful
            False: Transfer failed
        """
        status = self .check_funds(amount)
        if status == True:
            description = f"Transfer to {category.name}"
            self.withdraw(amount, description)
        
            description = f"Transfer from {self.name}"
            category.deposit(amount, description)
            return True
        else:
            return False
            quit()
    
    def check_funds(self, amount: int) -> bool:
        """Check whether current balance is greater than transaction amount.

        Args:
            amount (int): Transaction amount

        Returns (bool):
            True: Current balance is greater than transaction amount.
            False: Current balance is lesser than transaction amount.
        """
        if amount > self.amount:
            return False
        else:
            return True
    
def create_spend_chart(categories: list) -> str:
    """Bar chart for budget categories against percentage of deposits spent.

    Args:
        categories (list): list of budget categories.
        MAX categories = 4
    """
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")
