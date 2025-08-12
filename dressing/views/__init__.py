from dressing.views.hanger import HangerDetail, HangerList
from dressing.views.item import ItemDetail, ItemList
from dressing.views.order import OrderDetail, OrderList
from dressing.views.outfit import OutfitDetail, OutfitList
from dressing.views.tag import TagDetail, TagList
from dressing.views.tag_read import TagReadDetail, TagReadList, tag_wait
from dressing.views.user import UserViewSet

__all__ = [
    "HangerList",
    "HangerDetail",
    "ItemList",
    "ItemDetail",
    "OrderList",
    "OrderDetail",
    "OutfitList",
    "OutfitDetail",
    "TagList",
    "TagDetail",
    "TagReadList",
    "TagReadDetail",
    "tag_wait",
    "UserViewSet",
]
