import streamlit as st
import re

# --- 1. THE PASSWORD GATE ---
def check_password():
    if "password_correct" not in st.session_state:
        st.subheader("🔒 Access Restricted")
        pwd = st.text_input("Enter Team Password", type="password")
        if st.button("Unlock"):
            if pwd == "Password123": # <--- CHANGE THIS
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Incorrect password")
        return False
    return True

# --- 2. THE CALCULATION LOGIC ---
def process_data(text_input):
    grade_map = {"OUTSTANDING": 5, "ABOVE": 4, "MEETS": 3, "BELOW": 2, "DEFICIENT": 1}
    weights = [25, 5, 5, 5, 10, 10, 5, 5, 5, 25]
    questions = [
        "delivers work on time, on schedule and to specification i.e is efficient.",
        "demonstrates respect for his/her work and ideas of other members on the team.",
        "clearly communicates thoughts.",
        "interested in developing new skills and growing as a professional.",
        "accepts responsibility for his or her own actions.",
        "open to feedback.",
        "shows willingness and enthusiasm to do the job and tasks given",
        "exhibits effective problem solving skills.",
        "promptly communicates when there is a problem and asks for help.",
        "delivers lush quality work ie take initiative and improve work assignments in a way that shows growth"
    ]
    
    sections = re.split(r'(\w+)[’\']S ASSESSMENT SECTION', text_input, flags=re.IGNORECASE)
    results_output = ""
    
    for i in range(1, len(sections), 2):
        name = sections[i].upper()
        content = sections[i+1]
        found_ratings = re.findall(r'(OUTSTANDING|ABOVE|MEETS|BELOW|DEFICIENT)', content, re.IGNORECASE)
        
        if len(found_ratings) < 10:
            results_output += f"### ⚠️ Missing data for {name}\n\n"
            continue

        results_output += f"### {name}’S ASSESSMENT SECTION\n\n"
        subtotal = 0
        
        for j in range(10):
            grade_word = found_ratings[j].upper()
            rating_value = grade_map[grade_word]
            weight = weights[j]
            calc = rating_value * weight
            subtotal += calc
            
            display_grade = "Meets Expectations" if grade_word == "MEETS" else grade_word.capitalize()
            if grade_word == "ABOVE": display_grade = "Above Expectations"
            if grade_word == "BELOW": display_grade = "Below Standard"

            results_output += f"___ {questions[j]} (this score is {weight})  \n"
            results_output += f"{display_grade}  \n"
            results_output += f"{rating_value} x {weight} = {calc}  \n\n"
        
        final_score = subtotal / 4
        results_output += f"= {subtotal} / 4  \n"
        results_output += f"**Total: {final_score:.2f}** \n"
        results_output += "------------------------------\n\n"
    
    return results_output

# --- 3. THE MAIN APP INTERFACE ---
import streamlit as st
import re

# ... (Keep your check_password and process_data functions exactly as they are) ...

if check_password():
    # --- 3. THE MAIN APP INTERFACE ---
    
    # NEW: Add a Logo/Header Image at the top
    # You can replace this URL with your company logo link
    st.image("Joy_Logo.png", width=100)
    
    st.title("📊 Bi-Annual Review Scorer")
    st.markdown("### *Official Team Assessment Tool*") # Subheader
    
    user_input = st.text_area("Paste assessment text here:", height=300)

    if st.button("Generate Formatted Scores"):
        if user_input:
            final_report = process_data(user_input)
            st.markdown(final_report)
            
            st.download_button(
                label="📥 Download Report as Text File",
                data=final_report,
                file_name="Performance_Report.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please paste some text first.")