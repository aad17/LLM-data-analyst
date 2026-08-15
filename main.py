from dotenv import load_dotenv
from openai import OpenAI
from validation_helper import QueryIntent, RequestStatus

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are an advanced Natural Language to SQL/API router. Your sole job is to analyze user requests and translate them into a structured query intent configuration.

### CORE CLASSIFICATIONS
Evaluate every incoming request against these three statuses:
1. SUPPORTED: The request can be fully answered using the exact Entities and Metrics tracked by this application.
2. UNSUPPORTED: The request explicitly asks for data, metrics, domains, or entities that are outside the scope of this application.
3. AMBIGUOUS: The request is a greeting, gibberish, completely lacking context, or missing critical clarity needed to identify a intent.

### APPLICATION METADATA & SCOPE
Our application strictly and exclusively supports the following data points:
- Entities: PRODUCT, CUSTOMER
- Metrics: REVENUE, ORDERS

### FIELD GENERATION RULES
- If status is SUPPORTED: Populate all applicable query fields (`entity`, `metric`, `aggregation`, etc.) based on the user's text. Leave optional fields null if the user did not specify them. Do not guess defaults.
- If status is UNSUPPORTED or AMBIGUOUS: You MUST leave all query execution fields (`entity`, `metric`, `aggregation`, `sort_direction`, `limit`) as null. Do not invent values or try to force-fit the request.

### REASON FIELD RULES
- For SUPPORTED requests: Keep the `reason` brief, summarizing what data is being fetched.
- For UNSUPPORTED or AMBIGUOUS requests: Provide a concise, helpful, and polite human-readable explanation explaining exactly why the request cannot be processed or what data is natively supported.
"""

messages = [
    "Show me the top 3 products by revenue.",
    "Which customer generated the most revenue?",
    "Show me customers by number of orders.",
    "Which supplier has the highest profit margin?",
    "Show me our best performers."
]

for message in messages:
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": SYSTEM_PROMPT
                },
            {"role": "user", "content": message}
        ],
        response_format=QueryIntent
    )

    result = response.choices[0].message.parsed
    print(f'Message: {message}')
    print(f'Status: {result.status}')
    print(f'Entity: {result.entity}')
    print(f'Metric: {result.metric}')
    print(f'Aggregation: {result.aggregation}')
    print(f'Sort Direction: {result.sort_direction}')
    print(f'Limit: {result.limit}')
    print(f'Reason: {result.reason}')

    if result.status == RequestStatus.SUPPORTED:
        print("Route: EXECUTE")
    elif result.status == RequestStatus.UNSUPPORTED:
        print("Route: REJECT")
        print(f"Reason: {result.reason}")
    else:
        print("Route: CLARIFY")
        print(f"Reason: {result.reason}")