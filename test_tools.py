"""
Quick test to verify both tools work correctly
"""

from tools.data_loader import DataLoader
from tools.compatibility_scorer import CompatibilityScorer

print("="*60)
print("TESTING TOOLS")
print("="*60)

# TEST 1: DataLoader
print("\n[TEST 1] DataLoader - Loading CSV files...")
data_loader = DataLoader('animal_data.csv', 'adopter_data.csv')

# Get first animal
animal = data_loader.get_animal('1')
print(f"\nAnimal found: {animal['name']}")
print("Formatted for agent:")
print(data_loader.format_animal_for_agent(animal))

# Get first adopter
adopter = data_loader.get_adopter('1')
print(f"Adopter found: {adopter['name']}")
print("Formatted for agent:")
print(data_loader.format_adopter_for_agent(adopter))

# TEST 2: CompatibilityScorer
print("\n[TEST 2] CompatibilityScorer - Calculating scores...")
scorer = CompatibilityScorer()

# Calculate compatibility
score, reasoning = scorer.calculate_compatibility(animal, adopter)
print(f"\nCompatibility Score: {score}/100")
print(f"Reasoning:\n{reasoning}")

print("\n" + "="*60)
print("✓ TESTS PASSED - Both tools working!")
print("="*60)
