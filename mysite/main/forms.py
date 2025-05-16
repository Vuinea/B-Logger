from django import forms
from .models import Post
class PostForm(forms.ModelForm):
    # title = forms.CharField(max_length=200, label='Title')
    # content = forms.CharField(widget=forms.Textarea, label='Content')
    # categories = forms.ModelMultipleChoiceField(queryset=None, label='Categories')

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['categories'].queryset = Category.objects.all()

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title is required.")
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Content is required.")
        return content
    
class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=200, label='Search')
    
    def clean_search_query(self):
        search_query = self.cleaned_data.get('search_query')
        if not search_query:
            raise forms.ValidationError("Search query is required.")
        return search_query


class RatingForm(forms.Form):
    rating = forms.FloatField(label='Rating', min_value=1, max_value=5)
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
    



