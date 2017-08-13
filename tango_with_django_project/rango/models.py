from django.db import models
from django.contrib.auth.models import User #nutzen wir in UserProfile

# Wir importieren hier um unsere Url zu slugifyien (Leerzeichen durch Bindestriche ersetzen), siehe Tutorial Kapitel 7
from django.template.defaultfilters import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()
    #self ist immer erstes argument in soner methode in ner Klasse glaub ich
    #beim Aufruf wird das nciht angegeben. Quasi ein manuelles this
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
            #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self): #in Python 2, in Python 3 waere das __str__
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

#Hier folgt das Model, welches wir zur User-Authentication in Verbindung mit
#django.contrib.auth.User nutzen
class UserProfile(models.Model):
    #This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    #The additional attributes we wish to include
    website = models.URLField(blank=True)#blank=true->keine Angabe noetig
    picture = models.ImageField(upload_to='profile_images', blank=True)

    #Override the __unicode__() method to return out something meaningful
    # ZUR ERINNERUNG: in python3 waere das__str__() 
    def __unicode__(self):
        return self.user.username
