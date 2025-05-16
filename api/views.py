from rest_framework import generics , viewsets
from rest_framework.permissions import AllowAny
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

#------------------------------------------------------đăng kí------------------------------------------------------#
class RegisterSerializerView(generics.CreateAPIView):
    serializer_class = RegisterSerializers #kiểm tra và lưu
    permission_classes = [AllowAny] # cho phép tất cả đều dùng được api
    @swagger_auto_schema(
        operation_summary="Đăng ký người dùng",
        operation_id="Đăng_ký_người_dùng", 
        tags=["User"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
#------------------------------------------------------đăng nhập------------------------------------------------------#
class LoginSerializerView(APIView):
    permission_class = [AllowAny]
    @swagger_auto_schema(
        request_body=LoginSerializers,  # để hiện input khi đặt tên
        operation_summary="Đăng Nhập người dùng",
        operation_id="Đăng_nhập_người_dùng", 
        tags=["User"]
    )
    def post(self , request):
        serializer = LoginSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        
        user = authenticate(username = username , password = password)
        if user is not None:
            return Response({"message": "Đăng nhập thành công!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Tên đăng nhập hoặc mật khẩu không đúng."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
#------------------------------------------------------Reset mật khẩu------------------------------------------------------#
class ResetPassWordSerializerView(APIView):
    @swagger_auto_schema(
        request_body=ResetPassWordSerializers,  # để hiện input khi đặt tên
        operation_summary="Reset mật khẩu người dùng",
        operation_id="Reset_mật_khẩu_người_dùng", 
        tags=["User"]
    )
    def post(self , request):
        serializer = ResetPassWordSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(serializer.validated_data)
            return Response({"message": "Reset mật khẩu thành công"}, status=status.HTTP_200_OK)
        else :
            return Response({"message": "Reset mật khẩu thất bại"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
#------------------------------------------------------Category------------------------------------------------------#
class CategoryList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializers
    queryset = Category.objects.all()

    @swagger_auto_schema(
        operation_summary="Lấy tất cả hoặc tìm kiếm danh mục theo tên",
        operation_id="List_Category",
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY, description="Tìm theo tên danh mục", type=openapi.TYPE_STRING
            )
        ],
        tags=["categories"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    
class CategoryDetail(APIView):
    @swagger_auto_schema(
        operation_summary="Lấy chi tiết danh mục theo ID",
        operation_id="CategoryDetail",
    )
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializers(category)
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body = CategorySerializers,  # để hiện input khi đặt tên
        operation_summary="Thêm Danh mục",
        operation_id="Thêm danh mục", 
    )
    def post(self, request):
        serializer = CategorySerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Thành công"}, status=status.HTTP_200_OK)
        else :
            return Response({"message": "Lôi"}, status=status.HTTP_401_UNAUTHORIZED)
    @swagger_auto_schema(
        operation_summary="Cập nhật danh mục theo ID",
        operation_id="Update_Category",
        request_body=CategorySerializers,
        tags=["categories"]
    )
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializers(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cập nhật thành công"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="Xóa danh mục theo ID",
        operation_id="Delete_Category",
        tags=["categories"]
    )
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        category.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)


#------------------------------------------------------Product------------------------------------------------------#   
class ProductView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializers
    queryset = Product.objects.all()

    @swagger_auto_schema(
        operation_summary="Lấy tất cả hoặc tìm kiếm sản phẩm theo tên",
        operation_id="List_Product",
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY, description="Tìm theo tên sản phẩm", type=openapi.TYPE_STRING
            )
        ],
        tags=["Product"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    
    @swagger_auto_schema(
        request_body = ProductSerializers,  # để hiện input khi đặt tên
        operation_summary="Thêm sản phẩm",
        operation_id="Thêm sản phẩm", 
    )
    def post(self, request):
        serializer = ProductSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Thành công"}, status=status.HTTP_200_OK)
        else :
            return Response({"message": "Lôi"}, status=status.HTTP_401_UNAUTHORIZED)
   

    
class ProductDetail(APIView):
    @swagger_auto_schema(
        operation_summary="Lấy chi tiết sản phẩm theo ID",
        operation_id="ProductDetail",
       
    )
    def get(self, request, pk):
        try:
            product =  Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    @swagger_auto_schema(
        operation_summary="Cập nhật sản phẩm theo ID",
        operation_id="Update_Product",
        request_body=ProductSerializers,
        tags=["Product"]
    )
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cập nhật thành công"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="Xóa sản phẩm theo ID",
        operation_id="Delete_Product",
        tags=["Product"]
    )
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({"message": "Xóa thành công"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"message": "Không tìm thấy sản phẩm"}, status=status.HTTP_404_NOT_FOUND)
    