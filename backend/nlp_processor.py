import google.generativeai as genai
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('models/gemini-2.5-flash')

def extract_recipe_info(user_input):
    prompt = f"""
    Extract the following structured info from this natural language recipe:
    - A list of main ingredients (just nouns like 'mutton', 'rice', 'tomato')
    - Estimated cooking time in minutes if mentioned, else return 30
    - Ingredient count
    - Complexity score: count how many ingredients are rare or hard-to-cook (like chicken, saffron, mutton, fenugreek leaves etc.)

    Return result strictly in JSON format.
    feature names: {{
      "main_ingredients": [...],
      "estimated_cooking_time_minutes": number,
      "ingredient_count": number,
      "complexity_score": number
    }}

    Recipe: \"\"\"{user_input}\"\"\"
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Try to extract JSON from the response if it's wrapped in markdown
        if '```json' in response_text:
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
        elif '```' in response_text:
            json_match = re.search(r'```\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
        
        # Parse the JSON
        parsed_data = json.loads(response_text)
        
        # Validate the structure and provide defaults
        result = {
            "main_ingredients": parsed_data.get("main_ingredients", []),
            "estimated_cooking_time_minutes": parsed_data.get("estimated_cooking_time_minutes", 30),
            "ingredient_count": parsed_data.get("ingredient_count", len(parsed_data.get("main_ingredients", []))),
            "complexity_score": parsed_data.get("complexity_score", 1)
        }
        
        return result

    except Exception as e:
        print(f"Error in process_recipe_text: {str(e)}")
        # Return default values if processing fails
        return {
            "ingredients": [],
            "ingredient_count": 0,
            "estimated_cooking_time_minutes": 30,
            "complexity_score": 1,
            "main_ingredients_text": ""
        }
def process_recipe_text(recipe_text):
    """
    Process recipe text and return structured data for ML model
    This function is called by app.py
    """
    try:
        print(f"Processing recipe text: {recipe_text[:100]}...")
        
        # Extract recipe info using Gemini AI
        extracted_info = extract_recipe_info(recipe_text)
        print(f"Extracted info: {extracted_info}")
        
        # Ensure extracted_info is a dictionary
        if not isinstance(extracted_info, dict):
            print(f"Warning: extracted_info is not a dict, it's a {type(extracted_info)}")
            raise ValueError("Extracted info is not a dictionary")
        
        # Convert to format expected by frontend and ML model
        processed_data = {
            "ingredients": extracted_info.get("main_ingredients", []),
            "ingredient_count": extracted_info.get("ingredient_count", len(extracted_info.get("main_ingredients", []))),
            "estimated_cooking_time_minutes": extracted_info.get("estimated_cooking_time_minutes", 30),
            "complexity_score": extracted_info.get("complexity_score", 1),
            "main_ingredients_text": ", ".join(extracted_info.get("main_ingredients", []))
        }
        
        print(f"Final processed data: {processed_data}")
        return processed_data
        
    except Exception as e:
        print(f"Error in process_recipe_text: {str(e)}")
        # Return default values if processing fails
        return {
            "ingredients": [],
            "ingredient_count": 0,
            "estimated_cooking_time_minutes": 30,
            "complexity_score": 1,
            "main_ingredients_text": ""
        }

# Test function
if __name__ == "__main__":
    recipe_input = "Hyderabadi Mutton Biryani with basmati rice, mutton, saffron, ghee, yogurt, garam masala, bay leaves, cardamom, cinnamon, cloves, mint leaves, fried onions, rose water, cooking time 60 minutes"
    info = extract_recipe_info(recipe_input)
    print("Direct extraction test:")
    print(info)
    
    print("\nFull processing test:")
    processed = process_recipe_text(recipe_input)
    print(processed)