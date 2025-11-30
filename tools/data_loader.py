import csv
import json
from typing import Dict, List, Any

class DataLoader:
    """Load and structure adoption data from CSV files"""
    
    def __init__(self, animal_file: str, adopter_file: str):
        """
        Initialize DataLoader with CSV file paths
        
        Args:
            animal_file: Path to animal_data.csv
            adopter_file: Path to adopter_data.csv
        """
        self.animals = self._load_csv(animal_file)
        self.adopters = self._load_csv(adopter_file)
        print(f"✓ Loaded {len(self.animals)} animals")
        print(f"✓ Loaded {len(self.adopters)} adopters")
    
    def _load_csv(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Load CSV file into list of dictionaries
        
        Each row becomes a dictionary with column names as keys
        """
        data = []
        try:
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        except FileNotFoundError:
            print(f"ERROR: File not found - {filepath}")
            return []
    
    def get_animal(self, animal_id: str) -> Dict[str, Any]:
        """Retrieve specific animal by ID"""
        for animal in self.animals:
            if animal['animal_id'] == animal_id:
                return animal
        return None
    
    def get_adopter(self, adopter_id: str) -> Dict[str, Any]:
        """Retrieve specific adopter by ID"""
        for adopter in self.adopters:
            if adopter['adopter_id'] == adopter_id:
                return adopter
        return None
    
    def get_all_animals(self) -> List[Dict[str, Any]]:
        """Return all animals"""
        return self.animals
    
    def get_all_adopters(self) -> List[Dict[str, Any]]:
        """Return all adopters"""
        return self.adopters
    
    def format_animal_for_agent(self, animal: Dict) -> str:
        """
        Format animal data as readable text for agent
        The agent will read this formatted text
        """
        return f"""
Animal: {animal.get('name', 'Unknown')} (ID: {animal.get('animal_id')})
Species: {animal.get('species')}
Breed: {animal.get('breed')}
Age: {animal.get('age_years')} years
Energy Level: {animal.get('energy_level')}
Good with Kids: {animal.get('good_with_kids')}
Good with Dogs: {animal.get('good_with_dogs')}
Special Needs: {animal.get('special_needs')}
Traits: {animal.get('behavioral_traits')}
"""
    
    def format_adopter_for_agent(self, adopter: Dict) -> str:
        """
        Format adopter data as readable text for agent
        The agent will read this formatted text
        """
        return f"""
Adopter: {adopter.get('name', 'Unknown')} (ID: {adopter.get('adopter_id')})
Home Type: {adopter.get('home_type')}
Has Kids: {adopter.get('has_kids')}
Has Other Pets: {adopter.get('has_other_pets')}
Lifestyle: {adopter.get('lifestyle')}
Commitment Level: {adopter.get('commitment_level')}
Experience: {adopter.get('experience_level')}
Preferences: {adopter.get('preferences')}
"""
