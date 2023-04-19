from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignupView, TitleViewSet, UsersMeView,
                       UserViewSet, YamdbTokenObtainPairView)
from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()

router.register(
    r'users',
    UserViewSet,
    basename='user',
)
router.register(
    r'categories',
    CategoryViewSet,
    basename='category',
)
router.register(
    r'genres',
    GenreViewSet,
    basename='genre',
)
router.register(
    r'titles',
    TitleViewSet,
    basename='title',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)

urlpatterns = [

    path('v1/auth/token/', YamdbTokenObtainPairView.as_view(),
         name='create_token'),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/users/me/', UsersMeView.as_view(), name='me'),
    path('v1/', include(router.urls)),
]
