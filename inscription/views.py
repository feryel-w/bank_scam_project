# inscription/views.py

from django.shortcuts import render
from .forms import BankInscriptionForm
from .ml_model import predict_with_business_rule
from .watchlist import is_on_watchlist   # <= NOUVEL IMPORT


def inscription_view(request):
    if request.method == "POST":
        form = BankInscriptionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # Données envoyées au modèle IA (les 7 variables)
            ai_data = {
                "age": data["age"],
                "country": data["nationality"],
                "residence": data["residence_country"],
                "profession": data["profession"],
                "revenue": data["revenue"],
                "source_of_income": data["source_of_income"],
                "account_purpose": data["account_purpose"],
            }

            # 1) Prédiction du modèle ML (0 ou 1)
            risk_model = predict_with_business_rule(ai_data)

            # 2) Vérification dans la liste externe (id_type + id_number)
            id_type = data["id_type"]
            id_number = data["id_number"]

            is_sensitive = is_on_watchlist(id_type, id_number)

            # 3) Règle métier AML :
            #    si dans la liste externe => risque final = 1
            if is_sensitive:
                risk_final = 1
            else:
                risk_final = risk_model

            return render(request, "inscription/result.html", {
                "risk": risk_final,         # décision finale
                "risk_model": risk_model,   # sortie brute du modèle IA
                "is_sensitive": is_sensitive,
                "form_data": data,
            })

    else:
        form = BankInscriptionForm()

    return render(request, "inscription/form.html", {"form": form})


def result_view(request):
    return render(request, "inscription/result.html")