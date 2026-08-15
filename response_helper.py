from dotenv import load_dotenv
from openai import OpenAI
from data_helper import execute_query
import pandas as pd

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are a data analyst, presenting analysis results. You will be provided
with data. Use only facts present in the supplied data.
DO NOT INVENT data, causes, trends, comparisons or values.
The execution result is already fully computed by a trusted
deterministic analytics engine.
Treat every row and value as the final analytical result.
Do not perform arithmetic, aggregation, averaging,
ranking, filtering, or other transformations.
Preserve the granularity of the execution result.
If multiple rows are supplied, report those rows when relevant
rather than combining them into a new value.
Do not assume units, currencies, percentages, or other metadata
unless explicitly present in the result.
Your only job is to communicate the supplied result clearly.
If the result does not contain enough information, say so.
Answer should be consise.
"""

def user_response(data: pd.DataFrame, user_question: str) -> str:
    df_string = data.to_csv(index=False)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"{user_question}. Data: {df_string}"
            }
        ]
    )

    return response.choices[0].message.content

df_test = pd.DataFrame({
    'customer': ['Diana Prince'],
    'revenue': [3201.0]
})

print(user_response(df_test, "Why did Diana Prince generate the most revenue?"))