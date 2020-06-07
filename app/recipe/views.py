from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient

from recipe import serializers


class BaseRecipeAttrrViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    ''' base viewset for user own recipe attributes'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''return objects for current authenticated user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        ''' create a new object'''
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrrViewSet):
    ''' manage tags in the database'''
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
#    def get_queryset(self):
# '''Return objects for the current query set only'''
#        return self.queryset.filter(user=self.request.user).order_by('-name')
#
#    def perform_create(self, serializer):
#        '''Create a new tag '''
#        serializer.save(user=self.request.user)


class IngredientViewSet(BaseRecipeAttrrViewSet):
    '''manage ingredients in the data base'''
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
#    def get_queryset(self):
#        '''return objects for the current authenticated user'''
#        return self.queryset.filter(user=self.request.user).order_by('-name')
#
#    def perform_create(self, serializer):
#        '''Create a new ingredient'''
#        serializer.save(user=self.request.user)
