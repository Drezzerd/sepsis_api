import streamlit as st
import requests

# Définir l'URL de l'API
API_URL = "http://localhost:8000"

# Fonction pour appeler l'API
def call_api(endpoint, data=None):
    url = f"{API_URL}/{endpoint}"
    if endpoint == "predict/patient":
        response = requests.post(url, json=data)
    else:
        response = requests.get(url)
    return response.status_code, response.json()

# Interface Streamlit
def main():
    st.title("Prédiction de maladie")

    # Saisie des paramètres
    prg = st.number_input("Entrez la valeur de prg", value=0.0, step=0.1)
    pl = st.number_input("Entrez la valeur de pl", value=0.0, step=0.1)
    pr = st.number_input("Entrez la valeur de pr", value=0.0, step=0.1)
    sk = st.number_input("Entrez la valeur de sk", value=0.0, step=0.1)
    ts = st.number_input("Entrez la valeur de ts", value=0.0, step=0.1)
    m11 = st.number_input("Entrez la valeur de m11", value=0.0, step=0.1)
    bd2 = st.number_input("Entrez la valeur de bd2", value=0.0, step=0.1)
    age = st.number_input("Entrez l'âge", value=1, step=1, min_value=1, max_value=100)
    insurance = st.number_input("Entrez la valeur d'insurance", value=0, step=1, min_value=0, max_value=1)

    # Bouton pour appeler l'API
    if st.button("Prédire"):
        data = {
            "prg": prg,
            "pl": pl,
            "pr": pr,
            "sk": sk,
            "ts": ts,
            "m11": m11,
            "bd2": bd2,
            "age": age,
            "insurance": insurance
        }
        status_code, result = call_api("predict/patient", data=data)
        if status_code == 200:
            if result["malade"] == 0:
                st.write("Negatif")
            elif result["malade"] == 1:
                st.write("Positif")
        else:
            st.write(result)
        
        st.code(status_code)
            
    # Bouton pour vérifier l'état de l'API
    if st.button("Health"):
        status_code, response = call_api("health")
        st.code(status_code)
        st.write(response)

if __name__ == "__main__":
    main()
