import traceback

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.models import Books
from api.serializer import BookModelSerializer, BookDeModelSerializer


class BookAPIView(APIView):
    def get(self,request,*args,**kwargs):
        re = request.GET
        if re:
            id = re['id']
            print('单查', id)
            book = Books.objects.filter(id=id)[0]
            if book:
                flag = False
            else:
                return Response({'status': 500, 'message': '查新单个图书失败'})

        elif not re:
            # book = Books.objects.all()
            book = Books.objects.filter(is_delete=False)
            flag = True

        else:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': '查询失败'})

        book_ser = BookModelSerializer(book, many=flag).data
        return Response({'status': status.HTTP_200_OK, 'message': '查询图书成功', 'books': book_ser})

    def post(self, request, *args, **kwargs):
        # try:
            book_data = request.data
            print('获取新增数据',book_data)
            if isinstance(book_data,dict):
                flag=False
            elif isinstance(book_data,list):
                flag=True
            else:
                return Response(
                    {'status': status.HTTP_400_BAD_REQUEST, 'message': '格式有误'})
            ser = BookDeModelSerializer(data=book_data,many=flag)
            print(111, ser)
            # if ser.is_valid():
            ser.is_valid(raise_exception=True)
            book = ser.save()
            print(222)
            return Response({'status': status.HTTP_200_OK, 'message': '创建图书成功', 'book': BookModelSerializer(book,many=flag).data})
            # return Response({'status': 500, 'message': '创建失败', 'error': ser.errors})
        # except:
        #     traceback.print_exc()

    def delete(self,request,*args,**kwargs):
        book_id=kwargs.get('id')
        if book_id:
            ids=[book_id]
        else:
            ids=request.data.get('ids')
        books=Books.objects.filter(id__in=ids,is_delete=False).update(is_delete=True)
        if books:
            return Response({"status":status.HTTP_200_OK,'message':'删除成功'})
        return Response({"status":status.HTTP_400_BAD_REQUEST,'message':'删除失败'})

    def patch(self,request,*args,**kwargs):
        book_data=request.data
        book_id=kwargs.get('id')
        book=Books.objects.filter(id=book_id)[0]
        if book:
            booK_ser=BookDeModelSerializer(data=book_data,instance=book,partial=True)
            booK_ser.is_valid(raise_exception=True)
            booK_ser.save()
            return Response({"status": status.HTTP_200_OK, 'message': '更新成功'})
        return Response({"status": status.HTTP_400_BAD_REQUEST, 'message': '图书不存在'})

