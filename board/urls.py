from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('news/', NewsListView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('ads/', Ads.as_view(), name='ads'),
    path('ads/<int:pk>/', AdsDetail.as_view(), name='ads_detail'),
    path('adsprivate/', AdPrivatePage.as_view(), name='adsprivate'),
    path('adsprivate/<int:pk>/', AdPrivateDetail.as_view(), name='ad_private_detail'),
    path('adlike/', AdLike.as_view(), name='adlike'),
    path('create_ad/', create_ad, name='create_ad'),
    path('create_response/<int:ad_id>/', create_response, name='create_response'),
    path('user_responses/', user_responses, name='user_responses'),
    path('accept_response/<int:ad_id>/<int:response_id>/', accept_response, name='accept_response'),
    path('reject_response/<int:ad_id>/<int:response_id>/', reject_response, name='reject_response'),
    path('adsprivate/<int:pk>/delete_response/<int:response_id>/', delete_response, name='delete_response'),
    path('send_notification/<int:news_id>/', send_news_notification, name='send_news_notification'),
]