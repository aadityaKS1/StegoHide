from django.urls import path
from .views import encode_image,decode_message

urlpatterns = [
    path("encode/", encode_image),
    path("decode/", decode_message),

]