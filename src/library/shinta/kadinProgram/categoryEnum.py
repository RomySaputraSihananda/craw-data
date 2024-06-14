from enum import Enum

class BaseEnum(Enum):
    ...

class TentangKadinEnum(BaseEnum):
    TENTANG_KADIN  = 'https://kadin.id/tentang-kadin'
    KETUA_UMUM  = 'https://kadin.id/tentang-kadin/ketua-umum'
    STRUKTUR_ORGANISASI  = 'https://kadin.id/tentang-kadin/struktur-organisasi'
    FILOSOFI_LOGO  = 'https://kadin.id/tentang-kadin/filosofi-logo'
    HYMNE_MARS  = 'https://kadin.id/tentang-kadin/hymne-mars'
    SEJARAH_KADIN  = 'https://kadin.id/tentang-kadin/sejarah-kadin'
    PERATURAN_ORGANISASI  = 'https://kadin.id/tentang-kadin/peraturan-organisasi'

    @property
    def identity(self) -> str:
        return 'tentang_kadin'

class ProgramEnum(BaseEnum):
    PROGRAM  = 'https://kadin.id/program'
    INDONESIA_EMAS  = 'https://kadin.id/program/indonesia-emas'
    KADIN_CIPTA  = 'https://kadin.id/program/kadin-cipta'
    NET_ZERO_HUB  = 'https://kadin.id/program/net-zero-hub'
    KEBERLANJUTAN  = 'https://kadin.id/program/keberlanjutan'
    IBU_KOTA_NEGARA  = 'https://kadin.id/program/ibu-kota-negara'
    REFORMASI_PENDIDIKAN_PELATIHAN_VOKASI  = 'https://kadin.id/program/reformasi-pendidikan-pelatihan-vokasi'
    EKONOMI_BIRU  = 'https://kadin.id/program/ekonomi-biru'
    EKONOMI_DIGITAL  = 'https://kadin.id/program/ekonomi-digital'
    KESEHATAN  = 'https://kadin.id/program/kesehatan'
    CIPTA_KERJA  = 'https://kadin.id/program/cipta-kerja'
    BIDANG_ORGANISASI_HUKUM_DAN_KOMUNIKASI  = 'https://kadin.id/program/bidang-organisasi-hukum-dan-komunikasi'
    BIDANG_PEREKONOMIAN  = 'https://kadin.id/program/bidang-perekonomian'
    BIDANG_BIDANG_KEMARITIMAN_INVESTASI_DAN_LUAR_NEGERI  = 'https://kadin.id/program/bidang-bidang-kemaritiman-investasi-dan-luar-negeri'
    BIDANG_PENINGKATAN_KUALITAS_MANUSIA_RISTEK_DAN_INOVASI  = 'https://kadin.id/program/bidang-peningkatan-kualitas-manusia-ristek-dan-inovasi'
    BADAN_BADAN_DAN_POKJA  = 'https://kadin.id/program/badan-badan-dan-pokja'

    @property
    def identity(self) -> str:
        return 'program'

class SolusiBisnisEnum(BaseEnum):
    WIKI_WIRAUSAHA  = 'https://kadin.id/solusi-bisnis/wiki-wirausaha'
    CERTIFICATE_OF_ORIGIN  = 'https://kadin.id/solusi-bisnis/certificate-of-origin'
    BUSINESS_SERVICE_DESK  = 'https://kadin.id/solusi-bisnis/business-service-desk'
    ATA_CARNET  = 'https://kadin.id/solusi-bisnis/ata-carnet'
    APEC_BUSINESS_TRAVEL_CARD  = 'https://kadin.id/solusi-bisnis/apec-business-travel-card'
    KONSULTAN_HUKUM  = 'https://kadin.id/solusi-bisnis/konsultan-hukum'

    @property
    def identity(self) -> str:
        return 'solusi_bisnis'

class MediaEnum(BaseEnum):
    BERITA  = 'https://kadin.id/kabar-kadin'
    INFO_ADVOKASI_MEDIA  = 'https://kadin.id/info-advokasi-media'
    PRESS_RELEASE  = 'https://kadin.id/media/press-release'
    KADIN_NEWSLETTER  = 'https://kadin.id/media/kadin-newsletter'
    INTERNATIONAL_MONDAY  = 'https://kadin.id/media/international-monday'
    ANALISA  = 'https://kadin.id/media/analisa'
    MOUKADIN  = 'https://kadin.id/media/moukadin'
    DOKUMEN  = 'https://kadin.id/dokumen'

    @property
    def identity(self) -> str:
        return 'media'

class PengumumanEnum(BaseEnum):
    KADIN_DALAM_SEPEKAN  = 'https://kadin.id/kadin-dalam-sepekan'
    DAFTAR_INVENTARISASI_ISU_STRATEGIS  = 'https://kadin.id/daftar-inventarisasi-isu-strategis'
    RAPIMNAS_KADIN  = 'https://kadin.id/rapimnas-kadin'
    KADIN_IMPACT_AWARDS  = 'https://kadin.id/kadin-impact-awards'
    
    @property
    def identity(self) -> str:
        return 'pengumuman'
    
class RegulasiBisnisEnum(BaseEnum):
    REGULASI_BISNIS  = 'https://kadin.id/beranda/regulasi-bisnis'
    
    @property
    def identity(self) -> str:
        return 'regulasi_bisnis'

class DataDanStatistikEnum(BaseEnum):
    DATA_DAN_STATISTIK_PROFIL_EKONOMI_INDONESIA  = 'https://kadin.id/data-dan-statistik/profil-ekonomi-indonesia'
    DATA_DAN_STATISTIK_UMKM_INDONESIA  = 'https://kadin.id/data-dan-statistik/umkm-indonesia'
    DATA_DAN_STATISTIK_KETENAGAKERJAAN  = 'https://kadin.id/data-dan-statistik/ketenagakerjaan'
    DATA_DAN_STATISTIK_PROFILE_EKONOMI_PROVINSI  = 'https://kadin.id/data-dan-statistik/profile-ekonomi-provinsi'
    DATA_DAN_STATISTIK_UNGGULAN_EKSPOR_PROVINSI  = 'https://kadin.id/data-dan-statistik/unggulan-ekspor-provinsi'
    DATA_DAN_STATISTIK_POTENSI_PROVINSI  = 'https://kadin.id/data-dan-statistik/potensi-provinsi'
    
    @property
    def identity(self) -> str:
        return 'data_dan_statistik'

class AcaraKadinEnum(BaseEnum):
    ACARA_KADIN  = 'https://kadin.id/acara-kadin'

    @property
    def identity(self) -> str:
        return 'acara'
    

# class KeanggotaanEnum(BaseEnum):
#     ASOSIASI_ASOSIASI_INDUSTRI_PERTANIAN_DAN_KEHUTANAN = "Asosiasi-Asosiasi Industri Pertanian dan Kehutanan"
#     ASOSIASI_ASOSIASI_PETERNAKAN_PERIKANAN_DAN_PENGOLAHAN_MAKANAN = "Asosiasi-Asosiasi Peternakan Perikanan dan Pengolahan Makanan"
#     ASOSIASI_ASOSIASI_INDUSTRI_PERTAMBANGAN_DAN_ENERGI_ = "Asosiasi-Asosiasi Industri Pertambangan dan Energi "
#     ASOSIASI_ASOSIASI_INDUSTRI_PENGOLAHAN_KIMIA = "Asosiasi-Asosiasi Industri Pengolahan Kimia"
#     ASOSIASI_ASOSIASI_INDUSTRI_PENGOLAHAN_LOGAM_DAN_MESIN = "Asosiasi-Asosiasi Industri Pengolahan Logam dan Mesin"
#     ASOSIASI_ASOSIASI_INDUSTRI_PENGOLAHAN_LAIN_LAINNYA = "Asosiasi-Asosiasi Industri Pengolahan Lain-Lainnya"
#     ASOSIASI_ASOSIASI_JASA_PERDAGANGAN_DAN_JASA_EXPOR_IMPOR = "Asosiasi-Asosiasi Jasa Perdagangan dan Jasa Expor-Impor"
#     ASOSIASI_ASOSIASI_JASA_KONSTRUKSI_DAN_PROPERTI = "Asosiasi-Asosiasi Jasa Konstruksi dan Properti"
#     ASOSIASI_ASOSIASI_JASA_KEUANGAN_DAN_JASA_PROFESI = "Asosiasi-Asosiasi Jasa Keuangan dan Jasa Profesi"
#     ASOSIASI_ASOSIASI_JASA_PERHUBUNGAN_DAN_LOGISTIK = "Asosiasi-Asosiasi Jasa Perhubungan Dan Logistik"
#     ASOSIASI__ASOSIASI_,PERPOSAN,_MEDIA_MASSA,_TEKNOLOGI_KOMUNIKASI_DAN_INFORMASI = "Asosiasi - Asosiasi ,Perposan, Media Massa, Teknologi Komunikasi dan Informasi"
#     ASOSIASI_ASOSIASI_PARIWISATA_HOTEL_RESTORAN,_MICE = "Asosiasi-Asosiasi Pariwisata, Hotel &Restoran, MICE"
#     ASOSIASI_ASOSIASI_PENYEDIA_JASA__TENAGA_KERJA = "Asosiasi-Asosiasi Penyedia Jasa  Tenaga Kerja"
#     ASOSIASI_ASOSIASI_PENYEDIA_JASA_LAINNYA = "Asosiasi-Asosiasi Penyedia Jasa Lainnya"
#     HIMPUNAN_DAN_DEWAN_BISNIS = "Himpunan dan Dewan Bisnis"
#     @property
#     def identity(self) -> str:
#         return 'keanggotaan'