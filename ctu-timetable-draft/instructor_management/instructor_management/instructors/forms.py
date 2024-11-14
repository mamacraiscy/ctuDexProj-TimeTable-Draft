from django import forms
from .models import Instructor
from django.core.exceptions import ValidationError

class InstructorForm(forms.ModelForm):
    # Add custom fields if needed (e.g., to adjust the input size or add placeholders)
    availability_days = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter days separated by commas (e.g., M, T, W, TH, F, SAT, SUN)',
            'style': 'width: 300px;'  # Adjust size as needed
        }),
        help_text='Enter days separated by commas (e.g., M, T, W, TH, F, SAT, SUN).'
    )

    availability_times = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter times separated by commas (e.g., 7, 8, 9)',
            'style': 'width: 300px;'  # Adjust size as needed
        }),
        help_text='Enter times separated by commas (e.g., 7, 8, 9).'
    )

    class Meta:
        model = Instructor
        fields = '__all__'  # Include all fields in the form

    def clean_availability_days(self):
        availability_days_str = self.cleaned_data.get('availability_days', '')

        # Split by commas and strip any extra spaces
        availability_days_list = [day.strip().upper() for day in availability_days_str.split(',')]

        # Validate against accepted days
        valid_days = {"M", "T", "W", "TH", "F", "SAT", "SUN"}
        for day in availability_days_list:
            if day not in valid_days:
                raise ValidationError(f"Invalid day: {day}. Use only: {', '.join(valid_days)}")

        return availability_days_list  # Return as a list

    def clean_availability_times(self):
        availability_times_str = self.cleaned_data.get('availability_times', '')

        # Split by commas and strip any extra spaces
        availability_times_list = [time.strip() for time in availability_times_str.split(',')]

        # Validate that all times are numeric (we assume they're integers representing hours)
        for time in availability_times_list:
            if not time.isdigit():
                raise ValidationError(f"Invalid time: {time}. Use only numbers.")

        return availability_times_list  # Return as a list

    def clean(self):
        cleaned_data = super().clean()

        # Validate required fields
        if not cleaned_data.get('first_name'):
            self.add_error('first_name', 'This field should not be empty.')
        if not cleaned_data.get('last_name'):
            self.add_error('last_name', 'This field should not be empty.')
        if not cleaned_data.get('employment_type'):
            self.add_error('employment_type', 'This field should not be empty.')

        return cleaned_data


class InstructorSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)

    def clean_query(self):
        query = self.cleaned_data.get('query')
        if not query:
            raise forms.ValidationError("This field cannot be empty.")
        return query
