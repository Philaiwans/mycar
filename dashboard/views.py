from django.shortcuts import render, redirect
from django.utils import timezone
from .models import LicensePlate
from .forms import CarImageForm


def home(request):
    return render(request, "home.html")

def dashboard(request):
    # ดึงข้อมูลเรียงตาม created_at ล่าสุดก่อน
    plates = LicensePlate.objects.all().order_by("-created_at")
    return render(request, "dashboard.html", {
        "plates": plates
    })

# dashboard/views.py
from django.shortcuts import render, redirect
from .forms import CarImageForm
from .models import LicensePlate

def upload_car_image(request):
    if request.method == "POST":
        form = CarImageForm(request.POST, request.FILES)
        if form.is_valid():
            # สร้าง LicensePlate ใหม่ แต่ไม่บังคับ plate/province
            form.save()
            return redirect("dashboard")  # กลับไป dashboard
    else:
        form = CarImageForm()
    
    # แสดงฟอร์มอัปโหลดรูปอย่างเดียว
    return render(request, "upload_license_plate.html", {"form": form})
