from django.urls import path

from .views import HomePageView, NytMostPopularView, NytTopStoriesView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("nyt/top/", NytTopStoriesView.as_view(), name="nyt_top"),
    path("nyt/top/<str:section>/", NytTopStoriesView.as_view(), name="nyt_top_section"),
    path("nyt/popular/", NytMostPopularView.as_view(), name="nyt_popular"),
    path("nyt/popular/<int:period>/", NytMostPopularView.as_view(), name="nyt_popular_period"),
]
