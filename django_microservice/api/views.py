from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
  


class HelloView(APIView):
    permission_classes = (IsAuthenticated, )
  
    def get(self, request):
        content = {'message': 'Hello, GeeksforGeeks'}
        return Response(content)
# from .models import Book, Author, BookInstance, Genre


def index(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import UsersSerializer
from .models import Users

# class ProductViewSet(ReadOnlyModelViewSet):

#     serializer_class = UsersSerializer
#     queryset = Users.objects.all()
    
#     @action(detail=False)
#     def get_list(self, request):
#         pass
      
#     @action(detail=True)
#     def get_product(self, request, pk=None):
#         pass


#     @action(detail=True, methods=['post', 'delete'])
#     def delete_product(self, request, pk=None):
#         pass