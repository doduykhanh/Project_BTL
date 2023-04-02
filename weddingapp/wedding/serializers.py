from rest_framework import serializers
from .models import ThucDon, MonAn, DichVu, Tag, SanhCuoi, NguoiDung, BinhLuan
#Trang giao diện của Django REST framework


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, monan):
        if monan.image:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % monan.image.name) if request else ''


class NguoiDungSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='avatar')

    def get_image(self, nguoidung):
        if nguoidung.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % nguoidung.avatar.name) if request else ''

    def create(self, validated_data): #validated_data là những dữ liệu mà ta nhập vào từng key
        data = validated_data.copy()
        u = NguoiDung(**data)         #** là key, data là dữ liệu => Lấy hết
        u.set_password(u.password)    #Tiến hành băm mật khẩu
        u.save()
        return u

    class Meta:
        model = NguoiDung
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar', 'image']
        extra_kwargs = {
            'password': {'write_only': True},    #Cấu hình lại, ko cho xem chỉ cho tạo
            'avatar': {'write_only': True}
        }


class ThucDonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThucDon
        fields = ['id', 'name']


class MonAnSerializer(ImageSerializer):
    class Meta:
        model = MonAn
        fields = ['id', 'name', 'description', 'price', 'thucdon_id', 'image']


class SanhCuoiSerializer(ImageSerializer):
    class Meta:
        model = SanhCuoi
        fields = ['id', 'name', 'description', 'minimum_price', 'number_of_tables', 'image']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class DichVuSerializer(ImageSerializer):
    tags = TagSerializer(many=True) #Giúp hiển thị hết các tag

    class Meta:
        model = DichVu
        fields = ['id', 'subject', 'description', 'price', 'image', 'tags']


class BinhLuanSerializer(serializers.ModelSerializer):
    nguoidung = NguoiDungSerializer()

    class Meta:
        model = BinhLuan
        fields = ['id', 'content', 'created_date', 'nguoidung']


class AuthorizedSanhCuoiSerializer(SanhCuoiSerializer):
    liked = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    def get_liked(self, sanhcuoi):
        request = self.context.get('request')
        if request:
            return sanhcuoi.thich_set.filter(nguoidung=request.user, liked=True).exists()

    def get_rate(self, sanhcuoi):
        request = self.context.get('request')
        if request:
            r = sanhcuoi.xephang_set.filter(nguoidung=request.user).first()
            return r.rate if r else 0

    class Meta:
        model = SanhCuoiSerializer.Meta.model
        fields = SanhCuoiSerializer.Meta.fields + ['liked', 'rate']