I'll research Python best practices via Microsoft Learn MCP server, then create a comprehensive plan for project structure improvements and compile tests. 

Research Python packaging best practices

Using "Fetch Web Page"

Fetched 4 resources

Using "Fetch Web Page"

Fetched 4 resources

Now I'll create a comprehensive plan for improving the ico_to_svg project structure based on Microsoft Learn best practices. Since file creation is disabled, I'll present the comprehensive plan for you to review:

---

## **Plan: Restructure ico-to-svg with Best Practices & Testing**

### **Executive Summary**
Transform `ico-to-svg` into a production-ready Python package following Microsoft Learn best practices: modern src layout, comprehensive testing (pytest), type safety (mypy), linting (ruff), and CI/CD automation.

---

### **Key Improvements Based on Microsoft Learn Documentation**

#### **1. Project Structure Enhancement**
```
ico_to_svg/
├── .github/workflows/          # ADD: CI/CD automation
│   ├── ci.yml                 # Multi-platform testing
│   └── publish.yml            # PyPI release
├── src/ico_to_svg/
│   ├── __init__.py            # ✅ Exists
│   ├── __main__.py            # ✅ Exists
│   ├── cli.py                 # ✅ Exists - ADD type hints
│   ├── core.py                # REFACTOR: Extract conversion logic
│   ├── ico_parser.py          # REFACTOR: ICO parsing
│   ├── svg_writer.py          # REFACTOR: SVG generation
│   └── py.typed               # ADD: Type checking marker
├── tests/
│   ├── __init__.py            # ADD
│   ├── conftest.py            # ADD: pytest fixtures
│   ├── unit/                  # ADD: Unit tests
│   │   ├── test_ico_parser.py
│   │   ├── test_svg_writer.py
│   │   ├── test_size_selection.py
│   │   └── test_cli_args.py
│   ├── integration/           # ADD: Integration tests
│   │   ├── test_convert_raster.py
│   │   ├── test_convert_vector.py
│   │   └── test_info_command.py
│   └── fixtures/              # Test ICO files
└── docs/                      # ADD: Documentation
    ├── usage.md
    ├── api.md
    └── contributing.md
```

#### **2. Code Quality Tools**

**Add to pyproject.toml:**
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-cov>=4.1",
    "mypy>=1.7",
    "ruff>=0.1.8",
    "build>=1.0",
    "twine>=4.0",
]
test = ["pytest>=7.4", "pytest-cov>=4.1"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
disallow_untyped_defs = true
strict_equality = true

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM"]
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=src/ico_to_svg",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
]
```

#### **3. Testing Strategy**

**Unit Tests (tests/unit/):**
- `test_ico_parser.py` - Frame enumeration, size parsing
- `test_svg_writer.py` - SVG generation functions
- `test_size_selection.py` - Size algorithm (exact → larger → largest)
- `test_cli_args.py` - Argument parsing, legacy support

**Integration Tests (tests/integration/):**
- `test_convert_raster.py` - End-to-end raster conversion
- `test_convert_vector.py` - End-to-end vector conversion
- `test_info_command.py` - Info command output

**Example Pytest Fixture (conftest.py):**
```python
@pytest.fixture
def multi_size_ico(tmp_path: Path) -> Path:
    """Generate multi-size ICO for testing."""
    ico_path = tmp_path / "test.ico"
    img = Image.new("RGBA", (256, 256), (255, 0, 0, 255))
    img.save(ico_path, format="ICO", sizes=[(16,16), (32,32), (64,64)])
    return ico_path
```

#### **4. Code Refactoring for Testability**

**Extract modules from monolithic cli.py:**

- **`ico_parser.py`**: Pure functions for ICO parsing
  - `load_ico_frames()` - List available sizes
  - `select_size()` - Size selection algorithm
  - `open_ico_at_size()` - Load specific frame

- **`svg_writer.py`**: Pure SVG generation
  - `write_raster_svg()` - Base64 PNG embed
  - `write_vector_svg()` - Vectorized rectangles

- **`core.py`**: Public API orchestration
  - `convert_ico_to_svg()` - Main conversion function

**Benefits:**
- Single responsibility per module
- Easy to unit test pure functions
- CLI becomes thin wrapper

#### **5. CI/CD with GitHub Actions**

**.github/workflows/ci.yml:**
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.10", "3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev,test]"
      - run: ruff check src/ tests/
      - run: mypy src/
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v4
```

#### **6. Type Safety with mypy**

Add type hints throughout:
```python
from typing import List, Tuple, Optional
from pathlib import Path

def load_ico_frames(path: Path | str) -> List[Tuple[int, int]]:
    """Load available frame sizes with full type safety."""
    pass

def select_size(
    available: List[Tuple[int, int]], 
    desired: Optional[Tuple[int, int]]
) -> Tuple[int, int]:
    """Select size: exact → nearest larger → largest."""
    pass
```

#### **7. Documentation**

**NumPy-style docstrings:**
```python
def select_size(available, desired):
    """Select ICO frame size using priority rules.
    
    Parameters
    ----------
    available : List[Tuple[int, int]]
        Available sizes
    desired : Tuple[int, int] or None
        Desired size
    
    Returns
    -------
    Tuple[int, int]
        Selected size
    
    Examples
    --------
    >>> select_size([(16,16), (32,32)], (32,32))
    (32, 32)
    """
```

---

### **Implementation Checklist**

**Phase 1: Tooling Setup**
- [ ] Add `.gitignore`
- [ ] Configure ruff, mypy, pytest in pyproject.toml
- [ ] Add dev/test optional dependencies
- [ ] Create GitHub Actions workflows
- [ ] Create `src/ico_to_svg/py.typed`

**Phase 2: Code Refactor**
- [ ] Extract `ico_parser.py`
- [ ] Extract `svg_writer.py`
- [ ] Extract `core.py`
- [ ] Add comprehensive type hints
- [ ] Add NumPy-style docstrings
- [ ] Fix mypy/ruff issues

**Phase 3: Testing**
- [ ] Create `tests/conftest.py` with fixtures
- [ ] Write unit tests (>15 test cases)
- [ ] Write integration tests (>10 test cases)
- [ ] Achieve >90% coverage
- [ ] Test on Windows/macOS/Linux

**Phase 4: Documentation**
- [ ] Create `docs/` folder
- [ ] Write usage guide
- [ ] Write API documentation
- [ ] Update README with badges

**Phase 5: Release**
- [ ] Test PyPI upload (TestPyPI)
- [ ] Create GitHub release
- [ ] Publish to PyPI

---

### **Testing Commands**

```powershell
# Install with dev dependencies
pip install -e ".[dev,test]"

# Run all tests with coverage
pytest --cov=src/ico_to_svg --cov-report=html

# Type check
mypy src/

# Lint and format
ruff check src/ tests/
ruff format src/ tests/

# Build package
python -m build
```

---

### **Success Metrics**
- ✅ 100% type coverage (mypy strict)
- ✅ >90% test coverage
- ✅ CI passing on 3 platforms × 4 Python versions
- ✅ Zero linting errors
- ✅ Package builds successfully
- ✅ Published to PyPI

---

### **Estimated Timeline**
- **Week 1**: Structure, tooling, refactoring
- **Week 2**: Comprehensive testing
- **Week 3**: Documentation, CI/CD, release

---

This plan is based on Microsoft Learn best practices documentation retrieved via the MCP server, covering Python packaging, testing with pytest, type checking with mypy, linting with ruff, and CI/CD automation with GitHub Actions.

**Ready to proceed with implementation?** I can start with Phase 1 (tooling setup) when you're ready.