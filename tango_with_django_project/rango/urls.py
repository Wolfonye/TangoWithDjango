from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/', views.about, name='about'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),) #das?P captured den Teil in den runden Klammern, der dann mittels des Namens in <...> referenziert werden kann. Das + heisst einmal oder mehrfach das vorangegangene, als das in eckigen Klammern. Die repraesentieren ein ODER, also hier ein Wort (\w) oder einen Strich, sprich irgenwas der Form wort-wort-wort-... so wie wir das von was slugifytem erwarten wuerden.
