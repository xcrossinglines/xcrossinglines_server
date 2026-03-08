from django import forms


class DecimalWithSignInput(forms.TextInput):
    input_type = "text"
    template_name = "templates/decimal_with_sign.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Force numeric keyboard with minus sign
        context["widget"]["attrs"]["inputmode"] = "decimal"
        # Optional: pattern for client-side validation (accepts negative decimals)
        context["widget"]["attrs"]["pattern"] = "-?\\d+(\\.\\d+)?"
        context["widget"]["attrs"]["title"] = "Enter a number (negative allowed)"
        return context
