from django.urls import path
from .views import ZGMChartView



app_name = 'chart'
urlpatterns = [
    path('zgm-top-50/', ZGMChartView, name='zgm-chart'),
    #path('cu-top-30/', CUChartView, name='cu-chart'),
    #path('unilag-top-30/', UnilagChartView, name='unilag-chart'),
    #path('landmark-top-30/', LandmarkChartView, name='landmark-chart'),

]
