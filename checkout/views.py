from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import CheckoutForm
from .checkout_engine import Checkout, PricingRule

class CheckoutView(FormView):
    template_name = "checkout/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("checkout")

    def form_valid(self, form):
        cart = form.cleaned_data.get("items","").upper()
        if not cart:
            return self.render_to_response(self.get_context_data(form=form, total=0, cart=""))

        pricing_rules = {
            'A': PricingRule('A', 'discount', 50, 3, 130),
            'B': PricingRule('B', 'discount', 30, 2, 45),
            'C': PricingRule('C', 'individual', 20),
            'D': PricingRule('D', 'individual', 15),
        }

        co = Checkout(pricing_rules)
        for item in cart:
            if item in pricing_rules:
                co.scan_item(item)

        total = co.calculate_total()
        return self.render_to_response(self.get_context_data(form=form, total=total, cart=cart))
