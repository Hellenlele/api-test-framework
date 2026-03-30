#!/usr/bin/env python3

import subprocess
import sys
import os
import argparse


def run_tests(env="demo", test_path=None, markers=None, verbose=False):
    """
    Run API tests with specified parameters
    
    Args:
        env: Environment to test against (demo, local, dev, staging, prod)
        test_path: Specific test file or directory to run
        markers: Pytest markers to filter tests (e.g., 'smoke', 'not slow')
        verbose: Enable verbose output
    """
    
    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    
    # Build pytest command
    cmd = ['python', '-m', 'pytest']
    
    # Add environment
    cmd.extend(['--env', env])
    
    # Add test path if specified
    if test_path:
        cmd.append(test_path)
    
    # Add markers if specified
    if markers:
        cmd.extend(['-m', markers])
    
    # Add verbose flag
    if verbose:
        cmd.append('-v')
    
    # Set environment variable
    env_vars = os.environ.copy()
    env_vars['TEST_ENV'] = env
    
    print(f"Running command: {' '.join(cmd)}")
    print(f"Environment: {env}")
    print("-" * 50)
    
    try:
        # Run the tests
        result = subprocess.run(cmd, env=env_vars, cwd=os.path.dirname(__file__))
        
        print("-" * 50)
        print(f"Tests completed with exit code: {result.returncode}")
        print(f"Check reports/report.html for detailed results")
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Run API automation tests")
    
    parser.add_argument(
        '--env', 
        default='demo',
        choices=['demo', 'local', 'dev', 'staging', 'prod'],
        help='Environment to run tests against'
    )
    
    parser.add_argument(
        '--test', 
        help='Specific test file or directory to run'
    )
    
    parser.add_argument(
        '--markers', 
        help='Pytest markers to filter tests (e.g., "smoke", "not slow")'
    )
    
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--examples', 
        action='store_true',
        help='Show usage examples'
    )
    
    args = parser.parse_args()
    
    if args.examples:
        print_examples()
        return 0
    
    return run_tests(
        env=args.env,
        test_path=args.test,
        markers=args.markers,
        verbose=args.verbose
    )


def print_examples():
    """Print usage examples"""
    examples = """
Usage Examples:

1. Run all tests against demo environment:
   python run_tests.py

2. Run tests against staging environment:
   python run_tests.py --env staging

3. Run specific test file:
   python run_tests.py --test tests/test_users_api.py

4. Run only smoke tests:
   python run_tests.py --markers smoke

5. Run tests excluding slow ones:
   python run_tests.py --markers "not slow"

6. Run with verbose output:
   python run_tests.py -v

7. Run specific test method:
   python run_tests.py --test tests/test_users_api.py::TestUsersAPI::test_get_all_users

8. Combine multiple options:
   python run_tests.py --env dev --markers smoke -v

Environment Options:
- demo: JSONPlaceholder API (default, no auth required)
- local: Local development server
- dev: Development environment
- staging: Staging environment  
- prod: Production environment

Available Markers:
- smoke: Quick validation tests
- regression: Regression test suite
- integration: Integration tests
- slow: Long-running tests

Reports:
- HTML report: reports/report.html
- Execution logs: reports/test_execution.log
"""
    print(examples)


if __name__ == "__main__":
    sys.exit(main())