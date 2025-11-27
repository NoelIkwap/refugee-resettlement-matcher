# rl_matcher.py
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
import random
from collections import defaultdict
import json
import os

class RefugeeMatchingRL:
    def __init__(self, state_size=50, action_size=12):  # Larger state space for more precision
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size))
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        
        self.cities = [
            "Berlin", "London", "Stockholm", "Paris", "Amsterdam",
            "Toronto", "Vancouver", "Montreal", 
            "Sydney", "Melbourne", "New York City", "Los Angeles"
        ]
        
        # Load city data from your existing system
        self.city_data = self._load_city_data()
        self.placement_success = defaultdict(list)
        
        # Load existing Q-table if available
        self.load_model()
        
    def _load_city_data(self) -> Dict[str, Any]:
        """Load city data matching your existing system"""
        from global_matcher import get_global_cities_data  # Import your existing function
        
        cities_data = get_global_cities_data()
        city_info = {}
        for city in cities_data['cities']:
            city_info[city['city']] = {
                'cost_of_living': city['cost_of_living'],
                'mental_health_support': city['mental_health_support'],
                'job_market_score': city['job_market_score'],
                'support_services_score': city['support_services_score']
            }
        return city_info
        
    def state_to_index(self, refugee_state: Dict[str, Any]) -> int:
        """Convert refugee state to discrete state index with more granularity"""
        state_vector = []
        
        # Language complexity (0-3)
        lang_count = len(refugee_state.get('languages', []))
        state_vector.append(min(3, lang_count))
        
        # Job skills complexity (0-3)
        job_count = len(refugee_state.get('job_skills', []))
        state_vector.append(min(3, job_count))
        
        # Education level (0-4)
        edu_map = {'primary': 0, 'secondary': 1, 'vocational': 2, 'bachelors': 3, 'graduate': 4}
        edu_score = edu_map.get(refugee_state.get('education_level', 'primary'), 0)
        state_vector.append(edu_score)
        
        # Family size (0-4)
        family_size = min(4, refugee_state.get('family_size', 1))
        state_vector.append(family_size)
        
        # Health needs complexity (0-2)
        health_needs = len(refugee_state.get('health_requirements', []))
        mental_health = 1 if refugee_state.get('mental_health_support_needed', False) else 0
        state_vector.append(min(2, health_needs + mental_health))
        
        # Convert to state index (more granular)
        state_index = sum(val * (5**i) for i, val in enumerate(state_vector))
        return min(state_index, self.state_size - 1)
    
    def choose_action(self, state_index: int) -> int:
        """Epsilon-greedy action selection"""
        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)  # Explore
        else:
            return np.argmax(self.q_table[state_index])  # Exploit
    
    def get_reward(self, refugee_state: Dict, city_index: int, success_metric: float) -> float:
        """Calculate reward based on placement success and city compatibility"""
        base_reward = success_metric * 10
        
        city_name = self.cities[city_index]
        city_info = self.city_data.get(city_name, {})
        
        # Enhanced reward calculation
        family_size = refugee_state.get('family_size', 1)
        
        # Cost of living penalty
        if family_size > 2 and city_info.get('cost_of_living', 5) > 7:
            base_reward -= (city_info['cost_of_living'] - 7) * 0.5
        
        # Mental health support check
        if refugee_state.get('mental_health_support_needed', False) and not city_info.get('mental_health_support', True):
            base_reward -= 3
            
        # Bonus for good job market match
        job_skills = refugee_state.get('job_skills', [])
        if any(skill in ['technology', 'healthcare', 'engineering'] for skill in job_skills):
            base_reward += city_info.get('job_market_score', 5) * 0.2
            
        return max(0, base_reward)  # Ensure non-negative reward
    
    def update_q_value(self, state: int, action: int, reward: float, next_state: int):
        """Q-learning update rule"""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error
    
    def train_episode(self, refugee_state: Dict[str, Any], success_metric: float, actual_city: str = None):
        """Train on one refugee placement"""
        state = self.state_to_index(refugee_state)
        action = self.choose_action(state)
        
        # If we know the actual city used, use it for training
        if actual_city and actual_city in self.cities:
            action = self.cities.index(actual_city)
        
        next_state = state  # Simplified - in real scenario, this would evolve
        
        reward = self.get_reward(refugee_state, action, success_metric)
        self.update_q_value(state, action, reward, next_state)
        
        # Track placement success for this city
        city_name = self.cities[action]
        self.placement_success[city_name].append(success_metric)
        
        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        return action, reward, city_name
    
    def predict_best_cities(self, refugee_state: Dict[str, Any], top_k: int = 3) -> List[Tuple[str, float]]:
        """Predict top K best cities with confidence scores"""
        state = self.state_to_index(refugee_state)
        q_values = self.q_table[state]
        
        # Get top K actions
        top_actions = np.argsort(q_values)[-top_k:][::-1]
        
        results = []
        for action in top_actions:
            city = self.cities[action]
            confidence = q_values[action] / 10.0  # Normalize to 0-1
            results.append((city, min(1.0, confidence)))
            
        return results
    
    def save_model(self, filepath: str = "rl_model.json"):
        """Save Q-table and training state"""
        model_data = {
            'q_table': self.q_table.tolist(),
            'epsilon': self.epsilon,
            'placement_success': dict(self.placement_success)
        }
        
        with open(filepath, 'w') as f:
            json.dump(model_data, f)
        print(f"✅ RL model saved to {filepath}")
    
    def load_model(self, filepath: str = "rl_model.json"):
        """Load Q-table and training state"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    model_data = json.load(f)
                
                self.q_table = np.array(model_data['q_table'])
                self.epsilon = model_data['epsilon']
                self.placement_success = defaultdict(list, model_data['placement_success'])
                print(f"✅ RL model loaded from {filepath}")
        except Exception as e:
            print(f"❌ Error loading RL model: {e}")

# Integration with your existing system
def enhance_with_rl(refugee_data: Dict[str, Any], use_rl: bool = True) -> Dict[str, Any]:
    """Enhanced matching that combines rule-based and RL approaches"""
    # Initialize RL agent
    rl_agent = RefugeeMatchingRL()
    
    if use_rl and np.sum(rl_agent.q_table) > 0:  # Only use RL if trained
        # Get RL recommendations
        rl_recommendations = rl_agent.predict_best_cities(refugee_data, top_k=2)
        
        return {
            'rl_used': True,
            'rl_recommendations': rl_recommendations,
            'rl_confidence': rl_recommendations[0][1] if rl_recommendations else 0.0
        }
    else:
        return {
            'rl_used': False,
            'rl_recommendations': [],
            'rl_confidence': 0.0
        }

# Training function for collecting real data
def train_rl_from_feedback(refugee_data: Dict[str, Any], placed_city: str, success_score: float):
    """Train RL model from actual placement feedback"""
    rl_agent = RefugeeMatchingRL()
    action, reward, city_name = rl_agent.train_episode(refugee_data, success_score, placed_city)
    rl_agent.save_model()
    
    print(f"🧠 RL trained: {refugee_data['name']} -> {city_name} (Success: {success_score}, Reward: {reward:.2f})")

if __name__ == "__main__":
    # Demo the RL system
    rl_agent = RefugeeMatchingRL()
    
    # Simulate some training
    training_examples = [
        ({'name': 'Ahmed', 'languages': ['Arabic', 'English'], 'job_skills': ['construction'], 
          'education_level': 'secondary', 'family_size': 4, 'mental_health_support_needed': True}, 
         'Berlin', 0.8),
        ({'name': 'Maria', 'languages': ['Spanish'], 'job_skills': ['healthcare'], 
          'education_level': 'bachelors', 'family_size': 2, 'mental_health_support_needed': False}, 
         'Toronto', 0.9),
    ]
    
    for refugee_data, city, success in training_examples:
        train_rl_from_feedback(refugee_data, city, success)
    
    # Test prediction
    test_refugee = {
        'name': 'Test',
        'languages': ['Chinese', 'English'],
        'job_skills': ['technology'],
        'education_level': 'graduate',
        'family_size': 3,
        'mental_health_support_needed': True
    }
    
    recommendations = rl_agent.predict_best_cities(test_refugee)
    print("🤖 RL Recommendations:", recommendations)
    