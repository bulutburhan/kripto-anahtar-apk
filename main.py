import flet as ft
import hashlib
import hmac
import base64

def main(page: ft.Page):
    # 1. AYARLAR
    page.title = "Kripto Anahtar"
    page.theme_mode = ft.ThemeMode.DARK 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.scroll = "adaptive"

    # 2. FONKSİYONLAR
    def sifre_uret(e):
        master_key = txt_master.value
        app_name = txt_app.value

        if not master_key or not app_name:
            page.snack_bar = ft.SnackBar(ft.Text("Lütfen iki alanı da doldurun!"), bgcolor="red400")
            page.snack_bar.open = True
            page.update()
            return

        # Şifreleme
        key_bytes = bytes(master_key, 'utf-8')
        msg_bytes = bytes(app_name.lower().strip(), 'utf-8') 
        
        digester = hmac.new(key_bytes, msg_bytes, hashlib.sha256)
        signature = digester.digest()
        
        generated_pass = base64.b64encode(signature).decode('utf-8')[:16] + "1!" 
        
        lbl_result.value = generated_pass
        lbl_result.color = "green400"
        
        # Kopyalama
        page.set_clipboard(generated_pass)
        
        page.snack_bar = ft.SnackBar(ft.Text("Şifre panoya kopyalandı!"), bgcolor="green900")
        page.snack_bar.open = True
        
        page.update()

    # 3. ARAYÜZ
    icon_logo = ft.Icon(name="security", size=80, color="bluegrey200") 
    title = ft.Text("Anahtar Kripto", size=24, weight="bold", color="white70")
    
    txt_app = ft.TextField(
        label="Uygulama Adı (örn: instagram)", 
        border_color="bluegrey400",
        text_size=16,
        border_radius=15,
        content_padding=20,
        prefix_icon="apps"
    )
    
    txt_master = ft.TextField(
        label="Ana Anahtarın", 
        password=True, 
        can_reveal_password=True, 
        border_color="bluegrey400",
        text_size=16,
        border_radius=15,
        content_padding=20,
        prefix_icon="vpn_key"
    )

    btn_generate = ft.ElevatedButton(
        text="ÜRET VE KOPYALA", 
        on_click=sifre_uret,
        bgcolor="blue800",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        height=55,
        width=250
    )

    lbl_result = ft.Text(
        value="...", 
        size=22, 
        weight=ft.FontWeight.BOLD,
        font_family="monospace",
        selectable=True
    )

    page.add(
        ft.Column(
            [
                icon_logo,
                ft.Container(height=10),
                title,
                ft.Container(height=30),
                txt_app,
                ft.Container(height=10),
                txt_master,
                ft.Container(height=30),
                btn_generate,
                ft.Container(height=30),
                ft.Container(
                    content=lbl_result,
                    padding=15,
                    border_radius=10,
                    # GitHub'ın hata vermemesi için burayı düzelttim:
                    bgcolor=ft.colors.with_opacity(0.1, "white"), 
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

ft.app(target=main)