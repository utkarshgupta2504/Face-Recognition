from django.urls import path

from . import views, Recognize

urlpatterns = [
    path('', views.index, name='index'),
    path('recog/', Recognize.recog, name = 'recog'),
    path('addnew/<str:name>/', Recognize.addNewFace, name = 'addNewFace'),
    path('deleteFace/<str:name>/', Recognize.deleteFace, name = 'deleteFace'),
    path('change/<str:originalID>/<str:newID>/', Recognize.changeID, name = 'changeID'),
]