from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Keep default behavior
        return super().is_open_for_signup(request)

    def clean_email(self, email):
        # Optionally customize email cleaning here
        return super().clean_email(email)

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # Override to skip email confirmation for social logins
        if signup and emailconfirmation.email_address.user.socialaccount_set.exists():
            # Social login - skip sending confirmation email
            return
        super().send_confirmation_mail(request, emailconfirmation, signup)

    def is_email_verified(self, request, user):
        if hasattr(user, "socialaccount_set") and user.socialaccount_set.exists():
            return True
        return super().is_email_verified(request, user)
