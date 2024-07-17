# project_root/urls.py (确保替换为你的项目根目录的urls.py文件)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('network/', include('network.urls')),  # 包含network应用的URL配置
    path('', include('network.urls')),
]
