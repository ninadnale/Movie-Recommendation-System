from django.urls import path
from django.conf.urls import url
from hello_world import views
from django.conf import settings

urlpatterns = [
	path('', views.hello_world, name='hello_world'),
	url(r'^main_page', views.main_page, name='main_page'),
	url(r'^page_knn', views.page_knn, name='page_knn'),
	url(r'^kmeans', views.kmeans, name='kmeans'),
	url(r'^top', views.top, name='top'),
	url(r'^left', views.left, name='left'),
	url(r'^img1', views.img1, name='img1'),
	url(r'^img2', views.img2, name='img2'),
	url(r'^top_bg', views.top_bg, name='top_bg'),
	url(r'^left_bg', views.left_bg, name='left_bg'),
	url(r'^graph1', views.graph1, name='graph1'),
	url(r'^graph2', views.graph2, name='graph2'),
	url(r'^heatmap', views.heatmap, name='heatmap'),
	url(r'^external',views.external),
	url(r'^get_knn',views.get_knn),
]

#from . import views, settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
 
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
