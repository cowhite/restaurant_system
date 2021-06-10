from .views import *
def Initialize(xapp):
    px = "__menu_management__"

    xapp.add_url_rule("/api/v1/menu_details",
        px+"get_menu_details", view_func=get_menu_details, methods=["GET"])
    xapp.add_url_rule("/api/v1/menu_items/new",
        px+"add_menu_items", view_func=add_menu_items, methods=["POST"])
    xapp.add_url_rule("/api/v1/menu_items/update",
        px+"update_menu_item", view_func=update_menu_item, methods=["PUT"])
