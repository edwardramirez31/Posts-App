from django import forms
from .models import Comment
from emoji_picker.widgets import EmojiPickerTextareaAdmin

class CommentForm(forms.ModelForm):
    text = forms.CharField()
    class Meta:
        model = Comment
        fields = ['text']
