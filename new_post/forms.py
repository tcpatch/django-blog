from django import forms


class NewPost(forms.Form):
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.ChoiceField(label='Author', widget=forms.Select(attrs={'class': 'form-control'}),
                             choices=[('authUser1', 'authUser1'), ('authUser2', 'authUser2'), ('authUser3', 'authUser3')])
    content = forms.CharField(strip=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'Public'), ('1', 'Private')], initial='1')
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    video = forms.FileField(widget=forms.ClearableFileInput(), required=False)
    # https://stackoverflow.com/questions/56057223/video-upload-and-display-on-a-django-website
