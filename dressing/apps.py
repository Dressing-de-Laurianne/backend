import multiprocessing

from django.apps import AppConfig


class DressingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dressing"
    verbose_name = "Dressing API"

    def ready(self):

        from . import shared

        shared.manager = multiprocessing.Manager()
        shared.namespace = shared.manager.Namespace()
        # Initialise tes variables ici
        shared.namespace.TAG_WAIT_ID = None
        shared.namespace.TAG_WAIT_TYPE = None
        shared.namespace.TAG_FOUND_ID = None
        shared.namespace.TAG_FOUND_NAME = None
        shared.namespace.ITEM_FOUND = None
        shared.namespace.HANGER_FOUND = None
        pass
