import os
import subprocess

#
# Run through the common browser's and run selenium tests against each of them
# in case of small inconsistencies between browser implementations
#

# List of browser values to use during tests
browsers = ['chrome', 'firefox', 'edge'
            # ,'safari'  -> need to have a safari browser on local pc (or via another
            # platform. eg Selenium Grid) to use this.
            ]

DJANGO_TEST_BROWSER = 'DJANGO_TEST_BROWSER'

# Path to python inside the virtual environment
python_executable = r'venv\Scripts\python.exe'

# The Django manage.py command
command = [python_executable, 'manage.py', 'test']

for browser in browsers:
    # Set the environment variable for the test run
    os.environ[DJANGO_TEST_BROWSER] = browser
    print(f'Running tests with {DJANGO_TEST_BROWSER}={browser}')

    try:
        # Run the command to execute Django tests
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Tests failed with {DJANGO_TEST_BROWSER}={browser}. Error: {e}')
    else:
        print(f'Tests passed with {DJANGO_TEST_BROWSER}={browser}')

print("All test runs completed.")
