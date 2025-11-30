"""
MATCHING AGENT - Step 2 in the adoption process

Purpose: Compare animals and adopters, calculate compatibility
Role: Finds the best matches using scoring algorithm
"""

from tools.data_loader import DataLoader
from tools.compatibility_scorer import CompatibilityScorer
import json

class MatchingAgent:
    """
    Agent responsible for comparing animals and adopters and recommending matches.
    Think of this as the "matching counselor" who knows what works.
    """
    
    def __init__(self, data_loader: DataLoader):
        """Initialize with data loader and scorer"""
        self.data_loader = data_loader
        self.scorer = CompatibilityScorer()
        print("✓ Matching Agent initialized")
    
    def find_matches(self, adopter_id: str, top_n: int = 3) -> list:
        """
        Find best animals for a specific adopter
        
        Args:
            adopter_id: ID of adopter (e.g., '1')
            top_n: Number of top matches to return (default 3)
        
        Returns:
            List of matches sorted by score (highest first)
        """
        print(f"\n[MATCHING AGENT] Finding matches for adopter {adopter_id}...")
        
        adopter = self.data_loader.get_adopter(adopter_id)
        if not adopter:
            print(f"ERROR: Adopter {adopter_id} not found")
            return []
        
        matches = []
        
        # Score adopter against ALL animals
        for animal in self.data_loader.get_all_animals():
            # Calculate compatibility score
            score, reasoning = self.scorer.calculate_compatibility(animal, adopter)
            
            match = {
                'animal_id': animal['animal_id'],
                'animal_name': animal['name'],
                'adopter_id': adopter['adopter_id'],
                'adopter_name': adopter['name'],
                'score': score,
                'reasoning': reasoning
            }
            matches.append(match)
        
        # Sort by score (highest first)
        matches.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top N matches
        top_matches = matches[:top_n]
        
        print(f"✓ Found {len(top_matches)} matches")
        for i, match in enumerate(top_matches, 1):
            print(f"  {i}. {match['animal_name']} - Score: {match['score']}/100")
        
        return top_matches
    
    def get_detailed_match(self, animal_id: str, adopter_id: str) -> dict:
        """
        Get detailed analysis of a specific animal-adopter match
        
        Args:
            animal_id: ID of animal
            adopter_id: ID of adopter
        
        Returns:
            Dictionary with detailed match information
        """
        print(f"\n[MATCHING AGENT] Detailed analysis: Animal {animal_id} ↔ Adopter {adopter_id}")
        
        animal = self.data_loader.get_animal(animal_id)
        adopter = self.data_loader.get_adopter(adopter_id)
        
        if not animal or not adopter:
            return {"error": "Animal or adopter not found"}
        
        # Get compatibility score
        score, reasoning = self.scorer.calculate_compatibility(animal, adopter)
        
        # Create detailed analysis
        analysis = {
            'animal_id': animal_id,
            'animal_name': animal['name'],
            'adopter_id': adopter_id,
            'adopter_name': adopter['name'],
            'score': score,
            'reasoning': reasoning,
            'recommendation': self._get_recommendation(score),
            'animal_data': animal,
            'adopter_data': adopter
        }
        
        print(f"✓ Score: {score}/100")
        print(f"✓ Recommendation: {analysis['recommendation']}")
        
        return analysis
    
    def _get_recommendation(self, score: int) -> str:
        """Convert score to recommendation text"""
        if score >= 80:
            return "STRONG MATCH - Highly recommended"
        elif score >= 60:
            return "GOOD MATCH - Recommended with notes"
        elif score >= 40:
            return "POSSIBLE MATCH - Requires careful consideration"
        else:
            return "NOT RECOMMENDED - Compatibility concerns"

# Test the agent
if __name__ == "__main__":
    from tools.data_loader import DataLoader
    
    print("="*60)
    print("MATCHING AGENT TEST")
    print("="*60)
    
    loader = DataLoader('animal_data.csv', 'adopter_data.csv')
    matcher = MatchingAgent(loader)
    
    # Find matches for adopter 1
    matches = matcher.find_matches('1', top_n=3)
    
    print("\nTop 3 Matches:")
    for i, match in enumerate(matches, 1):
        print(f"\n{i}. {match['animal_name']} - {match['score']}/100")
        print(match['reasoning'])
    
    # Get detailed match
    detailed = matcher.get_detailed_match('1', '1')
    print(f"\nDetailed Match:\n{json.dumps(detailed, indent=2, default=str)}")
