from web3 import Web3
from django.core.management.base import BaseCommand
from django.conf import settings
from catalog.models import Collection, NFT
from referrals.models import ReferralPayment
import os
import time
import logging
from .abi import abi

logger = logging.getLogger(__name__)


os.environ['NO_PROXY'] = 'binance.org'

class Command(BaseCommand):

    def add_arguments(self, parser):
        # parser.add_argument('address', nargs='1', type=str)
        pass

    def handle(self, *args, **options):
        # address = options['address']
        # w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
        w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_NETWORK))  # Testnet
        # w3 = Web3(Web3.HTTPProvider("https://bsc.getblock.io/testnet/?api_key=25fca00a-e00c-41aa-a9e1-18f64e94e047"))  # Testnet

        # address = Web3.toChecksumAddress('0xdC9e873C1F5354688193472752A5ce006Ed6B4F7'.lower())  # Which one is this?
        address = Web3.toChecksumAddress(settings.BLOCKCHAIN_CONTRACT)

        contract = w3.eth.contract(address=address, abi=abi)



        # Referral Pay
        

        # purchase_nft_filter = contract.events.PurchaseNft.createFilter(fromBlock="0x0")
        # transfer_nft_filter = contract.events.TransferNft.createFilter(fromBlock="0x0")


        while True:
            time.sleep(5)

            # print("New events: ")
            # print(new_collection_filter.get_new_entries())
            # print(referral_pay_filter.get_new_entries())
            # print(add_nft_filter.get_new_entries())
            # print(purchase_nft_filter.get_new_entries())
            # print(transfer_nft_filter.get_new_entries())

            # New Collection
            new_collection_filter = contract.events.NewCollectionContract.createFilter(fromBlock="0x0")
            new_collections = new_collection_filter.get_new_entries()
            logger.info(new_collections)
            for new_collection in new_collections:
                try:
                    contract_address = new_collection['args']['contractAddress'].lower()
                    wallet = new_collection['args']['walletAddress'].lower()
                    username = new_collection['args']['modelName']
                    txhash = 'https://bscscan.com/tx/'.format(str(new_collection['transactionHash']))

                    collection = Collection.objects.filter(kyc_model__username__iexact=username,
                                                           kyc_model__wallet__address__iexact=wallet).first()
                    if collection:
                        collection.address = contract_address
                        collection.txhash = txhash
                        collection.save()
                except Exception as e:
                    logger.error(str(e))

            time.sleep(1)
            referral_pay_filter = contract.events.ReferralPay.createFilter(fromBlock="0x0")
            new_referrals = referral_pay_filter.get_new_entries()
            logger.info(new_referrals)
            for new_referral in new_referrals:
                try:
                    contract_address = new_referral['args']['contractAddress'].lower()
                    from_address = new_referral['args']['from'].lower()
                    to_address = new_referral['args']['to'].lower()
                    amount = new_referral['args']['amount']
                    token_address = new_referral['args']['token'].lower()

                    txhash = 'https://bscscan.com/tx/'.format(str(new_referral['transactionHash']))

                    collection = Collection.objects.filter(address__iexact=contract_address).first()
                    exists = ReferralPayment.objects.filter(txhash__iexact=txhash).exists()

                    if not exists:
                        ReferralPayment.objects.create(collection=collection,
                                                       from_address=from_address,
                                                       to_address=to_address,
                                                       amount=amount,
                                                       token_address=token_address,
                                                       txhash=txhash)
                except Exception as e:
                    logger.error(str(e))

            time.sleep(1)
            add_nft_filter = contract.events.AddNft.createFilter(fromBlock="0x0")
            new_nfts = add_nft_filter.get_new_entries()
            logger.info(new_nfts)
            for new_nft in new_nfts:

                try:
                    contract_address = new_nft['args']['contractAddress'].lower()
                    nftId = new_nft['args']['nftId']
                    uri = new_nft['args']['uri']
                    mintCap = new_nft['args']['mintCap']
                    token_address = new_nft['args']['token'].lower()
                    # price = new_nft['args']['tokenAmount']

                    txhash = 'https://bscscan.com/tx/'.format(str(new_nft['transactionHash']))

                    nft = NFT.objects.filter(collection__address__iexact=contract_address,
                                             uri__iexact=uri).first()
                    if nft:
                        # nft.price = price
                        nft.token_address = token_address
                        nft.mint_cap = mintCap
                        nft.nft_id = nftId
                        nft.txhash = txhash
                        nft.save()

                except Exception as e:
                    logger.error(str(e))

            # print("All events from beginning")
            # print(new_collection_filter.get_all_entries())
            # print(referral_pay_filter.get_all_entries())
            # print(add_nft_filter.get_all_entries())
            # print(purchase_nft_filter.get_all_entries())
            # print(transfer_nft_filter.get_all_entries())


            # print("is connected to bsc: ", w3.isConnected())
