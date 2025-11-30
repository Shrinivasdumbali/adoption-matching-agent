"""
MEMORY STORE - Session Persistence

Stores adoption sessions in JSON format.
This demonstrates Memory persistence and Long-term memory from the course.

In production, this would be a database.
For this prototype, we use JSON files for simplicity.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from models.adoption_session import AdoptionSession

class MemoryStore:
    """
    In-memory + file-based session and memory storage.
    
    Demonstrates:
    - Sessions & State Management
    - Long-term memory (JSON persistence)
    - Session history tracking
    """
    
    def __init__(self, storage_file: str = "sessions.json"):
        """Initialize memory store"""
        self.storage_file = storage_file
        self.sessions: Dict[str, AdoptionSession] = {}
        self.match_history: List[Dict] = []
        self.load_from_file()
        print(f"✓ Memory Store initialized (Storage: {storage_file})")
    
    def load_from_file(self):
        """Load sessions from JSON file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.match_history = data.get('match_history', [])
                print(f"  ✓ Loaded {len(self.match_history)} historical matches from file")
            except json.JSONDecodeError:
                print(f"  ⚠ Error reading {self.storage_file}, starting fresh")
    
    def save_to_file(self):
        """Save sessions to JSON file (Persistence)"""
        data = {
            'last_saved': datetime.now().isoformat(),
            'sessions': [s.to_dict() for s in self.sessions.values()],
            'match_history': self.match_history
        }
        
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"  ✓ Saved to {self.storage_file}")
    
    def create_session(self, session_id: str, adopter_id: str) -> AdoptionSession:
        """
        Create new adoption session
        
        Args:
            session_id: Unique session ID
            adopter_id: ID of adopter
        
        Returns:
            New AdoptionSession object
        """
        session = AdoptionSession(session_id=session_id, adopter_id=adopter_id)
        self.sessions[session_id] = session
        self.save_to_file()
        print(f"✓ New session created: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[AdoptionSession]:
        """Retrieve existing session"""
        session = self.sessions.get(session_id)
        if session:
            print(f"✓ Session retrieved: {session_id}")
        else:
            print(f"⚠ Session not found: {session_id}")
        return session
    
    def record_match(self, match_data: Dict):
        """
        Record a match in history
        
        This creates a permanent memory of the match
        """
        match_data['timestamp'] = datetime.now().isoformat()
        self.match_history.append(match_data)
        self.save_to_file()
        print(f"✓ Match recorded in history")
    
    def get_adopter_history(self, adopter_id: str) -> List[Dict]:
        """Get all matches for specific adopter"""
        history = [m for m in self.match_history if m.get('adopter_id') == adopter_id]
        print(f"✓ Retrieved {len(history)} matches for adopter {adopter_id}")
        return history
    
    def get_all_sessions(self) -> Dict[str, AdoptionSession]:
        """Get all sessions in memory"""
        return self.sessions
    
    def get_match_statistics(self) -> Dict:
        """Get statistics about matches"""
        if not self.match_history:
            return {"total_matches": 0}
        
        stats = {
            'total_matches': len(self.match_history),
            'average_score': sum(m.get('score', 0) for m in self.match_history) / len(self.match_history),
            'high_matches': len([m for m in self.match_history if m.get('score', 0) >= 80]),
            'total_adopters': len(set(m.get('adopter_id') for m in self.match_history))
        }
        
        return stats

# Test
if __name__ == "__main__":
    print("Testing MemoryStore...\n")
    
    store = MemoryStore()
    
    # Create session
    session = store.create_session("sess_001", "adopter_1")
    
    # Add some matches
    store.record_match({
        'animal_id': '1',
        'adopter_id': 'adopter_1',
        'animal_name': 'Max',
        'score': 85
    })
    
    store.record_match({
        'animal_id': '2',
        'adopter_id': 'adopter_1',
        'animal_name': 'Bella',
        'score': 78
    })
    
    # Get history
    history = store.get_adopter_history('adopter_1')
    print(f"\nHistory retrieved:")
    print(json.dumps(history, indent=2))
    
    # Get stats
    stats = store.get_match_statistics()
    print(f"\nStatistics:")
    print(json.dumps(stats, indent=2))
