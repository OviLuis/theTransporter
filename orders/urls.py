from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from .api_views import *

orders_list = OrderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    url(r'^v1/orders/$', orders_list, name='orders_list'),
    # url(r'^v1/orders/(?P<year>-?\d+)/$', company_detail, name='company_detail'),
    # url(r'^v1/companies/invited-users/(?P<invited_user_id>-?\d+)/$', companies_by_invited_user, name='companies_by_invited_user'),
    # url(r'^v1/companies/customers/(?P<user_id>-?\d+)/$', customer_companies_by_user, name='customer_companies_by_user'),

]

urlpatterns = format_suffix_patterns(urlpatterns)