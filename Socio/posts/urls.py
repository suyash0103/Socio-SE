from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'posts'

urlpatterns = [
    path('posts',views.postsView, name="allPosts"),
    path('posts/create',views.CreatePostView.as_view(), name="createPost"),
    path('posts/edit/<pk>',views.EditPostView.as_view(), name="editPost"),
    path('posts/delete/<pk>',views.DeletePostView.as_view(), name="deletePost"),
    path('post/download/<file_name>', views.downloadFile, name="downloadFile"),

    # path('posts/like/<pk>',views.LikePostView.as_view(), name="likePost"),
    path('posts/like',views.likePost, name="likePost"),
    # path('posts/comment/<pk>',views.CommentPostView.as_view(), name="commentPost"),
    path('posts/comment',views.commentPost, name="commentPost"),
    path('posts/users',views.GetUserView.as_view(), name="getUser"),

]
