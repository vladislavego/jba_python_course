from django.urls import path
from .views import NewsDetails, NewsPage, CreateNews, DeleteNews, EditNews

urlpatterns = [
    path('', NewsPage.as_view(), name='news_url'),
    path('create/', CreateNews.as_view(), name='create_news_url'),
    path('delete/<link>', DeleteNews.as_view(), name='delete_news_url'),
    path('edit/<link>', EditNews.as_view(), name='edit_news_url'),
    path('<link>/', NewsDetails.as_view(), name='news_detail_url'),
]