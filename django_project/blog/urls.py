from django.urls import path
from .views import *
# from django.conf import settings
# from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    path('', HomeView, name='home'),
    path('favs/', FavoritesView.as_view(), name='favorites'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('detail/<int:pk>', PostDetailView.as_view(), name='detail'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    path('delete/comment/<int:pk>', CommentDeleteView.as_view(), name='delete_comment'),
    path('update/comment/<int:pk>', CommentUpdateView, name='update_comment'),
    path('fav/<int:pk>', MarkFav.as_view(), name='fav'),
    path('unfav/<int:pk>', UnMarkFav.as_view(), name='unfav'),
    path('like/<int:pk>', LikeView.as_view(), name='like'),
    path('unlike/<int:pk>', UnLikeView.as_view(), name='un_like'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)