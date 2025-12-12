from django.contrib import admin
from .models import Buah, Pelanggan, Pembelian, DetailPembelian, Pemasok, Pengadaan, DetailPengadaan # , Admin
from django.contrib.auth.models import Group
admin.site.unregister(Group)

# Register your models here.

# from .models import Admin
# admin.site.register(Admin)

class BuahAdmin(admin.ModelAdmin):
    list_display = ('idBuah', 'namaBuah', 'stokBuah', 'hargaBuah')
    search_fields = ('namaBuah',)
    list_filter = ('hargaBuah',)
admin.site.register(Buah, BuahAdmin)

class PelangganAdmin(admin.ModelAdmin):
    list_display = ('idPelanggan', 'namaPelanggan', 'noHp')
    search_fields = ('namaPelanggan', 'noHp')
admin.site.register(Pelanggan, PelangganAdmin)

class PembelianAdmin(admin.ModelAdmin):
    list_display = ('idPembelian', 'idPelanggan', 'tanggalPembelian', 'totalHargaPembelian')
    search_fields = ('idPelanggan__namaPelanggan',)
    list_filter = ('tanggalPembelian',)
admin.site.register(Pembelian, PembelianAdmin)

class DetailPembelianAdmin(admin.ModelAdmin):
    list_display = ('idDetailPembelian', 'idPembelian', 'idBuah', 'kuantitas', 'subHarga')
    search_fields = ('idPembelian__idPembelian', 'idBuah__namaBuah')
admin.site.register(DetailPembelian, DetailPembelianAdmin)

class PemasokAdmin(admin.ModelAdmin):
    list_display = ('idPemasok', 'namaPemasok', 'noHp')
    search_fields = ('namaPemasok',)
admin.site.register(Pemasok, PemasokAdmin)

class PengadaanAdmin(admin.ModelAdmin):
    list_display = ('idPengadaan', 'totalHarga')
admin.site.register(Pengadaan, PengadaanAdmin)

class DetailPengadaanAdmin(admin.ModelAdmin):
    list_display = ('idDetailPengadaan', 'idPengadaan', 'idBuah', 'kuantitas', 'subHarga')
    search_fields = ('idPengadaan__idPengadaan', 'idBuah__namaBuah')
admin.site.register(DetailPengadaan, DetailPengadaanAdmin)