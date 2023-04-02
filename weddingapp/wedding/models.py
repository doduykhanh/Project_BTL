from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class NguoiDung(AbstractUser):
    avatar = models.ImageField(upload_to="nguoidung/%Y/%m", null=True)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ThucDon(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MonAn(BaseModel):
    name = models.CharField(max_length=255)
    description = RichTextField()
    price = models.IntegerField()
    thucdon = models.ForeignKey(ThucDon, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="monan/%Y/%m", null=True)

    def __str__(self):
        return self.name


class DichVu(BaseModel):
    subject = models.CharField(max_length=255)
    description = RichTextField()
    image = models.ImageField(upload_to="dichvu/%Y/%m", null=True)
    price = models.IntegerField()
    tags = models.ManyToManyField('Tag', related_name="dichvus")

    def __str__(self):
        return self.subject


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SanhCuoi(BaseModel):
    name = models.CharField(max_length=255)
    description = RichTextField()
    minimum_price = models.IntegerField()
    number_of_tables = models.IntegerField()
    image = models.ImageField(upload_to="sanhcuoi/%Y/%m", null=True)

    def __str__(self):
        return self.name


class BinhLuan(BaseModel):
    content = models.CharField(max_length=255)
    sanhcuoi = models.ForeignKey(SanhCuoi, on_delete=models.CASCADE)
    nguoidung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class ActionBase(BaseModel):
    sanhcuoi = models.ForeignKey(SanhCuoi, on_delete=models.CASCADE)
    nguoidung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

    #Rành buộc sảnh cưới chỉ đc like 1 lần, like lần 2 thành unlike
    class Meta:
        unique_together = ('sanhcuoi', 'nguoidung')
        abstract = True


class Thich(ActionBase):
    liked = models.BooleanField(default=True)


class XepHang(ActionBase):
    rate = models.SmallIntegerField(default=0)