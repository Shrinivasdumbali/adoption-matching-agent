"""
ADOPTION SESSION MODEL

Represents a single adoption inquiry/process
This demonstrates Sessions & State Management from the course
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any
import json

@dataclass
class AdoptionMatch:
    """Represents a single adoption match recommendation"""
    animal_id: str
    adopter_id: str
    animal_name: str
    adopter_name: str
    score: int
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "recommended"  # recommended, accepted, rejected, completed
    notes: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'animal_id': self.animal_id,
            'adopter_id': self.adopter_id,
            'animal_name': self.animal_name,
            'adopter_name': self.adopter_name,
            'score': self.score,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status,
            'notes': self.notes
        }

@dataclass
class AdoptionSession:
    """
    Session for tracking adoption process.
    
    This demonstrates:
    - Sessions & State Management (from course)
    - Continuity across interactions
    - Memory persistence
    
    Each adoption inquiry gets its own session.
    """
    session_id: str
    adopter_id: str
    created_at: datetime = field(default_factory=datetime.now)
    matches: List[AdoptionMatch] = field(default_factory=list)
    selected_animal: str = None
    adoption_date: datetime = None
    feedback: str = ""
    session_state: Dict[str, Any] = field(default_factory=dict)
    
    def add_match(self, match: AdoptionMatch):
        """Add a match recommendation to session history"""
        self.matches.append(match)
        print(f"  ✓ Match recorded: {match.animal_name} for {match.adopter_name}")
    
    def select_animal(self, animal_id: str):
        """Record selected animal"""
        self.selected_animal = animal_id
        self.session_state['selection_time'] = datetime.now().isoformat()
        print(f"  ✓ Animal {animal_id} selected")
    
    def complete_adoption(self):
        """Mark adoption as complete"""
        self.adoption_date = datetime.now()
        self.session_state['status'] = 'completed'
        print(f"  ✓ Adoption marked as complete")
    
    def add_feedback(self, feedback: str):
        """Add post-adoption feedback"""
        self.feedback = feedback
        self.session_state['feedback_time'] = datetime.now().isoformat()
        print(f"  ✓ Feedback recorded")
    
    def get_session_summary(self) -> str:
        """Get human-readable summary of session"""
        summary = f"""
SESSION SUMMARY
{'='*50}
Session ID: {self.session_id}
Adopter ID: {self.adopter_id}
Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}
Matches Explored: {len(self.matches)}
Selected Animal: {self.selected_animal if self.selected_animal else 'None yet'}
Status: {self.session_state.get('status', 'In Progress')}
Feedback: {self.feedback if self.feedback else 'No feedback yet'}
"""
        return summary
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage/JSON"""
        return {
            'session_id': self.session_id,
            'adopter_id': self.adopter_id,
            'created_at': self.created_at.isoformat(),
            'matches': [m.to_dict() for m in self.matches],
            'selected_animal': self.selected_animal,
            'adoption_date': self.adoption_date.isoformat() if self.adoption_date else None,
            'feedback': self.feedback,
            'session_state': self.session_state
        }

# Test
if __name__ == "__main__":
    print("Testing AdoptionSession...")
    
    session = AdoptionSession(
        session_id="sess_001",
        adopter_id="1"
    )
    
    # Add matches
    match1 = AdoptionMatch(
        animal_id="1",
        adopter_id="1",
        animal_name="Max",
        adopter_name="John",
        score=85
    )
    session.add_match(match1)
    
    # Select animal
    session.select_animal("1")
    
    # Add feedback
    session.add_feedback("Max is perfect! Very friendly.")
    
    # Complete
    session.complete_adoption()
    
    print(session.get_session_summary())
    print("\nSession as JSON:")
    print(json.dumps(session.to_dict(), indent=2, default=str))
