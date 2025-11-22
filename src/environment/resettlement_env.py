import pandas as pd
import numpy as np
from typing import List, Dict, Any

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
    
    def display_top_matches(self, refugee_profile: Dict, top_n: int = 5):
        """Display top matching states in a user-friendly format"""
        matches = self.match_refugee_to_states(refugee_profile)
        top_matches = matches.head(top_n)
        
        print(f"🎯 TOP {top_n} MATCHING STATES FOR REFUGEE")
        print("=" * 60)
        
        for idx, (_, match) in enumerate(top_matches.iterrows(), 1):
            print(f"\n#{idx} {match['state']}")
            print(f"   Overall Match Score: {match['match_score']}/10")
            print(f"   Language Match: {match['language_match']}/10")
            print(f"   Job Match: {match['job_match']}/10")
            print(f"   Education Match: {match['education_match']}/10")
            print(f"   Health Match: {match['health_match']}/10")
            print(f"   Mental Health Support: {'✅' if match['mental_health_match'] == 10 else '❌'}")
            print(f"   Job Market: {match['job_market_score']}/10")
            print(f"   Support Services: {match['support_services_score']}/10")

# Example usage and demonstration
def main():
    matcher = RefugeeStateMatcher()
    
    # Example refugee profiles
    example_refugees = {
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
    
    # Interactive matching
    print("🇺🇸 REFUGEE STATE MATCHING SYSTEM")
    print("=" * 50)
    
    # Test with example refugee
    test_refugee = example_refugees["middle_eastern_construction"]
    
    print(f"\n🧍 Testing with refugee: {test_refugee['name']}")
    print(f"📋 Profile: {test_refugee['cultural_background']}, {test_refugee['job_skills'][0]} skills")
    
    matcher.display_top_matches(test_refugee, top_n=5)
    
    return matcher

# Create interactive function for user input
def interactive_matching():
    """Interactive function for user to input refugee details"""
    matcher = RefugeeStateMatcher()
    
    print("\n🎯 REFUGEE PROFILE BUILDER")
    print("=" * 40)
    
    # Collect refugee information
    refugee_profile = {}
    
    refugee_profile['name'] = input("Enter refugee name: ")
    
    print("\n🗣️ Languages spoken (comma-separated):")
    print("Options: English, Spanish, Arabic, Chinese, Vietnamese, French, etc.")
    languages = input("Languages: ").split(',')
    refugee_profile['languages'] = [lang.strip() for lang in languages]
    
    print("\n💼 Job skills (comma-separated):")
    print("Options: construction, healthcare, technology, education, manufacturing, etc.")
    job_skills = input("Job skills: ").split(',')
    refugee_profile['job_skills'] = [skill.strip() for skill in job_skills]
    
    print("\n🎓 Education level:")
    print("Options: primary, secondary, vocational, bachelors, graduate")
    refugee_profile['education_level'] = input("Education level: ").strip().lower()
    
    print("\n🏥 Health requirements (comma-separated):")
    print("Options: general, mental_health, specialized, none")
    health_req = input("Health requirements: ").split(',')
    refugee_profile['health_requirements'] = [req.strip() for req in health_req if req.strip()]
    
    print("\n💚 Mental health support needed? (yes/no):")
    mental_health = input("Mental health support: ").strip().lower()
    refugee_profile['mental_health_support_needed'] = mental_health in ['yes', 'y', 'true']
    
    print("\n🌍 Cultural background:")
    refugee_profile['cultural_background'] = input("Cultural background: ").strip()
    
    print("\n👨‍👩‍👧‍👦 Family size:")
    refugee_profile['family_size'] = int(input("Family size: ").strip())
    
    # Perform matching
    print(f"\n🔍 Finding best states for {refugee_profile['name']}...")
    matcher.display_top_matches(refugee_profile, top_n=5)
    
    return refugee_profile, matcher

# Run the system
if __name__ == "__main__":
    # Initialize the matcher
    matcher = main()
    
    # Uncomment the line below for interactive input
    # refugee_profile, matcher = interactive_matching()