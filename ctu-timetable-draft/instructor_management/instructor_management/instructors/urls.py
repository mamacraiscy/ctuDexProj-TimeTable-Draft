# instructors/urls.py

from django.urls import path
from .views import (
    instructor_list,
    instructor_search,
    instructor_details,
    filter_instructors,
    index,
    teaching_load,  # Import the new view
    get_suggestions,
    save_teaching_load,
    editable_instructor_details
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('list/', instructor_list, name='instructor_list'),
    path('search/', instructor_search, name='instructor_search'),
    path('details/', instructor_details, name='instructor_details'),
    path('filter/', filter_instructors, name='filter_instructors'),
    path('create-teaching-load/', teaching_load, name='teaching_load'),
    path('get-suggestions/', get_suggestions, name='get_suggestions'),
    path('save-teaching-load/', save_teaching_load, name='save_teaching_load'),  # Define the URL for saving teaching load
    path('editable-instructor-details/', editable_instructor_details, name='editable_instructor_details'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
