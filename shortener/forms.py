from django import forms
from .models import ShortenedURL

class URLForm(forms.ModelForm):
    custom_code = forms.CharField(max_length=15, required=False, label="Custom Alias (Optional)")
    
    class Meta:
        model = ShortenedURL
        fields = ['long_url', 'expires_at']
        widgets = {
            'long_url': forms.URLInput(attrs={'placeholder': 'https://example.com', 'class': 'form-control'}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean_custom_code(self):
        custom_code = self.cleaned_data.get('custom_code')
        if custom_code:
            if ShortenedURL.objects.filter(short_code=custom_code).exists():
                raise forms.ValidationError("This custom alias is already taken.")
        return custom_code
