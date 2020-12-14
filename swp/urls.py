from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from swp.views import *


urlpatterns = [
    path('', SWPView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG_TOOLBAR:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),
    ]
