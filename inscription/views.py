# inscription/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
import random

from .forms import BankInscriptionForm
from .ml_model import predict_with_business_rule
from .watchlist import is_on_watchlist
from .models import Customer


# inscription/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
import random

from .forms import BankInscriptionForm
from .ml_model import predict_with_business_rule
from .watchlist import is_on_watchlist
from .models import Customer

def inscription_view(request):
    if request.method == "POST":
        form = BankInscriptionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # ---------------------------
            # CHECK IF CLIENT IS BLACKLISTED FIRST
            # ---------------------------
            id_type = data["id_type"]
            id_number = data["id_number"]
            existing_blacklisted = Customer.objects.filter(
                id_type=id_type,
                id_number=id_number,
                is_blacklisted=True
            ).first()

            if existing_blacklisted:
                # Blacklisted client → show generic error message
                return render(request, "inscription/blocked.html", {
                    "full_name": data.get("full_name", "Client")
                })

            # ---------------------------
            # AI INPUT
            # ---------------------------
            ai_data = {
                "age": data["age"],
                "country": data["nationality"],
                "residence": data["residence_country"],
                "profession": data["profession"],
                "revenue": data["revenue"],
                "source_of_income": data["source_of_income"],
                "account_purpose": data["account_purpose"],
            }

            # AI prediction: 0 = good, 1 = suspicious
            risk_model = predict_with_business_rule(ai_data)

            # Check watchlist
            is_sensitive = is_on_watchlist(id_type, id_number)

            # ---------------------------
            # IMMEDIATE REFUSAL FOR SENSITIVE CLIENTS
            # ---------------------------
            if is_sensitive:
                # Create a record marked as suspected and refused
                customer = Customer.objects.create(
                    full_name=data["full_name"],
                    age=data["age"],
                    gender=data["gender"],
                    nationality=data["nationality"],
                    residence_country=data["residence_country"],
                    phone=data["phone"],
                    email=data["email"],
                    address=data["address"],
                    profession=data["profession"],
                    revenue=data["revenue"],
                    source_of_income=data["source_of_income"],
                    account_purpose=data["account_purpose"],
                    account_type=data["account_type"],
                    id_type=id_type,
                    id_number=id_number,
                    is_suspected=True,
                    is_verified=False,
                    is_blacklisted=False,
                )

                return render(request, "inscription/blocked.html", {
                    "full_name": customer.full_name
                })

            # ---------------------------
            # FINAL RISK DECISION BASED ON AI
            # ---------------------------
            risk_final = risk_model

            # -------------------------------
            # CREATE CUSTOMER RECORD
            # -------------------------------
            customer = Customer.objects.create(
                full_name=data["full_name"],
                age=data["age"],
                gender=data["gender"],
                nationality=data["nationality"],
                residence_country=data["residence_country"],
                phone=data["phone"],
                email=data["email"],
                address=data["address"],
                profession=data["profession"],
                revenue=data["revenue"],
                source_of_income=data["source_of_income"],
                account_purpose=data["account_purpose"],
                account_type=data["account_type"],
                id_type=id_type,
                id_number=id_number,
                is_suspected=(risk_final != 0),
                is_verified=(risk_final == 0),
                is_blacklisted=False,
            )

            # -------------------------------
            # GOOD CLIENT → GENERATE RIB + EMAIL
            # -------------------------------
            if risk_final == 0:
                rib_code = "TN" + str(random.randint(10**19, 10**20 - 1))
                customer.rib_code = rib_code
                customer.save()

                # Send client email
                send_mail(
                    subject="Votre RIB - BlueWave Bank",
                    message=(
                        f"Bonjour {customer.full_name},\n\n"
                        f"Votre ouverture de compte est approuvée.\n"
                        f"Voici votre RIB : {rib_code}\n\n"
                        f"Merci pour votre confiance.\nBlueWave Bank"
                    ),
                    from_email=None,
                    recipient_list=[customer.email],
                    fail_silently=False,
                )

                return render(request, "inscription/success.html", {
                    "full_name": customer.full_name,
                    "rib_code": customer.rib_code
                })

            else:
                # -------------------------------
                # SUSPECTED CLIENT → NOTIFY ADMIN
                # -------------------------------
                send_mail(
                    subject="⚠ New Client Needs Verification",
                    message=(
                        f"A new client has been flagged as suspicious and requires verification.\n\n"
                        f"Name: {customer.full_name}\n"
                        f"ID: {customer.id_type} {customer.id_number}\n"
                        f"Reason: Flagged by AI\n\n"
                        f"--- Automated AML Alert ---"
                    ),
                    from_email=None,
                    recipient_list=["elkamelferyel@gmail.com"],  # admin email
                    fail_silently=False,
                )

                # Show generic pending page to client
                return render(request, "inscription/pending.html", {
                    "full_name": customer.full_name
                })

    else:
        form = BankInscriptionForm()

    return render(request, "inscription/form.html", {"form": form})


def result_view(request):
    return render(request, "inscription/result.html")


# ----------------------------
# ADMIN VERIFICATION VIEWS
# ----------------------------
def verify_clients_view(request):
    # Show all clients flagged as suspected but not verified or blacklisted
    suspected_clients = Customer.objects.filter(
        is_suspected=True,
        is_verified=False,
        is_blacklisted=False
    )

    return render(request, "inscription/verify_clients.html", {
        "suspected_clients": suspected_clients
    })


def verify_client_action(request, client_id):
    client = get_object_or_404(Customer, id=client_id)

    # Only verify if client is suspected AND not blacklisted
    if client.is_suspected and not client.is_blacklisted:
        client.is_suspected = False
        client.is_verified = True
        client.rib_code = "TN" + str(random.randint(10**19, 10**20 - 1))
        client.save()

        # Send RIB email
        send_mail(
            subject="Votre RIB - BlueWave Bank",
            message=(
                f"Bonjour {client.full_name},\n\n"
                f"Votre compte a été approuvé après vérification.\n"
                f"Voici votre RIB : {client.rib_code}\n\n"
                f"Merci,\nBlueWave Bank"
            ),
            from_email=None,
            recipient_list=[client.email],
            fail_silently=False,
        )

    return redirect("verify_clients")



def blacklist_client_action(request, client_id):
    client = get_object_or_404(Customer, id=client_id)

    if client.is_suspected:
        client.is_suspected = False
        client.is_blacklisted = True
        client.save()

    return redirect("verify_clients")


# ----------------------------
# ALL CLIENTS PAGE
# ----------------------------
def all_clients_view(request):
    query = request.GET.get('q')  # get search query from URL ?q=...
    if query:
        clients = Customer.objects.filter(full_name__icontains=query)
    else:
        clients = Customer.objects.all()
    return render(request, "inscription/all_clients.html", {
        "clients": clients
    })



