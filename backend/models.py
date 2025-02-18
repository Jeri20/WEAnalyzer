from pydantic import BaseModel
from typing import List

class WebsiteRequest(BaseModel):
    url: str

class AnalysisResult(BaseModel):
    title: str
    entities_found: List[str]
    missing_entities: List[str]
    search_intent: str
    chart_data: dict
