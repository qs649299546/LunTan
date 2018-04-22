"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from post import views as post_view
from user import views as user_view

urlpatterns = [
    url(r'^$', post_view.post_list),
    url(r'^post/list/', post_view.post_list),
    url(r'^post/create/', post_view.create_post),
    url(r'^post/edit/', post_view.edit_post),
    url(r'^post/read/', post_view.read_post),
    url(r'^post/top10/', post_view.top10_post),
    url(r'^post/comment/', post_view.comment),
    url(r'^post/tag/', post_view.tag_filter),
    url(r'^post/delete/', post_view.delete_post),

    url(r'^user/login/', user_view.login),
    url(r'^user/logout/', user_view.logout),
    url(r'^user/register/', user_view.register),
    url(r'^user/info/', user_view.user_info),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
