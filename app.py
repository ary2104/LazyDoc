import streamlit as st
import json
import os

# Load the symptoms data
DATA_PATH = "data/symptoms_data.json"

if not os.path.exists(DATA_PATH):
    st.error(f"Could not find the file: {DATA_PATH}")
else:
    with open(DATA_PATH, "r") as f:
        symptom_data = json.load(f)

    st.set_page_config(page_title="LazyDoc – Symptom Checker", layout="centered")
    st.title("🩺 LazyDoc – Symptom Checker")
    st.markdown("Welcome to LazyDoc! Select your symptoms to get a list of possible conditions. This tool is for preliminary assistance only.")

    all_symptoms = list(symptom_data.keys())
    selected_symptoms = st.multiselect("Select symptoms you are experiencing:", sorted(all_symptoms))

    if selected_symptoms:
        condition_counter = {}

        for symptom in selected_symptoms:
            possible_conditions = symptom_data[symptom]["possible_conditions"]
            for condition in possible_conditions:
                condition_counter[condition] = condition_counter.get(condition, 0) + 1

        # Sort conditions based on match count
        sorted_conditions = sorted(condition_counter.items(), key=lambda x: x[1], reverse=True)

        st.subheader("🔍 Possible Conditions based on selected symptoms:")
        if sorted_conditions:
            for condition, count in sorted_conditions:
                st.markdown(f"- **{condition}** – matched with **{count}** of your symptoms")
        else:
            st.info("No specific condition matches all the selected symptoms. Please consult a healthcare provider.")

        st.subheader("🧠 Clinical Notes on Selected Symptoms:")
        for symptom in selected_symptoms:
            notes = symptom_data[symptom].get("notes", "")
            if notes:
                st.markdown(f"- **{symptom}**: {notes}")
    else:
        st.warning("Please select at least one symptom to continue.")
