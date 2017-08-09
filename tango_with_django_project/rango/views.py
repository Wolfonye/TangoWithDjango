from django.shortcuts import render

#Import needed models here
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
#------------------------------------

from django.http import HttpResponse

# Create your views here.

def index(request):
#legacy, das bauen wir jetzt um    return HttpResponse("Ich bin Rango und gruesse sie, sie speckiges Schwabbelschweinchen!"+ '<a href="/rango/about">Klick mich</a>')
    #Construct a dictinary to pass to the template engine as its context
    #Note the key boldmessage is the same as {{ boldmessage }} in the template!
#legacy aus frueherem schritt des tuts    context_dict = {'boldmessage': "I am bold font from the context"}
    

    # Datenbank nach liste aller Kategorien fragen, ordne sie nach likes
    # in absteigender Reihenfolge(signalisiert durch das -). Ziehe die ersten 5 bzw. alle, 
    # falls weniger als 5 da sein sollten.
    # Die resultierende Liste wird dem Kontext-Dictionary uebergeben, damit wir sie spaeter nutzen koennen 
    # , wenn wir die template-engine nutzen.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    #Wir fuegen noch bissl was hinzu, um uns die derzeitigen Top 5 der Seiten anzeigen zu lassen.
    context_dict['pages'] = Page.objects.order_by('-views')[:5]
    # Return a rendered response to send to the client.
    # We make use of the shortcur function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    # Was macht das: insbesondere als zweites argument nen template namen entgegennehmen
    # , als drittes nen context und gibt vor allen dingen nen HttpResponse zurueck
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'paragraph1': "Ich bin ein wunderbarer Paragraph ueber einem hervorragenden Zitat"}

    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)

#view fuer die category-form
def add_category(request):
    # A HTTP POST? , dies ist ein Kommentar, keine Frage :D Hier soll schatz ich gesagt werden: war der request ein http-POST? Wenn ja, dann mache dies ansonsten halt wat anderes; siehe unten ;)
    if request.method == 'POST':
        form = CategoryForm(request.POST) #POST ist ein Feld eines HttpRequest-Objektes. Wie von Django Request-Objekte erzeugt werden siehe Internet; genaueres ueber HttpRequest.POST ist auf doc.djangoproject.com zu entnehmen.

        # Have we been provided with a valid form?
        if form.is_valid():
            #Save the new category to the database
            form.save(commit=True)

            #Now call the index() view. The user will be shown the homepage.
            return index(request)
        else:
            #The supplied form contained errors-just print them to the terminal.
            print form.errors
    else:
        #If the request was not a POST, display the form to enter details.
        form = CategoryForm()
    
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form':form})
