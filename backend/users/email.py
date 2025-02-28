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
        context["order"] = self.context.get("order")
        return context
