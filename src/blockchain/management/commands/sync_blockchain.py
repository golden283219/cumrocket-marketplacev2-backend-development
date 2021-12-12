from django.core.management.base import BaseCommand
import os
import logging

from blockchain.tasks import sync_blockchain

logger = logging.getLogger(__name__)


os.environ['NO_PROXY'] = 'binance.org'


class Command(BaseCommand):

    def add_arguments(self, parser):
        # parser.add_argument('address', nargs='1', type=str)
        pass

    def handle(self, *args, **options):
        sync_blockchain()
