from allauth.account.forms import SignupForm

class CustomUserCreationForm(SignupForm):
    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        return user