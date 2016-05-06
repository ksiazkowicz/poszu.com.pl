from django.conf.urls import url
from views import pull

urlpatterns = [
    url(r'^pull', pull, name='gumtree_pull'),
]