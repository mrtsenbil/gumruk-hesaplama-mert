# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
from urllib.request import urlopen
import xml.etree.ElementTree as ET


# ============================================================
# RENKLER
# ============================================================

BG = "#1e2329"
PANEL = "#252b33"
PANEL_2 = "#2d333b"
HEADER = "#11161c"

WHITE = "#ffffff"
TEXT = "#f2f2f2"
SUBTEXT = "#b8c0ca"

BLUE = "#1976d2"
BLUE_LIGHT = "#2196f3"

GREEN = "#168a4a"
GREEN_LIGHT = "#20a85a"

RED = "#c62828"
YELLOW = "#e0a800"

INPUT_BG = "#ffffff"
INPUT_TEXT = "#111111"

ROW_1 = "#292f37"
ROW_2 = "#242a31"


# ============================================================
# TARİFE LİSTESİ
# ============================================================

TARIFE = {

    # İHRACAT
    "İHR-1(HAVA-KARA)": 2050,
    "İHR-1 (DENİZ)": 2670,
    "İHR-2": 4100,
    "İHR-3": 4100,
    "İHR-4": 2740,
    "İHR-5": 5470,
    "İHR-6": 2740,
    "İHR-7": 8260,
    "İHR-8": 690,
    "İHR-9": 50,

    # İTHALAT
    "İTH-1 HAVA": 3320,
    "İTH-1 KARA": 3390,
    "İTH-2": 4670,
    "İTH-3": 2160,
    "İTH-4": 12900,
    "İTH-5": 10140,
    "İTH-6": 5470,
    "İTH-7": 3900,
    "İTH-8": 4670,
    "İTH-9": 8140,

    # İTH-10 CIF KADEMELİ
    "İTH-10": 0,

    "İTH-11": 2090,
    "İTH-12": 3410,

    # İTH-13 CIF KADEMELİ
    "İTH-13": 0,

    "İTH-14": 1350,
    "İTH-15": 70,

    # TRANSİT
    "TR-1": 3670,
    "TR-2": 940,

    # ANTREPO
    "ANT-1": 1350,
    "ANT-2": 3670,
    "ANT-3": 1000,

    # ÖZELLİK ARZ EDEN
    "SB-1": 1350,
    "ÖZ-1": 900,
    "ÖZ-2": 2160,
    "ÖZ-3": 1590,
    "ÖZ-4": 940,
    "ÖZ-5": 350,
}


KODLAR = list(TARIFE.keys())


# ============================================================
# SAYI ÇEVİR
# ============================================================

def sayiya_cevir(deger):

    if deger is None:
        return 0.0

    metin = str(deger).strip()

    if metin == "":
        return 0.0

    try:

        if "," in metin and "." in metin:

            if metin.rfind(",") > metin.rfind("."):

                metin = metin.replace(".", "")
                metin = metin.replace(",", ".")

            else:

                metin = metin.replace(",", "")

        elif "," in metin:

            metin = metin.replace(",", ".")

        return float(metin)

    except:

        return 0.0


# ============================================================
# TL FORMAT
# ============================================================

def tl_format(tutar):

    metin = "{:,.2f}".format(tutar)

    metin = metin.replace(",", "X")
    metin = metin.replace(".", ",")
    metin = metin.replace("X", ".")

    return metin + " TL"


# ============================================================
# TCMB USD KURU
# ============================================================

def tcmb_usd_kuru():

    adres = "https://www.tcmb.gov.tr/kurlar/today.xml"

    veri = urlopen(
        adres,
        timeout=15
    ).read()

    root = ET.fromstring(veri)

    for currency in root.findall("Currency"):

        if currency.get("CurrencyCode") == "USD":

            forex_buying = currency.find(
                "ForexBuying"
            )

            if forex_buying is not None:

                return float(
                    forex_buying.text.replace(
                        ",",
                        "."
                    )
                )

    raise Exception(
        "USD kuru bulunamadı."
    )


# ============================================================
# İTH-10 HESAPLAMA
# ============================================================

def ith10_hesapla(cif_usd):

    if cif_usd <= 500000:

        return 8140.0

    elif cif_usd <= 1000000:

        return 10740.0

    elif cif_usd <= 1500000:

        return 13340.0

    else:

        return 15940.0


# ============================================================
# İTH-13 HESAPLAMA
#
# 0 - 15.000 USD:
# Tarifedeki temel ücret uygulanır.
#
# Bu programda İTH-13 için temel ücret:
# 0 TL kabul edilmiştir.
#
# 15.000 USD üzerindeki kısım:
#
# 15.000 - 225.000     %0,3
# 225.000 - 2.000.000   %0,1
# 2.000.000 - 10.000.000 %0,01
# 10.000.000 üzeri       %0,003
# ============================================================

def ith13_hesapla(cif_usd, usd_tl):

    if cif_usd <= 15000:

        return 0.0


    # 15.000 USD çıkarılıyor

    kalan = cif_usd - 15000.0


    # --------------------------------------------------------
    # B DİLİMİ
    # 15.000 - 225.000
    # 210.000 USD
    # %0,3
    # --------------------------------------------------------

    b_matrah = min(
        kalan,
        210000.0
    )

    b_usd = (
        b_matrah * 0.003
    )

    kalan -= b_matrah


    # --------------------------------------------------------
    # C DİLİMİ
    # 225.000 - 2.000.000
    # 1.775.000 USD
    # %0,1
    # --------------------------------------------------------

    c_usd = 0.0

    if kalan > 0:

        c_matrah = min(
            kalan,
            1775000.0
        )

        c_usd = (
            c_matrah * 0.001
        )

        kalan -= c_matrah


    # --------------------------------------------------------
    # D DİLİMİ
    # 2.000.000 - 10.000.000
    # 8.000.000 USD
    # %0,01
    # --------------------------------------------------------

    d_usd = 0.0

    if kalan > 0:

        d_matrah = min(
            kalan,
            8000000.0
        )

        d_usd = (
            d_matrah * 0.0001
        )

        kalan -= d_matrah


    # --------------------------------------------------------
    # 10.000.000 USD ÜZERİ
    #
    # CIF kıymetin %0,003'ü
    # --------------------------------------------------------

    if cif_usd > 10000000:

        toplam_usd = (
            cif_usd * 0.00003
        )

    else:

        toplam_usd = (
            b_usd +
            c_usd +
            d_usd
        )


    # USD → TL

    toplam_tl = (
        toplam_usd * usd_tl
    )


    return toplam_tl


# ============================================================
# ANA PENCERE
# ============================================================

pencere = tk.Tk()

pencere.title(
    "2026 Gümrük Müşavirliği Ücret Hesaplama"
)

# Daha kompakt pencere
pencere.geometry(
    "1100x880"
)

pencere.configure(
    bg=BG
)

pencere.resizable(
    False,
    False
)


# ============================================================
# TK STYLE
# ============================================================

style = ttk.Style()

try:

    style.theme_use("clam")

except:

    pass


style.configure(
    "TCombobox",
    padding=2
)


# ============================================================
# BAŞLIK
# ============================================================

baslik_frame = tk.Frame(
    pencere,
    bg=HEADER,
    height=58
)

baslik_frame.pack(
    fill="x"
)

baslik_frame.pack_propagate(
    False
)


tk.Label(
    baslik_frame,
    text="2026 GÜMRÜK MÜŞAVİRLİĞİ ÜCRET HESAPLAMA",
    bg=HEADER,
    fg=WHITE,
    font=("Arial", 16, "bold")
).pack(
    pady=(9, 1)
)


tk.Label(
    baslik_frame,
    text="İthalat • İhracat • Transit • Antrepo • Özellik Arz Eden İşlemler",
    bg=HEADER,
    fg=SUBTEXT,
    font=("Arial", 8)
).pack()


# ============================================================
# KUR PANELİ
# ============================================================

kur_frame = tk.Frame(
    pencere,
    bg=PANEL,
    bd=1,
    relief="solid"
)

kur_frame.pack(
    fill="x",
    padx=15,
    pady=(8, 4)
)


tk.Label(
    kur_frame,
    text="USD KURU",
    bg=PANEL,
    fg=BLUE_LIGHT,
    font=("Arial", 10, "bold")
).pack(
    side="left",
    padx=(12, 8)
)


tk.Label(
    kur_frame,
    text="USD/TL:",
    bg=PANEL,
    fg=TEXT,
    font=("Arial", 9, "bold")
).pack(
    side="left"
)


genel_kur_entry = tk.Entry(
    kur_frame,
    width=13,
    bg=INPUT_BG,
    fg=INPUT_TEXT,
    font=("Arial", 10, "bold"),
    relief="flat"
)

genel_kur_entry.pack(
    side="left",
    padx=5,
    pady=6,
    ipady=3
)


# ============================================================
# TCMB KUR BUTONU
# ============================================================

def tcmb_kur_getir():

    try:

        kur = tcmb_usd_kuru()

        metin = "{:.4f}".format(
            kur
        )

        metin = metin.replace(
            ".",
            ","
        )


        genel_kur_entry.delete(
            0,
            tk.END
        )

        genel_kur_entry.insert(
            0,
            metin
        )


        # SADECE İTH-13 SATIRLARINA KUR YAZ

        for i in range(15):

            kod = (
                kod_entries[i]
                .get()
                .strip()
            )

            if kod == "İTH-13":

                kur_entries[i].delete(
                    0,
                    tk.END
                )

                kur_entries[i].insert(
                    0,
                    metin
                )


        hesapla()


    except Exception as hata:

        messagebox.showerror(
            "TCMB Kuru Alınamadı",
            "TCMB'den USD kuru alınamadı.\n\n"
            + str(hata)
        )


tk.Button(
    kur_frame,
    text="TCMB GÜNCEL KURU GETİR",
    command=tcmb_kur_getir,
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE_LIGHT,
    activeforeground=WHITE,
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=5
).pack(
    side="left",
    padx=8
)


tk.Label(
    kur_frame,
    text="Geçmiş kur kullanacaksanız İTH-13 satırındaki USD/TL alanına manuel kur girebilirsiniz.",
    bg=PANEL,
    fg=SUBTEXT,
    font=("Arial", 8)
).pack(
    side="left",
    padx=5
)


# ============================================================
# TABLO
# ============================================================

tablo_panel = tk.Frame(
    pencere,
    bg=PANEL,
    bd=1,
    relief="solid"
)

tablo_panel.pack(
    fill="x",
    padx=15,
    pady=4
)


tk.Label(
    tablo_panel,
    text="HİZMET GİRİŞLERİ",
    bg=PANEL,
    fg=BLUE_LIGHT,
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=0,
    columnspan=7,
    sticky="w",
    padx=10,
    pady=5
)


basliklar = [
    "NO",
    "HİZMET KODU",
    "ADET",
    "CIF USD",
    "USD/TL",
    "BİRİM ÜCRET",
    "SATIR TOPLAMI"
]


for i, baslik in enumerate(basliklar):

    tk.Label(
        tablo_panel,
        text=baslik,
        bg=HEADER,
        fg=WHITE,
        font=("Arial", 8, "bold"),
        pady=4
    ).grid(
        row=1,
        column=i,
        sticky="nsew",
        padx=1,
        pady=1
    )


# ============================================================
# ALAN LİSTELERİ
# ============================================================

kod_entries = []
adet_entries = []
cif_entries = []
kur_entries = []

birim_labels = []
toplam_labels = []


# ============================================================
# KOD SEÇME PENCERESİ
# ============================================================

def kod_sec(index):

    popup = tk.Toplevel(
        pencere
    )

    popup.title(
        "Hizmet Kodu Seç"
    )

    popup.geometry(
        "430x500"
    )

    popup.configure(
        bg=BG
    )

    popup.grab_set()


    tk.Label(
        popup,
        text="HİZMET KODU SEÇ",
        bg=BG,
        fg=WHITE,
        font=("Arial", 13, "bold")
    ).pack(
        pady=(12, 5)
    )


    arama = tk.Entry(
        popup,
        width=36,
        bg=INPUT_BG,
        fg=INPUT_TEXT,
        font=("Arial", 10)
    )

    arama.pack(
        pady=6,
        ipady=4
    )


    liste_frame = tk.Frame(
        popup,
        bg=BG
    )

    liste_frame.pack(
        fill="both",
        expand=True,
        padx=12
    )


    liste = tk.Listbox(
        liste_frame,
        bg=PANEL_2,
        fg=WHITE,
        selectbackground=BLUE,
        selectforeground=WHITE,
        font=("Arial", 9),
        relief="flat"
    )

    liste.pack(
        side="left",
        fill="both",
        expand=True
    )


    scrollbar = tk.Scrollbar(
        liste_frame,
        command=liste.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    liste.config(
        yscrollcommand=scrollbar.set
    )


    def liste_doldur():

        liste.delete(
            0,
            tk.END
        )

        aranan = (
            arama.get()
            .strip()
            .upper()
        )

        for kod in KODLAR:

            if (
                aranan == ""
                or aranan in kod.upper()
            ):

                liste.insert(
                    tk.END,
                    kod
                )


    liste_doldur()


    arama.bind(
        "<KeyRelease>",
        lambda event:
        liste_doldur()
    )


    def sec():

        secimler = (
            liste.curselection()
        )

        if not secimler:
            return


        kod = liste.get(
            secimler[0]
        )


        kod_entries[index].set(
            kod
        )


        # İTH-13 seçildiğinde
        # genel kur sadece o satıra aktarılır

        if kod == "İTH-13":

            kur = (
                genel_kur_entry.get()
                .strip()
            )

            if kur != "":

                kur_entries[index].delete(
                    0,
                    tk.END
                )

                kur_entries[index].insert(
                    0,
                    kur
                )


        popup.destroy()

        hesapla()


    tk.Button(
        popup,
        text="SEÇ",
        command=sec,
        bg=BLUE,
        fg=WHITE,
        activebackground=BLUE_LIGHT,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=35,
        pady=6
    ).pack(
        pady=8
    )


    liste.bind(
        "<Double-Button-1>",
        lambda event:
        sec()
    )


# ============================================================
# HESAPLAMA
# ============================================================

def hesapla():

    genel_toplam = 0.0


    for i in range(15):

        kod = (
            kod_entries[i]
            .get()
            .strip()
        )


        # ----------------------------------------------------
        # BOŞ SATIR
        # ----------------------------------------------------

        if kod == "":

            birim_labels[i].config(
                text=""
            )

            toplam_labels[i].config(
                text=""
            )

            continue


        adet = sayiya_cevir(
            adet_entries[i].get()
        )

        if adet <= 0:

            adet = 1


        satir_toplam = 0.0


        # ====================================================
        # İTH-13
        # ====================================================

        if kod == "İTH-13":

            cif = sayiya_cevir(
                cif_entries[i].get()
            )

            kur = sayiya_cevir(
                kur_entries[i].get()
            )


            if cif <= 0:

                birim_labels[i].config(
                    text="CIF GİRİNİZ",
                    fg=YELLOW
                )

                toplam_labels[i].config(
                    text=""
                )

                continue


            if kur <= 0:

                birim_labels[i].config(
                    text="KUR GİRİNİZ",
                    fg=YELLOW
                )

                toplam_labels[i].config(
                    text=""
                )

                continue


            birim = ith13_hesapla(
                cif,
                kur
            )


            satir_toplam = (
                birim * adet
            )


            birim_labels[i].config(
                text=tl_format(birim),
                fg=GREEN_LIGHT
            )


        # ====================================================
        # İTH-10
        # ====================================================

        elif kod == "İTH-10":

            cif = sayiya_cevir(
                cif_entries[i].get()
            )


            if cif <= 0:

                birim_labels[i].config(
                    text="CIF GİRİNİZ",
                    fg=YELLOW
                )

                toplam_labels[i].config(
                    text=""
                )

                continue


            birim = ith10_hesapla(
                cif
            )


            satir_toplam = (
                birim * adet
            )


            birim_labels[i].config(
                text=tl_format(birim),
                fg=GREEN_LIGHT
            )


        # ====================================================
        # DİĞER HİZMETLER
        # ====================================================

        elif kod in TARIFE:

            birim = TARIFE[kod]


            satir_toplam = (
                birim * adet
            )


            birim_labels[i].config(
                text=tl_format(birim),
                fg=TEXT
            )


        else:

            birim_labels[i].config(
                text="GEÇERSİZ KOD",
                fg=RED
            )

            toplam_labels[i].config(
                text=""
            )

            continue


        toplam_labels[i].config(
            text=tl_format(
                satir_toplam
            ),
            fg=GREEN_LIGHT
        )


        # GENEL TOPLAMA EKLE

        genel_toplam += satir_toplam


    # ========================================================
    # KDV
    # ========================================================

    kdv = (
        genel_toplam * 0.20
    )


    # ========================================================
    # KDV DAHİL
    # ========================================================

    kdv_dahil = (
        genel_toplam + kdv
    )


    # ========================================================
    # SONUÇLARI GÖSTER
    # ========================================================

    kdv_haric_label.config(
        text=tl_format(
            genel_toplam
        )
    )


    kdv_label.config(
        text=tl_format(
            kdv
        )
    )


    kdv_dahil_label.config(
        text=tl_format(
            kdv_dahil
        )
    )


# ============================================================
# TEMİZLE
# ============================================================

def temizle():

    for i in range(15):

        kod_entries[i].set("")


        adet_entries[i].delete(
            0,
            tk.END
        )

        adet_entries[i].insert(
            0,
            "1"
        )


        cif_entries[i].delete(
            0,
            tk.END
        )


        kur_entries[i].delete(
            0,
            tk.END
        )


        birim_labels[i].config(
            text=""
        )


        toplam_labels[i].config(
            text=""
        )


    genel_kur_entry.delete(
        0,
        tk.END
    )


    kdv_haric_label.config(
        text="0,00 TL"
    )


    kdv_label.config(
        text="0,00 TL"
    )


    kdv_dahil_label.config(
        text="0,00 TL"
    )


# ============================================================
# 15 SATIR OLUŞTUR
# ============================================================

for i in range(15):

    satir_rengi = (
        ROW_1
        if i % 2 == 0
        else ROW_2
    )


    # --------------------------------------------------------
    # NO
    # --------------------------------------------------------

    tk.Label(
        tablo_panel,
        text=str(i + 1),
        bg=satir_rengi,
        fg=SUBTEXT,
        font=("Arial", 8, "bold")
    ).grid(
        row=i + 2,
        column=0,
        sticky="nsew",
        padx=1,
        pady=1,
        ipady=2
    )


    # --------------------------------------------------------
    # KOD
    # --------------------------------------------------------

    kod_frame = tk.Frame(
        tablo_panel,
        bg=satir_rengi
    )

    kod_frame.grid(
        row=i + 2,
        column=1,
        sticky="nsew",
        padx=1,
        pady=1
    )


    kod_entry = ttk.Combobox(
        kod_frame,
        values=KODLAR,
        width=25,
        font=("Arial", 8)
    )

    kod_entry.pack(
        side="left",
        padx=(2, 1),
        pady=2
    )


    tk.Button(
        kod_frame,
        text="...",
        width=2,
        command=lambda x=i:
        kod_sec(x),
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        font=("Arial", 8, "bold")
    ).pack(
        side="right",
        padx=1
    )


    kod_entries.append(
        kod_entry
    )


    # --------------------------------------------------------
    # ADET
    # --------------------------------------------------------

    adet_entry = tk.Entry(
        tablo_panel,
        width=7,
        bg=INPUT_BG,
        fg=INPUT_TEXT,
        font=("Arial", 8)
    )

    adet_entry.insert(
        0,
        "1"
    )

    adet_entry.grid(
        row=i + 2,
        column=2,
        sticky="nsew",
        padx=2,
        pady=2,
        ipady=1
    )

    adet_entries.append(
        adet_entry
    )


    # --------------------------------------------------------
    # CIF USD
    # --------------------------------------------------------

    cif_entry = tk.Entry(
        tablo_panel,
        width=13,
        bg=INPUT_BG,
        fg=INPUT_TEXT,
        font=("Arial", 8)
    )

    cif_entry.grid(
        row=i + 2,
        column=3,
        sticky="nsew",
        padx=2,
        pady=2,
        ipady=1
    )

    cif_entries.append(
        cif_entry
    )


    # --------------------------------------------------------
    # USD/TL
    # --------------------------------------------------------

    kur_entry = tk.Entry(
        tablo_panel,
        width=11,
        bg=INPUT_BG,
        fg=INPUT_TEXT,
        font=("Arial", 8)
    )

    kur_entry.grid(
        row=i + 2,
        column=4,
        sticky="nsew",
        padx=2,
        pady=2,
        ipady=1
    )

    kur_entries.append(
        kur_entry
    )


    # --------------------------------------------------------
    # BİRİM ÜCRET
    # --------------------------------------------------------

    birim_label = tk.Label(
        tablo_panel,
        text="",
        anchor="e",
        bg=satir_rengi,
        fg=TEXT,
        font=("Arial", 8)
    )

    birim_label.grid(
        row=i + 2,
        column=5,
        sticky="nsew",
        padx=2,
        pady=1,
        ipady=2
    )

    birim_labels.append(
        birim_label
    )


    # --------------------------------------------------------
    # SATIR TOPLAMI
    # --------------------------------------------------------

    toplam_label = tk.Label(
        tablo_panel,
        text="",
        anchor="e",
        bg=satir_rengi,
        fg=GREEN_LIGHT,
        font=("Arial", 8, "bold")
    )

    toplam_label.grid(
        row=i + 2,
        column=6,
        sticky="nsew",
        padx=2,
        pady=1,
        ipady=2
    )

    toplam_labels.append(
        toplam_label
    )


# ============================================================
# OTOMATİK HESAPLAMA
# ============================================================

for i in range(15):

    kod_entries[i].bind(
        "<<ComboboxSelected>>",
        lambda event:
        hesapla()
    )

    adet_entries[i].bind(
        "<KeyRelease>",
        lambda event:
        hesapla()
    )

    cif_entries[i].bind(
        "<KeyRelease>",
        lambda event:
        hesapla()
    )

    kur_entries[i].bind(
        "<KeyRelease>",
        lambda event:
        hesapla()
    )


# ============================================================
# BUTONLAR
# ============================================================

buton_frame = tk.Frame(
    pencere,
    bg=BG
)

buton_frame.pack(
    pady=6
)


tk.Button(
    buton_frame,
    text="HESAPLA",
    command=hesapla,
    bg=GREEN,
    fg=WHITE,
    activebackground=GREEN_LIGHT,
    activeforeground=WHITE,
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    padx=45,
    pady=6
).grid(
    row=0,
    column=0,
    padx=6
)


tk.Button(
    buton_frame,
    text="TÜMÜNÜ TEMİZLE",
    command=temizle,
    bg=RED,
    fg=WHITE,
    activebackground="#e53935",
    activeforeground=WHITE,
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    padx=25,
    pady=6
).grid(
    row=0,
    column=1,
    padx=6
)


# ============================================================
# SONUÇ PANELİ
# ============================================================

sonuc_frame = tk.Frame(
    pencere,
    bg=PANEL,
    bd=2,
    relief="solid"
)

sonuc_frame.pack(
    fill="x",
    padx=15,
    pady=(2, 8)
)


tk.Label(
    sonuc_frame,
    text="HESAPLAMA SONUÇLARI",
    bg=PANEL,
    fg=BLUE_LIGHT,
    font=("Arial", 9, "bold")
).grid(
    row=0,
    column=0,
    columnspan=2,
    pady=(5, 2)
)


# ============================================================
# KDV HARİÇ
# ============================================================

tk.Label(
    sonuc_frame,
    text="KDV HARİÇ TOPLAM:",
    bg=PANEL,
    fg=TEXT,
    font=("Arial", 10, "bold")
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=25,
    pady=2
)


kdv_haric_label = tk.Label(
    sonuc_frame,
    text="0,00 TL",
    bg=PANEL,
    fg=TEXT,
    font=("Arial", 11, "bold")
)

kdv_haric_label.grid(
    row=1,
    column=1,
    sticky="e",
    padx=25,
    pady=2
)


# ============================================================
# KDV
# ============================================================

tk.Label(
    sonuc_frame,
    text="%20 KDV:",
    bg=PANEL,
    fg=YELLOW,
    font=("Arial", 10, "bold")
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=25,
    pady=2
)


kdv_label = tk.Label(
    sonuc_frame,
    text="0,00 TL",
    bg=PANEL,
    fg=YELLOW,
    font=("Arial", 11, "bold")
)

kdv_label.grid(
    row=2,
    column=1,
    sticky="e",
    padx=25,
    pady=2
)


# ============================================================
# KDV DAHİL GENEL TOPLAM
# ============================================================

kdv_dahil_frame = tk.Frame(
    sonuc_frame,
    bg=GREEN
)

kdv_dahil_frame.grid(
    row=3,
    column=0,
    columnspan=2,
    sticky="ew",
    padx=10,
    pady=6
)


tk.Label(
    kdv_dahil_frame,
    text="KDV DAHİL GENEL TOPLAM",
    bg=GREEN,
    fg=WHITE,
    font=("Arial", 11, "bold")
).pack(
    side="left",
    padx=15,
    pady=7
)


kdv_dahil_label = tk.Label(
    kdv_dahil_frame,
    text="0,00 TL",
    bg=GREEN,
    fg=WHITE,
    font=("Arial", 14, "bold")
)

kdv_dahil_label.pack(
    side="right",
    padx=20,
    pady=5
)


# ============================================================
# SÜTUN GENİŞLİKLERİ
# ============================================================

tablo_panel.grid_columnconfigure(
    0,
    minsize=35
)

tablo_panel.grid_columnconfigure(
    1,
    minsize=250
)

tablo_panel.grid_columnconfigure(
    2,
    minsize=65
)

tablo_panel.grid_columnconfigure(
    3,
    minsize=115
)

tablo_panel.grid_columnconfigure(
    4,
    minsize=100
)

tablo_panel.grid_columnconfigure(
    5,
    minsize=145
)

tablo_panel.grid_columnconfigure(
    6,
    minsize=175
)


sonuc_frame.grid_columnconfigure(
    0,
    minsize=400
)

sonuc_frame.grid_columnconfigure(
    1,
    minsize=300
)


# ============================================================
# BAŞLANGIÇ
# ============================================================

pencere.mainloop()
