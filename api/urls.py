from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ExpenseViewSet, current_user
from django.urls import path, include
from .views import RegisterView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path('me/', current_user, name='current_user')

]