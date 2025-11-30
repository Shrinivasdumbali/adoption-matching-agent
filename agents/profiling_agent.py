"""
PROFILING AGENT - Step 1 in the adoption process

Purpose: Understand and structure information about animals and adopters
Role: Extracts key traits, creates profiles, prepares data for matching
"""

import sys
sys.path.insert(0, '.')
from tools.data_loader import DataLoader

import json

class ProfilingAgent:
    """
    Agent responsible for gathering and structuring animal/adopter data.
    Think of this as the "intake specialist" at a shelter.
    """
    
    def __init__(self, data_loader: DataLoader):
        """Initialize with data loader"""
        self.data_loader = data_loader
        print("✓ Profiling Agent initialized")
    
    def profile_animal(self, animal_id: str) -> dict:
        """
        Profile a specific animal
        
        Args:
            animal_id: ID of animal to profile (e.g., '1')
        
        Returns:
            Dictionary with animal profile information
        """
        print(f"\n[PROFILING AGENT] Analyzing animal {animal_id}...")
        
        animal = self.data_loader.get_animal(animal_id)
        if not animal:
            return {"error": f"Animal {animal_id} not found"}
        
        # Extract and structure key information
        profile = {
            "type": "animal",
            "id": animal_id,
            "name": animal.get('name'),
            "species": animal.get('species'),
            "breed": animal.get('breed'),
            "age_years": int(animal.get('age_years', 0)),
            "energy_level": animal.get('energy_level'),
            "good_with_kids": animal.get('good_with_kids').lower() == 'yes',
            "good_with_dogs": animal.get('good_with_dogs').lower() == 'yes',
            "special_needs": animal.get('special_needs').lower() == 'yes',
            "behavioral_traits": animal.get('behavioral_traits').split(';'),
            "raw_data": animal
        }
        
        # Create summary
        traits_text = ', '.join(profile['behavioral_traits'])
        profile['summary'] = (
            f"{profile['name']}, a {profile['age_years']}-year-old {profile['breed']} "
            f"with {profile['energy_level']} energy. Traits: {traits_text}. "
            f"Good with kids: {profile['good_with_kids']}, "
            f"Good with dogs: {profile['good_with_dogs']}"
        )
        
        print(f"✓ Profile created: {profile['summary']}")
        return profile
    
    def profile_adopter(self, adopter_id: str) -> dict:
        """
        Profile a specific adopter
        
        Args:
            adopter_id: ID of adopter to profile (e.g., '1')
        
        Returns:
            Dictionary with adopter profile information
        """
        print(f"\n[PROFILING AGENT] Analyzing adopter {adopter_id}...")
        
        adopter = self.data_loader.get_adopter(adopter_id)
        if not adopter:
            return {"error": f"Adopter {adopter_id} not found"}
        
        # Extract and structure key information
        profile = {
            "type": "adopter",
            "id": adopter_id,
            "name": adopter.get('name'),
            "home_type": adopter.get('home_type'),
            "has_kids": adopter.get('has_kids').lower() == 'yes',
            "has_other_pets": adopter.get('has_other_pets').lower() == 'yes',
            "lifestyle": adopter.get('lifestyle'),
            "commitment_level": adopter.get('commitment_level'),
            "experience_level": adopter.get('experience_level'),
            "preferences": adopter.get('preferences').split(';'),
            "raw_data": adopter
        }
        
        # Create summary
        profile['summary'] = (
            f"{profile['name']}, living in a {profile['home_type']} "
            f"with {profile['lifestyle']} lifestyle. "
            f"Experience: {profile['experience_level']}, "
            f"Commitment: {profile['commitment_level']}"
        )
        
        print(f"✓ Profile created: {profile['summary']}")
        return profile
    
    def format_profile_for_matching(self, profile: dict) -> str:
        """
        Convert profile to text format that matching agent can process
        """
        return f"""
Type: {profile.get('type')}
ID: {profile.get('id')}
Name: {profile.get('name')}
Summary: {profile.get('summary')}
"""

# Test the agent
if __name__ == "__main__":
    from tools.data_loader import DataLoader
    
    print("="*60)
    print("PROFILING AGENT TEST")
    print("="*60)
    
    loader = DataLoader('animal_data.csv', 'adopter_data.csv')
    profiler = ProfilingAgent(loader)
    
    # Test animal profile
    animal_profile = profiler.profile_animal('1')
    print(f"\nAnimal Profile:\n{json.dumps(animal_profile, indent=2, default=str)}")
    
    # Test adopter profile
    adopter_profile = profiler.profile_adopter('1')
    print(f"\nAdopter Profile:\n{json.dumps(adopter_profile, indent=2, default=str)}")
