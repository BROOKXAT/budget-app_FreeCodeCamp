class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def __str__(self) :
        lines = [f"{self.category.center(30, '*')}"]
        for item in self.ledger:
            description = item["description"][:23].ljust(23)
            amount = "{:.2f}".format(item["amount"]).rjust(7)
            lines.append(f"{description}{amount}")
        total = "{:.2f}".format(self.get_balance())
        lines.append(f"Total: {total}")
        return "\n".join(lines)
        

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount): return False
        self.ledger.append({"amount": -amount, "description": description})
        return True

    def get_balance(self):
        balance = 0
        for i in self.ledger:
            balance += i["amount"]
        return balance

    def transfer(self, amount, category):
        if self.withdraw(amount,"Transfer to " + category.category):

            category.deposit(amount, "Transfer from " + self.category)
            return True
        else:
            return False


def create_spend_chart(categories):
    chart = "Percentage spent by category\n"
    
    total_withdrawals = sum(sum(i["amount"] for i in category.ledger if i["amount"] < 0 ) for category in categories)
    
    percentages = [((sum(i["amount"] for i in category.ledger if i["amount"] < 0 )) / total_withdrawals) * 100 for category in categories]
    
    for percentage in range(100, -10, -10):
        chart += f"{percentage:3d}| {' '.join('o ' if p >= percentage else '  '         for p in percentages)} \n"
    chart += "    ----------\n"
    max_label_length = max(len(category.category) for category in categories)
    for i in range(max_label_length):
        chart += "     "
        for category in categories:
            if i < len(category.category):
                chart += f"{category.category[i]}  "
            else:
                chart += "   "
        chart += "\n"
    chart = chart[:-1]
    return chart
    

