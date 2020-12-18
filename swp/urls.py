from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from swp.views import *
from swp.api import v1


react = SWPView.as_view()


urlpatterns = [
    path('', react, name='index'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', include(([
        path('', PasswordResetView.as_view(), name='start'),
        path('<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='confirm'),
        path('complete/', PasswordResetCompleteView.as_view(), name='complete'),
        path('done/', PasswordResetDoneView.as_view(), name='done'),
    ], 'password-reset'))),
    path('admin/', admin.site.urls),

    # api
    path('api/', v1.urls),

    # app
    path('scraper/', include(([
        path('', react, name='list'),
        path('<int:pk>/', react, name='detail'),
    ], 'scraper'))),
]

if settings.DEBUG_TOOLBAR:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),
    ]
