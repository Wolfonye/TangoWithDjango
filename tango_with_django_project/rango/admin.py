from django.contrib import admin
from rango.models import Category, Page, UserProfile

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

#die Beschreibung fuer diese prepopulated fields Sache gefaellt mir noch nicht
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)} #ein Feld der Superklasse ModelAdmin, erhaelt ein Dictionary das Feldnamen auf
                                             #diejenigen Feldnamen mappt von denen aus es ersteres befuellen soll
                                             #Wir benutzen das fuer Category, dort gibt es ein Feld 'name'
                                             #Das slug ist ein weiteres Feld in Category. Wenn wir auf unserer Admin-Page
                                             #ne neue Category anlegen und da im Namen eintippen erscheint dann direkt
                                             #die slugifiete Version im entsprechenden Feld. Ich gehe davon aus, dass
                                             #das dadurch kommt, dass wir das als SlugField definiert haben. Das
                                             #save wird da naemlich glaube ich noch gar nicht ausgefuehrt.

# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile) #Registrierung damit wir UserProfile im 
                                 #admin Webinterface drin haben.
