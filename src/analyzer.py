# Example Python snippet using OpenAI API
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_investment_advice(experience, risk, timeframe, sectors, goal):
    prompt = f"""
    User Profile:
    Experience: {experience}
    Risk tolerance: {risk}
    Timeframe: {timeframe}
    Interested sectors: {sectors}
    Goal: {goal}

    Provide a clear, beginner-friendly investment overview and suggestions. Explain why these investments fit this profile.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    return response.choices[0].message.content

# Example call
print(get_investment_advice("beginner", "low", "short-term", "tech, healthcare", "growth"))
