import openai
import os
import json
from dotenv import load_dotenv


load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')


data = {
    "profile_context": {
        "patient_profile": "Age - 25 Patient Preferred Language - ENGLISH Patient Conditions - PCOS Patient Nutritional Deficiencies - Hb Diet Preference - Veg",
        "program_name": "PCOS",
        "diet_chart": {
            "diet_chart_url": "https://clchatagentassessment.s3.ap-south-1.amazonaws.com/3a16cf52-26a0-47d6-8c91-9810039676ee_CL.pdf"
        }
    },
    "latest_query": {
        "ideal_response": "Great job for having methi water, continue having it daily, it will help boost your metabolism. Varsha, but I also noticed that you are having figs and raisins but they are not prescribed in the diet plan, can I know why you have added them?"
    },
    "chat_context": {
        "ticket_created": "June 14, 2024, 07:05 AM",
        "ticket_id": "3a16cf52-26a0-47d6-8c91-9810039676ee",
        "chat_history": [
            {
                "role": "User",
                "message": "Sent an image (The image shows a hand holding a small metal bowl containing yellowish-brown seeds soaked in water. The background includes a bed with a colorful bedsheet and a tiled wall.)",
                "timestamp": "June 14, 2024, 07:05 AM",
                "asset_url": "https://assets.curelinktech.in/media/documents/user_03cb4939-231a-4ed8-bcb2-17ad81ecf9db/2024-06-14T013505113482.jpg",
                "type": 1
            },
            {
                "role": "User",
                "message": "Sent an image (The image shows a small metal bowl containing a variety of dried fruits and nuts. Visible items include a dried fig, almonds, walnuts, and raisins. The bowl is placed on a dark fabric surface, possibly someone's lap.) with the following caption Dry fruits.",
                "timestamp": "June 14, 2024, 07:05 AM",
                "asset_url": "https://assets.curelinktech.in/media/documents/user_03cb4939-231a-4ed8-bcb2-17ad81ecf9db/2024-06-14T013505105149.jpg",
                "type": 1
            },
            {
                "role": "User",
                "message": "Replied to the following message: \"Sent an image (The image shows a hand holding a small metal bowl containing yellowish-brown seeds soaked in water. The background includes a bed with a colorful bedsheet and a tiled wall.)\", with: \"Methi dana done\"",
                "timestamp": "June 14, 2024, 07:05 AM",
                "asset_url": None,
                "type": 0
            }
        ]
    }
}

def generate_response(patient_profile, message):

    prompt = f"""
    Patient Profile: {patient_profile}
    Message: {message}

    Generate a concise and specific response for the patient based on the diet chart and the chat history. And suggest him next meal plan
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return response.choices[0].message['content'].strip()


patient_profile = data['profile_context']['patient_profile']
message = "Patient consumed methi dana and dry fruits like figs and raisins."


generated_response = generate_response(patient_profile, message)

output_data = {
    "ticket_id": data['chat_context']['ticket_id'],
    "latest_query": message,
    "generated_response": generated_response,
    "ideal_response": data['latest_query']['ideal_response']
}

with open('output.json', 'w') as outfile:
    json.dump(output_data, outfile, indent=4)

print("Generated response saved to output.json")
