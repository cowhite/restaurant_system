from .views import *
def Initialize(xapp):
    px = "__orders_management__"

    xapp.add_url_rule("/api/v1/orders/new",
        px+"create_order", view_func=create_order, methods=["POST"])
    xapp.add_url_rule("/api/v1/orders/<order_id>/update",
        px+"update_order", view_func=update_order, methods=["PUT"])
    xapp.add_url_rule("/api/v1/<order_status>/orders",
        px+"get_orders_details", view_func=get_orders_details, methods=["GET"])