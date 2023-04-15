from rest_framework import routers

from django.urls import include, path

from .views import ReviewViewSet, CommentViewSet


router = routers.DefaultRouter()


router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet, basename='review'
)
router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
