from openai import OpenAI
import os
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_reminder_message(student_name, amount_owed, term):
    prompt = (
        f"""Write a short, polite fee reminder message (2-3 sentences) for a school 
        to send to a parent/guardian. Student name: {student_name}.
        Amount owed: {amount_owed}. Term: {term}. 
        Keep it warm but clear, no subject line, just the message body."
     """
    )

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,#Maximum amount of tokens to be used when generating the response
    )
    return response.choices[0].message.content.strip()