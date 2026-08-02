import json
import time

from openai import OpenAI

from config import OPENROUTER_API_KEY, AI_MODEL


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def analyze_ticket(title: str, description: str):

    prompt = f"""
You are a Senior Enterprise IT Service Desk Engineer.

Analyze the following IT support ticket.

Title:
{title}

Description:
{description}

Return ONLY valid JSON in this format:

{{
    "category": "",
    "priority": "",
    "severity": "",
    "summary": "",
    "root_cause": "",
    "resolution": "",
    "assigned_team": "",
    "estimated_time": ""
}}

Rules:

Category must be one of:
VPN
Network
Software
Hardware
Database
Cloud
Email
Security
Operating System

Priority:
Low
Medium
High
Critical

Severity:
Minor
Major
Critical

Summary:
Maximum 20 words.

Root Cause:
Maximum 25 words.

Resolution:
Provide 2-3 concise troubleshooting actions in one sentence.
Maximum 40 words.

Assigned Team:
Maximum 3 words.

Estimated Time:
Examples:
15 minutes
30 minutes
1 hour
2 hours
4 hours
1 business day

Return ONLY JSON.
"""

    start = time.perf_counter()

    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Senior Enterprise IT Service Desk Engineer."
                    "Base your analysis on standard enterprise troubleshooting practices."
                    "If the exact cause is uncertain, use words like 'Likely' or 'Possible'."
                   " Return ONLY valid JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=500,
    )

    print(f"AI Time: {time.perf_counter() - start:.2f}s")

    # ---------- DEBUG ----------
    print("\n========== RAW RESPONSE ==========")
    print(response)
    print("==================================\n")

    if not getattr(response, "choices", None):
        raise Exception(f"No choices returned.\nResponse:\n{response}")

    content = response.choices[0].message.content

    if content is None:
        raise Exception("Model returned empty content.")

    content = content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()

    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    # Extract JSON safely
    start_json = content.find("{")
    end_json = content.rfind("}")

    if start_json != -1 and end_json != -1:
        content = content[start_json:end_json + 1]

    print("\n========== MODEL OUTPUT ==========")
    print(content)
    print("==================================\n")

    try:
        return json.loads(content)

    except Exception as e:

        print("\n========== JSON ERROR ==========")
        print(e)
        print("================================\n")

        return {
            "category": "Unknown",
            "priority": "Medium",
            "severity": "Minor",
            "summary": "AI analysis unavailable.",
            "root_cause": "The AI response could not be parsed.",
            "resolution": "Please classify this ticket manually.",
            "assigned_team": "IT Operations",
            "estimated_time": "Unknown"
        }