import os
import json
import uuid
from dotenv import load_dotenv
from tools.data_loader import DataLoader
from agents.profiling_agent import ProfilingAgent
from agents.matching_agent import MatchingAgent
from agents.support_agent import SupportAgent
from models.memory_store import MemoryStore
from models.adoption_session import AdoptionMatch

# Load environment
load_dotenv()

class AdoptionMatchingSystem:
    """
    Main orchestration layer combining all three agents.
    This is the Think → Act → Observe loop.
    """
    
    def __init__(self):
        # Initialize data
        self.data_loader = DataLoader('animal_data.csv', 'adopter_data.csv')
        
        # Initialize agents
        self.profiler = ProfilingAgent(self.data_loader)
        self.matcher = MatchingAgent(self.data_loader)
        self.support = SupportAgent()
        
        # Initialize memory/sessions
        self.memory = MemoryStore()
    
    def process_adoption_inquiry(self, adopter_id: str) -> dict:
        """
        Main workflow: Process an adopter's inquiry
        
        STEP 1 (THINK): Understand adopter preferences
        STEP 2 (ACT): Find compatible animals
        STEP 3 (OBSERVE): Present options and gather feedback
        """
        
        print(f"\n{'='*60}")
        print(f"PROCESSING ADOPTION INQUIRY FOR ADOPTER {adopter_id}")
        print(f"{'='*60}\n")
        
        # Create session (Memory: Sessions concept)
        session_id = str(uuid.uuid4())
        session = self.memory.create_session(session_id, adopter_id)
        
        # STEP 1: THINK - Profile the adopter
        print("[STEP 1: PROFILING AGENT]")
        print("Analyzing adopter profile...")
        adopter_profile = self.profiler.profile_adopter(adopter_id)
        print(f"✓ Profile complete: {json.dumps(adopter_profile, indent=2)}\n")
        
        # STEP 2: ACT - Find matches
        print("[STEP 2: MATCHING AGENT]")
        print("Finding compatible animals...")
        matches = self.matcher.find_matches(adopter_id, top_n=3)
        
        print(f"Found {len(matches)} potential matches:\n")
        for i, match in enumerate(matches, 1):
            print(f"{i}. {match['adopter_name']} → {match['animal_name']}")
            print(f"   Score: {match['score']}/100")
            print(f"   {match['reasoning']}\n")
            
            # Record in session (Memory: storing recommendations)
            adoption_match = AdoptionMatch(
                animal_id=match['animal_id'],
                adopter_id=match['adopter_id'],
                animal_name=match['animal_name'],
                adopter_name=match['adopter_name'],
                score=match['score'],
                status='recommended'
            )
            session.add_match(adoption_match)
        
        # STEP 3: OBSERVE & Provide guidance
        print("[STEP 3: SUPPORT AGENT]")
        if matches:
            best_match = matches[0]
            animal = self.data_loader.get_animal(best_match['animal_id'])
            adopter = self.data_loader.get_adopter(adopter_id)
            
            print(f"Providing post-adoption guidance for recommended match...")
            guidance = self.support.get_post_adoption_guidance(
                animal_name=animal['name'],
                animal_breed=animal['breed'],
                adopter_name=adopter['name']
            )
            print(f"Guidance:\n{guidance}\n")
        
        # Save session (Memory: persisting session data)
        self.memory.save_to_file()
        
        return {
            'session_id': session_id,
            'adopter_id': adopter_id,
            'matches_found': len(matches),
            'top_match': matches[0] if matches else None,
            'session_data': session.to_dict()
        }
    
    def simulate_adoption_process(self):
        """
        Run full simulation with multiple adopters
        """
        print("\n" + "="*60)
        print("ADOPTION MATCHING SYSTEM - DEMONSTRATION")
        print("="*60)
        
        # Process first 2 adopters as demonstration
        adopter_ids = ['1', '2']
        
        results = []
        for adopter_id in adopter_ids:
            result = self.process_adoption_inquiry(adopter_id)
            results.append(result)
            print("\n" + "-"*60)
        
        # Summary
        print("\n" + "="*60)
        print("PROCESS SUMMARY")
        print("="*60)
        for result in results:
            print(f"Adopter {result['adopter_id']}: {result['matches_found']} matches found")
            if result['top_match']:
                print(f"  Top recommendation: {result['top_match']['animal_name']} (Score: {result['top_match']['score']}/100)")
        
        return results

if __name__ == "__main__":
    system = AdoptionMatchingSystem()
    results = system.simulate_adoption_process()
    
    print("\n✓ Simulation complete. Sessions saved to sessions.json")
