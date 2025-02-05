from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={
        'class':'share-email__name',
        'required':'required',
        'maxlength':'25',
        'placeholder':'Your name',
    }))
    email = forms.EmailField(min_length=8, required=True, widget=forms.EmailInput(attrs={
        'class':'share-email__email',
        'required':'required',
        'minlength':'8',
        'placeholder':'YourEmail@example.com',
        'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'autocomplete': 'off',
        'spellcheck': 'false',
    }))
    to = forms.EmailField(min_length=8, required=True, widget=forms.EmailInput(attrs={
        'class':'share-email__email',
        'required':'required',
        'minlength':'8',
        'placeholder':'YourEmail@example.com',
        'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'autocomplete': 'off',
        'spellcheck': 'false',
    }))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class':'share-email__comments',
        'placeholder':'Your comments here...',
    }))

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]

class SearchForm(forms.Form):
    query = forms.CharField(
        label="Search for posts",  # Este es el texto del label (puedes personalizarlo aquí)
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Type your search term...'})
    )