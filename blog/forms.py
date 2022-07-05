from django import forms
from django.forms import Textarea
from blog.models import Post, Comment



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "text",
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'text',
        )
        widgets = {
            'text': Textarea(attrs={'rows': 5, 'cols': 48})
        }