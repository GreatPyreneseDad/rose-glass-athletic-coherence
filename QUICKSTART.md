# Rose Looking Glass - Quick Start Guide

Get up and running in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/GreatPyreneseDad/rose-looking-glass.git
cd rose-looking-glass

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Hello World

Create a file `hello_rose.py`:

```python
from src.core import RoseLookingGlass

# Initialize the lens
glass = RoseLookingGlass()

# Translate some text
text = "Therefore, based on the evidence, I conclude this is correct."
result = glass.translate_text(text)

# View the translation
print(result.get_narrative())
```

Run it:
```bash
python hello_rose.py
```

You should see:
```
Pattern Visibility Report
=========================
Lens: Modern Academic
Time: 2024-12-12 15:30:45

Dimensions:
-----------
• Ψ (Internal Consistency): 0.80
• ρ (Wisdom Depth): 0.65
• q (Emotional Activation): 0.15
• f (Social Belonging): 0.20

Overall Coherence: 0.68
Confidence: 85%
```

## Try Different Lenses

```python
# Switch to digital native lens
glass.select_lens('digital_native')

text = "omg this is SO cool!! 🎉"
result = glass.translate_text(text)

print(f"Coherence: {result.coherence:.2f}")
print(f"Emotional activation: {result.q:.2f}")
```

## Start the API Server

```bash
uvicorn src.api.main:app --reload
```

Navigate to `http://localhost:8000/docs` for interactive API documentation.

## Run Examples

```bash
python examples/basic_usage.py
```

This will run 7 comprehensive examples demonstrating all features.

## Run Tests

```bash
pytest tests/ -v
```

## Using Docker

```bash
# Build and run
docker-compose up -d

# API will be available at http://localhost:8000
```

## What's Next?

- Read the full [README.md](./README.md) for detailed documentation
- Explore `examples/basic_usage.py` for more examples
- Try the REST API at `http://localhost:8000/docs`
- Read about cultural lenses in the main README

## Common First Steps

### 1. Compare how different lenses see the same text

```python
glass = RoseLookingGlass()

# Extract variables once
vars = glass.gct_extractor.extract("Your text here")

# Compare across all lenses
comparisons = glass.compare_lenses(
    psi=vars.psi,
    rho=vars.rho,
    q=vars.q,
    f=vars.f
)

for lens_name, visibility in comparisons.items():
    print(f"{lens_name}: {visibility.coherence:.2f}")
```

### 2. Detect high-stress/crisis situations

```python
glass = RoseLookingGlass(default_lens='trauma_informed')

text = "I'm terrified and don't know what to do"
result = glass.translate_text(text)

if result.q > 0.7:
    print("⚠️  HIGH EMOTIONAL ACTIVATION - Crisis response needed")
```

### 3. Create a custom lens

```python
from src.core import CulturalLens

my_lens = CulturalLens(
    name='my_custom_lens',
    display_name='My Custom Lens',
    description='For my specific use case',
    weight_psi=0.3,
    weight_rho=0.3,
    weight_q=0.2,
    weight_f=0.2
)

glass.add_lens(my_lens)
glass.select_lens('my_custom_lens')
```

## Troubleshooting

**Import errors?**
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

**Tests failing?**
- Check Python version: `python --version` (requires 3.9+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

**API not starting?**
- Check port 8000 is not in use: `lsof -i :8000`
- Try a different port: `uvicorn src.api.main:app --port 8001`

## Help & Support

- **GitHub Issues**: [Report bugs](https://github.com/GreatPyreneseDad/rose-looking-glass/issues)
- **Discussions**: [Ask questions](https://github.com/GreatPyreneseDad/rose-looking-glass/discussions)
- **Documentation**: See [README.md](./README.md)

Happy translating! 🌹
