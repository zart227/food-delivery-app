from djoser import email

class ActivationEmail(email.ActivationEmail):
    template_name = "email/activation_email.html"

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "email/password_reset_email.html"

class PasswordChangedEmail(email.PasswordChangedConfirmationEmail):
    template_name = "email/password_changed_email.html"
