from django import forms
from .models import Comment, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What are your thoughts?', 'class': 'rounded-pill decoration'}))

    class Meta:
        model = Comment
        fields = ['text']

class PostForm(forms.ModelForm):
    max_upload_limit = 4 * 1024 * 1024
    max_upload_limit_text = "4 MB"

    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

    def clean(self):
        cleaned_data = super().clean()
        picture = cleaned_data.get("image")
        # if picture is None:
            # return
        if len(picture) > self.max_upload_limit:
            self.add_error(
                "image", "The picture size must be less than 2.0 MB")
