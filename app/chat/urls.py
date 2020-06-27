from django.urls import path, re_path


from .views import ThreadView, InboxView, inbox_view

app_name = 'chat'
urlpatterns = [
    path("", inbox_view, name="chats"),
    re_path(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view(),),
]
