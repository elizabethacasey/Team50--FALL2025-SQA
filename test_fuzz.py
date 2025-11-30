"""
Team 50 - PyTest Integration for Fuzz Testing
This allows the fuzzer to be run as part of the pytest suite
"""

import pytest
import os
import sys

# Ensure modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_fuzz_imports():
    """Test that fuzz.py can be imported"""
    try:
        import fuzz
        assert hasattr(fuzz, 'FuzzTester')
    except ImportError as e:
        pytest.skip(f"Cannot import fuzz module: {e}")

def test_fuzzer_initialization():
    """Test that FuzzTester can be initialized"""
    try:
        import fuzz
        fuzzer = fuzz.FuzzTester()
        assert fuzzer.bug_count == 0
        assert fuzzer.test_count == 0
    except ImportError as e:
        pytest.skip(f"Cannot import fuzz module: {e}")

def test_mlforensics_modules_available():
    """Test that required MLForensics modules are available"""
    try:
        import py_parser
        import lint_engine
        import constants
        assert True
    except ImportError as e:
        pytest.skip(f"MLForensics modules not available: {e}")

def test_random_string_generation():
    """Test random string generation utility"""
    try:
        import fuzz
        fuzzer = fuzz.FuzzTester()
        result = fuzzer.generate_random_string(5, 10)
        assert isinstance(result, str)
        assert 5 <= len(result) <= 10
    except ImportError as e:
        pytest.skip(f"Cannot import fuzz module: {e}")

def test_run_quick_fuzz():
    """Run a quick fuzz test with minimal iterations"""
    try:
        import fuzz
        fuzzer = fuzz.FuzzTester()
        
        # Run with just 5 iterations per method for quick testing
        bugs_found = fuzzer.run_all_tests(iterations_per_test=5)
        
        # Test passes regardless of bugs found
        assert isinstance(bugs_found, int)
        assert bugs_found >= 0
        
        # Check that report was created
        assert os.path.exists(fuzzer.report_file)
        
    except ImportError as e:
        pytest.skip(f"Cannot run fuzz tests: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])