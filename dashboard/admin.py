from django.contrib import admin
from django import forms
from django.utils import timezone
from django.contrib.admin.widgets import AdminSplitDateTime
from django.utils.html import format_html   # ✨ ใช้ทำรูปย่อ
from .models import LicensePlate

class LicensePlateForm(forms.ModelForm):
    class Meta:
        model = LicensePlate
        # ✨ ใส่ car_image ในฟอร์มด้วย
        fields = ("plate", "province", "car_image", "check_in", "check_out")
        widgets = {
            "check_in":  AdminSplitDateTime(),
            "check_out": AdminSplitDateTime(),
        }

@admin.register(LicensePlate)
class LicensePlateAdmin(admin.ModelAdmin):
    form = LicensePlateForm

    # ✨ เพิ่มคอลัมน์ thumb ใน list
    list_display = ("thumb", "plate", "province", "check_in", "check_out")
    list_filter = ("province",)
    search_fields = ("plate", "province")

    # ถ้าใช้ fieldsets อยู่ ให้เพิ่ม car_image และ thumb (readonly) เข้าไป
    fieldsets = (
        (None, {
            "fields": ("plate", "province", "car_image", "thumb"),  # ✨ เพิ่มสองอันนี้
        }),
        ("เวลาเข้า/ออก", {
            "fields": ("check_in", "check_out"),
            "description": "ปล่อยว่างได้ ถ้าไม่ทราบเวลาแน่ชัด",
        }),
    )
    readonly_fields = ("thumb",)  # ✨ ป้องกันไม่ให้แก้ไขรูปย่อ

    # ✨ ฟังก์ชันแสดงภาพย่อใน admin (list + form)
    def thumb(self, obj):
        if obj.car_image:
            return format_html(
                '<img src="{}" style="width:80px;height:56px;object-fit:cover;border-radius:6px;">',
                obj.car_image.url
            )
        return "—"
    thumb.short_description = "รูปรถ"

    # เติมค่าเริ่มต้น check_in เป็นตอนนี้ ถ้าเว้นว่างไว้
    def save_model(self, request, obj, form, change):
        if not obj.check_in:
            obj.check_in = timezone.now()
        super().save_model(request, obj, form, change)

    # (ตัวเลือก) actions
    actions = ["mark_checkout_now", "clear_checkout"]
    def mark_checkout_now(self, request, queryset):
        queryset.update(check_out=timezone.now())
    mark_checkout_now.short_description = "ตั้ง 'เวลาออก' เป็นตอนนี้"

    def clear_checkout(self, request, queryset):
        queryset.update(check_out=None)
    clear_checkout.short_description = "ล้างค่า 'เวลาออก'"
