from django.urls import path
from skincare_recommendation_app.views import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("product", views.user_product, name="user_product"),
    path("about", views.about, name="about"),
    path("", views.user_home, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)