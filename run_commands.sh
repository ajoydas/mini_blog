#!/bin/bash

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
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
      # Unknown option
      echo "Unknown option: $key"
      exit 1
      ;;
  esac
  shift
done

# Run tests
if [ "$RUN_TESTS" = true ]; then
  echo "Running tests..."
  pytest
fi

# Run linting
if [ "$RUN_LINT" = true ]; then
  echo "Running linting..."
  flake8
fi

# Calculate code coverage
if [ "$RUN_COVERAGE" = true ]; then
  echo "Calculating code coverage..."
  coverage run manage.py test
  coverage html
fi

echo "Process completed."
