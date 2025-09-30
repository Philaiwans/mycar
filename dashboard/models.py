from django.db import models
from django.utils import timezone

class LicensePlate(models.Model):
    plate = models.CharField("เลขทะเบียน", max_length=20, unique=True)
    province = models.CharField("จังหวัด", max_length=100)

    # แก้จาก auto_now_add=True -> ให้แก้ได้ และมีค่าเริ่มต้นเป็นเวลาปัจจุบัน
    check_in  = models.DateTimeField("เวลาเข้า",  null=True, blank=True, default=timezone.now)
    check_out = models.DateTimeField("เวลาออก",  null=True, blank=True)

    # รูปรถ (อัปโหลดได้, ไม่บังคับใส่)
    car_image = models.ImageField("รูปรถ", upload_to="cars/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plate} - {self.province}"