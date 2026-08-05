import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_risk_tier(score):
    if score < 40:
        return "low"
    elif score < 60:
        return "moderate"
    elif score < 80:
        return "moderate-high"
    else:
        return "high"


def generate_explanation(ml_risk_score, disaster_risk_score, shap_values, raw_values, sentiment_data=None):
    top_contributors = sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)[:4]

    contributor_lines = []
    for feature, impact in top_contributors:
        raw_value = raw_values.get(feature, "unknown")
        if isinstance(raw_value, (int, float)):
            raw_value = round(raw_value, 2)
            if raw_value == int(raw_value):
                raw_value = int(raw_value)
        direction = "increased" if impact > 0 else "decreased"
        contributor_lines.append(f"- {feature}: value={raw_value}, {direction} the risk score by {abs(impact):.2f} points")

    risk_tier = get_risk_tier(ml_risk_score)

    if sentiment_data:
        sentiment_line = f"Local news sentiment: {sentiment_data['average_sentiment']:.2f} (scale -1 to +1, based on {sentiment_data['article_count']} recent articles)"
    else:
        sentiment_line = "Local news sentiment: unavailable"

    prompt = f"""You are explaining a property investment risk score to an investor.

Risk score: {ml_risk_score:.1f}/100 ({risk_tier} risk)
Disaster risk score (FEMA data): {disaster_risk_score if disaster_risk_score is not None else "unavailable"}
{sentiment_line}

Top factors driving this score, in order of impact:
{chr(10).join(contributor_lines)}

Write a 3-4 sentence explanation for the investor, in plain language. Use ONLY the
numbers and factors provided above — do not invent, assume, or reference any
information not explicitly given here. Do not mention SHAP, models, or technical
ML terminology. If local sentiment data is available, briefly mention whether it's
positive or negative as additional context, without treating it as a primary risk
driver. Focus on what an investor would actually care about."""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text
