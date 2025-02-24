import flet as ft

def user_info_view(page, radius_avatar):
    avatar = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
        radius=radius_avatar,
    )
    title = ft.Container(
        content=ft.Text("KIVI Retail DEV", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
        padding=ft.Padding(top=10, right=0, bottom=0, left=0)
    )
    subtitle = ft.Container(
        content=ft.Text("Олександр Риженков", size=26, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREEN_600),
        padding=ft.Padding(top=0, right=0, bottom=10, left=0)
    )
    info = ft.Row(
        alignment="center",
        controls=[
            avatar,
            ft.Column(
                [
                    title,
                    subtitle,
                ],
                alignment="spaceBetween",
                expand=True
            ),
        ],
    )
    return info, avatar, title, subtitle
