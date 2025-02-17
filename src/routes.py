from views.news_feed_view import news_feed_view
from views.order_view import order_view
from views.favorites_view import favorites_view
from views.user_info_view import user_info_view
import flet as ft

def route_change(route, content, page):
    content.controls.clear()

    if route == "/news_feed":
        content.controls.append(news_feed_view(page))
    elif route == "/order":
        content.controls.append(order_view(page))
    elif route == "/favorites":
        content.controls.append(favorites_view(page))
    elif route == "/user_info":
        content.controls.append(user_info_view(page))
    else:
        content.controls.append(ft.Text("Добро пожаловать в Kivi Retail!", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER))
    
    content.update()
