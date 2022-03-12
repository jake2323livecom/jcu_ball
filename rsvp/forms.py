from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation
from .widgets import HorizontalRadioSelect

class ReservationForm(forms.ModelForm):

    # This is the easiest way to edit widget attributes for every field in the form at once.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            if field != 'has_paid':
                self.fields[field].widget.attrs.update({'class':'form-control form-rounded'})

    class Meta:
        model = Reservation
        # The full_name field is not editable, therefore by default it will not be included in the form
        fields = '__all__'
        widgets = {
            'has_paid': HorizontalRadioSelect(),
        }

    # Make sure the number of entrees matches the number of attendees
    def clean(self):
        cleaned_data = super().clean()
        total_attendees = cleaned_data.get('total_attendees')
        chicken = cleaned_data.get('chicken')
        beef = cleaned_data.get('beef')
        fish = cleaned_data.get('fish')
        total_entrees = sum([chicken, beef, fish])


        if total_attendees != total_entrees:
            raise ValidationError(
                "The total number of entrees does not match the total number of attendees"
            )