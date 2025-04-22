class PricingRule:
    def __init__(self, item_code, rule_type, price, quantity=None, discounted_price=None):
        self.item_code = item_code
        self.type = rule_type
        self.price = price
        self.quantity = quantity
        self.discounted_price = discounted_price

    def apply_rule(self, quantity):
        pricing_functions = {
            'individual': self._apply_individual,
            'discount': self._apply_discount
        }
        return pricing_functions[self.type](quantity)

    def _apply_individual(self, quantity):
        return quantity * self.price

    def _apply_discount(self, quantity):
        discounted_price = 0
        while quantity >= self.quantity:
            discounted_price += self.discounted_price
            quantity -= self.quantity
        discounted_price += quantity * self.price
        return discounted_price
    
    def __str__(self):
        if self.type == 'individual':
            return f"Type: {self.type}, Price: {self.price}"
        elif self.type == 'discount':
            return f"Type: {self.type}, Price: {self.price}, Quantity: {self.quantity}, Discounted Price: {self.discounted_price}"

class Checkout:
    def __init__(self, pricing_rules):
        self.pricing_rules = pricing_rules
        self.cart = {}

    def scan_item(self, item_code):
        if item_code == "":
            return 0   
        self.cart[item_code] = self.cart.get(item_code, 0) + 1

    def calculate_total(self):
        total_price = 0
        if not self.cart:  # Check if cart is empty
            return total_price  # Return 0 if cart is empty

        for item_code, quantity in self.cart.items():
            pricing_rule = self.pricing_rules.get(item_code)
            if pricing_rule:
                try:
                    total_price += pricing_rule.apply_rule(quantity)
                except TypeError:
                    print(f"Error: Invalid pricing rule for item {item_code}.")
            else:
                print(f"Warning: No pricing rule found for item {item_code}.")
        return total_price