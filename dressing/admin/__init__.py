from django.contrib import admin

from dressing.admin.hanger import HangerAdmin
from dressing.admin.item import ItemAdmin
from dressing.admin.order import OrderAdmin
from dressing.admin.outfit import OutfitAdmin
from dressing.admin.tag import TagAdmin
from dressing.admin.tag_read import TagReadAdmin
from dressing.models import (
    Hanger,
    Item,
    Order,
    Outfit,
    Tag,
    TagRead,
)

admin.site.register(Hanger, HangerAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Outfit, OutfitAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagRead, TagReadAdmin)
