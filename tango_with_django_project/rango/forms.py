from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category-name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    #An inline Class to provide additional information on the form.
    class Meta:
        #Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',) #siehe weiter unten fuer erklaerung


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        #Provide an association between the ModelForm and a moel
        model = Page

        #What fields do we want to include in our form?
        #This way we dont need every field in the model present.
        #Some fields may allow NULL values, so we may not want to include them...
        #Here, we are hiding the foreign key.
        #We can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (leaving out what we don't want)
        #fields = ('title','url','views')
    #wir ueberschreiben hier die Methode clean. Diese wird aufgerufen, bevor form
    #-daten in eine neue Model-Instanz gespeichert werden.
    def clean(self):
        cleaned_data = self.cleaned_data #cleaned_data scheint ein Feld von ModelForm zu sein, zumindest in django 1.7
        url = cleaned_data.get('url')

        if url and not(url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
            cleaned_data['url'] = url
        
        return cleaned_data

#Es folgen die Klassen fuer die User und UserProfile-Forms
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
