import requests
import json
import matplotlib.pyplot as plt
import numpy as np

def get_refugee_details():
    """Prompt user for refugee details"""
    print("🌍 GLOBAL REFUGEE MATCHING SYSTEM")
    print("=" * 50)
    print("Please enter the refugee details:\n")
    
    refugee_data = {}
    
    # Get basic information
    refugee_data['name'] = input("Refugee Name: ").strip()
    
    # Get languages
    print("\n🗣️ Enter languages spoken (comma-separated):")
    print("Example: Arabic, English, Spanish, French, German")
    languages = input("Languages: ").split(',')
    refugee_data['languages'] = [lang.strip() for lang in languages if lang.strip()]
    
    # Get job skills
    print("\n💼 Enter job skills (comma-separated):")
    print("Example: construction, healthcare, technology, engineering, education")
    job_skills = input("Job Skills: ").split(',')
    refugee_data['job_skills'] = [skill.strip() for skill in job_skills if skill.strip()]
    
    # Get education level
    print("\n🎓 Enter education level:")
    print("Options: primary, secondary, vocational, bachelors, graduate")
    refugee_data['education_level'] = input("Education Level: ").strip().lower()
    
    # Get health requirements
    print("\n🏥 Enter health requirements (comma-separated):")
    print("Options: general, mental_health, specialized, disability, none")
    health_req = input("Health Requirements: ").split(',')
    refugee_data['health_requirements'] = [req.strip() for req in health_req if req.strip() and req.strip() != 'none']
    
    # Get mental health support needed
    print("\n💚 Mental health support needed?")
    mental_health = input("(yes/no): ").strip().lower()
    refugee_data['mental_health_support_needed'] = mental_health in ['yes', 'y', 'true', '1']
    
    # Get cultural background
    print("\n🌍 Enter cultural background:")
    print("Example: Middle Eastern, Asian, African, Latin American, European")
    refugee_data['cultural_background'] = input("Cultural Background: ").strip()
    
    # Get family size
    print("\n👨‍👩‍👧‍👦 Enter family size (including the refugee):")
    try:
        refugee_data['family_size'] = int(input("Family Size: ").strip())
    except ValueError:
        refugee_data['family_size'] = 1
        print("⚠️  Invalid input, defaulting to family size 1")
    
    # Get preferred regions
    print("\n🌐 Preferred regions (comma-separated):")
    print("Options: USA, Canada, Europe, Australia, Any")
    regions = input("Regions: ").split(',')
    refugee_data['preferred_regions'] = [region.strip() for region in regions if region.strip()]
    
    return refugee_data

def get_global_cities_data():
    """Comprehensive global cities data for matching"""
    return {
        "cities": [
            # EUROPE
            {
                "city": "Berlin",
                "country": "Germany",
                "region": "Europe",
                "languages": ["German", "English", "Turkish", "Arabic"],
                "job_skills": ["technology", "engineering", "healthcare", "creative", "education"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "African", "Asian", "Eastern European"],
                "job_market_score": 8,
                "support_services_score": 9,
                "cost_of_living": 7
            },
            {
                "city": "London",
                "country": "United Kingdom", 
                "region": "Europe",
                "languages": ["English", "Polish", "Arabic", "French", "Spanish"],
                "job_skills": ["finance", "technology", "healthcare", "education", "creative"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "African", "Asian", "European"],
                "job_market_score": 9,
                "support_services_score": 8,
                "cost_of_living": 9
            },
            {
                "city": "Stockholm",
                "country": "Sweden",
                "region": "Europe",
                "languages": ["Swedish", "English", "Arabic", "Somali", "Persian"],
                "job_skills": ["technology", "engineering", "healthcare", "clean_energy"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "African", "Asian"],
                "job_market_score": 8,
                "support_services_score": 9,
                "cost_of_living": 8
            },
            {
                "city": "Paris",
                "country": "France",
                "region": "Europe",
                "languages": ["French", "English", "Arabic", "Spanish", "Portuguese"],
                "job_skills": ["tourism", "healthcare", "education", "creative", "technology"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["African", "Middle Eastern", "Asian"],
                "job_market_score": 7,
                "support_services_score": 8,
                "cost_of_living": 8
            },
            {
                "city": "Amsterdam",
                "country": "Netherlands",
                "region": "Europe",
                "languages": ["Dutch", "English", "Turkish", "Arabic", "Spanish"],
                "job_skills": ["technology", "logistics", "creative", "tourism", "engineering"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "African", "Asian"],
                "job_market_score": 8,
                "support_services_score": 8,
                "cost_of_living": 7
            },
            
            # CANADA
            {
                "city": "Toronto",
                "country": "Canada",
                "region": "Canada",
                "languages": ["English", "French", "Chinese", "Arabic", "Spanish"],
                "job_skills": ["finance", "technology", "healthcare", "education", "construction"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "Asian", "African", "Latin American"],
                "job_market_score": 8,
                "support_services_score": 9,
                "cost_of_living": 8
            },
            {
                "city": "Vancouver",
                "country": "Canada", 
                "region": "Canada",
                "languages": ["English", "Chinese", "Punjabi", "Arabic", "Spanish"],
                "job_skills": ["technology", "film", "tourism", "healthcare", "construction"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Asian", "Middle Eastern", "Latin American"],
                "job_market_score": 7,
                "support_services_score": 8,
                "cost_of_living": 9
            },
            {
                "city": "Montreal",
                "country": "Canada",
                "region": "Canada",
                "languages": ["French", "English", "Arabic", "Spanish", "Italian"],
                "job_skills": ["technology", "aerospace", "gaming", "healthcare", "education"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "African", "Asian", "Latin American"],
                "job_market_score": 7,
                "support_services_score": 8,
                "cost_of_living": 7
            },
            
            # AUSTRALIA
            {
                "city": "Sydney",
                "country": "Australia",
                "region": "Australia",
                "languages": ["English", "Chinese", "Arabic", "Vietnamese", "Greek"],
                "job_skills": ["finance", "technology", "healthcare", "construction", "tourism"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Asian", "Middle Eastern", "African", "European"],
                "job_market_score": 8,
                "support_services_score": 8,
                "cost_of_living": 9
            },
            {
                "city": "Melbourne",
                "country": "Australia",
                "region": "Australia",
                "languages": ["English", "Chinese", "Arabic", "Vietnamese", "Italian"],
                "job_skills": ["technology", "healthcare", "education", "creative", "manufacturing"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Asian", "Middle Eastern", "African", "European"],
                "job_market_score": 8,
                "support_services_score": 8,
                "cost_of_living": 8
            },
            
            # USA (additional cities)
            {
                "city": "New York City",
                "country": "USA",
                "region": "USA",
                "languages": ["English", "Spanish", "Chinese", "Russian", "Arabic"],
                "job_skills": ["finance", "technology", "healthcare", "creative", "education"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Middle Eastern", "Asian", "African", "Latin American", "European"],
                "job_market_score": 9,
                "support_services_score": 9,
                "cost_of_living": 9
            },
            {
                "city": "Los Angeles",
                "country": "USA",
                "region": "USA", 
                "languages": ["English", "Spanish", "Chinese", "Korean", "Arabic"],
                "job_skills": ["entertainment", "technology", "healthcare", "creative", "logistics"],
                "education_levels": ["secondary", "vocational", "bachelors", "graduate"],
                "health_requirements": ["general", "mental_health", "specialized"],
                "mental_health_support": True,
                "refugee_communities": ["Latin American", "Asian", "Middle Eastern", "African"],
                "job_market_score": 8,
                "support_services_score": 8,
                "cost_of_living": 9
            }
        ]
    }

def calculate_global_match_score(refugee, city):
    """Calculate matching scores for global cities"""
    scores = {}
    
    # Language matching (25% weight)
    refugee_langs = set(refugee.get('languages', []))
    city_langs = set(city['languages'])
    language_overlap = len(refugee_langs.intersection(city_langs))
    scores['language_score'] = min(10, language_overlap * 2.5)
    
    # Job skills matching (25% weight)
    refugee_skills = set(refugee.get('job_skills', []))
    city_skills = set(city['job_skills'])
    job_overlap = len(refugee_skills.intersection(city_skills))
    scores['job_score'] = min(10, job_overlap * 2.5)
    
    # Education level matching (15% weight)
    refugee_edu = refugee.get('education_level', '')
    city_edus = city['education_levels']
    scores['education_score'] = 10 if refugee_edu in city_edus else 5
    
    # Health requirements matching (15% weight)
    refugee_health = set(refugee.get('health_requirements', []))
    city_health = set(city['health_requirements'])
    health_overlap = len(refugee_health.intersection(city_health))
    scores['health_score'] = min(10, health_overlap * 3)
    
    # Mental health support (10% weight)
    refugee_needs_mental = refugee.get('mental_health_support_needed', False)
    city_has_mental = city['mental_health_support']
    scores['mental_health_score'] = 10 if (not refugee_needs_mental or city_has_mental) else 0
    
    # Cultural community matching (5% weight)
    refugee_culture = refugee.get('cultural_background', '').lower()
    city_communities = [comm.lower() for comm in city['refugee_communities']]
    scores['cultural_score'] = 10 if any(refugee_culture in comm for comm in city_communities) else 5
    
    # Cost of living adjustment (5% weight) - penalize high cost for large families
    family_size = refugee.get('family_size', 1)
    cost_of_living = city['cost_of_living']
    cost_penalty = 0
    if family_size > 3 and cost_of_living >= 8:
        cost_penalty = 2
    elif family_size > 2 and cost_of_living >= 7:
        cost_penalty = 1
    scores['cost_adjustment'] = -cost_penalty
    
    # Calculate total weighted score
    weights = {
        'language_score': 0.25,
        'job_score': 0.25,
        'education_score': 0.15,
        'health_score': 0.15,
        'mental_health_score': 0.10,
        'cultural_score': 0.05,
        'cost_adjustment': 0.05
    }
    
    total_score = sum(scores[key] * weights[key] for key in weights)
    scores['total_score'] = round(total_score, 2)
    
    return scores

def find_global_matches(refugee_data):
    """Find best global city matches"""
    cities_data = get_global_cities_data()
    matches = []
    
    preferred_regions = refugee_data.get('preferred_regions', [])
    
    for city in cities_data['cities']:
        # Filter by preferred regions if specified
        if preferred_regions and 'Any' not in preferred_regions:
            if city['region'] not in preferred_regions:
                continue
        
        score = calculate_global_match_score(refugee_data, city)
        
        matches.append({
            'city': city['city'],
            'country': city['country'],
            'region': city['region'],
            'match_score': score['total_score'],
            'language_match': score['language_score'],
            'job_match': score['job_score'],
            'education_match': score['education_score'],
            'health_match': score['health_score'],
            'mental_health_match': score['mental_health_score'],
            'cultural_match': score['cultural_score'],
            'job_market_score': city['job_market_score'],
            'support_services_score': city['support_services_score'],
            'cost_of_living': city['cost_of_living']
        })
    
    # Sort by match score
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return matches

def plot_match_results(refugee_name, matches, top_n=8):
    """Create matplotlib visualizations of the matching results"""
    
    if not matches:
        print("❌ No matches to plot.")
        return
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'🌍 Refugee Resettlement Matching Results for {refugee_name}', fontsize=16, fontweight='bold')
    
    # Top cities bar chart
    top_cities = matches[:top_n]
    cities = [f"{m['city']}\n({m['country']})" for m in top_cities]
    scores = [m['match_score'] for m in top_cities]
    colors = plt.cm.YlOrRd(np.linspace(0.6, 1, len(top_cities)))
    
    bars = ax1.bar(cities, scores, color=colors, edgecolor='black', alpha=0.8)
    ax1.set_title('🏆 Top Matching Cities (Overall Score)', fontweight='bold', pad=20)
    ax1.set_ylabel('Match Score /10', fontweight='bold')
    ax1.set_ylim(0, 10)
    
    # Add value labels on bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{score:.1f}', ha='center', va='bottom', fontweight='bold')
    
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # Breakdown for top city
    if top_cities:
        top_city = top_cities[0]
        categories = ['Languages', 'Jobs', 'Education', 'Healthcare', 'Cultural Fit']
        scores_breakdown = [
            top_city['language_match'],
            top_city['job_match'],
            top_city['education_match'],
            top_city['health_match'],
            top_city['cultural_match']
        ]
        
        colors_breakdown = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
        
        bars2 = ax2.bar(categories, scores_breakdown, color=colors_breakdown, edgecolor='black', alpha=0.8)
        ax2.set_title(f'📊 Score Breakdown for {top_city["city"]}', fontweight='bold', pad=20)
        ax2.set_ylabel('Score /10', fontweight='bold')
        ax2.set_ylim(0, 10)
        
        # Add value labels
        for bar, score in zip(bars2, scores_breakdown):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{score:.1f}', ha='center', va='bottom', fontweight='bold')
        
        ax2.grid(axis='y', alpha=0.3)
    
    # Regional distribution
    regions = {}
    for match in matches:
        region = match['region']
        if region not in regions:
            regions[region] = []
        regions[region].append(match['match_score'])
    
    region_avg = {region: np.mean(scores) for region, scores in regions.items()}
    
    colors_region = plt.cm.Set3(np.linspace(0, 1, len(regions)))
    wedges, texts, autotexts = ax3.pie(region_avg.values(), labels=region_avg.keys(), autopct='%1.1f%%',
                                      colors=colors_region, startangle=90)
    ax3.set_title('🌐 Distribution by Region', fontweight='bold', pad=20)
    
    # Make autotexts bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # City metrics comparison for top 3 cities
    if len(top_cities) >= 3:
        top_3 = top_cities[:3]
        metrics = ['Job Market', 'Support Services', 'Cost of Living']
        
        x = np.arange(len(metrics))
        width = 0.25
        
        for i, city in enumerate(top_3):
            city_metrics = [
                city['job_market_score'],
                city['support_services_score'],
                10 - city['cost_of_living']  # Invert cost (lower is better)
            ]
            ax4.bar(x + i*width, city_metrics, width, label=f"{city['city']}", alpha=0.8)
        
        ax4.set_title('📈 City Metrics Comparison (Top 3)', fontweight='bold', pad=20)
        ax4.set_ylabel('Score /10', fontweight='bold')
        ax4.set_xticks(x + width)
        ax4.set_xticklabels(metrics)
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)
        ax4.set_ylim(0, 10)
    
    plt.tight_layout()
    plt.show()
    
    # Additional detailed plot for top city
    if top_cities:
        plot_detailed_city_analysis(top_cities[0])

def plot_detailed_city_analysis(top_city):
    """Create a detailed radar chart for the top matching city"""
    
    categories = ['Language\nMatch', 'Job\nMatch', 'Education\nMatch', 
                  'Healthcare\nMatch', 'Cultural\nFit', 'Job\nMarket', 
                  'Support\nServices', 'Affordability']
    
    scores = [
        top_city['language_match'],
        top_city['job_match'],
        top_city['education_match'],
        top_city['health_match'],
        top_city['cultural_match'],
        top_city['job_market_score'],
        top_city['support_services_score'],
        10 - top_city['cost_of_living']  # Affordability (inverted cost)
    ]
    
    # Complete the circle
    categories += [categories[0]]
    scores += [scores[0]]
    
    angles = np.linspace(0, 2*np.pi, len(categories)-1, endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    ax.plot(angles, scores, 'o-', linewidth=2, label='Scores', color='#e74c3c')
    ax.fill(angles, scores, alpha=0.25, color='#e74c3c')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories[:-1])
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'])
    ax.grid(True)
    
    plt.title(f'🎯 Detailed Analysis: {top_city["city"]}, {top_city["country"]}\n'
              f'Overall Match Score: {top_city["match_score"]}/10', 
              size=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()

def display_global_results(refugee_name, matches):
    """Display global matching results"""
    print("\n" + "="*70)
    print("🌍 GLOBAL MATCHING RESULTS")
    print("="*70)
    print(f"Refugee: {refugee_name}")
    
    if not matches:
        print("❌ No suitable matches found for the given criteria.")
        return
    
    print(f"🏆 BEST GLOBAL MATCHES:")
    
    for i, match in enumerate(matches[:3], 1):
        print(f"\n#{i} {match['city']}, {match['country']} ({match['region']})")
        print(f"   Overall Match Score: {match['match_score']}/10")
        print(f"   📊 Breakdown:")
        print(f"      • Languages: {match['language_match']}/10")
        print(f"      • Jobs: {match['job_match']}/10")
        print(f"      • Education: {match['education_match']}/10")
        print(f"      • Healthcare: {match['health_match']}/10")
        print(f"      • Mental Health: {'✅' if match['mental_health_match'] == 10 else '⚠️'}")
        print(f"      • Cultural Fit: {match['cultural_match']}/10")
        print(f"   💼 Job Market: {match['job_market_score']}/10")
        print(f"   🛠️  Support Services: {match['support_services_score']}/10")
        print(f"   💰 Cost of Living: {match['cost_of_living']}/10")

def main():
    try:
        # Get refugee details from user
        refugee_data = get_refugee_details()
        
        # Show what we're sending
        print(f"\n🔍 Searching for best global cities for {refugee_data['name']}...")
        print("Please wait while we analyze cities worldwide...")
        
        # Find global matches
        all_matches = find_global_matches(refugee_data)
        
        # Display results
        display_global_results(refugee_data['name'], all_matches)
        
        # Plot results
        print(f"\n📈 Generating visualizations...")
        plot_match_results(refugee_data['name'], all_matches)
        
        # Show available regions
        print(f"\n{'='*70}")
        see_all = input("\n🔍 Would you like to see all available cities? (yes/no): ").strip().lower()
        if see_all in ['yes', 'y']:
            cities_data = get_global_cities_data()
            print(f"\n🏙️  ALL AVAILABLE CITIES:")
            for city in cities_data['cities']:
                print(f"   • {city['city']}, {city['country']} ({city['region']})")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Run the interactive global matching system
if __name__ == "__main__":
    # Install required package if not already installed
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("📦 Installing matplotlib...")
        import subprocess
        subprocess.check_call(["pip", "install", "matplotlib"])
        import matplotlib.pyplot as plt
    
    main()
    
    # Ask if user wants to run another match
    while True:
        print(f"\n{'='*70}")
        another = input("\n🔄 Would you like to match another refugee globally? (yes/no): ").strip().lower()
        if another in ['yes', 'y']:
            main()
        else:
            print("👋 Thank you for using the Global Refugee Matching System!")
            break