from django.contrib import admin
from .models import ThucDon, MonAn, DichVu, Tag, SanhCuoi
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
#Trang giao diện của ADMIN


class MonAnForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = MonAn
        fields = '__all__'


class DichVuForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = DichVu
        fields = '__all__'


class SanhCuoiForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = SanhCuoi
        fields = '__all__'


class MonAnAdmin(admin.ModelAdmin):
    form = MonAnForm

    list_display = ["id", "name", "description", "price"]
    search_fields = ["name"]
    list_filter = ["id", "name", "thucdon", "price"]


class DichVuAdmin(admin.ModelAdmin):
    form = DichVuForm

    list_display = ["id", "subject", "description", "price"]


class SanhCuoiAdmin(admin.ModelAdmin):
    form = SanhCuoiForm

    list_display = ["id", "name", "description", "minimum_price", "number_of_tables"]


admin.site.register(ThucDon)
admin.site.register(MonAn, MonAnAdmin)
admin.site.register(DichVu, DichVuAdmin)
admin.site.register(Tag)
admin.site.register(SanhCuoi, SanhCuoiAdmin)
