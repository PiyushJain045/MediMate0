#Gemini
import os
from dotenv import load_dotenv
load_dotenv() 

# Setup GEMINI API
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash-latest") 

# 
from google import genai
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()


def gemini_advice_disease(disease_name, body_part=None, symptoms=None):
    print("INSIDE GEMINI ADVICE")
    print(body_part)
    print(symptoms)
    print(disease_name)
    prompt = f"""
                    Persona: You are an AI Clinical Diagnostic Assistant. Your primary function is to provide a brief, informational assessment based on user-provided data.

                    CRITICAL SAFETY INSTRUCTION: You are not a medical professional. Your response MUST begin with a clear disclaimer stating that this is not a medical diagnosis and the user must consult a qualified healthcare provider for any health concerns.

                    ---
                    **Diagnostic Data:**
                    - **Initial Complaint:** Discomfort in the {body_part or 'unspecified'} area.
                    - **Positive Symptoms (User answered 'Yes'):** {symptoms or 'None specified'}
                    - **AI Preliminary Prediction:** {disease_name}
                    ---

                    **Your Task:**
                    Based ONLY on the data provided above, generate a concise 4-5 line assessment. Structure your response exactly as follows, without any extra formatting like markdown bolding:

                    Assessment Category: [Choose ONE: "Self-Care", "non-urgent medical condition", or "Serious Condition"]
                    Explanation: [1-2 sentence explanation of the predicted condition, {disease_name}]
                    Clinical Reasoning: [1-2 sentence explanation connecting the positive symptoms to the prediction]
             """
    print("OUTSIDE TRY")            
    try:
        print("INSIDE 1")
        response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
            )
        # response = model.generate_content(prompt)
        print("RESPONSE:", response)
        raw_advice = response.candidates[0].content.parts[0].text.replace('*', '')
        print('RAW ADVICE:', raw_advice)

        # --- COMPLETE PARSING LOGIC ---
        assessment_category = "Unknown"
        category_color_class = "category-gray"  # Default color

        # Split the raw text into lines to find the category
        advice_lines = raw_advice.splitlines()
        
        for line in advice_lines:
            # Find the line that contains "Assessment Category:"
            if "Assessment Category:" in line:
                print("LINE:", line)
                # Extract the text after the colon and strip whitespace
                assessment_category = line.split(":", 1)[1].strip()
                
                # Assign a color class based on keywords in the category
                if "serious" in assessment_category or "Serious" in assessment_category:
                    category_color_class = "category-red"
                elif "Non-Urgent" in assessment_category or "non-urgent" in assessment_category:
                    category_color_class = "category-yellow"
                elif "Self-Care" in assessment_category:
                    category_color_class = "category-green"
                break # Stop searching once the category is found

        # Return a structured dictionary
        return {
            'advice': raw_advice,
            'assessment_category': assessment_category,
            'category_color_class': category_color_class
        }

    except Exception as e:
        print(f"---!!! API CALL FAILED !!!---")
        print(f"ERROR: {e}")
        if 'response' in locals():
            print(f"RESPONSE OBJECT: {response}")
        return "Error generating advice!"
        

