from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from django.contrib import admin, auth

urlpatterns = [
    url(r'^mileage/', include('mileage.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth.views.login,
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', auth.views.logout,
        {'template_name': 'accounts/logged_out.html'}),
]
