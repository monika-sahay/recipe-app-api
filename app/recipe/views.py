from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

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


class RecipeViewSet(viewsets.ModelViewSet):
    ''' manage recipes in the database'''
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        ''' Retrieve the recipes for the authenticated users'''
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        '''return appropriate serializer class '''
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        '''create a new recipe '''
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        '''Upload an image to a recipe'''
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
