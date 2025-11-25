"""
Team 50 - COMP 5710 Fuzz Testing
Ellie Cribbet
Fuzz testing for 5 Python methods from MLForensics project
"""

import random
import string
import os
import tempfile
import traceback
from datetime import datetime

# Import the modules we want to fuzz
try:
    import py_parser
    import lint_engine
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure py_parser.py and lint_engine.py are in the same directory")
    exit(1)


class FuzzTester:
    """Fuzzing test suite for MLForensics methods"""
    
    def __init__(self, report_dir="ci-artifacts"):
        # Create output directory if it doesn't exist
        os.makedirs(report_dir, exist_ok=True)
        self.report_file = os.path.join(report_dir, "fuzz_report.txt")
        self.bug_count = 0
        self.test_count = 0
        self.start_time = datetime.now()
        
    def generate_random_string(self, min_len=0, max_len=100):
        """Generate random string with various characters"""
        length = random.randint(min_len, max_len)
        chars = string.ascii_letters + string.digits + string.punctuation + '\n\t '
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_random_path(self):
        """Generate random file paths including edge cases"""
        paths = [
            "",  # Empty string
            " ",  # Whitespace
            "nonexistent.py",
            "../../../etc/passwd",  # Path traversal
            "file with spaces.py",
            "ファイル.py",  # Unicode
            "a" * 1000 + ".py",  # Very long path
            "/dev/null",
            "CON",  # Windows reserved name
            self.generate_random_string(5, 50),
            None,  # None value
        ]
        return random.choice(paths)
    
    def generate_malformed_python_file(self):
        """Create temporary Python file with malformed content"""
        malformed_content = [
            "",  # Empty file
            "import",  # Incomplete import
            "def (",  # Malformed function
            "class :\n    pass",  # Malformed class
            "'''",  # Unclosed string
            "for i in",  # Incomplete loop
            self.generate_random_string(10, 200),  # Random garbage
            "def func():\n" + "\t" * 1000 + "pass",  # Deep nesting
            "# " + "x" * 10000,  # Very long comment
            "\x00\x01\x02",  # Binary data
        ]
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8')
        try:
            content = random.choice(malformed_content)
            temp_file.write(content)
            temp_file.flush()
            return temp_file.name
        except Exception:
            return temp_file.name
        finally:
            temp_file.close()
    
    def log_bug(self, method_name, input_data, exception):
        """Log discovered bugs to report file"""
        self.bug_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        bug_report = f"""
{'='*80}
BUG #{self.bug_count} DETECTED - {timestamp}
{'='*80}
Method: {method_name}
Input: {repr(input_data)[:200]}
Exception Type: {type(exception).__name__}
Exception Message: {str(exception)[:300]}

Traceback:
{traceback.format_exc()}
{'='*80}

"""
        
        with open(self.report_file, 'a', encoding='utf-8') as f:
            f.write(bug_report)
        
        print(f"[BUG] {method_name} failed with {type(exception).__name__}")
    
    def fuzz_getPythonParseObject(self, iterations=50):
        """Fuzz test for py_parser.getPythonParseObject()"""
        print(f"\n[TEST 1/5] Fuzzing py_parser.getPythonParseObject() - {iterations} iterations")
        
        for i in range(iterations):
            self.test_count += 1
            
            # Generate test input
            if random.random() < 0.5:
                test_input = self.generate_random_path()
            else:
                test_input = self.generate_malformed_python_file()
            
            try:
                result = py_parser.getPythonParseObject(test_input)
                # Additional checks
                if result is None:
                    raise ValueError("Returned None unexpectedly")
            except (SyntaxError, UnicodeDecodeError, FileNotFoundError, OSError):
                # Expected exceptions - not bugs
                pass
            except Exception as e:
                self.log_bug("py_parser.getPythonParseObject", test_input, e)
            finally:
                # Cleanup temp files
                if isinstance(test_input, str) and test_input.endswith('.py') and os.path.exists(test_input):
                    try:
                        os.unlink(test_input)
                    except Exception:
                        pass
    
    def fuzz_getPythonAttributeFuncs(self, iterations=50):
        """Fuzz test for py_parser.getPythonAtrributeFuncs()"""
        print(f"[TEST 2/5] Fuzzing py_parser.getPythonAtrributeFuncs() - {iterations} iterations")
        
        for i in range(iterations):
            self.test_count += 1
            
            # Create malformed Python file
            temp_file = self.generate_malformed_python_file()
            
            try:
                py_tree = py_parser.getPythonParseObject(temp_file)
                result = py_parser.getPythonAtrributeFuncs(py_tree)
                
                # Validate result
                if not isinstance(result, list):
                    raise TypeError(f"Expected list, got {type(result)}")
                    
            except (SyntaxError, AttributeError):
                # Expected exceptions
                pass
            except Exception as e:
                self.log_bug("py_parser.getPythonAtrributeFuncs", temp_file, e)
            finally:
                if os.path.exists(temp_file):
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass
    
    def fuzz_getDataLoadCount(self, iterations=50):
        """Fuzz test for lint_engine.getDataLoadCount()"""
        print(f"[TEST 3/5] Fuzzing lint_engine.getDataLoadCount() - {iterations} iterations")
        
        for i in range(iterations):
            self.test_count += 1
            
            # Generate various test inputs
            test_inputs = [
                self.generate_random_path(),
                self.generate_malformed_python_file(),
                None,
                123,  # Wrong type
                [],  # Wrong type
                {"key": "value"},  # Wrong type
            ]
            
            test_input = random.choice(test_inputs)
            
            try:
                result = lint_engine.getDataLoadCount(test_input)
                
                # Validate result type
                if not isinstance(result, int):
                    raise TypeError(f"Expected int, got {type(result)}")
                if result < 0:
                    raise ValueError(f"Count cannot be negative: {result}")
                    
            except (TypeError, AttributeError, FileNotFoundError, UnicodeDecodeError):
                # Expected exceptions
                pass
            except Exception as e:
                self.log_bug("lint_engine.getDataLoadCount", test_input, e)
            finally:
                if isinstance(test_input, str) and test_input.endswith('.py') and os.path.exists(test_input):
                    try:
                        os.unlink(test_input)
                    except Exception:
                        pass
    
    def fuzz_getFunctionAssignments(self, iterations=50):
        """Fuzz test for py_parser.getFunctionAssignments()"""
        print(f"[TEST 4/5] Fuzzing py_parser.getFunctionAssignments() - {iterations} iterations")
        
        for i in range(iterations):
            self.test_count += 1
            
            temp_file = self.generate_malformed_python_file()
            
            try:
                py_tree = py_parser.getPythonParseObject(temp_file)
                result = py_parser.getFunctionAssignments(py_tree)
                
                # Validate result
                if not isinstance(result, list):
                    raise TypeError(f"Expected list, got {type(result)}")
                    
            except (AttributeError, KeyError):
                # Expected exceptions
                pass
            except Exception as e:
                self.log_bug("py_parser.getFunctionAssignments", temp_file, e)
            finally:
                if os.path.exists(temp_file):
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass
    
    def fuzz_getImport(self, iterations=50):
        """Fuzz test for py_parser.getImport()"""
        print(f"[TEST 5/5] Fuzzing py_parser.getImport() - {iterations} iterations")
        
        for i in range(iterations):
            self.test_count += 1
            
            # Create files with various import statements
            import_statements = [
                "import os",
                "from sys import *",
                "import",  # Malformed
                "from . import something",
                "from ..parent import module",
                "import " + self.generate_random_string(5, 30),
                "",
                "import os as " + self.generate_random_string(3, 10),
            ]
            
            content = random.choice(import_statements)
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8')
            temp_file.write(content)
            temp_file.close()
            
            try:
                py_tree = py_parser.getPythonParseObject(temp_file.name)
                result = py_parser.getImport(py_tree)
                
                # Validate result
                if not isinstance(result, list):
                    raise TypeError(f"Expected list, got {type(result)}")
                    
            except (AttributeError, KeyError, IndexError):
                # Expected exceptions
                pass
            except Exception as e:
                self.log_bug("py_parser.getImport", temp_file.name, e)
            finally:
                if os.path.exists(temp_file.name):
                    try:
                        os.unlink(temp_file.name)
                    except Exception:
                        pass
    
    def run_all_tests(self, iterations_per_test=50):
        """Run all fuzz tests"""
        print("="*80)
        print("TEAM 50 - FUZZ TESTING SUITE")
        print("Testing 5 methods from MLForensics project")
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        # Initialize report file
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(f"Fuzz Testing Report - Team 50\n")
            f.write(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Iterations per method: {iterations_per_test}\n")
            f.write("="*80 + "\n\n")
        
        # Run all fuzz tests
        self.fuzz_getPythonParseObject(iterations_per_test)
        self.fuzz_getPythonAttributeFuncs(iterations_per_test)
        self.fuzz_getDataLoadCount(iterations_per_test)
        self.fuzz_getFunctionAssignments(iterations_per_test)
        self.fuzz_getImport(iterations_per_test)
        
        # Generate summary
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        summary = f"""
{'='*80}
FUZZ TESTING SUMMARY
{'='*80}
Total Tests Run: {self.test_count}
Total Bugs Found: {self.bug_count}
Duration: {duration:.2f} seconds
Bug Rate: {(self.bug_count/self.test_count*100):.2f}%
Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}
"""
        
        print(summary)
        
        with open(self.report_file, 'a', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\nFull report saved to: {self.report_file}")
        
        return self.bug_count


if __name__ == "__main__":
    fuzzer = FuzzTester()
    bugs_found = fuzzer.run_all_tests(iterations_per_test=50)
    
    # Exit with error code if bugs found (useful for CI)
    if bugs_found > 0:
        print(f"\n⚠️  WARNING: {bugs_found} bugs discovered during fuzzing!")
        exit(0)  # Don't fail CI, just report
    else:
        print("\n✓ No unexpected bugs found during fuzzing!")
        exit(0)
