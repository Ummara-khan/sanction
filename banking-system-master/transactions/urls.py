from django.urls import path


from .views import list_management
app_name = 'transactions'


urlpatterns = [
    path('list-management/', list_management, name='list_management'),


]
