from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

#Import needed models here------------------------------------------------------
from rango.models import Category
from rango.models import Page
#-------------------------------------------------------------------------------

#Import needed forms here-------------------------------------------------------
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
#-------------------------------------------------------------------------------

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
        context_dict['category_name_slug'] = category_name_slug
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

#Code fuer die Aufgabe aus Kapitel 8 hier fuegen wir die view zum Page hinzufuegen hinzu
def add_page(request, category_name_slug): 
    try:
        cat = Category.objects.get(slug=category_name_slug)
        #slug ist ein Feld von Category; wir ziehen die category, bei der der slug
        #gleich dem oben mitgegebenen category_name_slug ist; quasi ein select
    except Category.DoesNotExist: 
        cat = None
    #erstmal der Fall, dass der request ein POST war; das heisst, dass
    #es nicht darum ging die Seite zur Eingabe anzuzeigen, sondern
    #eine Eingabe bereits erfolgt ist und diese jetzt abgeschickt werden soll.
    if request.method == 'POST':
        print(request.POST)
        #wenn das also ein Post gewesen ist, dann kreiere ein PageForm Objekt,
        #welches von ModelForm erbt mit den gegebenen POST-Daten
        form = PageForm(request.POST)
        #wir checken, ob die eingegebenen Daten valide sind, wenn ja koennen wir
        #weiter damit arbeiten
        if form.is_valid():
            if cat:
                #das commit=false bewirkt, dass das generierte Datenbankobjekt
                #(das ist es was save macht; ein Datenbankobjekt generieren)
                #nicht sofort gespeichert wird in der DB; wir koennen es daher
                #noch customizen. Bedeutet allerdings, dass wir nachher
                #nochmal manuell save ausfuehren muessen.
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                #Wir redirecten auf die category-page, hier ist category die view
                #remember kleingeschrieben. Da wird also die funktion category
                #mit den entsprechenden Argumenten aufgerufen, was letztlich
                #wieder zu einem render(...) fuehrt. Ich sollte mich auch noch
                #in class based views einlesen.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        print("das war kein post")
        #wenn der request kein POST war, dann wuerden wir gerne eine Form
        #ohne irgendwelche Daten erzeugen; diese wird dann dem context_dict
        #als Argument mitgegeben, damit sie genutzt werden kann um die Seite
        #mit der leeren Form zu generieren (die ich jetzt noch nicht konfiguriert)
        #habe, was ich jetzt gleich machen werde.
        form = PageForm()

    context_dict = {'form':form, 'category':cat, 'category_name_slug': category_name_slug}
    
    return render(request, 'rango/add_page.html', context_dict)

#Code fuer die register View, in der sich User registrieren koennen.
#Besonderheit ist hier, dass wir User und UserProfile zusammenbringen muessen
#Wir brauchen ja eine feste Assoziation der richtigen Instanzen zueinander
def register(request):

    #A boolean value for telling the template whether the registration was successful.
    #Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    #If it is a HTTP POST, we are interested in processing form data (wie vorher)
    if request.method == 'POST':
        #Attempt to grab information from the raw form information.
        #Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            #Save the users's form data to the database.
            user = user_form.save()

            #Now we hash the password with the set_password method.
            #Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            #Now sort out the UserProfile instance.
            #Since we neet to set the user attribute ourselves, we set commit = False.
            #This delays sacing the model until we are ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            #Did the user provide a profile picture=
            #If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #Now we sace the UserProfile model instance
            profile.save()

            #Update our variable to tell the template registration was successful.
            registered = True

        #Invalid form(s) - mistakes or something else?
        # Print problems to the terminal.
        # They will also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template debending on the context.
    return render(request,
                  'rango/register.html',
                  {'user_form':user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        #Gather the username and password provided by the user.
        #This information is obtained from the login form
            #We use request.POST.get('<variable>') as opposed to request.POST['<variable>']
            #because the request.POST.get('<variable>') returns None, if the value
            #does not exist while request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Use Django's machinery to attempt to see if the username/password
        #combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # As inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, 
        # hence the blank dictionary object.
        return render(request, 'rango/login.html',{})
