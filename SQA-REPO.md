**COMP 5710: Team 50% Project Outline** 

Elizabeth Casey, Ellie Cribbet, Avery Fox, & Jewels Wolter 

December 1, 2025

I.  **Fuzzing**

We first created a fuzz testing framework designed to test the
MLForensics project, which is a static analysis tool for detecting
security and quality issues in machine learning python code. This fuzz
testing framework has a variety of use cases, including security
auditing, code quality checks, machine learning operations,
compliance, and robustness testing.

The folder holds a variety of files, each with a unique purpose in the
fuzz testing framework. The constants.py file serves as a central
repository for all constants used throughout the MLForensics project.
This file defines keyword constants, library detection keywords,
forensic event categories, and the output format for forensic analysis
reports. The py_parser.py file is a Python Abstract Syntax Tree parser
that extracts code patterns from python files. The lint_engine.py file
serves as a pattern matching engine that executes data flow analysis
on ML code. These files were provided by the instructor.

The fuzz.py file is an automated fuzz testing suite to discover bugs
in the MLForensics parsers. We tested the following five methods,
including testing the parser with malformed files, attribute function
extraction, data loading detection with invalid inputs, assignment
extraction, and import detection with malformed imports. We first
imported the modules we wanted to test from py_parser.py and
lint_engine.py. We then generated random strings, random paths, and
random malformed python files. We then use the randomly generated
inputs and test them against the five implemented methods while also
generating a report file. We ran 50 iterations of each method, created
timestamped reports of each bug. Figure 1 shows the test output.

The test_fuzz.py file integrates pytest for the fuzz testing suite. It
tests five functions, including if the fuzz module can be imported,
tests the FuzzTester implementation, tests that the required
MLForensics modules are available, tests random string generation
utility, and executes a quick test. These methods are tested via a
pytest command. The test outflow is show in Figure 2. This pytest
integration allows us to run tests with just one command and to run
automatically as part of continuous integration workflows. It also
provides quick validation and better reporting than a standalone
fuzzer script.

One lesson learned when developing the fuzz file was that fuzzing itself
is more about discovering how a code breaks so you can fix it. It’s not
as much about proving the code works, but finding the issues with it to
make it better. We also learned the importance of good logging. When a bug
is found, it’s important to have a detailed log so a developer can find
exactly what went wrong and can track when and where the issues occur.
Each bug report for the fuzzer includes the exact input and timestamp which
provides everything needed to reproduce or fix any issues.

![: fuzz.py test output
results](./reportfigures/media/image1.png)*Figure 1*

![: test_fuzz.py test output
results](./reportfigures/media/image2.png)*Figure 2*

II. **Integrating Forensics**

We also integrated a forensics logging and analysis system into the
MLForensics project. This system provides decorator-based function
logging and statistical analysis tools for machine learning security
event metrics. This system has several use cases, including research
analysis, benchmarking, code quality checks, debugging, and auditing.

In order to implement this system, we were provided with two files:
frequency.py and report.py. The file frequency.py generates proportion
and density metrics from the MLForensics analysis results. It has three
core functions, one to count the total source lines of code across all
python files, one to calculate the proportion of files that contain at
least one occurrence of each event, and one to calculate the event
density. These functions also utilized a wrapper for automatic logging
of inputs and outputs. The file report.py aims to collect proportion and
density metrics statistics. It has two core functions, one to compute
the average and median proportions across repositories and one to
compute the average and median densities across repositories. When this
file is executed, it analyzes the three provided datasets.

In order to provide function code logging in our forensic logging
system, we first need to implement the core forensics infrastructure.
The file forsenics.py serves to wrap functions so they automatically log
function entry with all arguments, return values, and exceptions with
full stack traces. The logging follows the following format: \[CALL\],
\[RETURN\], \[EXCEPTION\] and writes to a forsenics.log file upon
execution. Figure 3 shows an example of the logging output. The
run_forsenics_demo.py file shows a small demonstration of the forensic
logging system and how it works. It creates dummy files and csv files
and runs the forensics analysis on these dummy files. The results were
stored in the demo_outputs file. Figure 4 shows the demo results.

One of the main problems encountered during this aspect of the project was 
working within a multi-module codebase where each component depended on the 
behavior of several others. Before implementing the required functionality, 
a clear understanding was required of how data flowed across modules and 
how each script interacted with the next. This was very different from 
typical assignments, where work is usually isolated to a single file.

![: forsenics.py logging output
example](./reportfigures/media/image3.png)*Figure 3*

![: Demo analysis
results](./reportfigures/media/image4.png)*Figure 4*

III. **Continuous Integration**

Finally, we integrated continuous integration with GitHub Actions. The
ci.yml file automates testing and fuzzing on every push to the main
branch and captures output for later analysis. The file is triggered on
pushes to the main branch, pull requests to the main branch, and can be
manually executed with workflow-dispatch. Once triggered, the core steps
include fetching the repository code, setting up python, installing
dependencies, running tests, running fuzzing, and uploading artifacts.

When installing dependencies, the runner upgrades pip and installs
pytest. It also installs top level requirements.txt, if available.
Figure 5 shows our projects requirements.txt file. To run the tests, the
runner creates the ci-artifacts directory and executes pytest, storing
the output in the ci-artifacts directory. To run fuzzing, the runner
creates the ci-artifacts directory and runs the fuzzer, once again
storing the output in the ci-artifacts directory. This step collects
logs from the fuzzer and writes a detailed report to fuzz_report.txt.
Figure 6 shows a snippet of this report. Additionally, both testing and
fuzzing are allowed to fail without failing the job. Finally, we upload
the artifacts stored in ci-artifacts as ci-results.

While setting up CI, there were a few issues that helped us better understand 
how GitHub Actions works. The first problem was how strict GitHub is about 
workflow file locations. At first, we accidentally used “workflow” instead of 
“workflows,” so nothing showed up in the Actions tab until I corrected the 
folder path to .github/workflows/. We also struggled a bit with YAML syntax, 
since even small indentation mistakes can break a workflow without giving 
clear error messages. Finally, we ran into dependency setup issues because the 
project didn’t originally include a requirements.txt, so we had to create one 
to ensure the runner could install everything correctly. These challenges ended 
up being helpful, because they taught us how precise CI configurations need to be 
and how easily small details can cause a pipeline to fail.

![: Requirements.txt
file](./reportfigures/media/image5.png)*Figure 5*

![: fuzz_report.txt
example](./reportfigures/media/image6.png)*Figure 6*
