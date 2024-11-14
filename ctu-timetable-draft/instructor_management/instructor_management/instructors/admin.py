from django import forms
from django.contrib import admin
from .models import Instructor
from django.forms.widgets import TimeInput
import json
from django.core.exceptions import ValidationError


class TimePickerWidget(TimeInput):
    input_type = 'time'


class InstructorForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        help_text='Upload a profile picture.',
        widget=forms.ClearableFileInput
    )

    qualified_course = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter courses separated by commas'}),
        help_text='Enter courses separated by commas (e.g., "AST, FOLA, PROGRAMMING").',
    )

    college_id = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter College ID',
            'style': 'width: 300px;'  # Adjust size as needed
        }),
        help_text='Enter the College ID (number only 1, 2, 3 or 4).',
    )

    availability_days = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter days separated by commas',
            'style': 'width: 300px;'  # Adjust size as needed
        }),
        help_text='Enter days separated by commas.',
    )

    availability_times = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter times separated by commas',
            'style': 'width: 300px;'  # Adjust size as needed
        }),
        help_text='Enter times separated by commas (e.g., "8, 9, 12, 2").',
    )

    class Meta:
        model = Instructor
        fields = '__all__'

    def clean_college_id(self):
        college_id_str = self.cleaned_data.get('college_id', '')
        
        # Validate that the input is a digit
        if not college_id_str.isdigit():
            raise ValidationError("College ID must be a number.")

        return college_id_str  # Return as a string for display

    def clean_availability_days(self):
        availability_days_str = self.cleaned_data.get('availability_days', '')
        availability_days_list = [day.strip().upper() for day in availability_days_str.split(',')]

        # Validate against accepted days
        valid_days = {"M", "T", "W", "TH", "F", "SAT", "SUN"}
        for day in availability_days_list:
            if day not in valid_days:
                raise ValidationError(f"Invalid day: {day}. Use only: {', '.join(valid_days)}")

        return availability_days_list  # return as a list not a string

    def clean_availability_times(self):
        availability_times_str = self.cleaned_data.get('availability_times', '')
        availability_times_list = [time.strip() for time in availability_times_str.split(',')]
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

        qualified_courses = cleaned_data.get('qualified_course', '')
        if qualified_courses:
            cleaned_data['qualified_course'] = [course.strip() for course in qualified_courses.split(',')]

        return cleaned_data


class InstructorAdmin(admin.ModelAdmin):
    form = InstructorForm

    list_display = ('first_name', 'middle_initial', 'last_name','display_college_id', 'display_availability_days', 'display_availability_times', 'display_employment_type')
    search_fields = ('first_name', 'middle_initial', 'last_name', 'employment_type')
    list_filter = ('employment_type',)
    
    
        # Method to display college_id
    def display_college_id(self, obj):
        return obj.college_id  # Access the college_id directly from the model
    display_college_id.short_description = 'College ID'  # Set the column title

    def display_availability_days(self, obj):
        # Assuming availability_days is stored as a string
        if obj.availability_days:
            return obj.availability_days  # Return the string as is
        return ''

    def display_availability_times(self, obj):
        # Check if availability_times exists and is not empty
        if obj.availability_times:
            try:
                # If it's a string that looks like JSON, try to load it
                availability_times = json.loads(obj.availability_times)
                if isinstance(availability_times, list):
                    return ', '.join(availability_times)  # Join list items with a comma
                return obj.availability_times  # Return it as-is if it's not a list
            except (json.JSONDecodeError, TypeError):
                # If it fails to decode, return it as-is
                return obj.availability_times  # Fallback to the original string
        return ''

    def display_employment_type(self, obj):
        return obj.get_employment_type_display()  # Ensure 'employment_type' is a valid choice field in your model

    display_availability_days.short_description = 'Availability Days'
    display_availability_times.short_description = 'Availability Times'
    display_employment_type.short_description = 'Employment Type'

    fieldsets = (
        (None, {
            'fields': ('first_name', 'middle_initial', 'last_name', 'employment_type', 'qualified_course', 'college_id', 'availability_days', 'availability_times')  # Added 'college_id'
        }),
    )

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/jquery-timepicker/1.13.18/jquery.timepicker.min.css',
            )
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/jquery-timepicker/1.13.18/jquery.timepicker.min.js',
        )


admin.site.site_header = "CTU Dumanug Extension Campus"
admin.site.site_title = "CTU-DEx"
admin.site.index_title = "Welcome to My Admin Panel"

# Register the updated admin class
admin.site.register(Instructor, InstructorAdmin)
