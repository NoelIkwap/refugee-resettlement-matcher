import requests
import json

def get_refugee_details():
    """Prompt user for refugee details"""
    print("🎯 REFUGEE MATCHING SYSTEM")
    print("=" * 40)
    print("Please enter the refugee details:\n")
    
    refugee_data = {}
    
    # Get basic information
    refugee_data['name'] = input("Refugee Name: ").strip()
    
    # Get languages
    print("\n🗣️ Enter languages spoken (comma-separated):")
    print("Example: Arabic, English, Spanish")
    languages = input("Languages: ").split(',')
    refugee_data['languages'] = [lang.strip() for lang in languages if lang.strip()]
    
    # Get job skills
    print("\n💼 Enter job skills (comma-separated):")
    print("Example: construction, carpentry, driving, healthcare")
    job_skills = input("Job Skills: ").split(',')
    refugee_data['job_skills'] = [skill.strip() for skill in job_skills if skill.strip()]
    
    # Get education level
    print("\n🎓 Enter education level:")
    print("Options: primary, secondary, vocational, bachelors, graduate")
    refugee_data['education_level'] = input("Education Level: ").strip().lower()
    
    # Get health requirements
    print("\n🏥 Enter health requirements (comma-separated):")
    print("Options: general, mental_health, specialized, none")
    health_req = input("Health Requirements: ").split(',')
    refugee_data['health_requirements'] = [req.strip() for req in health_req if req.strip() and req.strip() != 'none']
    
    # Get mental health support needed
    print("\n💚 Mental health support needed?")
    mental_health = input("(yes/no): ").strip().lower()
    refugee_data['mental_health_support_needed'] = mental_health in ['yes', 'y', 'true', '1']
    
    # Get cultural background
    print("\n🌍 Enter cultural background:")
    print("Example: Middle Eastern, Asian, African, Latin American")
    refugee_data['cultural_background'] = input("Cultural Background: ").strip()
    
    # Get family size
    print("\n👨‍👩‍👧‍👦 Enter family size (including the refugee):")
    try:
        refugee_data['family_size'] = int(input("Family Size: ").strip())
    except ValueError:
        refugee_data['family_size'] = 1
        print("⚠️  Invalid input, defaulting to family size 1")
    
    return refugee_data

def display_results(result):
    """Display matching results in a nice format"""
    print("\n" + "="*60)
    print("🎯 MATCHING RESULTS")
    print("="*60)
    print(f"Refugee: {result['refugee_name']}")
    print(f"🏆 BEST MATCH: {result['top_match']['state']} (Score: {result['top_match']['match_score']}/10)")
    
    print(f"\n📊 BREAKDOWN FOR BEST MATCH:")
    top = result['top_match']
    print(f"   • Language Compatibility: {top['language_match']}/10")
    print(f"   • Job Market Match: {top['job_match']}/10")
    print(f"   • Education Fit: {top['education_match']}/10")
    print(f"   • Healthcare Support: {top['health_match']}/10")
    print(f"   • Mental Health: {'✅ Available' if top['mental_health_match'] == 10 else '❌ Limited'}")
    print(f"   • Job Market Score: {top['job_market_score']}/10")
    print(f"   • Support Services: {top['support_services_score']}/10")
    
    print(f"\n🏅 TOP 5 MATCHING STATES:")
    for i, match in enumerate(result['matches'][:5], 1):
        print(f"\n#{i} {match['state']} - Overall: {match['match_score']}/10")
        print(f"   📈 Breakdown: Lang({match['language_match']}/10) Job({match['job_match']}/10) Edu({match['education_match']}/10) Health({match['health_match']}/10)")
        print(f"   💼 Job Market: {match['job_market_score']}/10, Support: {match['support_services_score']}/10")

def main():
    # API endpoint
    url = "http://localhost:8000/match"
    
    try:
        # Get refugee details from user
        refugee_data = get_refugee_details()
        
        # Show what we're sending
        print(f"\n🔍 Sending data for {refugee_data['name']}...")
        print("Please wait while we find the best matching states...")
        
        # Send the request to API
        response = requests.post(url, json=refugee_data, timeout=30)
        
        # Display results
        if response.status_code == 200:
            result = response.json()
            display_results(result)
            
            # Ask if user wants to see more details
            print(f"\n{'='*60}")
            see_details = input("\n🔍 Would you like to see details for a specific state? (yes/no): ").strip().lower()
            if see_details in ['yes', 'y']:
                state_name = input("Enter state name: ").strip()
                state_url = f"http://localhost:8000/states/{state_name}"
                state_response = requests.get(state_url)
                if state_response.status_code == 200:
                    state_info = state_response.json()
                    print(f"\n🏛️  DETAILS FOR {state_name.upper()}:")
                    print(f"   Languages: {', '.join(state_info['languages'])}")
                    print(f"   Job Skills Needed: {', '.join(state_info['job_skills'])}")
                    print(f"   Education Levels: {', '.join(state_info['education_levels'])}")
                    print(f"   Health Services: {', '.join(state_info['health_requirements'])}")
                    print(f"   Mental Health Support: {'✅ Yes' if state_info['mental_health_support'] else '❌ No'}")
                    print(f"   Refugee Communities: {', '.join(state_info['refugee_communities'])}")
                else:
                    print(f"❌ Could not find details for {state_name}")
                    
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Message: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API server!")
        print("💡 Make sure the API is running. Run this command in another terminal:")
        print("   python main.py")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The server is taking too long to respond.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Run the interactive matching system
if __name__ == "__main__":
    main()
    
    # Ask if user wants to run another match
    while True:
        print(f"\n{'='*60}")
        another = input("\n🔄 Would you like to match another refugee? (yes/no): ").strip().lower()
        if another in ['yes', 'y']:
            main()
        else:
            print("👋 Thank you for using the Refugee Matching System!")
            break