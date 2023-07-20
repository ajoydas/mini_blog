#!/bin/bash

# Function to display the help message
function show_help() {
    echo "Usage: ./run-tests.sh [OPTIONS]"
    echo "Run tests, linter, and calculate code coverage for the Django project."
    echo ""
    echo "Options:"
    echo "-h, --help    Show this help message"
    echo "-t, --tests   Run tests"
    echo "-l, --lint    Run linter"
    echo "-c, --coverage   Calculate code coverage"
    echo ""
    exit 0
}

# Variables
RUN_TESTS=false
RUN_LINT=false
RUN_COVERAGE=false

# Parse command line options
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            show_help
            ;;
        -t|--tests)
            RUN_TESTS=true
            ;;
        -l|--lint)
            RUN_LINT=true
            ;;
        -c|--coverage)
            RUN_COVERAGE=true
            ;;
        *)
            echo "Unknown option: $key"
            echo "Use './run-tests.sh --help' to see the available options."
            exit 1
            ;;
    esac
    shift
done

# Run tests if specified
if [ "$RUN_TESTS" = true ]; then
    python manage.py test
fi

# Run linter if specified
if [ "$RUN_LINT" = true ]; then
    flake8 .
fi

# Calculate code coverage if specified
if [ "$RUN_COVERAGE" = true ]; then
    coverage run --source='.' manage.py test
    coverage report
    coverage html
fi
