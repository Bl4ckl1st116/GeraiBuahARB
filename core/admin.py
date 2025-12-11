from django.contrib import admin
from .models import Buah, Pelanggan, Pembelian, DetailPembelian, Pemasok, Pengadaan, DetailPengadaan # , Admin
from django.contrib.auth.models import Group
admin.site.unregister(Group)

# Register your models here.

# from .models import Admin
# admin.site.register(Admin)

from .models import Buah
admin.site.register(Buah)

from .models import Pelanggan
admin.site.register(Pelanggan)

from .models import Pembelian
admin.site.register(Pembelian)

from .models import DetailPembelian
admin.site.register(DetailPembelian)

from .models import Pemasok
admin.site.register(Pemasok)

from .models import Pengadaan
admin.site.register(Pengadaan)

from .models import DetailPengadaan
admin.site.register(DetailPengadaan)