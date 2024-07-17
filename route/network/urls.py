from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('topology/', views.topology_view, name='topology_view'),
    path('receive_link_data/', views.receive_link_data, name='receive_link_data'), # 链路数据
    # path('generate_topology/', views.generate_topology, name='generate_topology'),
    path('get_link_data/', views.get_link_data, name='get_link_data'),
    path('topology_data/', views.generate_topology, name='topology_data'), 
    path('link_data_table/', views.link_data_table, name='link_data_table'),
    path('dynamic-routing/', views.dynamic_routing_decision, name='dynamic-routing'), # 处理前端请求，并发送最短路径
    path('reachable-nodes/', views.reachable_nodes, name='reachable_nodes'),
] 

