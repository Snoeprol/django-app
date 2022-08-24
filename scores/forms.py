from django import forms
from .models import Score

class EditUserForm(forms.ModelForm):
  class Meta:
    model = Score
    fields = ["date","score"]
    widgets = {
            'date': forms.TextInput(attrs={'placeholder': 'Date (YYYY-MM-DD)'}),
            'score': forms.TextInput(attrs={'placeholder': 'Score'}),
              }
class DateRange(forms.Form):
  # Date 1
  date1 = forms.DateField(label="Starting Date", widget=forms.SelectDateWidget(years=range(2000 ,2025)))
  date2 = forms.DateField(label="Ending Date", widget=forms.SelectDateWidget(years=range(2000,2025)))