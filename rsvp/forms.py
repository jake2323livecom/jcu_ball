from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm

from .models import Reservation


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control mb-2','placeholder':'Username...'})
        self.fields['email'].widget.attrs.update({'class':'form-control mb-2','placeholder':'Email...'})
        self.fields['password1'].widget.attrs.update({'class':'form-control mb-2','placeholder':'Enter password...'})
        self.fields['password2'].widget.attrs.update({'class':'form-control mb-2','placeholder':'Re-enter password...'})

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control mb-2','placeholder':'Enter Username...'})
        self.fields['password'].widget.attrs.update({'class':'form-control mb-2','placeholder':'Enter Pasword...'})


class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class':'form-control mb-2','placeholder':'Old password...'})
        self.fields['new_password1'].widget.attrs.update({'class':'form-control mb-2','placeholder':'New password...'})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control mb-2','placeholder':'Confirm new password...'})

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control form-rounded", "cols": 1}
            ),
            "middle_initial": forms.TextInput(
                attrs={"class": "form-control form-rounded"}
            ),
            "last_name": forms.TextInput(attrs={"class": "form-control form-rounded"}),
            "total_attendees": forms.NumberInput(
                attrs={"class": "form-control form-rounded"}
            ),
            "chicken": forms.NumberInput(attrs={"class": "form-control form-rounded"}),
            "beef": forms.NumberInput(attrs={"class": "form-control form-rounded"}),
            "fish": forms.NumberInput(attrs={"class": "form-control form-rounded"}),
            "has_paid": forms.Select(attrs={"class": "form-control form-rounded"}),
            "comments": forms.Textarea(
                attrs={"cols": 10, "rows": 2, "class": "form-control form-rounded"}
            ),
        }
        labels = {
            "has_paid": _("Has made payment"),
            "chicken": _("Number of chicken orders:"),
            "beef": _("Number of beef orders"),
            "fish": _("Number of fish orders"),
        }
        help_texts = {
            "comments": _("Enter any food allergies or special considerations.")
        }

    # Make sure the number of entrees matches the number of attendees
    def clean(self):
        cleaned_data = super().clean()
        total_attendees = cleaned_data.get("total_attendees")
        chicken = cleaned_data.get("chicken")
        beef = cleaned_data.get("beef")
        fish = cleaned_data.get("fish")
        total_entrees = sum([chicken, beef, fish])

        if total_attendees != total_entrees:
            raise ValidationError(
                "The total number of entrees does not match the total number of attendees"
            )