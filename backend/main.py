from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from services import analyze_with_llm, get_embedding
from backend.services import analyze_with_llm, get_embedding

# Importing modules from the backend
from services import analyze_with_llm, get_embedding
from crawler.spiders.website_spider import crawl_website
from db import store_in_db

# Initialize FastAPI app
app = FastAPI()

# CORS Configuration to allow requests from Next.js frontend
origins = [
    "http://localhost:3000",  # Frontend URL running locally
    "http://192.168.137.173:3000",  # For local network access
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows frontend to access the backend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request and response validation
class WebsiteRequest(BaseModel):
    url: str

class AnalysisResult(BaseModel):
    title: str
    entities_found: List[str]
    search_intent: str
    chart_data: dict
    frontend_url: str  # Frontend URL to return

@app.post("/analyze-website", response_model=AnalysisResult)
async def analyze_website(request: WebsiteRequest):
    # Step 1: Crawl the website and extract content
    crawled_data = crawl_website(request.url)
    
    # Step 2: Analyze content using LLM (OpenAI) - Extract entities and search intent
    content = crawled_data['title'] + "\n" + " ".join(crawled_data['headings'])
    analysis = analyze_with_llm(content)  # This will return the entity extraction and search intent
    
    # Step 3: Extract entities and search intent from the LLM response
    entities, search_intent = parse_analysis(analysis)
    
    # Step 4: Store in the database (with vectorization)
    embedding = get_embedding(content)  # Get vector embedding for the content
    store_in_db(crawled_data['title'], entities, search_intent, embedding)
    
    # Prepare chart data
    chart_data = {
        'labels': entities,
        'datasets': [
            {
                'label': 'Entities Detected',
                'data': [1 for _ in entities],  # Mark all entities as detected
                'borderColor': '#0070f3',
                'backgroundColor': 'rgba(0, 112, 243, 0.2)',
                'tension': 0.4
            }
        ]
    }
    
    # Return the result including the frontend URL
    return AnalysisResult(
        title=crawled_data['title'],
        entities_found=entities,
        search_intent=search_intent,
        chart_data=chart_data,
        frontend_url="http://localhost:3001"  # Provide frontend URL in the response
    )

def parse_analysis(analysis: str):
    """
    Function to parse the LLM's output analysis, extracting entities and search intent.
    """
    # Assuming the LLM returns the result in a format like:
    # "Entities: Apple Inc., iPhone 15, Paris. Search Intent: Transactional."
    
    # Parse the entities and search intent from the analysis result
    entities_str = analysis.split('Entities:')[1].split('Search Intent:')[0].strip()
    entities = [entity.strip() for entity in entities_str.split(',')]
    
    search_intent = analysis.split('Search Intent:')[1].strip()
    
    return entities, search_intent
