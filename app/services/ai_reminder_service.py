from openai import OpenAI
import os
client = OpenAI(
    base_url="https://api.featherless.ai/v1",
  api_key=os.getenv("FEATHERLESS_API_KEY"),
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
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        
    )
    return response.choices[0].message.content.strip()