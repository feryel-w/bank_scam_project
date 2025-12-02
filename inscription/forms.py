from django import forms

class BankInscriptionForm(forms.Form):

    FULL_COUNTRIES = [
        ("Tunisia", "Tunisia"),
        ("France", "France"),
        ("Germany", "Germany"),
        ("Syria", "Syria"),
        ("Spain", "Spain"),
        ("Italy", "Italy"),
        ("Canada", "Canada"),
        ("USA", "USA"),
        ("Turkey", "Turkey"),
        ("Morocco", "Morocco"),
        ("Algeria", "Algeria"),
        ("KSA", "Saudi Arabia"),
        ("UAE", "UAE (Dubai / Abu Dhabi)"),
        ("UK", "United Kingdom"),
        ("Japan", "Japan"),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    INCOME_SOURCES = [
        ("salary", "Salary"),
        ("business", "Business"),
        ("freelance", "Freelance"),
        ("investments", "Investments"),
        ("family_support", "Family Support"),
    ]

    ACCOUNT_PURPOSES = [
        ("salary_deposit", "Salary Deposit"),
        ("investment", "Investment"),
        ("business", "Business"),
        ("transfers_family", "Transfers to Family"),
        ("savings", "Savings"),
    ]

    ACCOUNT_TYPES = [
        ("current", "Current Account"),
        ("savings", "Savings Account"),
        ("premium", "Premium Account"),
        ("youth", "Youth Account"),
    ]

    ID_TYPES = [
        ("passport", "Passport"),
        ("national_id", "National ID"),
        ("residence_permit", "Residence Permit"),
    ]

    # ---------- PERSONAL ----------
    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Full Name',
            'class': 'input-field',
        })
    )

    age = forms.IntegerField(
        required=True,
        min_value=18,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Age',
            'class': 'input-field',
        })
    )

    gender = forms.ChoiceField(
        required=True,
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'input-field'})
    )

    nationality = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nationality',
            'class': 'input-field'
        })
    )

    residence_country = forms.ChoiceField(
        required=True,
        choices=FULL_COUNTRIES,
        widget=forms.Select(attrs={'class': 'input-field'})
    )

    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number',
            'class': 'input-field',
            'pattern': r'^[0-9+\-\s]{6,15}$',
            'title': 'Enter a valid phone number (numbers only)',
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Address',
            'class': 'input-field'
        })
    )

    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Full Address',
            'class': 'input-field textarea-field',
            'rows': 3
        })
    )

    # ---------- FINANCIAL ----------
    profession = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Profession',
            'class': 'input-field'
        })
    )

    revenue = forms.IntegerField(
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Monthly Revenue',
            'class': 'input-field'
        })
    )

    source_of_income = forms.ChoiceField(
        required=True,
        choices=INCOME_SOURCES,
        widget=forms.Select(attrs={'class': 'input-field'})
    )

    account_purpose = forms.ChoiceField(
        required=True,
        choices=ACCOUNT_PURPOSES,
        widget=forms.Select(attrs={'class': 'input-field'})
    )

    account_type = forms.ChoiceField(
        required=True,
        choices=ACCOUNT_TYPES,
        widget=forms.Select(attrs={'class': 'input-field'})
    )

    id_type = forms.ChoiceField(
        required=True,
        choices=ID_TYPES,
        widget=forms.Select(attrs={'class': 'input-field'})
    )

    id_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'ID Number',
            'class': 'input-field'
        })
    )
