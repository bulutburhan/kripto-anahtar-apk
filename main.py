import flet as ft
import hashlib
import base64

def main(page: ft.Page):
    page.title = "CipherVault"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 390
    page.window.height = 750
    
    # --- 1. FONKSİYONLAR ---

    # Kayıtlı servisleri hafızadan çekelim, yoksa boş liste başlatalım
    def servisleri_getir():
        return page.client_storage.get("servisler") or []

    # Yeni servis ekleme
    def servis_ekle(e):
        if yeni_servis_input.value:
            mevcut_liste = servisleri_getir()
            mevcut_liste.append(yeni_servis_input.value)
            page.client_storage.set("servisler", mevcut_liste) # Hafızaya kaydet
            yeni_servis_input.value = ""
            listeyi_guncelle()
            page.update()

    # Bir servise tıklayınca şifre üretme ekranına veriyi taşıma
    def servise_tikla(servis_adi):
        txt_servis.value = servis_adi # Ana ekrandaki kutuyu doldur
        page.go("/uret") # Üretim sayfasına git

    # Servis silme (Opsiyonel)
    def servis_sil(servis_adi):
        mevcut_liste = servisleri_getir()
        if servis_adi in mevcut_liste:
            mevcut_liste.remove(servis_adi)
            page.client_storage.set("servisler", mevcut_liste)
            listeyi_guncelle()

    # Listeyi ekrana çizme
    servisler_kolonu = ft.Column()

    def listeyi_guncelle():
        servisler_kolonu.controls.clear()
        kayitli_liste = servisleri_getir()
        
        for servis in kayitli_liste:
            servisler_kolonu.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.KEY),
                    title=ft.Text(servis),
                    on_click=lambda e, x=servis: servise_tikla(x), # Tıklayınca seç
                    trailing=ft.IconButton(
                        ft.icons.DELETE_OUTLINE, 
                        on_click=lambda e, x=servis: servis_sil(x)
                    )
                )
            )
        page.update()

    # --- 2. SAYFALAR ---
    
    # Giriş/Liste Sayfası Elemanları
    yeni_servis_input = ft.TextField(hint_text="Yeni Servis Ekle (örn: Twitter)", expand=True)
    ekle_btn = ft.IconButton(ft.icons.ADD_CIRCLE, on_click=servis_ekle, icon_color="green")

    # Şifre Üretme Sayfası Elemanları
    txt_servis = ft.TextField(label="Servis Adı (Otomatik Gelir)")
    txt_anahtar = ft.TextField(label="Gizli Anahtarın", password=True, can_reveal_password=True)
    txt_sonuc = ft.TextField(label="Oluşturulan Şifre", read_only=True)
    
    def sifre_uret(e):
        # Senin klasik şifre üretme kodun buraya...
        if not txt_servis.value or not txt_anahtar.value:
            return
        
        birlestirilmis = txt_servis.value + txt_anahtar.value
        imza = hashlib.sha256(birlestirilmis.encode()).digest()
        sonuc = base64.b64encode(imza).decode('utf-8')[:16]
        txt_sonuc.value = sonuc
        page.update()

    # Sayfa Yönlendirme Sistemi (Routing)
    def route_change(e):
        page.views.clear()
        
        # 1. SAYFA: SERVİS LİSTESİ
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Kasam"), bgcolor="bluegrey900"),
                    ft.Row([yeni_servis_input, ekle_btn]),
                    ft.Divider(),
                    ft.Text("Kayıtlı Servislerin:", size=16, weight="bold"),
                    servisler_kolonu
                ]
            )
        )

        # 2. SAYFA: ŞİFRE ÜRETME
        if page.route == "/uret":
            page.views.append(
                ft.View(
                    "/uret",
                    [
                        ft.AppBar(title=ft.Text("Şifre Üret")),
                        txt_servis,
                        txt_anahtar,
                        ft.ElevatedButton("Oluştur", on_click=sifre_uret),
                        txt_sonuc,
                        ft.IconButton(ft.icons.COPY, on_click=lambda e: page.set_clipboard(txt_sonuc.value))
                    ]
                )
            )
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    listeyi_guncelle() # Uygulama açılınca listeyi yükle
    page.go(page.route)

ft.app(target=main)
