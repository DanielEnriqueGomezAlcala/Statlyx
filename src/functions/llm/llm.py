from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_text(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un analista de datos experto y conciso. Tu objetivo es generar una conclusión de exactamente 7 líneas basada en los patrones o datos observados."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=250
        )
        
        conclusion = response.choices[0].message.content
        return conclusion

    except Exception as e:
        return f"Ha ocurrido un error: {e}"