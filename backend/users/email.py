from djoser import email

class ActivationEmail(email.ActivationEmail):
    template_name = "email/activation_email.html"

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "email/password_reset_email.html"

class PasswordChangedEmail(email.PasswordChangedConfirmationEmail):
    template_name = "email/password_changed_email.html"

class EmailResetEmail(email.ActivationEmail):
    template_name = "email/email_reset_email.html"

class WelcomeEmail(email.BaseEmailMessage):
    template_name = "email/welcome_email.html"

class OrderConfirmationEmail(email.BaseEmailMessage):
    template_name = "email/order_confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        # print(f"Context: {context}")
        context["order"] = self.context.get("order")
        context["site_name"] = self.context.get("site_name")
        context["domain"] = self.context.get("domain")
        context["protocol"] = self.context.get("protocol")
        context["delivery_address"] = self.context.get("delivery_address")
        context["order_status_display"] = self.context.get("order_status_display")
        # product_detail для каждого item, если есть
        if context["order"]:
            for item in context["order"].items.all():
                if hasattr(item, 'product_detail'):
                    item.product_detail = item.product_detail
        return context
