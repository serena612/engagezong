from django.db.models import F, Prefetch
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import  timedelta
from engage.account.constants import SubscriptionPlan
from engage.tournament.models import Tournament, TournamentParticipant, TournamentPrize
from engage.account.models import User
from base64 import b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from django.contrib.auth import get_user_model, login
from engage.account.api import do_register
from engage.account.constants import SubscriptionPlan

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from base64 import b64encode
from base64 import b64decode
from os import urandom

UserModel = get_user_model()

def encrypt_msisdn(msisdn):
    key = 'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
    cipher_suite = Fernet(key)
    encrypted_msisdn = cipher_suite.encrypt(msisdn.encode())
    return encrypted_msisdn

def encrypt_msisdn(key, msisdn):
    key = b64decode(key)
    iv = urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(msisdn.encode('utf-8')) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    iv_and_ciphertext = iv + ciphertext
    base64_encrypted_msisdn = b64encode(iv_and_ciphertext).decode('utf-8')
    base64_encrypted_msisdn_new = base64_encrypted_msisdn.replace("/", "dsslsshd").replace("+", "dsplussd")
    print('$$$$$$$$$ base64_encrypted_msisdn_new', base64_encrypted_msisdn_new)
    return base64_encrypted_msisdn_new


def decrypt_msisdn(key, encrypted_msisdn):
    key = b64decode(key)
    
    # Reverse the replacements in the encrypted MSISDN
    encrypted_msisdn = encrypted_msisdn.replace("dsslsshd", "/").replace("dsplussd", "+")
    
    # Decode the base64-encoded encrypted MSISDN
    iv_and_ciphertext = b64decode(encrypted_msisdn.encode('utf-8'))
    
    # Split IV and ciphertext
    iv = iv_and_ciphertext[:16]
    ciphertext = iv_and_ciphertext[16:]
    
    # Initialize the decryption cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    # Decrypt and unpad the data
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    # Decode the UTF-8 data to get the original MSISDN
    msisdn = unpadded_data.decode('utf-8')
    
    return msisdn

def attempt_login_register(request):
    print("-----------------------------------attempt_login_register")
    print("-----------------------------------request.session", request.session)
    print("-----------------------------------request.user.is_authenticated", request.user.is_authenticated)
    if 'msisdn' not in request.session or request.user.is_authenticated:
       print("inside first if")
       return
    try:
        mobilen = request.session['msisdn']
        print("----------------------------------mobilen ",mobilen)
        #request.user = mobilen
        print("yos-request.user",request.user)
        user = UserModel.objects.filter(
            mobile__iexact=mobilen,
            region=request.region,
            is_active = True
        ).first()
        if user:
            #user found attempt direct login
            usermob = str(user.mobile)
            print("------------------------------login")
            request.user = mobilen
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
#            # user not found attempt registration
#            usermob = mobilen
#            print("-------------------------------usermob",usermob)
#            do_register(None, request, usermob, SubscriptionPlan.FREE)
          return
    
    except UserModel.DoesNotExist:
        usermob = mobilen
        do_register(None, request, usermob, SubscriptionPlan.FREE)
        

def tournament_view(request, slug):
    user = request.user

    now = timezone.now()

    key = "Zjg0ZGJhYmI1MzJjNTEwMTNhZjIwYWE2N2QwZmQ1MzU="  # Replace with your encryption key
    encrypted_msisdn = request.GET.get('app', '')  # Replace with the encrypted MSISDN

    if encrypted_msisdn:
        decrypted_msisdn = decrypt_msisdn(key, encrypted_msisdn)
        if decrypted_msisdn.startswith('0'):
            without_0 = decrypted_msisdn[1:]
            decrypted_msisdn = '92' + without_0
        print("^^^Decrypted msisdn", decrypted_msisdn)
    
        request.session['msisdn'] = decrypted_msisdn
        user = decrypted_msisdn
        attempt_login_register(request)
        return redirect(request.path)
    else:
      print("CHC-request.user not found")


    try:
        tournament = Tournament.objects.select_related(
            'game',
        ).prefetch_related(
            'tournamentparticipant_set',
            Prefetch(
                'tournamentprize_set',
                queryset=TournamentPrize.objects.order_by('position')
            ),
        ).annotate(
            starts_in=F('start_date') - now
        ).get(
            slug=slug,
            regions__in=[request.region]
        )
    except Tournament.DoesNotExist:
        #if slug has been changed get by id

        try:
            tournament = Tournament.objects.select_related(
                'game',
            ).prefetch_related(
                'tournamentparticipant_set',
                Prefetch(
                    'tournamentprize_set',
                    queryset=TournamentPrize.objects.order_by('position')
                ),
            ).annotate(
                starts_in=F('start_date') - now
            ).get(
                id=slug,
                regions__in=[request.region]
            )
        except:
            #if slug has been changed get by id
            
            return redirect('/')

    participant = None
    if user.is_authenticated:
        participant = tournament.get_participant(user)

    can_join = True
    if user.is_authenticated and user.subscription == SubscriptionPlan.PAID1 and user.is_billed == True:
        can_join = not TournamentParticipant.objects.filter(
            tournament__regions__in=[request.region],
            participant=user,
            created__date=now.date()
        ).exists()
    if user.is_authenticated :
        key = 'Zjg0ZGJhYmI1MzJjNTEwMTNhZjIwYWE2N2QwZmQ1MzU='
        print("////tournament request.user.mobile", request.user.mobile)
        msisdn = getattr(request.user, 'mobile', None)  # Replace 'msisdn_attribute_name' with the actual attribute name
        print("tournament msisdn authenticated", msisdn)
        if msisdn:
            encrypted_data = encrypt_msisdn(key, msisdn)
            print ("////tournament encrypted_data", encrypted_data)
        else:
            # Handle the case where MSISDN is not available for the authenticated user
            print("MSISDN not available for the authenticated user", request.user.mobile)

        game_account = tournament.game.usergamelinkedaccount_set.filter(user=user).last()
    else :
        game_account = tournament.game.usergamelinkedaccount_set.last()   
    
    now = timezone.now()
    starts_in = tournament.start_date - now
    if starts_in.days :
        starts_in_full = f'{starts_in.days} days, {int(starts_in.seconds // 3600)} hours and {int((starts_in.seconds // 60) % 60)} minutes'
    else:
        starts_in_full = f'{int(starts_in.seconds // 3600)} hours and {int((starts_in.seconds // 60) % 60)} minutes'
    
    tournament_started = tournament.start_date
    if tournament.time_compared_to_gmt and int(tournament.time_compared_to_gmt)>=0 :  # '+' in 
        tournament_started = tournament.start_date + timedelta(hours=int(tournament.time_compared_to_gmt))
    if tournament.time_compared_to_gmt and int(tournament.time_compared_to_gmt)<0 :  # '-' in 
        tournament_started = tournament.start_date - timedelta(hours=int(tournament.time_compared_to_gmt))
    
    tournament_closed = tournament.close_date
    if tournament.time_compared_to_gmt and int(tournament.time_compared_to_gmt)>=0 :  # '+' in 
        tournament_closed = tournament.close_date + timedelta(hours=int(tournament.time_compared_to_gmt))
    if tournament.time_compared_to_gmt and int(tournament.time_compared_to_gmt)<0 :  # '-' in 
        tournament_closed = tournament.close_date - timedelta(hours=int(tournament.time_compared_to_gmt))
    
    tournament_joined_today = User.objects.filter(username=user.username).values_list('tournament_joined_today', flat=True).first()

    return render(request, 'tournament.html', {'tournament': tournament,
                                               'user': user,
                                               'starts_in_full': starts_in_full,
                                               'game_account': game_account,
                                               'tournament_started': tournament_started,
                                               'tournament_closed': tournament_closed,
                                               'participant': participant,
                                               'can_join': can_join,
                                               'currentDate':now,
                                               'tournament_joined_today':tournament_joined_today,
                                               'encrypted_data':encrypted_data})
