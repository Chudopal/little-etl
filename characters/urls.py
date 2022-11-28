from django.urls import path
from characters.views import get_characters, download_file

urlpatterns = [
    path('<int:character_page>', view=get_characters, name='get_characters'),
    path('<int:character_page>/download', view=download_file, name='download_csv'),
]
