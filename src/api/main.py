"""
Rose Looking Glass - REST API
=============================

FastAPI application exposing Rose Looking Glass translation services.

Endpoints:
- POST /translate - Translate text through current lens
- POST /view - View GCT variables through specific lens
- GET /lenses - List available cultural lenses
- POST /compare - Compare across all lenses
- POST /lens/select - Switch active lens
- POST /lens/add - Register new cultural lens
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

from ..core import (
    RoseLookingGlass,
    PatternVisibility,
    CulturalLens,
    BiologicalParameters
)

# Initialize FastAPI
app = FastAPI(
    title="Rose Looking Glass API",
    description="Translation service for synthetic-organic intelligence",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Rose Looking Glass instance
rose_glass = RoseLookingGlass()


# === Request/Response Models ===

class TranslateRequest(BaseModel):
    """Request to translate text"""
    text: str = Field(..., description="Text to translate", min_length=1)
    lens_name: Optional[str] = Field(None, description="Cultural lens to use (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Therefore, based on extensive research, I conclude that this approach is optimal.",
                "lens_name": "modern_academic"
            }
        }


class ViewRequest(BaseModel):
    """Request to view GCT variables through lens"""
    psi: float = Field(..., ge=0.0, le=1.0, description="Internal consistency (0-1)")
    rho: float = Field(..., ge=0.0, le=1.0, description="Wisdom depth (0-1)")
    q: float = Field(..., ge=0.0, le=1.0, description="Emotional activation (0-1)")
    f: float = Field(..., ge=0.0, le=1.0, description="Social belonging (0-1)")
    lens_name: Optional[str] = Field(None, description="Cultural lens to use (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "psi": 0.85,
                "rho": 0.90,
                "q": 0.25,
                "f": 0.30,
                "lens_name": "modern_academic"
            }
        }


class CompareRequest(BaseModel):
    """Request to compare across all lenses"""
    psi: float = Field(..., ge=0.0, le=1.0)
    rho: float = Field(..., ge=0.0, le=1.0)
    q: float = Field(..., ge=0.0, le=1.0)
    f: float = Field(..., ge=0.0, le=1.0)


class LensSelectRequest(BaseModel):
    """Request to select a lens"""
    lens_name: str = Field(..., description="Name of lens to activate")


class AddLensRequest(BaseModel):
    """Request to add a new cultural lens"""
    name: str
    display_name: str
    description: str
    weight_psi: float = Field(0.25, ge=0.0, le=1.0)
    weight_rho: float = Field(0.25, ge=0.0, le=1.0)
    weight_q: float = Field(0.25, ge=0.0, le=1.0)
    weight_f: float = Field(0.25, ge=0.0, le=1.0)
    typical_patterns: Optional[str] = None
    use_cases: Optional[List[str]] = None


class PatternVisibilityResponse(BaseModel):
    """Response containing pattern visibility"""
    psi: float
    rho: float
    q: float
    f: float
    coherence: float
    lens_name: str
    timestamp: str
    original_text_hash: str
    confidence: float
    alternative_lenses: List[str]
    uncertainty_notes: Optional[str]
    narrative: str

    @classmethod
    def from_visibility(cls, visibility: PatternVisibility) -> 'PatternVisibilityResponse':
        """Convert PatternVisibility to response model"""
        return cls(
            psi=visibility.psi,
            rho=visibility.rho,
            q=visibility.q,
            f=visibility.f,
            coherence=visibility.coherence,
            lens_name=visibility.lens_name,
            timestamp=visibility.timestamp.isoformat(),
            original_text_hash=visibility.original_text_hash,
            confidence=visibility.confidence,
            alternative_lenses=visibility.alternative_lenses,
            uncertainty_notes=visibility.uncertainty_notes,
            narrative=visibility.get_narrative()
        )


# === API Endpoints ===

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Rose Looking Glass",
        "version": "2.1.0",
        "description": "Translation service for synthetic-organic intelligence",
        "docs": "/docs",
        "current_lens": rose_glass.current_lens_name
    }


@app.post("/translate", response_model=PatternVisibilityResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text through Rose Looking Glass.

    Extracts GCT variables from text and computes pattern visibility
    through the specified cultural lens (or current lens if not specified).
    """
    try:
        visibility = rose_glass.translate_text(
            text=request.text,
            lens_name=request.lens_name
        )
        return PatternVisibilityResponse.from_visibility(visibility)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@app.post("/view", response_model=PatternVisibilityResponse)
async def view_through_lens(request: ViewRequest):
    """
    View GCT variables through a cultural lens.

    Applies biological optimization and computes coherence
    without extracting variables (use when you already have them).
    """
    try:
        visibility = rose_glass.view_through_lens(
            psi=request.psi,
            rho=request.rho,
            q=request.q,
            f=request.f,
            lens_name=request.lens_name
        )
        return PatternVisibilityResponse.from_visibility(visibility)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"View error: {str(e)}")


@app.post("/compare")
async def compare_lenses(request: CompareRequest):
    """
    Compare how the same pattern appears through ALL cultural lenses.

    Returns a map of lens names to pattern visibility results,
    revealing how different contexts interpret the same expression.
    """
    try:
        results = rose_glass.compare_lenses(
            psi=request.psi,
            rho=request.rho,
            q=request.q,
            f=request.f
        )

        return {
            lens_name: PatternVisibilityResponse.from_visibility(visibility).dict()
            for lens_name, visibility in results.items()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")


@app.get("/lenses")
async def list_lenses():
    """
    List all available cultural lenses.

    Returns a map of lens names to descriptions.
    """
    return {
        "current_lens": rose_glass.current_lens_name,
        "available_lenses": rose_glass.list_lenses(),
        "lens_details": {
            name: {
                "display_name": lens.display_name,
                "description": lens.description,
                "weights": {
                    "psi": lens.weight_psi,
                    "rho": lens.weight_rho,
                    "q": lens.weight_q,
                    "f": lens.weight_f
                },
                "use_cases": lens.use_cases
            }
            for name, lens in rose_glass.lenses.items()
        }
    }


@app.post("/lens/select")
async def select_lens(request: LensSelectRequest):
    """
    Switch to a different cultural lens.

    All subsequent /translate requests will use this lens
    unless overridden with lens_name parameter.
    """
    try:
        rose_glass.select_lens(request.lens_name)
        return {
            "message": f"Switched to lens: {request.lens_name}",
            "current_lens": rose_glass.current_lens_name,
            "lens_details": {
                "display_name": rose_glass.current_lens.display_name,
                "description": rose_glass.current_lens.description
            }
        }

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/lens/add")
async def add_lens(request: AddLensRequest):
    """
    Register a new cultural lens.

    Allows community contributions of new cultural calibrations.
    Weights must sum to 1.0.
    """
    try:
        lens = CulturalLens(
            name=request.name,
            display_name=request.display_name,
            description=request.description,
            weight_psi=request.weight_psi,
            weight_rho=request.weight_rho,
            weight_q=request.weight_q,
            weight_f=request.weight_f,
            typical_patterns=request.typical_patterns,
            use_cases=request.use_cases
        )

        rose_glass.add_lens(lens)

        return {
            "message": f"Lens '{request.name}' registered successfully",
            "lens_name": request.name,
            "display_name": request.display_name
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding lens: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.1.0",
        "lenses_loaded": len(rose_glass.lenses)
    }


# === Development Helpers ===

@app.get("/examples")
async def get_examples():
    """
    Get example requests for each endpoint.

    Useful for API exploration and testing.
    """
    return {
        "translate": {
            "url": "/translate",
            "method": "POST",
            "example": {
                "text": "I feel deeply connected to this community and our shared purpose.",
                "lens_name": "activist"
            }
        },
        "view": {
            "url": "/view",
            "method": "POST",
            "example": {
                "psi": 0.7,
                "rho": 0.8,
                "q": 0.5,
                "f": 0.6,
                "lens_name": "modern_academic"
            }
        },
        "compare": {
            "url": "/compare",
            "method": "POST",
            "example": {
                "psi": 0.5,
                "rho": 0.9,
                "q": 0.3,
                "f": 0.4
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
