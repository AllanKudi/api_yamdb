from rest_framework import routers

from django.urls import include, path

from .views import (ReviewViewSet, CommentViewSet, CategoryViewSet,
                    GenreViewSet, TitleViewSet, UsersViewSet)


router = routers.DefaultRouter()


router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet, basename='review'
)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet, basename='comment'
)
router.register('auth', UsersViewSet, basename='auths')
router.register('users', UsersViewSet, basename='auths')


urlpatterns = [
    path('v1/', include(router.urls)),
]
