from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from swp.views import *
from swp.api import default_router as v1

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
    path('monitor/', include(([
        path('', react, name='list'),
        path('add/', react, name='add'),
        path('<int:pk>/', react, name='detail'),
        path('<int:pk>/edit/', react, name='edit'),
        path('<int:pk>/edit/query/', react, name='edit-query'),
        path('<int:pk>/publications/', include([
            path('', react, name='publications'),
            path('download/', MonitorRISDownloadView.as_view(), name='download'),
            path('new/', react, name='new-publications'),
            path('new/download/', MonitorRISDownloadView.as_view(exclude_sent=True), name='download-new'),
        ])),
    ], 'monitor'))),

    path('thinktank/', include(([
        path('', react, name='list'),
        path('add/', react, name='add'),
        path('<int:pk>/', react, name='detail'),
        path('<int:pk>/edit/', react, name='edit'),
        path('<int:pk>/download/', ThinkTankRISDownloadView.as_view(), name='download'),
        path('<int:thinktank_pk>/publications/', react, name='publications'),
        path('<int:thinktank_pk>/scraper/', include(([
            path('add/', react, name='add'),
            path('<int:pk>/', react, name='edit'),
        ], 'scraper'))),
    ], 'thinktank'))),

    path('search/', include([
        path('', react, name='search'),
        path('publication-list/', include(([
            path('', react, name='list'),
            path('<int:pk>/', react, name='detail'),
        ], 'publication-list'))),
    ])),

    # snippets
    path('snippet/<path:identifier>/', SnippetView.as_view(), name='snippet'),
]

if settings.DEBUG:
    urlpatterns += [
        path('mail/preview/<slug:identifier>/', MailPreView.as_view(), name='mail-preview'),
    ]

if settings.DEBUG_TOOLBAR:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),
    ]
