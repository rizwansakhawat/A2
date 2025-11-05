from django import forms
from .models import Bank, Branch

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'description', 'inst_num', 'swift_code']

    def clean(self):
        cleaned_data = super().clean()
        for field in ['name', 'description', 'inst_num', 'swift_code']:
            value = cleaned_data.get(field, '')
            if value == '':
                self.add_error(field, 'This field is required')
            elif len(value) > 100:
                self.add_error(field, f'Ensure this value has at most 200 characters (it has {len(value)})')
        return cleaned_data


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'transit_num', 'address', 'email', 'capacity']

    def clean(self):
        cleaned_data = super().clean()
        for field in ['name', 'transit_num', 'address']:
            value = cleaned_data.get(field, '')
            if value == '':
                self.add_error(field, 'This field is required')
            elif len(value) > 100:
                self.add_error(field, f'Ensure this value has at most 200 characters (it has {len(value)})')

        email = cleaned_data.get('email', '')
        if email and '@' not in email:
            self.add_error('email', 'Enter a valid email address')

        capacity = cleaned_data.get('capacity')
        if capacity is not None and capacity < 0:
            self.add_error('capacity', 'Ensure this value is greater than or equal to 0')

        return cleaned_data
