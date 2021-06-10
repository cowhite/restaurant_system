from .views import *
def Initialize(xapp):
    px = "__table_management__"

    xapp.add_url_rule("/api/v1/tables/new",
        px+"add_table", view_func=add_table, methods=["POST"])
    xapp.add_url_rule("/api/v1/tables/<_id>/",
        px+"delete_table", view_func=delete_table, methods=["DELETE"])
    xapp.add_url_rule("/api/v1/tables/<_id>/update",
        px+"update_table", view_func=update_table, methods=["PUT"])
