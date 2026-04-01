#Gemini
import os
from dotenv import load_dotenv
load_dotenv() 

# Setup GEMINI API
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash-latest") 

####
from google import genai
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

def gemini_advice_skin(age, gender, result):
    prompt = f"""You are being used in Skin Disease Classification Project. 
            Your role is to provide  1)advice 2)Remedies and 3)Medicine to the user based on the provided 
            data:

            - age: {age}
            - Gender: {gender}
            - Identified Disease: {result}

            Answer in structured format. Keep the respons size around 7-8 lines.
            """
    try:
        # advice = model.generate_content(prompt)
        response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
            )
        print(response.text)
        advice = response.text

        # advice = advice.candidates[0].content.parts[0].text.replace('*', '')
        print('RAW ADVICE:', advice)
        return advice
    
    except Exception as e:
        print(f"---!!! API CALL FAILED !!!---")
        print(f"ERROR: {e}")
        if 'response' in locals():
            print(f"RESPONSE OBJECT: {advice}")
        return "Error generating advice!"

    



        
        
            
        
        

