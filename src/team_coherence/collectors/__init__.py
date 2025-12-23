"""
Data Collectors for Team Coherence Assessment
==============================================

Collectors gather data from various sources for coherence analysis.
All collectors respect privacy, require consent, and anonymize data.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import re


@dataclass
class CollectedItem:
    """A single collected data item"""
    source_type: str
    source_id: str
    timestamp: datetime
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    member_id: Optional[str] = None  # Anonymized identifier
    anonymized: bool = True


class BaseCollector(ABC):
    """Base class for data collectors"""
    
    def __init__(self, 
                 privacy_mode: str = "public_only",
                 anonymize: bool = True):
        self.privacy_mode = privacy_mode
        self.anonymize = anonymize
        self.collected: List[CollectedItem] = []
    
    @abstractmethod
    def collect(self, **kwargs) -> List[CollectedItem]:
        """Collect data from source"""
        pass
    
    def _anonymize_text(self, text: str) -> str:
        """Remove PII from text"""
        if not self.anonymize:
            return text
        
        # Remove names (basic pattern)
        text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME]', text)
        
        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        
        # Remove emails
        text = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[EMAIL]', text)
        
        # Remove SSN patterns
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
        
        # Remove addresses (basic)
        text = re.sub(r'\b\d+ [A-Z][a-z]+ (St|Ave|Rd|Blvd|Dr|Ln)\b', '[ADDRESS]', text)
        
        return text


class SocialMediaCollector(BaseCollector):
    """
    Collects public social media posts for coherence analysis.
    
    PRIVACY REQUIREMENTS:
    - Only collects public posts
    - Requires explicit consent from unit members
    - Anonymizes all PII before analysis
    - Never stores raw data
    """
    
    def __init__(self,
                 platforms: List[str] = None,
                 privacy_mode: str = "public_only",
                 anonymize: bool = True):
        super().__init__(privacy_mode, anonymize)
        self.platforms = platforms or ["twitter", "instagram", "reddit"]
    
    def collect(self, 
                unit_id: str = None,
                member_ids: List[str] = None,
                days_back: int = 30,
                **kwargs) -> List[CollectedItem]:
        """
        Collect public posts from configured platforms.
        
        In production, this would connect to social media APIs.
        Currently returns placeholder structure.
        """
        # Placeholder - actual implementation would use platform APIs
        self.collected = []
        
        # This is where API calls would go
        # For now, return empty list
        return self.collected
    
    def collect_unit(self, unit_id: str, days_back: int = 30) -> List[CollectedItem]:
        """Collect posts from all consented unit members"""
        return self.collect(unit_id=unit_id, days_back=days_back)


class CISDCollector(BaseCollector):
    """
    Collects CISD (Critical Incident Stress Debriefing) reports.
    
    PRIVACY REQUIREMENTS:
    - Reports are de-identified before analysis
    - Individual statements are not attributed
    - Focus on aggregate patterns, not individuals
    """
    
    def __init__(self, anonymize: bool = True):
        super().__init__(privacy_mode="authorized", anonymize=anonymize)
    
    def collect(self,
                unit_id: str = None,
                date_range: tuple = None,
                **kwargs) -> List[CollectedItem]:
        """
        Collect CISD reports for analysis.
        
        In production, this would connect to CISD documentation systems.
        """
        self.collected = []
        
        # Placeholder for actual CISD system integration
        return self.collected
    
    def collect_by_incident(self, incident_id: str) -> List[CollectedItem]:
        """Collect reports related to a specific incident"""
        return self.collect(incident_id=incident_id)


class DebriefCollector(BaseCollector):
    """
    Collects debrief transcripts and summaries.
    
    Handles:
    - Combat debriefs
    - Training debriefs  
    - Supervisor evaluations
    """
    
    def __init__(self, anonymize: bool = True):
        super().__init__(privacy_mode="authorized", anonymize=anonymize)
        self.debrief_types = ["combat", "training", "supervisor"]
    
    def collect(self,
                unit_id: str = None,
                debrief_type: str = None,
                date_range: tuple = None,
                **kwargs) -> List[CollectedItem]:
        """
        Collect debrief records.
        
        In production, connects to unit documentation systems.
        """
        self.collected = []
        
        # Placeholder for actual system integration
        return self.collected


class MediaMonitor(BaseCollector):
    """
    Monitors media stories that may affect unit coherence.
    
    Tracks:
    - News stories mentioning unit/base
    - Social media trending topics
    - Local media coverage
    """
    
    def __init__(self,
                 keywords: List[str] = None,
                 sources: List[str] = None):
        super().__init__(privacy_mode="public_only", anonymize=False)
        self.keywords = keywords or []
        self.sources = sources or ["news", "military_times"]
    
    def collect(self, 
                timeframe_hours: int = 24,
                **kwargs) -> List[CollectedItem]:
        """
        Scan for relevant media stories.
        
        In production, connects to news APIs and monitoring services.
        """
        self.collected = []
        
        # Placeholder for actual media monitoring
        return self.collected
    
    def scan(self, 
             timeframe_hours: int = 24,
             relevance_threshold: float = 0.7) -> List[CollectedItem]:
        """Scan for relevant stories above threshold"""
        return self.collect(
            timeframe_hours=timeframe_hours,
            relevance_threshold=relevance_threshold
        )
    
    def add_keywords(self, keywords: List[str]):
        """Add keywords to monitor"""
        self.keywords.extend(keywords)
        self.keywords = list(set(self.keywords))  # Dedupe


# Export
__all__ = [
    'CollectedItem',
    'BaseCollector',
    'SocialMediaCollector',
    'CISDCollector', 
    'DebriefCollector',
    'MediaMonitor'
]
