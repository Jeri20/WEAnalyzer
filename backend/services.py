# services.py
import openai
import os

# OpenAI API key (set the key in your environment variables or a .env file)
openai.api_key = os.getenv('OPENAI_API_KEY')  # Replace with your environment variable

# Function to analyze content and extract entities and search intent
def analyze_with_llm(content: str):
    prompt = f"""
    Analyze the following content. Extract all entities (like company names, product names, places) and determine the search intent (Informational, Transactional, Commercial, Navigational).
    
    Content: {content}
    
    Return the entities and search intent in the following format:
    Entities: <list of entities>
    Search Intent: <Search Intent Type>
    """
    
    # Send to OpenAI for analysis
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # You can use a more specific model if needed
            prompt=prompt,
            max_tokens=500
        )

        # Parse and return the response
        result = response.choices[0].text.strip()

        # Ensure that the response is in the expected format
        if "Entities:" in result and "Search Intent:" in result:
            entities_section = result.split("Entities:")[1].split("Search Intent:")[0].strip()
            search_intent_section = result.split("Search Intent:")[1].strip()

            entities = [e.strip() for e in entities_section.split(',')]
            search_intent = search_intent_section

            return entities, search_intent
        else:
            raise ValueError("Unexpected response format from OpenAI API.")

    except Exception as e:
        print(f"Error during OpenAI API request: {e}")
        return [], "Unknown"

# Function to get embeddings for the given text
def get_embedding(text: str) -> list:
    try:
        # Use OpenAI's API or another embedding model to generate embeddings
        response = openai.Embedding.create(model="text-embedding-ada-002", input=text)
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Error during OpenAI embedding request: {e}")
        return []
