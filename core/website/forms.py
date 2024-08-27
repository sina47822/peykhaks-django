from django import forms
from .models import Comment
# from .models import Rating


# class RatingForm(forms.ModelForm):
#     stars = forms.IntegerField(
#         label='امتیاز شما به محتوا',
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
#         min_value=1,
#         max_value=5,
#     )

#     class Meta:
#         model = Rating
#         fields = ['stars']


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea,required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

class SearchForm(forms.Form):
    query = forms.CharField()