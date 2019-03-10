from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

# from graphene_django.views import GraphQLView
from core.file_upload.views import FileUploadGraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=settings.DEBUG))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
