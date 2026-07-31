"""
Grant-O-Matic Deadline Tracking and Alert System
"""
import json
import datetime
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DeadlineTracker:
    def __init__(self):
        self.deadlines = []  # List of deadline objects
    
    def add_deadline(self, grant_id: str, program_name: str, administering_agency: str,
                    deadline_date: datetime.date, frequency: str = None,
                    application_window: str = None, url: str = None) -> None:
        """
        Add a grant deadline to the tracker
        
        Args:
            grant_id: Unique identifier for the grant
            program_name: Name of the grant program
            administering_agency: Organization administering the grant
            deadline_date: Date of the deadline
            frequency: How often the grant is offered (e.g., "Annual", "Quarterly", "Rolling")
            application_window: Description of the application window period
            url: URL for more information about the grant
        """
        deadline_obj = {
            'id': grant_id,
            'program_name': program_name,
            'administering_agency': administering_agency,
            'deadline_date': deadline_date.isoformat() if isinstance(deadline_date, datetime.date) else deadline_date,
            'frequency': frequency,
            'application_window': application_window,
            'url': url,
            'added_date': datetime.date.today().isoformat(),
            'status': 'upcoming'  # upcoming, passed, completed
        }
        
        self.deadlines.append(deadline_obj)
        logger.info(f"Added deadline for {program_name}: {deadline_date}")
    
    def clear(self) -> None:
        """Remove all tracked deadlines."""
        self.deadlines = []

    def load_deadlines_from_grants(self, grants: List[Dict[str, Any]]) -> None:
        """
        Load deadlines from a list of grant objects.
        Replaces existing deadlines so reloads stay in sync with grant data.
        
        Args:
            grants: List of grant dictionaries with deadline information
        """
        self.clear()
        for grant in grants:
            grant_id = grant.get('id')
            program_name = grant.get('program_name')
            administering_agency = grant.get('administering_agency')
            
            deadline_info = grant.get('deadline_info', {})
            if deadline_info:
                next_deadline_str = deadline_info.get('next_deadline')
                if next_deadline_str:
                    try:
                        # Parse the deadline date
                        deadline_date = datetime.date.fromisoformat(next_deadline_str)
                        
                        self.add_deadline(
                            grant_id=grant_id,
                            program_name=program_name,
                            administering_agency=administering_agency,
                            deadline_date=deadline_date,
                            frequency=deadline_info.get('frequency'),
                            application_window=deadline_info.get('application_window'),
                            url=grant.get('url')
                        )
                    except ValueError as e:
                        logger.warning(f"Could not parse deadline date '{next_deadline_str}' for grant {grant_id}: {e}")
                else:
                    logger.info(f"No next deadline specified for grant {grant_id}")
            else:
                logger.info(f"No deadline info found for grant {grant_id}")
    
    def get_upcoming_deadlines(self, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """
        Get deadlines that are coming up within the specified number of days
        
        Args:
            days_ahead: Number of days ahead to look for deadlines
            
        Returns:
            List of deadline objects sorted by date (soonest first)
        """
        today = datetime.date.today()
        cutoff_date = today + datetime.timedelta(days=days_ahead)
        
        upcoming = []
        for deadline in self.deadlines:
            deadline_date = datetime.date.fromisoformat(deadline['deadline_date'])
            if today <= deadline_date <= cutoff_date:
                # Add days until deadline for display
                days_until = (deadline_date - today).days
                deadline_copy = deadline.copy()
                deadline_copy['days_until'] = days_until
                upcoming.append(deadline_copy)
        
        # Sort by deadline date (soonest first)
        upcoming.sort(key=lambda x: x['deadline_date'])
        return upcoming
    
    def get_passed_deadlines(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Get deadlines that have passed within the specified number of days
        
        Args:
            days_back: Number of days back to look for passed deadlines
            
        Returns:
            List of deadline objects sorted by date (most recent first)
        """
        today = datetime.date.today()
        cutoff_date = today - datetime.timedelta(days=days_back)
        
        passed = []
        for deadline in self.deadlines:
            deadline_date = datetime.date.fromisoformat(deadline['deadline_date'])
            if cutoff_date <= deadline_date < today:
                # Add days since deadline for display
                days_since = (today - deadline_date).days
                deadline_copy = deadline.copy()
                deadline_copy['days_since'] = days_since
                passed.append(deadline_copy)
        
        # Sort by deadline date (most recent first)
        passed.sort(key=lambda x: x['deadline_date'], reverse=True)
        return passed
    
    def get_deadline_calendar(self, month: int = None, year: int = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get a calendar view of deadlines for a specific month
        
        Args:
            month: Month (1-12), defaults to current month
            year: Year, defaults to current year
            
        Returns:
            Dictionary mapping dates (as strings) to lists of deadlines on that date
        """
        if month is None:
            month = datetime.date.today().month
        if year is None:
            year = datetime.date.today().year
        
        # Get all deadlines in the specified month/year
        month_deadlines = []
        for deadline in self.deadlines:
            deadline_date = datetime.date.fromisoformat(deadline['deadline_date'])
            if deadline_date.month == month and deadline_date.year == year:
                month_deadlines.append(deadline)
        
        # Group by date
        calendar = {}
        for deadline in month_deadlines:
            date_str = deadline['deadline_date']
            if date_str not in calendar:
                calendar[date_str] = []
            calendar[date_str].append(deadline)
        
        return calendar
    
    def generate_deadline_alerts(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """
        Generate alert objects for upcoming deadlines
        
        Args:
            days_ahead: Number of days ahead to generate alerts for
            
        Returns:
            List of alert objects
        """
        upcoming = self.get_upcoming_deadlines(days_ahead=days_ahead)
        alerts = []
        
        for deadline in upcoming:
            days_until = deadline['days_until']
            
            # Determine alert urgency
            if days_until == 0:
                urgency = "high"
                message = f"DEADLINE TODAY: {deadline['program_name']}"
            elif days_until <= 2:
                urgency = "high"
                message = f"URGENT: {days_until} days left to apply for {deadline['program_name']}"
            elif days_until <= 7:
                urgency = "medium"
                message = f"Reminder: {days_until} days left to apply for {deadline['program_name']}"
            else:
                urgency = "low"
                message = f"Upcoming: {days_until} days left to apply for {deadline['program_name']}"
            
            alert = {
                'id': f"alert_{deadline['id']}_{datetime.date.today().isoformat()}",
                'grant_id': deadline['id'],
                'program_name': deadline['program_name'],
                'administering_agency': deadline['administering_agency'],
                'deadline_date': deadline['deadline_date'],
                'days_until': days_until,
                'urgency': urgency,
                'message': message,
                'url': deadline.get('url'),
                'generated_at': datetime.datetime.now().isoformat()
            }
            
            alerts.append(alert)
        
        return alerts
    
    def get_all_deadlines(self) -> List[Dict[str, Any]]:
        """
        Return all tracked deadlines with days_until (negative if passed), soonest first.
        """
        today = datetime.date.today()
        results = []
        for deadline in self.deadlines:
            deadline_date = datetime.date.fromisoformat(deadline['deadline_date'])
            deadline_copy = deadline.copy()
            deadline_copy['days_until'] = (deadline_date - today).days
            if deadline_date < today:
                deadline_copy['status'] = 'passed'
            else:
                deadline_copy['status'] = 'upcoming'
            results.append(deadline_copy)
        results.sort(key=lambda x: x['deadline_date'])
        return results

    def generate_ics(self, days_ahead: int = 365, calendar_name: str = "Grant-O-Matic Deadlines") -> str:
        """
        Build a downloadable iCalendar (ICS) document for upcoming deadlines.

        This is the primary alert channel (no email secrets required).
        """
        upcoming = self.get_upcoming_deadlines(days_ahead=days_ahead)
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Grant-O-Matic//Deadline Tracker//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            f"X-WR-CALNAME:{self._ics_escape(calendar_name)}",
        ]
        for deadline in upcoming:
            uid = f"{deadline['id']}-{deadline['deadline_date']}@grant-o-matic"
            dt = deadline['deadline_date'].replace("-", "")
            summary = f"{deadline['program_name']} deadline"
            description_parts = [
                f"Agency: {deadline.get('administering_agency') or 'Unknown'}",
                f"Frequency: {deadline.get('frequency') or 'n/a'}",
            ]
            if deadline.get("application_window"):
                description_parts.append(f"Window: {deadline['application_window']}")
            if deadline.get("url"):
                description_parts.append(f"URL: {deadline['url']}")
            description = "\\n".join(self._ics_escape(p) for p in description_parts)
            lines.extend(
                [
                    "BEGIN:VEVENT",
                    f"UID:{uid}",
                    f"DTSTAMP:{now}",
                    f"DTSTART;VALUE=DATE:{dt}",
                    f"SUMMARY:{self._ics_escape(summary)}",
                    f"DESCRIPTION:{description}",
                ]
            )
            if deadline.get("url"):
                lines.append(f"URL:{deadline['url']}")
            lines.append("END:VEVENT")
        lines.append("END:VCALENDAR")
        return "\r\n".join(lines) + "\r\n"

    @staticmethod
    def _ics_escape(value: str) -> str:
        return (
            (value or "")
            .replace("\\", "\\\\")
            .replace(";", "\\;")
            .replace(",", "\\,")
            .replace("\n", "\\n")
        )

    def save_to_file(self, filepath: str) -> None:
        """
        Save deadlines to a JSON file
        
        Args:
            filepath: Path to the JSON file
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.deadlines, f, indent=2)
            logger.info(f"Saved {len(self.deadlines)} deadlines to {filepath}")
        except Exception as e:
            logger.error(f"Error saving deadlines to {filepath}: {e}")
    
    def load_from_file(self, filepath: str) -> None:
        """
        Load deadlines from a JSON file
        
        Args:
            filepath: Path to the JSON file
        """
        try:
            with open(filepath, 'r') as f:
                self.deadlines = json.load(f)
            logger.info(f"Loaded {len(self.deadlines)} deadlines from {filepath}")
        except FileNotFoundError:
            logger.warning(f"Deadlines file not found: {filepath}")
            self.deadlines = []
        except Exception as e:
            logger.error(f"Error loading deadlines from {filepath}: {e}")
            self.deadlines = []

# Example usage
if __name__ == "__main__":
    # Create a deadline tracker
    tracker = DeadlineTracker()
    
    # Add some sample deadlines
    tracker.add_deadline(
        grant_id="factor001",
        program_name="Juried Sound Recording",
        administering_agency="FACTOR",
        deadline_date=datetime.date(2024, 3, 15),
        frequency="Quarterly",
        application_window="Jan 1 - Mar 15",
        url="https://factor.ca/programs/juried-sound-recording/"
    )
    
    tracker.add_deadline(
        grant_id="factor002",
        program_name="Artist Development",
        administering_agency="FACTOR",
        deadline_date=datetime.date(2024, 6, 30),
        frequency="Rolling",
        application_window="Ongoing",
        url="https://factor.ca/programs/artist-development/"
    )
    
    tracker.add_deadline(
        grant_id="canadacouncil001",
        program_name="Explore and Create: Research and Creation",
        administering_agency="Canada Council for the Arts",
        deadline_date=datetime.date(2024, 5, 1),
        frequency="Rolling",
        application_window="Ongoing",
        url="https://canadacouncil.ca/funding/grants/explore-and-create-research-and-creation"
    )
    
    # Get upcoming deadlines
    upcoming = tracker.get_upcoming_deadlines(days_ahead=60)
    print(f"\nUpcoming deadlines (next 60 days):")
    for deadline in upcoming:
        print(f"- {deadline['program_name']} ({deadline['administering_agency']}): {deadline['deadline_date']} ({deadline['days_until']} days)")
    
    # Generate alerts
    alerts = tracker.generate_deadline_alerts(days_ahead=14)
    print(f"\nDeadline alerts (next 14 days):")
    for alert in alerts:
        print(f"- [{alert['urgency'].upper()}] {alert['message']}")
    
    # Save to file
    tracker.save_to_file("deadlines.json")
    
    # Load from file (demo)
    new_tracker = DeadlineTracker()
    new_tracker.load_from_file("deadlines.json")
    print(f"\nLoaded {len(new_tracker.deadlines)} deadlines from file")