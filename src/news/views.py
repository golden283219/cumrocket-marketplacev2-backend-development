from rest_framework import viewsets, mixins
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    API endpoint that allows create new Collections
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
