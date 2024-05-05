from django.urls import include, path
from rest_framework import routers

from . import views


# Fix for TC `test_multi_update`. Add PATCH to the HTTP methods allowed and its mapping to `partial_update`
class CustomRouter(routers.DefaultRouter):
    """
    Custom router extending DefaultRouter to handle PATCH method for partial updates.

    This router customizes the behavior of the DefaultRouter provided by DRFramework.
    By inheriting from DefaultRouter, it maintains all the default routing behavior
    while adding PATCH support to the List route in the SimpleRouter inherited by
    the DefaultRouter.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add the PATCH method to DefaultRouter -> SimpleRoute -> List router
        self.routes[0].mapping.update({"patch": "partial_update"})


# Fix for TC `test_multi_update`. Add PATCH to the HTTP methods allowed and its mapping to `partial_update`
router = CustomRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"questions", views.QuestionViewSet)
router.register(r"choices", views.ChoiceViewSet)

# app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
