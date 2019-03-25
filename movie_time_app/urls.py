from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<movie_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^update/(?P<movie_id>[0-9]+)/$', views.update, name='update'),
    url(r'index', views.index2, name='index'),
    url(r'loginSucess', views.loginSuccess, name='loginSucess'),
    url(r'dashboard', views.dashboard, name='dashboard'),
    url(r'^register/$',views.registerUser, name='register')

    # url(r'^form/$', views.form, name='form')
]