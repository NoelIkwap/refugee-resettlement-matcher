from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import uvicorn
from datetime import datetime

# Your existing RefugeeStateMatcher class
class RefugeeStateMatcher:
    def __init__(self):
        self.states_data = self._initialize_states_data()
        self.df = pd.DataFrame(self.states_data)
    
    def _initialize_states_data(self) -> List[Dict[str, Any]]:
        """Initialize comprehensive US states demographic data"""
        return [
            {
                "state": "California",
                "languages": ["English", "Spanish", "Chinese", "Arabic", "Vietnamese"],
                "job_skills": ["technology", "healthcare", "construction", "agriculture", "education"],
                "education_levels": ["secondary", "bachelors", "graduate"],
                "health_requirements": ["general", "specialized", "mental_health"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "Asian", "Latin American"],
                "job_market_score": 9,
                "support_services_score": 8
            },
            {
                "state": "Texas",
                "languages": ["English", "Spanish", "Vietnamese", "Arabic", "Chinese"],
                "job_skills": ["construction", "oil_gas", "healthcare", "technology", "logistics"],
                "education_levels": ["secondary", "vocational", "bachelors"],
                "health_requirements": ["general", "mental_health"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "Latin American", "African"],
                "job_market_score": 8,
                "support_services_score": 7
            },
            {
                "state": "New York",
                "languages": ["English", "Spanish", "Chinese", "Russian", "Arabic"],
                "job_skills": ["finance", "healthcare", "technology", "hospitality", "education"],
                "education_levels": ["secondary", "bachelors", "graduate"],
                "health_requirements": ["general", "specialized", "mental_health"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "Asian", "African", "European"],
                "job_market_score": 9,
                "support_services_score": 9
            },
            {
                "state": "Michigan",
                "languages": ["English", "Arabic", "Spanish", "Chinese"],
                "job_skills": ["automotive", "manufacturing", "healthcare", "technology"],
                "education_levels": ["secondary", "vocational", "bachelors"],
                "health_requirements": ["general", "mental_health"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "Asian"],
                "job_market_score": 7,
                "support_services_score": 8
            },
            {
                "state": "Washington",
                "languages": ["English", "Spanish", "Chinese", "Vietnamese", "Arabic"],
                "job_skills": ["technology", "aviation", "healthcare", "construction"],
                "education_levels": ["secondary", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "Asian", "African"],
                "job_market_score": 8,
                "support_services_score": 8
            },
            {
                "state": "Florida",
                "languages": ["English", "Spanish", "Haitian Creole", "Arabic"],
                "job_skills": ["tourism", "healthcare", "construction", "agriculture"],
                "education_levels": ["secondary", "vocational"],
                "health_requirements": ["general", "mental_health"],
                "mental_health_support": True,
                "refugee_communities": ["Latin American", "Caribbean", "Middle Eastern"],
                "job_market_score": 7,
                "support_services_score": 7
            },
            {
                "state": "Illinois",
                "languages": ["English", "Spanish", "Polish", "Arabic"],
                "job_skills": ["manufacturing", "healthcare", "finance", "logistics"],
                "education_levels": ["secondary", "bachelors"],
                "health_requirements": ["general", "mental_health"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "Eastern European", "Asian"],
                "job_market_score": 7,
                "support_services_score": 8
            },
            {
                "state": "Ohio",
                "languages": ["English", "Spanish", "Arabic"],
                "job_skills": ["manufacturing", "healthcare", "logistics", "construction"],
                "education_levels": ["secondary", "vocational"],
                "health_requirements": ["general"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "Asian"],
                "job_market_score": 6,
                "support_services_score": 7
            },
            {
                "state": "Georgia",
                "languages": ["English", "Spanish", "Korean", "Arabic"],
                "job_skills": ["logistics", "healthcare", "technology", "film"],
                "education_levels": ["secondary", "bachelors"],
                "health_requirements": ["general", "mental_health"],
                "mental_health_support": True,
                "refugee_communities": ["Asian", "African", "Middle Eastern"],
                "job_market_score": 7,
                "support_services_score": 7
            },
            {
                "state": "Arizona",
                "languages": ["English", "Spanish", "Navajo", "Arabic"],
                "job_skills": ["construction", "healthcare", "technology", "tourism"],
                "education_levels": ["secondary", "vocational"],
                "health_requirements": ["general"],
                "mental_health_support": True,
                "refugee_communities": ["Latin American", "Middle Eastern"],
                "job_market_score": 6,
                "support_services_score": 6
            }
        ]
    
    def match_refugee_to_states(self, refugee_profile: Dict[str, Any]) -> pd.DataFrame:
        """
        Match a refugee profile to suitable US states based on multiple criteria
        """
        scores = []
        
        for state in self.states_data:
            score = self._calculate_match_score(refugee_profile, state)
            scores.append({
                'state': state['state'],
                'match_score': score['total_score'],
                'language_match': score['language_score'],
                'job_match': score['job_score'],
                'education_match': score['education_score'],
                'health_match': score['health_score'],
                'mental_health_match': score['mental_health_score'],
                'job_market_score': state['job_market_score'],
                'support_services_score': state['support_services_score']
            })
        
        results_df = pd.DataFrame(scores)
        return results_df.sort_values('match_score', ascending=False)
    
    def _calculate_match_score(self, refugee: Dict, state: Dict) -> Dict[str, float]:
        """Calculate matching scores for different criteria"""
        scores = {}
        
        # Language matching (30% weight)
        refugee_langs = set(refugee.get('languages', []))
        state_langs = set(state['languages'])
        language_overlap = len(refugee_langs.intersection(state_langs))
        scores['language_score'] = min(10, language_overlap * 3)  # Max 10 points
        
        # Job skills matching (25% weight)
        refugee_skills = set(refugee.get('job_skills', []))
        state_skills = set(state['job_skills'])
        job_overlap = len(refugee_skills.intersection(state_skills))
        scores['job_score'] = min(10, job_overlap * 2.5)  # Max 10 points
        
        # Education level matching (15% weight)
        refugee_edu = refugee.get('education_level', '')
        state_edus = state['education_levels']
        scores['education_score'] = 10 if refugee_edu in state_edus else 5
        
        # Health requirements matching (15% weight)
        refugee_health = set(refugee.get('health_requirements', []))
        state_health = set(state['health_requirements'])
        health_overlap = len(refugee_health.intersection(state_health))
        scores['health_score'] = min(10, health_overlap * 3)
        
        # Mental health support (15% weight)
        refugee_needs_mental = refugee.get('mental_health_support_needed', False)
        state_has_mental = state['mental_health_support']
        scores['mental_health_score'] = 10 if (not refugee_needs_mental or state_has_mental) else 0
        
        # Calculate total weighted score
        weights = {
            'language_score': 0.3,
            'job_score': 0.25,
            'education_score': 0.15,
            'health_score': 0.15,
            'mental_health_score': 0.15
        }
        
        total_score = sum(scores[key] * weights[key] for key in scores)
        scores['total_score'] = round(total_score, 2)
        
        return scores
    
    def get_detailed_state_info(self, state_name: str) -> Dict:
        """Get detailed information for a specific state"""
        for state in self.states_data:
            if state['state'].lower() == state_name.lower():
                return state
        return {}
    
    def get_all_states(self) -> List[Dict]:
        """Get information for all states"""
        return self.states_data

# Pydantic models for API request/response
class RefugeeProfile(BaseModel):
    name: str
    languages: List[str]
    job_skills: List[str]
    education_level: str
    health_requirements: List[str]
    mental_health_support_needed: bool
    cultural_background: Optional[str] = None
    family_size: Optional[int] = None

class StateMatch(BaseModel):
    state: str
    match_score: float
    language_match: float
    job_match: float
    education_match: float
    health_match: float
    mental_health_match: float
    job_market_score: int
    support_services_score: int

class MatchResponse(BaseModel):
    refugee_name: str
    matches: List[StateMatch]
    top_match: StateMatch
    timestamp: str
    total_states_evaluated: int

class StateInfoResponse(BaseModel):
    state: str
    languages: List[str]
    job_skills: List[str]
    education_levels: List[str]
    health_requirements: List[str]
    mental_health_support: bool
    refugee_communities: List[str]
    job_market_score: int
    support_services_score: int

# Initialize FastAPI app
app = FastAPI(
    title="Refugee State Matching API",
    description="API for matching refugees to suitable US states based on demographics and skills",
    version="1.0.0"
)

# Initialize the matcher
matcher = RefugeeStateMatcher()

@app.get("/")
async def root():
    return {
        "message": "Refugee State Matching API",
        "version": "1.0.0",
        "endpoints": {
            "POST /match": "Match refugee to states",
            "GET /states": "Get all states data",
            "GET /states/{state_name}": "Get specific state info",
            "GET /health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "states_loaded": len(matcher.states_data)
    }

@app.post("/match", response_model=MatchResponse)
async def match_refugee(refugee: RefugeeProfile):
    """
    Match a refugee profile to suitable US states
    """
    try:
        # Convert Pydantic model to dict
        refugee_dict = refugee.dict()
        
        # Perform matching
        matches_df = matcher.match_refugee_to_states(refugee_dict)
        
        # Convert matches to list of dictionaries
        matches_list = matches_df.to_dict('records')
        
        # Get top match
        top_match = matches_list[0] if matches_list else None
        
        return MatchResponse(
            refugee_name=refugee.name,
            matches=matches_list,
            top_match=top_match,
            timestamp=datetime.now().isoformat(),
            total_states_evaluated=len(matches_list)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/states", response_model=List[StateInfoResponse])
async def get_all_states():
    """
    Get demographic information for all available states
    """
    return matcher.get_all_states()

@app.get("/states/{state_name}", response_model=StateInfoResponse)
async def get_state_info(state_name: str):
    """
    Get detailed information for a specific state
    """
    state_info = matcher.get_detailed_state_info(state_name)
    if not state_info:
        raise HTTPException(status_code=404, detail=f"State '{state_name}' not found")
    return state_info

@app.get("/example-profiles")
async def get_example_profiles():
    """
    Get example refugee profiles for testing
    """
    examples = {
        "middle_eastern_construction": {
            "name": "Ahmed",
            "languages": ["Arabic", "English"],
            "job_skills": ["construction", "carpentry", "driving"],
            "education_level": "secondary",
            "health_requirements": ["general"],
            "mental_health_support_needed": True,
            "cultural_background": "Middle Eastern",
            "family_size": 4
        },
        "asian_tech_professional": {
            "name": "Ling",
            "languages": ["Chinese", "English"],
            "job_skills": ["technology", "software development"],
            "education_level": "bachelors",
            "health_requirements": ["general", "mental_health"],
            "mental_health_support_needed": True,
            "cultural_background": "Asian",
            "family_size": 3
        },
        "latin_american_healthcare": {
            "name": "Maria",
            "languages": ["Spanish", "English"],
            "job_skills": ["healthcare", "nursing"],
            "education_level": "bachelors",
            "health_requirements": ["general"],
            "mental_health_support_needed": False,
            "cultural_background": "Latin American",
            "family_size": 5
        }
    }
    return examples

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")