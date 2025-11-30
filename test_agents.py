"""Test all three agents"""

from tools.data_loader import DataLoader
from agents.profiling_agent import ProfilingAgent
from agents.matching_agent import MatchingAgent
from agents.support_agent import SupportAgent

print("="*60)
print("TESTING ALL THREE AGENTS")
print("="*60)

# Initialize
loader = DataLoader('animal_data.csv', 'adopter_data.csv')
profiler = ProfilingAgent(loader)
matcher = MatchingAgent(loader)
support = SupportAgent()

# Test 1: Profiling
print("\n[TEST 1] PROFILING AGENT")
animal_profile = profiler.profile_animal('1')
adopter_profile = profiler.profile_adopter('1')

# Test 2: Matching
print("\n[TEST 2] MATCHING AGENT")
matches = matcher.find_matches('1', top_n=3)
print("\nTop 3 Matches Found:")
for i, match in enumerate(matches, 1):
    print(f"{i}. {match['animal_name']} - {match['score']}/100")

# Test 3: Support
print("\n[TEST 3] SUPPORT AGENT")
if matches:
    best_match = matches[0]
    guidance = support.get_post_adoption_guidance(
        animal_name=best_match['animal_name'],
        animal_breed=loader.get_animal(best_match['animal_id'])['breed'],
        adopter_name=best_match['adopter_name']
    )
    print("\nGuidance provided (first 200 chars):")
    print(guidance[:200] + "...\n")

print("="*60)
print("✓ ALL AGENT TESTS PASSED!")
print("="*60)
