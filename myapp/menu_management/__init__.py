from .views import *
def Initialize(xapp):
    px = "__menu_management__"


    xapp.add_url_rule("/api/v1/menu_items/new",
        px+"add_menu_items", view_func=add_menu_items, methods=["POST"])
    xapp.add_url_rule("/api/v1/menu_items/update",
        px+"update_menu_item", view_func=update_menu_item, methods=["PUT"])
    xapp.add_url_rule("/api/v1/menu_items/<_id>",
        px+"delete_menu_item", view_func=delete_menu_item, methods=["DELETE"])

