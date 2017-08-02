from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

def index(request):
#legacy, das bauen wir jetzt um    return HttpResponse("Ich bin Rango und gruesse sie, sie speckiges Schwabbelschweinchen!"+ '<a href="/rango/about">Klick mich</a>')
    #Construct a dictinary to pass to the template engine as its context
    #Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcur function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    # Was macht das: insbesondere als zweites argument nen template namen entgegennehmen
    # , als drittes nen context und gibt vor allen dingen nen HttpResponse zurueck
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return HttpResponse("Ich bin die ziemlich nutzlose About-Page." + '<a href="/rango/"> Und zurueck</a>')
