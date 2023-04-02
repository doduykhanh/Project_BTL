from rest_framework import viewsets, generics, permissions, parsers, status
from rest_framework.decorators import action
from rest_framework.views import Response
from .models import ThucDon, MonAn, SanhCuoi, DichVu, Tag, NguoiDung, BinhLuan, Thich, XepHang
from .serializers import (ThucDonSerializer, MonAnSerializer, SanhCuoiSerializer,
                          DichVuSerializer, TagSerializer, NguoiDungSerializer,
                          BinhLuanSerializer, AuthorizedSanhCuoiSerializer)
from .paginators import MonAnPaginator, SanhCuoiPaginator
from .perms import BinhLuanOwner


#Xuất ra hết các chức năng (ModelViewSet làm hết rồi)
# class ThucDonViewSet(viewsets.ModelViewSet):
#     queryset = ThucDon.objects.all()
#     serializer_class = ThucDonSerializer


#Xuất ra hết các chức năng (ModelViewSet làm hết rồi)
# class MonAnViewSet(viewsets.ModelViewSet):
#     queryset = MonAn.objects.all()
#     serializer_class = MonAnSerializer
#     pagination_class = MonAnPaginator


#Xuất ra hết các chức năng (ModelViewSet làm hết rồi)
# class SanhCuoiViewSet(viewsets.ModelViewSet):
#     queryset = SanhCuoi.objects.filter(active=True)
#     serializer_class = SanhCuoiSerializer
#     pagination_class = SanhCuoiPaginator


#Xuất ra hết các chức năng (ModelViewSet làm hết rồi)
# class DichVuViewSet(viewsets.ModelViewSet):
#     queryset = DichVu.objects.filter(active=True)
#     serializer_class = DichVuSerializer


#Tự viết lại API tạo người dùng
class NguoiDungViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = NguoiDung.objects.filter(is_active=True)
    serializer_class = NguoiDungSerializer
    parser_classes = [parsers.MultiPartParser, ] #Lấy tập tin(ảnh) ở dưới client để xử lý và upload lên

    def get_permissions(self):
        if self.action in ['detail_nguoidung']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    #Hiển thị thông tin chi tiết, chỉnh sửa người dùng
    @action(methods=['get', 'put'], detail=False, url_path='chitiet-nguoidung')
    def detail_nguoidung(self, request):
        #Sau khi nguoidung đc chứng thực thì nó có sẵn ở trong đây luôn và mặc định là request.user
        u = request.user

        if request.method.__eq__('PUT'):
            for k, v in request.data.items():
                setattr(u, k, v)
            u.save()

        return Response(NguoiDungSerializer(u, context={'request': request}).data)


#Tự viết lại API xuất danh sách thực đơn
class ThucDonViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ThucDon.objects.all()
    serializer_class = ThucDonSerializer

    #Tìm kiếm tên thực đơn(http://127.0.0.1:8000/thucdon/?kw=kim)
    # def get_queryset(self):
    #     q = self.queryset
    #     kw = self.request.query_params.get('kw')
    #     if kw:
    #         q = q.filter(name__icontains=kw)
    #     return q

    #Vẫn là tìm kiếm tên thực đơn nhưng nâng cao(http://127.0.0.1:8000/thucdon/?kw=kim)
    def filter_queryset(self, queryset):
        q = queryset
        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)
        return q

    #Từ thực đơn đc chỉ định, lấy danh sách các món ăn thuộc thực đơn đó(http://127.0.0.1:8000/thucdon/2/ds_monan/)
    @action(methods=['get'], detail=True, url_path='ds-monan')
    def list_monan(self, request, pk):
        t = self.get_object()
        my_monan = t.monan_set.filter(active=True)

        #Lấy đc danh sách tìm tên món ăn trong danh sách đó(http://127.0.0.1:8000/thucdon/2/ds_monan/?q=thit)
        kw = request.query_params.get('q')
        if kw:
            my_monan = my_monan.filter(name__icontains=kw)

        return Response(MonAnSerializer(my_monan, many=True, context={'request':request}).data)


#Tự viết lại API xuất danh sách món ăn
class MonAnViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = MonAn.objects.all()
    serializer_class = MonAnSerializer
    pagination_class = MonAnPaginator
    permission_classes = [permissions.IsAuthenticated] #Đã tạo chứng thưc, phải đc chứng thực mới đc truy cập

    #Tìm kiếm tên món ăn(http://127.0.0.1:8000/monan/?kw=súp)
    def get_queryset(self):
        q = self.queryset
        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)

        #Lấy danh sách các món ăn thuộc thực đơn món nào đó(http://127.0.0.1:8000/monan/?thucdon_id=1)
        td_id = self.request.query_params.get('thucdon_id')
        if td_id:
            q = q.filter(thucdon_id=td_id)

        return q


#Tự viết lại API xuất danh sách, xem chi tiết sảnh cưới
class SanhCuoiViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = SanhCuoi.objects.filter(active=True)
    serializer_class = SanhCuoiSerializer
    pagination_class = SanhCuoiPaginator

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthorizedSanhCuoiSerializer
        return self.serializer_class

    #Tìm kiếm tên sảnh(http://127.0.0.1:8000/sanhcuoi/?kw=aqua)
    def get_queryset(self):
        q = self.queryset
        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)
        return q

    def get_permissions(self):
        if self.action in ['comment_sanhcuoi', 'like_sanhcuoi', 'rating_sanhcuoi']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    #Thêm bình luận từ người dùng vào sảnh cưới
    @action(methods=['post'], detail=True, url_path='binhluan-sanhcuoi')
    def comment_sanhcuoi(self, request, pk):
        bl = BinhLuan(content=request.data['content'],
                      nguoidung=request.user,
                      sanhcuoi=self.get_object())
        bl.save()
        return Response(BinhLuanSerializer(bl, context={'request': request}).data, status=status.HTTP_201_CREATED)

    #Like một sảnh cưới
    @action(methods=['post'], detail=True, url_path='thich-sanhcuoi')
    def like_sanhcuoi(self, request, pk):
        l, created = Thich.objects.get_or_create(nguoidung=request.user,
                                                 sanhcuoi=self.get_object())
        if not created:
            l.liked = not l.liked
        l.save()
        return Response(status=status.HTTP_200_OK)

    #Xếp hạng một sảnh cưới
    @action(methods=['post'], detail=True, url_path='xephang-sanhcuoi')
    def rating_sanhcuoi(self, request, pk):
        r, created = XepHang.objects.get_or_create(nguoidung=request.user,
                                                   sanhcuoi=self.get_object())
        r.rate = request.data['rate']
        r.save()
        return Response(status=status.HTTP_200_OK)


#Tự viết lại API xem thông tin chi tiết dịch vụ
class DichVuViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = DichVu.objects.filter(active=True)
    serializer_class = DichVuSerializer

    # Tìm kiếm tên dịch vụ(http://127.0.0.1:8000/dichvu/?kw=MC)
    # def get_queryset(self):
    #     q = self.queryset
    #     kw = self.request.query_params.get('kw')
    #     if kw:
    #         q = q.filter(subject__icontains=kw)
    #     return q

    def get_permissions(self):
        if self.action in ['assign_tags']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    #Thêm một tag vào một dịch vụ(nếu có sẵn trong database thì ko tạo chỉ thêm, chưa có thì tạo và thêm)
    @action(methods=['post'], detail=True, url_path='them-tags')
    def assign_tags(self, request, pk):
        dichvu = self.get_object()

        tags = request.data.get('tags')
        for t in tags:
            tag, _ = Tag.objects.get_or_create(name=t)
            dichvu.tags.add(tag)

        dichvu.save()
        return Response(DichVuSerializer(dichvu, context={'request': request}).data)


#Tự viết lại API xóa và chỉnh sửa bình luận
class BinhLuanViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = BinhLuan.objects.filter(active=True)
    serializer_class = BinhLuanSerializer
    permissions_classes = [BinhLuanOwner, ] #Phải là người viết mới đc xóa và chỉnh sửa