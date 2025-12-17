from urllib import request
from django.contrib import admin
from .models import Buah, Pelanggan, Pembelian, DetailPembelian, Pemasok, Pengadaan, DetailPengadaan # , Admin
from django.contrib.humanize.templatetags.humanize import intcomma

from django.contrib.auth.models import Group
admin.site.unregister(Group)

from django.http import FileResponse
from .utils.pdf import generate_pdf

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils import timezone



# Register your models here.

# from .models import Admin
# admin.site.register(Admin)

@admin.register(Buah)
class BuahAdmin(admin.ModelAdmin):
    list_display = ("namaBuah", "harga_rupiah", "stokBuah", "diskon", "tanggalKadaluarsa")
    search_fields = ("namaBuah",)
    
    
    actions = ["export_pdf"]

    def harga_rupiah(self, obj):
        return f"Rp {intcomma(obj.hargaBuah)}"

    harga_rupiah.short_description = "Harga"

    def export_pdf(self, request, queryset):
        data = [["Nama", "Harga", "Stok", "Diskon", "Kadaluarsa"]]

        for b in queryset:
            data.append([
                b.namaBuah,
                f"Rp {intcomma(b.hargaBuah)}",
                b.stokBuah,
                #f"{b.diskon*100}%",
                f"{b.diskon * 100:.0f}%",
                b.tanggalKadaluarsa or "-"
            ])

        pdf_buffer = generate_pdf("LAPORAN DATA BUAH", data)
        return FileResponse(pdf_buffer, as_attachment=True, filename="laporan_buah.pdf")

    export_pdf.short_description = "Cetak Laporan PDF"

@admin.register(Pelanggan)
class PelangganAdmin(admin.ModelAdmin):
    list_display = ("namaPelanggan", "username", "noHp", "alamat")
    search_fields = ("namaPelanggan", "username", "noHp", "alamat")
    

    actions = ["export_pdf"]

    def export_pdf(self, request, queryset):
        data = [["Nama", "Username", "No HP", "Alamat"]]

        for p in queryset:
            data.append([
                p.namaPelanggan,
                p.username,
                p.noHp,
                p.alamat
            ])

        pdf_buffer = generate_pdf("LAPORAN DATA PELANGGAN", data)
        return FileResponse(pdf_buffer, as_attachment=True, filename="laporan_pelanggan.pdf")


class DetailPembelianInline(admin.TabularInline):
    model = DetailPembelian
    extra = 1

@admin.register(Pembelian)
class PembelianAdmin(admin.ModelAdmin):
    list_display = (
        "idPembelian",
        "nama_pelanggan",
        "totalBuah",
        "total_harga_rupiah",
        "statusPembelian",
        "tanggalPembelian"
    )
    inlines = [DetailPembelianInline]
    actions = ["export_pdf", "export_pdf_by_date"]


    list_filter = ("tanggalPembelian", "statusPembelian")



    def nama_pelanggan(self, obj):
        return obj.idPelanggan.namaPelanggan

    def total_harga_rupiah(self, obj):
        return f"Rp {intcomma(obj.totalHargaPembelian)}"

    total_harga_rupiah.short_description = "Total Harga"

    def export_pdf(self, request, queryset):
        data = [["ID", "Pelanggan", "Total Buah", "Total Harga", "Status", "Tanggal Pembelian"]]

        for pb in queryset:
            data.append([
                pb.idPembelian,
                f"Rp {intcomma(pb.totalHargaPembelian)}",
                pb.totalBuah,
                pb.totalHargaPembelian,
                pb.statusPembelian,
                pb.tanggalPembelian
            ])

            # Detail pembelian
            data.append(["--- DETAIL PEMBELIAN ---", "", "", "", ""])
            detail = pb.detailpembelian_set.all()
            data.append(["Buah", "Qty", "Harga/Qty", "Subtotal", ""])

            for d in detail:
                data.append([
                    d.idBuah.namaBuah,
                    d.kuantitas,
                    f"Rp {intcomma(d.idBuah.hargaBuah)}",
                    f"Rp {intcomma(d.subHarga)}",
                    ""
                ])



        pdf_buffer = generate_pdf("LAPORAN PEMBELIAN", data)
        return FileResponse(pdf_buffer, as_attachment=True, filename="laporan_pembelian.pdf")
    
    def export_pdf_by_date(self, request, queryset):
        # Jika form sudah disubmit
        if "start_date" in request.POST and "end_date" in request.POST:
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")

            filtered = Pembelian.objects.filter(
                tanggalPembelian__date__gte=start_date,
                tanggalPembelian__date__lte=end_date
            )

            data = [["ID", "Pelanggan", "Total Buah", "Total Harga", "Status", "Tanggal Pembelian"]]

            for pb in filtered:
                data.append([
                    pb.idPembelian,
                    pb.idPelanggan.namaPelanggan,
                    pb.totalBuah,
                    f"Rp {intcomma(pb.totalHargaPembelian)}",
                    pb.statusPembelian,
                    pb.tanggalPembelian
                ])

            pdf_buffer = generate_pdf(
                f"LAPORAN PEMBELIAN {start_date} s/d {end_date}",
                data
            )

            return FileResponse(
                pdf_buffer,
                as_attachment=True,
                filename="laporan_pembelian_rentang_tanggal.pdf"
            )

        # Jika belum submit → tampilkan form
        return render(
        request,
        "core/admin/pembelian/date_range_form.html",
        {
            "queryset": queryset
        }
)
    export_pdf_by_date.short_description = "Cetak Laporan (Rentang Tanggal)" 



@admin.register(Pemasok)
class PemasokAdmin(admin.ModelAdmin):
    list_display = ("namaPemasok", "noHp", "alamat")
    search_fields = ("namaPemasok", "noHp", "alamat")
    actions = ["export_pdf"]

    def export_pdf(self, request, queryset):
        data = [["Nama", "No HP", "Alamat"]]

        for s in queryset:
            data.append([
                s.namaPemasok,
                s.noHp,
                s.alamat
            ])

        pdf_buffer = generate_pdf("LAPORAN DATA PEMASOK", data)
        return FileResponse(pdf_buffer, as_attachment=True, filename="laporan_pemasok.pdf")

from django.contrib.admin import SimpleListFilter
from datetime import date, timedelta

class PengadaanTanggalFilter(SimpleListFilter):
    title = "Tanggal Masuk"
    parameter_name = "tanggal_masuk"

    def lookups(self, request, model_admin):
        return (
            ("hari_ini", "Hari Ini"),
            ("7_hari", "7 Hari Terakhir"),
            ("30_hari", "30 Hari Terakhir"),
        )

    def queryset(self, request, queryset):
        today = date.today()

        if self.value() == "hari_ini":
            return queryset.filter(detailpengadaan__tanggalMasuk=today)

        if self.value() == "7_hari":
            return queryset.filter(
                detailpengadaan__tanggalMasuk__gte=today - timedelta(days=7)
            )

        if self.value() == "30_hari":
            return queryset.filter(
                detailpengadaan__tanggalMasuk__gte=today - timedelta(days=30)
            )

        return queryset


class DetailPengadaanInline(admin.TabularInline):
    model = DetailPengadaan
    extra = 1

@admin.register(Pengadaan)
class PengadaanAdmin(admin.ModelAdmin):
    list_display = ("idPengadaan", "nama_pemasok", "total_harga_rupiah",)
    inlines = [DetailPengadaanInline]
    list_filter = (PengadaanTanggalFilter,)

    actions = ["export_pdf", "export_pdf_by_date"]

    def nama_pemasok(self, obj):
        return obj.idPemasok.namaPemasok

    def total_harga_rupiah(self, obj):
        return f"Rp {intcomma(obj.totalHarga)}"

    total_harga_rupiah.short_description = "Total Harga"

    def export_pdf(self, request, queryset):
        data = [["ID", "Pemasok", "Total Harga"]]

        for pg in queryset:
            data.append([
                pg.idPengadaan,
                pg.idPemasok.namaPemasok,
                f"Rp {intcomma(pg.totalHarga)}",
            ])

            data.append(["--- DETAIL PENGADAAN ---", "", ""])
            detail = pg.detailpengadaan_set.all()
            data.append(["Buah", "Qty", "Subtotal"])

            for d in detail:
                data.append([
                    d.idBuah.namaBuah,
                    d.kuantitas,
                    f"Rp {intcomma(d.subHarga)}",
                ])

        pdf_buffer = generate_pdf("LAPORAN PENGADAAN", data)
        return FileResponse(pdf_buffer, as_attachment=True, filename="laporan_pengadaan.pdf")

    def export_pdf_by_date(self, request, queryset):
        # Jika form disubmit
        if "start_date" in request.POST and "end_date" in request.POST:
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")

            filtered = Pengadaan.objects.filter(
                detailpengadaan__tanggalMasuk__gte=start_date,
                detailpengadaan__tanggalMasuk__lte=end_date 
            ).distinct()

            data = [["ID", "Pemasok", "Total Harga"]]

            for pg in filtered:
                data.append([
                    pg.idPengadaan,
                    pg.idPemasok.namaPemasok,
                    f"Rp {intcomma(pg.totalHarga)}",
                ])

                data.append(["--- DETAIL PENGADAAN ---", "", ""])
                data.append(["Buah", "Qty", "Subtotal", "Tanggal Masuk"])

                for d in pg.detailpengadaan_set.all():
                    data.append([
                        d.idBuah.namaBuah,
                        d.kuantitas,
                        f"Rp {intcomma(d.subHarga)}",
                        d.tanggalMasuk
                    ])

            pdf_buffer = generate_pdf(
                f"LAPORAN PENGADAAN {start_date} s/d {end_date}",
                data
            )

            return FileResponse(
                pdf_buffer,
                as_attachment=True,
                filename="laporan_pengadaan_rentang_tanggal.pdf"
            )

        # Jika belum submit → tampilkan form
        return render(
            request,
            "core/admin/pengadaan/date_range_form.html",
            {
                "queryset": queryset
            }
        )

    export_pdf_by_date.short_description = "Cetak Laporan (Rentang Tanggal)"


