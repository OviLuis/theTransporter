from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'thetransporter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # API
    url(r'^api/', include('orders.urls', namespace="Orders_API", app_name="Orders_API")),
    url(r'^api/', include('drivers.urls', namespace="Drivers_API", app_name="Drivers_API")),
]
