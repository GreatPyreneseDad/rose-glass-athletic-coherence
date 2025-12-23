"""
Pattern Analyzers for Team Coherence
=====================================

Analyzers extract coherence patterns from collected data.
They translate raw data into Rose Glass dimensions.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import re
import sys
import os

# Try to import Rose Glass core
try:
    # Add potential paths
    potential_paths = [
        os.path.expanduser('~/rose-looking-glass/src'),
        os.path.expanduser('~/rose-glass'),
        '/Users/chris/rose-looking-glass/src',
        '/Users/chris/rose-glass',
    ]
    for path in potential_paths:
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, path)
    
    from core import RoseLookingGlass
    ROSE_GLASS_AVAILABLE = True
except ImportError:
    ROSE_GLASS_AVAILABLE = False


@dataclass
class PatternResult:
    """Result of pattern analysis"""
    psi: float
    rho: float
    q: float
    f: float
    tau: float
    
    confidence: float
    source_count: int
    notes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, float]:
        return {
            'psi': self.psi,
            'rho': self.rho,
            'q': self.q,
            'f': self.f,
            'tau': self.tau
        }


@dataclass
class CISDAnalysisResult:
    """Result of CISD report analysis"""
    processing_ratio: float      # % showing authentic processing
    performance_ratio: float     # % showing masking
    
    processing_indicators: List[str]
    performance_indicators: List[str]
    
    environmental_concerns: List[str]
    facilitator_notes: Optional[str]
    
    pattern: PatternResult


@dataclass
class TrajectoryPoint:
    """Single point in a trajectory"""
    timestamp: datetime
    pattern: PatternResult


class BaseAnalyzer:
    """Base class for pattern analyzers"""
    
    def __init__(self, use_ml: bool = True):
        self.use_ml = use_ml and ROSE_GLASS_AVAILABLE
        
        if self.use_ml:
            try:
                self.rose_glass = RoseLookingGlass()
            except:
                self.use_ml = False
                self.rose_glass = None
        else:
            self.rose_glass = None
    
    def _extract_pattern_ml(self, text: str) -> PatternResult:
        """Extract pattern using Rose Glass ML"""
        if not self.rose_glass:
            return self._extract_pattern_regex(text)
        
        result = self.rose_glass.translate_text(text)
        return PatternResult(
            psi=result.psi,
            rho=result.rho,
            q=result.q,
            f=result.f,
            tau=0.5,  # Estimate tau separately
            confidence=result.confidence,
            source_count=1
        )
    
    def _extract_pattern_regex(self, text: str) -> PatternResult:
        """Extract pattern using regex (fallback)"""
        text_lower = text.lower()
        words = text_lower.split()
        word_count = max(len(words), 1)
        
        # f-dimension: social belonging
        isolation_patterns = [
            r'\b(alone|lonely|isolated|nobody|no one)\b',
            r'\b(by myself|on my own)\b',
        ]
        connection_patterns = [
            r'\b(we|us|our|together|team)\b',
            r'\b(support|helped|buddy|brother|sister)\b',
        ]
        
        isolation = sum(len(re.findall(p, text_lower)) for p in isolation_patterns)
        connection = sum(len(re.findall(p, text_lower)) for p in connection_patterns)
        total = isolation + connection
        f = connection / total if total > 0 else 0.5
        
        # q-dimension: emotional activation
        activation_patterns = [
            r'\b(stressed|angry|frustrated|scared|anxious)\b',
            r'\b(worried|tense|overwhelmed|exhausted)\b',
        ]
        activation = sum(len(re.findall(p, text_lower)) for p in activation_patterns)
        exclamations = text.count('!')
        q = min(0.3 + activation * 0.1 + exclamations * 0.05, 1.0)
        
        # psi-dimension: consistency (limited with single text)
        psi = 0.7  # Default moderate
        
        # rho-dimension: wisdom
        wisdom_patterns = [
            r'\b(learned|realized|experience|wisdom)\b',
            r'\b(years|before|remember|history)\b',
        ]
        wisdom = sum(len(re.findall(p, text_lower)) for p in wisdom_patterns)
        rho = min(0.3 + wisdom * 0.1, 1.0)
        
        # tau: temporal depth
        past_patterns = [r'\b(was|were|used to|before|ago)\b']
        present_patterns = [r'\b(now|today|right now|currently)\b']
        past = sum(len(re.findall(p, text_lower)) for p in past_patterns)
        present = sum(len(re.findall(p, text_lower)) for p in present_patterns)
        
        if past > present:
            tau = min(0.5 + past * 0.05, 1.0)
        elif present > past:
            tau = max(0.5 - present * 0.05, 0.1)
        else:
            tau = 0.5
        
        return PatternResult(
            psi=psi,
            rho=rho,
            q=q,
            f=f,
            tau=tau,
            confidence=0.6,  # Lower confidence for regex
            source_count=1
        )


class CISDAnalyzer(BaseAnalyzer):
    """
    Analyzes CISD reports for processing vs. performance patterns.
    
    Does NOT diagnose individuals.
    Surfaces aggregate patterns and environmental factors.
    """
    
    # Processing indicators (authentic engagement)
    PROCESSING_INDICATORS = [
        r'\b(realized|understood|felt|struggled)\b',
        r'\b(hard|difficult|challenging|painful)\b',
        r'\b(support|helped|talked|shared)\b',
        r'\b(processing|working through|dealing with)\b',
    ]
    
    # Performance indicators (masking)
    PERFORMANCE_INDICATORS = [
        r'\b(fine|okay|good|normal|usual)\b',
        r'\b(handled|managed|no problem)\b',
        r'\b(moved on|over it|past it)\b',
        r'\b(don\'t need|unnecessary)\b',
    ]
    
    # Environmental concerns
    ENVIRONMENTAL_CONCERNS = [
        (r'career|promotion|evaluation', 'Career concerns may affect disclosure'),
        (r'command|leadership|supervisor', 'Command presence may affect openness'),
        (r'mandatory|required|ordered', 'Mandatory nature may reduce authenticity'),
        (r'quiet|silent|uncomfortable', 'Unusual silence may indicate unsafe environment'),
    ]
    
    def analyze(self,
                cisd_document: str,
                incident_date: Optional[datetime] = None,
                facilitator_notes: Optional[str] = None) -> CISDAnalysisResult:
        """
        Analyze CISD report for patterns.
        
        Returns processing/performance ratio and environmental factors.
        """
        doc_lower = cisd_document.lower()
        
        # Count indicators
        processing_matches = []
        for pattern in self.PROCESSING_INDICATORS:
            matches = re.findall(pattern, doc_lower)
            processing_matches.extend(matches)
        
        performance_matches = []
        for pattern in self.PERFORMANCE_INDICATORS:
            matches = re.findall(pattern, doc_lower)
            performance_matches.extend(matches)
        
        total = len(processing_matches) + len(performance_matches)
        if total > 0:
            processing_ratio = len(processing_matches) / total
            performance_ratio = len(performance_matches) / total
        else:
            processing_ratio = 0.5
            performance_ratio = 0.5
        
        # Check environmental concerns
        environmental_concerns = []
        for pattern, concern in self.ENVIRONMENTAL_CONCERNS:
            if re.search(pattern, doc_lower):
                environmental_concerns.append(concern)
        
        # Extract pattern
        pattern = self._extract_pattern_regex(cisd_document)
        
        return CISDAnalysisResult(
            processing_ratio=processing_ratio,
            performance_ratio=performance_ratio,
            processing_indicators=list(set(processing_matches)),
            performance_indicators=list(set(performance_matches)),
            environmental_concerns=environmental_concerns,
            facilitator_notes=facilitator_notes,
            pattern=pattern
        )
    
    def assess_cisd_program(self,
                           reports: List[str],
                           timeframe_months: int = 6) -> Dict[str, Any]:
        """
        Assess CISD program effectiveness across multiple reports.
        
        Returns aggregate metrics about program function.
        """
        if not reports:
            return {
                'processing_rate': 0.0,
                'performance_rate': 0.0,
                'sample_size': 0,
                'environmental_factors': [],
                'recommendation': 'Insufficient data'
            }
        
        analyses = [self.analyze(r) for r in reports]
        
        avg_processing = sum(a.processing_ratio for a in analyses) / len(analyses)
        avg_performance = sum(a.performance_ratio for a in analyses) / len(analyses)
        
        # Collect all environmental concerns
        all_concerns = []
        for a in analyses:
            all_concerns.extend(a.environmental_concerns)
        
        # Count frequency
        concern_counts = {}
        for c in all_concerns:
            concern_counts[c] = concern_counts.get(c, 0) + 1
        
        frequent_concerns = [c for c, count in concern_counts.items() 
                           if count > len(analyses) * 0.3]
        
        # Generate recommendation
        if avg_performance > 0.6:
            recommendation = (
                "High performance indicators suggest environment may not feel safe "
                "for authentic disclosure. Consider peer-led vs. command-adjacent facilitation."
            )
        elif avg_processing > 0.7:
            recommendation = "Healthy processing indicators. Program appears effective."
        else:
            recommendation = "Mixed indicators. Consider follow-up assessment."
        
        return {
            'processing_rate': avg_processing,
            'performance_rate': avg_performance,
            'sample_size': len(analyses),
            'environmental_factors': frequent_concerns,
            'recommendation': recommendation
        }


class DebriefAnalyzer(BaseAnalyzer):
    """Analyzes debrief transcripts for coherence patterns"""
    
    def analyze_transcript(self,
                          transcript: str,
                          participants: Optional[List[str]] = None,
                          incident_type: Optional[str] = None) -> PatternResult:
        """Analyze a single debrief transcript"""
        return self._extract_pattern_regex(transcript)
    
    def track_trajectory(self,
                        transcripts: List[Tuple[datetime, str]],
                        unit_id: str) -> List[TrajectoryPoint]:
        """Track pattern trajectory across multiple debriefs"""
        trajectory = []
        
        for timestamp, transcript in sorted(transcripts, key=lambda x: x[0]):
            pattern = self._extract_pattern_regex(transcript)
            trajectory.append(TrajectoryPoint(
                timestamp=timestamp,
                pattern=pattern
            ))
        
        return trajectory


class SocialPatternAnalyzer(BaseAnalyzer):
    """Analyzes social media patterns for coherence signals"""
    
    def analyze_posts(self, posts: List[Dict]) -> PatternResult:
        """
        Analyze collection of posts for aggregate pattern.
        
        Args:
            posts: List of dicts with 'content' and 'timestamp' keys
        """
        if not posts:
            return PatternResult(
                psi=0.5, rho=0.5, q=0.5, f=0.5, tau=0.5,
                confidence=0.0, source_count=0
            )
        
        # Analyze each post
        patterns = []
        for post in posts:
            content = post.get('content', '')
            if content:
                patterns.append(self._extract_pattern_regex(content))
        
        if not patterns:
            return PatternResult(
                psi=0.5, rho=0.5, q=0.5, f=0.5, tau=0.5,
                confidence=0.0, source_count=0
            )
        
        # Aggregate
        return PatternResult(
            psi=sum(p.psi for p in patterns) / len(patterns),
            rho=sum(p.rho for p in patterns) / len(patterns),
            q=sum(p.q for p in patterns) / len(patterns),
            f=sum(p.f for p in patterns) / len(patterns),
            tau=sum(p.tau for p in patterns) / len(patterns),
            confidence=0.7,
            source_count=len(patterns)
        )


class TrajectoryAnalyzer:
    """Analyzes coherence trajectories over time"""
    
    def analyze(self, 
                trajectory: List[TrajectoryPoint]) -> Dict[str, Any]:
        """
        Analyze trajectory for trends and concerns.
        """
        if len(trajectory) < 2:
            return {
                'psi_trend': 0.0,
                'rho_trend': 0.0,
                'q_trend': 0.0,
                'f_trend': 0.0,
                'tau_trend': 0.0,
                'concerns': [],
                'sample_size': len(trajectory)
            }
        
        # Calculate trends (simple slope)
        def calc_trend(dim: str) -> float:
            values = [getattr(p.pattern, dim) for p in trajectory]
            n = len(values)
            if n < 2:
                return 0.0
            
            x_mean = (n - 1) / 2
            y_mean = sum(values) / n
            
            numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
            denominator = sum((i - x_mean) ** 2 for i in range(n))
            
            if denominator == 0:
                return 0.0
            return numerator / denominator
        
        trends = {
            'psi_trend': calc_trend('psi'),
            'rho_trend': calc_trend('rho'),
            'q_trend': calc_trend('q'),
            'f_trend': calc_trend('f'),
            'tau_trend': calc_trend('tau'),
        }
        
        # Identify concerns
        concerns = []
        
        if trends['f_trend'] < -0.02:
            concerns.append('f-dimension declining (isolation increasing)')
        
        if trends['q_trend'] > 0.03:
            concerns.append('q-dimension rising (activation increasing)')
        
        if trends['psi_trend'] < -0.02:
            concerns.append('psi-dimension declining (consistency fragmenting)')
        
        trends['concerns'] = concerns
        trends['sample_size'] = len(trajectory)
        
        return trends


# Export
__all__ = [
    'PatternResult',
    'CISDAnalysisResult',
    'TrajectoryPoint',
    'BaseAnalyzer',
    'CISDAnalyzer',
    'DebriefAnalyzer',
    'SocialPatternAnalyzer',
    'TrajectoryAnalyzer'
]
