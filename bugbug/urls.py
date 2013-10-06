"""URL routing for project
"""
from django.conf.urls import patterns, url, include
from bugbug import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'homepage.views.homepage', name='home'),
    url(r'^teams/(\d+)', 'teams.views.roster', name='team_roster'),
    url(r'^teams/', 'teams.views.homepage', name='teams_home'),
    url(r'^meets/(\d+)', 'meets.views.results', name='meet_results'),
    url(r'^meets/', 'meets.views.homepage', name='meets_home'),
    url(r'^courses/(\d+)', 'courses.views.results', name='courses_meets'),
    url(r'^courses/', 'courses.views.homepage', name='courses_home'),
    url(r'^predictions/',
        'predictions.views.homepage',
        name='predictions_home'),
    url(r'^runners/(\d+)', 'runners.views.results', name='runners_results'),
    url(r'^runners/search/', 'runners.views.search', name='runner_search'),
    url(r'^runners/search/',include('haystack.urls')),
    url(r'^static/(.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    # url(r'^bugbug/', include('bugbug.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
