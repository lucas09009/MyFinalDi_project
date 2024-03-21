import requests
import json

def send_payment_request(auth_token, phone_number, amount, identifier, network):
    # URL de l'API du service de paiement
    api_url = 'https://paygateglobal.com/api/v1/pay'

    # Paramètres de la requête
    payload = {
        'auth_token': auth_token,
        'phone_number': phone_number,
        'amount': amount,
        'description': 'Description de la transaction',
        'identifier': identifier,
        'network': network
    }

    # Envoi de la requête HTTP POST avec les paramètres JSON
    response = requests.post(api_url, json=payload)

    # Traitement de la réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json()
        return data  # Vous pouvez traiter les données renvoyées par l'API ici
    else:
        # La requête a échoué
        return {'error': f'Erreur {response.status_code}: {response.text}'}
