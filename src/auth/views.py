from django.http import Http404, HttpResponse, JsonResponse
from django.core.cache import cache
from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from magiclink.helpers import create_magiclink
from magiclink import settings as magiclink_settings
from magiclink.models import MagicLink, MagicLinkError
from django.contrib.auth import authenticate, get_user_model, login, logout
from web3 import Web3
from eth_account.messages import defunct_hash_message
from django.utils.crypto import get_random_string
from uuid import uuid4
from kyc.models import KYCModel, Wallet
from django.contrib.auth import get_user_model

import logging

log = logging.getLogger(__name__)


class LoginAPIView(views.APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        if not email:
            response = {'status': 'No email given'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        magiclink = create_magiclink(email, request, redirect_url='')
        # Generates the magic link url and sends it in an email
        magiclink.send(request)

        response = {'status': 'Email sent'}

        return Response(response)


class LoginVerifyApiView(views.APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        email = request.GET.get('email')
        user = authenticate(request, token=token, email=email)
        if not user:
            if not magiclink_settings.LOGIN_FAILED_TEMPLATE_NAME:
                raise Http404()

            try:
                magiclink = MagicLink.objects.get(token=token)
            except MagicLink.DoesNotExist:
                error = 'A magic link with that token could not be found'
                log.error(error)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                magiclink.validate(request, email)
            except MagicLinkError as error:
                log.error(str(error))

            return Response(status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        log.info(f'Login successful for {email}')
        response = {
            'status': f'Login successful for {email}'
        }

        return Response(response)



class Web3LoginAPIView(views.APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        session_id = get_random_string(length=8)
        auth = uuid4()
        message = "Authenticating with CumRocket servers... ID:{0}".format(session_id)
        data = {
            "message": message,
            "auth": auth
        }
        response = JsonResponse(data)
        # response.set_cookie('auth', auth)

        session = {
            'session_id': session_id,
            'auth': auth,
            'message': message
        }

        cache.set(auth, session)
        return response

    def post(self, request):
        w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_NETWORK))  # TODO: Testnet

        auth_cookie = request.data.get('auth')

        # auth_cookie = request.COOKIES['auth']
        session = cache.get(auth_cookie)

        # message = request.data.get('message', None)
        message = session['message']
        # message = 'test'
        signature = request.data.get('signature', '')
        address = request.data.get('address', '').lower()

        message_hash = defunct_hash_message(text=message)
        decrypted_address = w3.eth.account.recoverHash(message_hash, signature=signature).lower()

        if decrypted_address != address:
            response = {
                'error': 'Invalid address or message'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # kyc_model = KYCModel.objects.filter(wallet_address=address).first()
        wallet = Wallet.objects.filter(address__iexact=address).first()
        if not wallet:
            # Create new User and Wallet.
            user_model = get_user_model()
            new_user = user_model.objects.create_user(address, '{0}@change.com'.format(address))
            wallet = Wallet.objects.create(address=address, user=new_user)

        kyc_model = KYCModel.objects.filter(wallet=wallet).first()
        model_id = None
        username = None
        kyc_status = 'NONE'
        collections = []
        if kyc_model:
            model_id = kyc_model.pk
            username = kyc_model.username
            kyc_status = kyc_model.status
            collections = [ c.pk for c in kyc_model.collection_set.all()]


        # token = get_random_string(length=256)
        Token.objects.filter(user=wallet.user).delete()
        token = Token.objects.create(user=wallet.user).key


        session['token'] = token
        session['address'] = address
        session['user_id'] = wallet.user.pk
        cache.set(auth_cookie, session)

        response = {
            'token': token,
            'kyc_status': kyc_status,
            'model_id': model_id,
            'collections': collections,
            'username': username
        }
        return Response(response)
