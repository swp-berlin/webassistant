from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from swp.views import *
from swp.api import v1


react = SWPView.as_view()


urlpatterns = [
    path('', react, name='index'),
    path('admin/', admin.site.urls),

    # api
    path('api/', v1.urls),

    # app
    path('scraper/', include(([
        path('<int:pk>/', react, name='detail'),
    ], 'scraper'))),
]

if settings.DEBUG_TOOLBAR:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),
    ]
