from django.core.management.base import BaseCommand, CommandError
from spiral.models import *
from spiral.publisher.SaveContent import refreshContent
from spiral.es_spiral.es_utils import refreshdbtoes
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def handle(self, *args, **options):
        import crsq.tagfilegenerators import *
        return

