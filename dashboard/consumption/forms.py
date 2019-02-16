from django import forms

class monthChoice(forms.Form):
    MONTH_CHOICES = (
        ('2016 12', '2016-12'),
        ('2016 11', '2016-11'),
        ('2016 10', '2016-10'),
        ('2016 9', '2016-9'),
        ('2016 8', '2016-8'),
        ('2016 7', '2016-7'),
    )
    month_choice = forms.ChoiceField(label='month', choices=MONTH_CHOICES, initial='2016 12')

class areaChoice(forms.Form):
    AREA_CHOICES = (
        ('all', 'all'),
        ('a1', 'a1'),
        ('a2', 'a2'),
    )
    area_choice = forms.ChoiceField(label='area', choices=AREA_CHOICES, initial='all')

class tariffChoice(forms.Form):
    TARIFF_CHOICES = (
        ('all', 'all'),
        ('t1', 't1'),
        ('t2', 't2'),
        ('t3', 't3'),
    )
    tariff_choice = forms.ChoiceField(label='tariff', choices=TARIFF_CHOICES, initial='all')