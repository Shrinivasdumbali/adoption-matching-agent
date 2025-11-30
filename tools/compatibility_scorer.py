from typing import Dict, Any, Tuple

class CompatibilityScorer:
    """Calculate adoption compatibility scores between animals and adopters"""
    
    def __init__(self):
        """
        Initialize with scoring weights
        These weights determine what factors matter most (0.30 = 30%)
        """
        self.weights = {
            'lifestyle_match': 0.30,      # How well lifestyles align
            'experience_match': 0.20,     # Can adopter handle the animal's needs
            'home_fit': 0.20,             # Does home type fit the animal
            'behavioral_fit': 0.20,       # Are they compatible (kids/pets)
            'special_needs': 0.10         # Can adopter handle special needs
        }
    
    def calculate_compatibility(self, animal: Dict[str, Any], 
                               adopter: Dict[str, Any]) -> Tuple[int, str]:
        """
        Calculate compatibility score (0-100) and reasoning
        
        Returns:
            Tuple of (score as integer, reasoning as string)
        
        Example:
            score, reason = scorer.calculate_compatibility(max_dog, john_adopter)
            # Returns: (85, "Score breakdown: ...")
        """
        
        # Calculate individual scores for each aspect (all 0-100)
        scores = {
            'lifestyle_match': self._score_lifestyle(animal, adopter),
            'experience_match': self._score_experience(animal, adopter),
            'home_fit': self._score_home(animal, adopter),
            'behavioral_fit': self._score_behavior(animal, adopter),
            'special_needs': self._score_special_needs(animal, adopter)
        }
        
        # Calculate WEIGHTED total score
        # Example: 85 * 0.30 + 90 * 0.20 + ... = final_score
        total_score = sum(
            scores[key] * self.weights[key] 
            for key in scores.keys()
        )
        
        # Generate human-readable explanation
        reasoning = self._generate_reasoning(animal, adopter, scores)
        
        return int(total_score), reasoning
    
    def _score_lifestyle(self, animal: Dict, adopter: Dict) -> int:
        """
        Score lifestyle compatibility (0-100)
        
        Example:
        - High-energy dog + Active person = HIGH score
        - High-energy dog + Quiet person = LOW score
        """
        animal_energy = animal.get('energy_level', 'medium').lower()
        adopter_lifestyle = adopter.get('lifestyle', 'moderate').lower()
        
        # Map text to numeric values (1=low, 2=medium, 3=high)
        energy_map = {'low': 1, 'medium': 2, 'high': 3}
        lifestyle_map = {
            'quiet': 1, 
            'relaxed': 1, 
            'moderate': 2, 
            'active': 3, 
            'outdoor-person': 3,
            'family-focused': 2,
            'busy': 1
        }
        
        animal_level = energy_map.get(animal_energy, 2)
        adopter_level = lifestyle_map.get(adopter_lifestyle, 2)
        
        # Calculate score based on difference
        diff = abs(animal_level - adopter_level)
        if diff == 0:
            return 100  # Perfect match
        elif diff == 1:
            return 70   # Close match
        else:
            return 40   # Poor match
    
    def _score_experience(self, animal: Dict, adopter: Dict) -> int:
        """
        Score adopter experience level vs animal needs
        
        Example:
        - Animal needs training + Experienced adopter = HIGH
        - Animal needs training + Beginner adopter = LOW
        """
        animal_needs_training = animal.get('special_needs', '').lower() == 'yes'
        adopter_experience = adopter.get('experience_level', 'beginner').lower()
        
        if animal_needs_training and adopter_experience == 'experienced':
            return 100  # Expert handling difficult animal
        elif animal_needs_training and adopter_experience == 'beginner':
            return 40   # Beginner with difficult animal = risky
        elif not animal_needs_training and adopter_experience == 'beginner':
            return 90   # Beginner with easy animal = good
        else:
            return 100  # Experienced with any animal = good
    
    def _score_home(self, animal: Dict, adopter: Dict) -> int:
        """
        Score if home type fits animal size
        
        Example:
        - Large dog + House = HIGH
        - Large dog + Apartment = LOW
        """
        animal_size = self._estimate_size(animal.get('breed', ''))
        home_type = adopter.get('home_type', 'apartment').lower()
        
        if home_type == 'house':
            # Houses fit most animals well
            if animal_size == 'large':
                return 100
            else:
                return 90
        else:  # apartment
            # Apartments better for small/calm animals
            if animal_size == 'large':
                return 40
            else:
                return 85
    
    def _estimate_size(self, breed: str) -> str:
        """Estimate animal size from breed name"""
        large_breeds = ['retriever', 'shepherd', 'labrador', 'pit bull']
        small_breeds = ['cat', 'tabby', 'persian', 'beagle']
        
        breed_lower = breed.lower()
        if any(b in breed_lower for b in large_breeds):
            return 'large'
        elif any(b in breed_lower for b in small_breeds):
            return 'small'
        else:
            return 'medium'
    
    def _score_behavior(self, animal: Dict, adopter: Dict) -> int:
        """
        Score behavioral compatibility (kids/pets)
        
        Example:
        - Animal good with kids + Adopter has kids = HIGH
        - Animal NOT good with kids + Adopter has kids = LOW
        """
        has_kids = adopter.get('has_kids', 'no').lower() == 'yes'
        has_other_pets = adopter.get('has_other_pets', 'no').lower() == 'yes'
        
        animal_good_kids = animal.get('good_with_kids', 'no').lower() == 'yes'
        animal_good_pets = animal.get('good_with_dogs', 'no').lower() == 'yes'
        
        score = 100
        
        # Penalize if adopter has kids but animal not safe with them
        if has_kids and not animal_good_kids:
            score -= 40  # Major penalty
        
        # Penalize if adopter has pets but animal not compatible
        if has_other_pets and not animal_good_pets:
            score -= 30  # Moderate penalty
        
        return max(score, 10)  # Keep minimum score of 10
    
    def _score_special_needs(self, animal: Dict, adopter: Dict) -> int:
        """
        Score adopter's ability to handle special needs
        
        Example:
        - Animal has special needs + High commitment adopter = GOOD
        - Animal has special needs + Low commitment adopter = BAD
        """
        has_special_needs = animal.get('special_needs', 'no').lower() == 'yes'
        commitment = adopter.get('commitment_level', 'medium').lower()
        
        if not has_special_needs:
            return 100  # No special needs = no problem
        
        if commitment == 'high':
            return 95   # High commitment can handle it
        elif commitment == 'medium':
            return 60   # Medium commitment is risky
        else:
            return 30   # Low commitment = won't work
    
    def _generate_reasoning(self, animal: Dict, adopter: Dict, 
                          scores: Dict[str, int]) -> str:
        """
        Generate human-readable explanation of the score
        Helps judges understand WHY the score is what it is
        """
        animal_name = animal.get('name', 'Unknown')
        adopter_name = adopter.get('name', 'Unknown')
        
        reasoning = f"Match Analysis: {animal_name} ↔ {adopter_name}\n"
        reasoning += f"- Lifestyle Compatibility: {scores['lifestyle_match']}/100\n"
        reasoning += f"- Experience Match: {scores['experience_match']}/100\n"
        reasoning += f"- Home Fit: {scores['home_fit']}/100\n"
        reasoning += f"- Behavioral Compatibility: {scores['behavioral_fit']}/100\n"
        reasoning += f"- Special Needs Capability: {scores['special_needs']}/100\n"
        
        return reasoning
