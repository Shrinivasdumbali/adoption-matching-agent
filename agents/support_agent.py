"""
SUPPORT AGENT - Step 3 in the adoption process

Purpose: Provide post-adoption guidance and support
Role: Helps families adjust to their new pets
"""

class SupportAgent:
    """
    Agent responsible for providing post-adoption guidance and support.
    Think of this as the "family counselor" who helps with the transition.
    """
    
    def __init__(self):
        """Initialize support agent"""
        print("✓ Support Agent initialized")
    
    def get_post_adoption_guidance(self, animal_name: str, 
                                   animal_breed: str,
                                   adopter_name: str,
                                   adopter_concern: str = None) -> str:
        """
        Provide post-adoption support and guidance
        
        Args:
            animal_name: Name of adopted animal
            animal_breed: Breed of animal
            adopter_name: Name of adopter
            adopter_concern: Specific concern or question (optional)
        
        Returns:
            Supportive guidance text
        """
        print(f"\n[SUPPORT AGENT] Providing guidance for {adopter_name} ({animal_name})...")
        
        # Base guidance for successful adoption
        guidance = f"""
POST-ADOPTION GUIDANCE FOR {adopter_name}
{'='*50}

Congratulations on adopting {animal_name}, a {animal_breed}!

FIRST WEEK TIPS:
1. Create a safe space for {animal_name} with familiar items
2. Establish a consistent routine (feeding, play, rest)
3. Let {animal_name} explore your home gradually
4. Be patient - adjustment takes time (2-4 weeks)
5. Maintain contact with the shelter if questions arise

BUILDING THE BOND:
- Spend quality time together daily
- Use positive reinforcement (treats, praise)
- Be consistent with rules and boundaries
- Exercise regularly (appropriate for the breed)
- Provide mental stimulation

WHEN TO SEEK HELP:
- Behavioral issues emerge
- Health concerns develop
- Significant anxiety or aggression
- Struggling with adjustment

RESOURCES:
- Contact your local shelter for support
- Veterinary guidance for health questions
- Professional trainer if needed

Remember: Every adoption is unique. Be patient and celebrate small wins!
"""
        
        # Add specific concern response if provided
        if adopter_concern:
            concern_response = self._respond_to_concern(animal_name, adopter_concern)
            guidance += f"\n\nYOUR SPECIFIC CONCERN:\n{concern_response}"
        
        print("✓ Guidance provided")
        return guidance
    
    def _respond_to_concern(self, animal_name: str, concern: str) -> str:
        """Provide tailored response to specific adopter concern"""
        
        concern_lower = concern.lower()
        
        if 'aggressive' in concern_lower or 'behavior' in concern_lower:
            return f"""
BEHAVIORAL CONCERNS:
{animal_name} may need time to feel secure. Consider:
- Working with a professional trainer
- Using positive reinforcement techniques
- Consulting your veterinarian for any medical causes
- Patience - behavioral change takes weeks/months
"""
        
        elif 'scared' in concern_lower or 'afraid' in concern_lower or 'anxious' in concern_lower:
            return f"""
ANXIETY/FEAR CONCERNS:
{animal_name} may have had a difficult past. Tips:
- Create a safe, quiet space initially
- Gradually introduce to new environments
- Use calming techniques (music, pheromone products)
- Let them set the pace for interaction
- Consider anxiety medication if severe
"""
        
        elif 'training' in concern_lower or 'obedience' in concern_lower:
            return f"""
TRAINING TIPS:
- Start with basic commands (sit, stay, come)
- Use positive reinforcement (treats, praise)
- Keep sessions short (5-10 minutes)
- Be consistent with commands
- Consider professional training if needed
"""
        
        elif 'health' in concern_lower or 'sick' in concern_lower:
            return f"""
HEALTH CONCERNS:
- Schedule a vet checkup within first week
- Keep vaccination records up to date
- Monitor for signs of illness
- Report any health issues immediately to veterinarian
- Ask about pet insurance for ongoing care
"""
        
        else:
            return f"""
GENERAL SUPPORT:
The shelter and veterinarian are your best resources.
{animal_name} needs time to adjust. Be patient and celebrate progress!
"""
    
    def get_training_tips(self, animal_species: str, breed: str, 
                         age_years: int, behavior: str) -> str:
        """Get training recommendations"""
        
        print(f"\n[SUPPORT AGENT] Providing training tips for {breed}...")
        
        tips = f"""
TRAINING GUIDE: {breed}
{'='*50}

ANIMAL: {breed} ({animal_species}), Age: {age_years} years
BEHAVIOR TO ADDRESS: {behavior}

GENERAL APPROACH:
1. Use positive reinforcement (treats, praise)
2. Keep sessions short (10-15 minutes)
3. Practice daily for consistency
4. Be patient - training takes weeks
5. Never use punishment or force

NEXT STEPS:
1. Identify the trigger for {behavior}
2. Use redirection techniques
3. Reward desired behavior immediately
4. If issues persist, consult a professional trainer

TIMELINE:
- Week 1-2: Initial understanding
- Week 3-4: Noticeable improvement
- Week 5+: Behavioral habits forming

If concerns persist, seek professional help.
"""
        
        print("✓ Training tips provided")
        return tips

# Test the agent
if __name__ == "__main__":
    print("="*60)
    print("SUPPORT AGENT TEST")
    print("="*60)
    
    support = SupportAgent()
    
    # Test basic guidance
    guidance = support.get_post_adoption_guidance(
        animal_name="Max",
        animal_breed="Golden Retriever",
        adopter_name="John Smith"
    )
    print(guidance)
    
    # Test with concern
    guidance_with_concern = support.get_post_adoption_guidance(
        animal_name="Max",
        animal_breed="Golden Retriever",
        adopter_name="John Smith",
        adopter_concern="He's a bit anxious"
    )
    print("\n" + "="*60)
    print(guidance_with_concern)
