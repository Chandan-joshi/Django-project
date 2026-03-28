from django import forms
from .models import Comment
class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=25)
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(widget=forms.Textarea)
class CommentForm(forms.Form):
    class Meta:
        model=Comment
        fields=['name','email','body']