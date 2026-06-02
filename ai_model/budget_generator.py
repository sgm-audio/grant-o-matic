"""
Grant-O-Matic Budget Justification Generator
"""
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class BudgetJustificationGenerator:
    def __init__(self):
        # Standard budget categories for Canadian arts grants
        self.budget_categories = {
            'creation': [
                'Artist fees',
                'Collaborator fees',
                'Materials and supplies',
                'Studio rental',
                'Equipment rental',
                'Research expenses',
                'Travel (research)',
                'Accessibility costs'
            ],
            'production': [
                'Artist fees',
                'Production crew fees',
                'Studio rental',
                'Equipment rental/purchase',
                'Materials and supplies',
                'Travel (production)',
                'Accommodation',
                'Per diems',
                'Post-production',
                'Mixing and mastering',
                'Accessibility costs'
            ],
            'marketing': [
                'Marketing and promotion',
                'Publicity',
                'Advertising',
                'Touring expenses',
                'Venue fees',
                'Artist fees (performance)',
                'Technical rider',
                'Transportation',
                'Accommodation',
                'Per diems',
                'Accessibility costs'
            ],
            'recording': [
                'Artist fees',
                'Session musician fees',
                'Producer fees',
                'Engineer fees',
                'Studio rental',
                'Equipment rental',
                'Tape/digital storage',
                'Mixing',
                'Mastering',
                'Accessibility costs'
            ],
            'video': [
                'Artist fees',
                'Production crew fees',
                'Director fees',
                'Editor fees',
                'Cinematographer fees',
                'Equipment rental',
                'Studio/location rental',
                'Set construction',
                'Wardrobe',
                'Makeup',
                'Transportation',
                'Accommodation',
                'Per diems',
                'Editing',
                'Color correction',
                'Accessibility costs'
            ],
            'touring': [
                'Artist fees',
                'Technical crew fees',
                'Transportation',
                'Vehicle rental/fuel',
                'Accommodation',
                'Per diems',
                'Venue fees',
                'Technical rider',
                'Equipment rental',
                'Insurance',
                'Booking agent fees',
                'Accessibility costs'
            ],
            'general': [
                'Artist fees',
                'Administrative costs',
                'Office supplies',
                'Software/subscriptions',
                'Website maintenance',
                'Accounting/legal fees',
                'Insurance',
                'Accessibility costs',
                'Contingency (10-15%)'
            ]
        }
        
        # Typical percentage allocations for different project types
        self.allocations = {
            'creation': {
                'Artist fees': 0.30,
                'Collaborator fees': 0.20,
                'Materials and supplies': 0.15,
                'Studio rental': 0.10,
                'Equipment rental': 0.10,
                'Research expenses': 0.05,
                'Travel (research)': 0.05,
                'Accessibility costs': 0.05
            },
            'production': {
                'Artist fees': 0.20,
                'Production crew fees': 0.15,
                'Studio rental': 0.10,
                'Equipment rental/purchase': 0.15,
                'Materials and supplies': 0.10,
                'Travel (production)': 0.10,
                'Accommodation': 0.05,
                'Per diems': 0.05,
                'Post-production': 0.05,
                'Mixing and mastering': 0.05,
                'Accessibility costs': 0.05
            },
            'marketing': {
                'Marketing and promotion': 0.25,
                'Publicity': 0.15,
                'Advertising': 0.20,
                'Touring expenses': 0.15,
                'Venue fees': 0.10,
                'Artist fees (performance)': 0.10,
                'Technical rider': 0.05,
                'Accessibility costs': 0.05
            },
            'recording': {
                'Artist fees': 0.25,
                'Session musician fees': 0.20,
                'Producer fees': 0.15,
                'Engineer fees': 0.10,
                'Studio rental': 0.10,
                'Equipment rental': 0.05,
                'Tape/digital storage': 0.05,
                'Mixing': 0.05,
                'Mastering': 0.05
            },
            'video': {
                'Artist fees': 0.20,
                'Production crew fees': 0.15,
                'Director fees': 0.10,
                'Editor fees': 0.10,
                'Cinematographer fees': 0.10,
                'Equipment rental': 0.10,
                'Studio/location rental': 0.10,
                'Set construction': 0.05,
                'Wardrobe': 0.05,
                'Makeup': 0.05,
                'Transportation': 0.05,
                'Accommodation': 0.05,
                'Per diems': 0.05,
                'Editing': 0.05,
                'Color correction': 0.05
            },
            'touring': {
                'Artist fees': 0.25,
                'Technical crew fees': 0.15,
                'Transportation': 0.20,
                'Vehicle rental/fuel': 0.10,
                'Accommodation': 0.10,
                'Per diems': 0.05,
                'Venue fees': 0.05,
                'Technical rider': 0.05,
                'Equipment rental': 0.05,
                'Insurance': 0.05,
                'Accessibility costs': 0.05
            }
        }

    def generate_budget_justification(self, project_type: str, total_budget: float, 
                                    project_description: str, artist_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a budget justification for a grant application
        
        Args:
            project_type: Type of project (creation, production, marketing, recording, video, touring, general)
            total_budget: Total budget amount in CAD
            project_description: Description of the project
            artist_info: Optional dictionary with artist details
            
        Returns:
            Dictionary containing budget breakdown and justification text
        """
        # Normalize project type
        project_type = project_type.lower()
        if project_type not in self.allocations:
            project_type = 'general'
        
        # Get allocation percentages for this project type
        allocations = self.allocations[project_type]
        categories = self.budget_categories[project_type]
        
        # Calculate dollar amounts for each category
        budget_breakdown = {}
        for category, percentage in allocations.items():
            amount = round(total_budget * percentage, 2)
            budget_breakdown[category] = amount
        
        # Calculate remaining amount (should be zero or very small due to rounding)
        allocated_total = sum(budget_breakdown.values())
        remaining = total_budget - allocated_total
        
        # If there's a remainder, add it to the largest category or a contingency line
        if abs(remaining) > 0.01:
            if project_type == 'general' and 'Contingency (10-15%)' in budget_breakdown:
                budget_breakdown['Contingency (10-15%)'] += remaining
            else:
                # Add to the first category
                first_category = list(budget_breakdown.keys())[0]
                budget_breakdown[first_category] += remaining
        
        # Generate justification text
        justification = self._generate_justification_text(
            project_type, total_budget, project_description, budget_breakdown, artist_info
        )
        
        return {
            'project_type': project_type,
            'total_budget': total_budget,
            'budget_breakdown': budget_breakdown,
            'justification_text': justification,
            'notes': self._get_budget_notes(project_type, total_budget)
        }
    
    def _generate_justification_text(self, project_type: str, total_budget: float,
                                   project_description: str, budget_breakdown: Dict[str, float],
                                   artist_info: Dict[str, Any] = None) -> str:
        """Generate a narrative justification for the budget"""
        
        artist_name = artist_info.get('name', 'the artist') if artist_info else 'the artist'
        project_desc = project_description[:100] + "..." if len(project_description) > 100 else project_description
        
        justification = f"""
BUDGET JUSTIFICATION FOR: {project_desc}

TOTAL REQUESTED: ${total_budget:,.2f} CAD

This budget has been carefully calculated to support the successful completion of the proposed {project_type} project. Each line item is essential to achieving the artistic goals outlined in the project description.

KEY BUDGET COMPONENTS:
"""
        
        # Add top 3 budget items by amount
        sorted_items = sorted(budget_breakdown.items(), key=lambda x: x[1], reverse=True)
        for category, amount in sorted_items[:3]:
            percentage = (amount / total_budget) * 100
            justification += f"- {category}: ${amount:,.2f} ({percentage:.1f}% of total budget)\n"
        
        justification += f"""
DETAILED BREAKDOWN:
"""
        
        for category, amount in budget_breakdown.items():
            percentage = (amount / total_budget) * 100
            justification += f"- {category}: ${amount:,.2f} ({percentage:.1f}%)\n"
        
        justification += f"""
ACCESSIBILITY CONSIDERATIONS:
Accessibility costs have been included in accordance with best practices and funding body requirements to ensure the project is accessible to artists and audiences with disabilities.

ARTIST COMPENSATION:
Artist fees have been calculated in line with industry standards and CARFAC fee schedules where applicable, ensuring fair compensation for creative labor.

PROJECT VIABILITY:
This budget represents a realistic and achievable financial plan for the proposed project. All costs have been researched and are based on current market rates for services and materials in the Canadian cultural sector.

CONTINGENCY PLANNING:
Where applicable, a contingency fund has been included to address unforeseen expenses that may arise during project implementation.
"""
        
        return justification.strip()
    
    def _get_budget_notes(self, project_type: str, total_budget: float) -> List[str]:
        """Generate helpful notes for the budget"""
        notes = [
            "All amounts are in Canadian dollars (CAD)",
            "Budget based on current market rates for Canadian cultural sector",
            "Artist fees comply with CARFAC minimum fee schedules where applicable",
            "Accessibility costs included as per accessibility best practices"
        ]
        
        if total_budget > 50000:
            notes.append("For budgets over $50,000, consider obtaining multiple quotes for major expenses")
        
        if project_type in ['production', 'video', 'touring']:
            notes.append("Consider including equipment insurance for valuable gear")
            
        if project_type == 'touring':
            notes.append("Tour budgets should account for potential date changes or cancellations")
            
        return notes

# Example usage
if __name__ == "__main__":
    generator = BudgetJustificationGenerator()
    
    # Test with a recording project
    result = generator.generate_budget_justification(
        project_type="recording",
        total_budget=15000.00,
        project_description="Recording and production of a 5-song EP featuring original compositions blending electronic and traditional instrumentation",
        artist_info={
            "name": "Alex Morgan",
            "location": "Toronto, ON",
            "genre": "Electronic/Folk fusion"
        }
    )
    
    print("Generated Budget Justification:")
    print("=" * 50)
    print(f"Project Type: {result['project_type']}")
    print(f"Total Budget: ${result['total_budget']:,.2f}")
    print("\nBudget Breakdown:")
    for category, amount in result['budget_breakdown'].items():
        print(f"  {category}: ${amount:,.2f}")
    print("\nJustification Text:")
    print(result['justification_text'])
    print("\nNotes:")
    for note in result['notes']:
        print(f"  - {note}")