# Contributing to Mitsuba 3 Learning Demos

Thank you for your interest in contributing! This project aims to help people learn Mitsuba 3 through clear, well-documented examples.

## How Can I Contribute?

### 1. 🐛 Report Bugs

Found a bug? Please open an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Mitsuba version)
- Screenshots if applicable

### 2. 💡 Suggest Enhancements

Have ideas for improvements? Open an issue with:
- Feature description
- Why it would be useful
- Possible implementation approach
- Examples or mockups if relevant

### 3. 📝 Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add more examples
- Improve code comments
- Translate documentation
- Create tutorials or guides

### 4. 🎨 Add New Examples

Want to contribute a new demo? Great! Please ensure:
- Code is well-commented and educational
- Follows the existing style
- Includes detailed explanations
- Renders successfully
- Is appropriately scoped (not too complex for learners)

### 5. 🔧 Fix Issues

Check the issue tracker for open issues.

## Development Process

### 1. Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Mitsuba3-Learning-Demos.git
cd Mitsuba3-Learning-Demos
```

### 2. Set Up Environment

```powershell
# Create virtual environment
python -m venv mitsuba_venv

# Activate it
.\mitsuba_venv\Scripts\Activate.ps1  # Windows
source mitsuba_venv/bin/activate      # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 4. Make Changes

- Write clean, readable code
- Add comments explaining complex parts
- Follow existing code style
- Test your changes thoroughly

### 5. Test Your Changes

```bash
# Run the example you modified
python examples/01_basic_scene.py

# Check for Python errors
python -m py_compile examples/*.py

# Verify documentation renders correctly
```

### 6. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add feature: brief description

- More detailed explanation
- What changed and why
- Any relevant issue numbers"
```

### 7. Push & Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear title and description
- What problem it solves
- How you tested it
- Screenshots if applicable

## Code Style Guidelines

### Python Code

- **PEP 8**: Follow Python style guide
- **Comments**: Explain *why*, not just *what*
- **Docstrings**: Use for functions and classes
- **Variable names**: Descriptive and clear
- **Line length**: Keep under 100 characters when possible

Example:
```python
def create_glass_material(ior=1.5):
    """
    Create a glass dielectric material.
    
    Args:
        ior (float): Index of refraction (default: 1.5 for glass)
        
    Returns:
        dict: Mitsuba BSDF dictionary
    """
    return {
        'type': 'dielectric',
        'int_ior': ior,
    }
```

### Documentation

- **Clear headers**: Use proper Markdown hierarchy
- **Code blocks**: Specify language for syntax highlighting
- **Examples**: Show before/after or expected output
- **Links**: Use descriptive link text

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- First line: brief summary (50 chars or less)
- Blank line, then detailed description if needed
- Reference issues: "Fixes #123" or "Relates to #456"

Example:
```
Add advanced volumetric rendering example

- Demonstrates smoke and fog effects
- Includes heterogeneous media
- Adds comprehensive comments explaining volume parameters
- Updates documentation with volumetric concepts

Fixes #42
```

## File Organization

```
Mitsuba3-Learning-Demos/
├── examples/          # All demo Python files
├── docs/              # Documentation
│   └── .local/        # Local notes (not committed)
├── assets/            # Images, diagrams (if needed)
├── requirements.txt   # Dependencies
├── README.md          # Main documentation
├── LICENSE            # License information
└── CONTRIBUTING.md    # This file
```

### Adding New Examples

Place in `examples/` with naming convention:
- `XX_descriptive_name.py` where XX is number (06, 07, etc.)
- Include comprehensive comments
- Add entry to main README.md

### Adding Documentation

Place in `docs/` with clear, descriptive names:
- Use `.md` extension
- Link from main README if appropriate
- Keep focused on specific topics

## What NOT to Commit

❌ Virtual environments (`mitsuba_venv/`)
❌ Rendered images (`output/`, `*.png`, `*.jpg`)
❌ IDE configuration (`.vscode/`, `.idea/`)
❌ Personal notes (`docs/.local/`)
❌ Cache files (`__pycache__/`, `*.pyc`)
❌ Large binary files

These are already in `.gitignore`.

## Pull Request Review Process

1. **Automated checks**: Code must be valid Python
2. **Manual review**: Maintainer will review code and suggestions
3. **Discussion**: Constructive feedback and iterations
4. **Approval**: Once approved, PR will be merged
5. **Acknowledgment**: Contributors will be credited

## Questions?

- **Issues**: Open an issue for questions
- **Discussions**: Use GitHub Discussions for general topics
- **Email**: Contact repository owner for sensitive matters

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other conduct inappropriate in a professional setting

### Enforcement

Violations may result in:
- Warning
- Temporary ban
- Permanent ban

Report issues to repository maintainers.

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (if we create one)
- Mentioned in release notes
- Credited in relevant documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License, the same as the project.

## Thank You! 🙏

Every contribution, no matter how small, helps make this project better for learners worldwide. We appreciate your time and effort!

---

**Questions?** Feel free to open an issue or reach out!
