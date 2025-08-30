#!/bin/bash

# Start the Kafka cluster and its dependencies in the background
echo "Starting Kafka cluster with Docker Compose..."
docker-compose up -d

# Wait for Kafka to be ready to accept connections.
# This prevents the tests from failing because they can't connect.
echo "Waiting for Kafka broker to be ready..."
./wait-for-it.sh kafka-broker:9092 -t 30 || { echo "Kafka broker not ready. Aborting."; exit 1; }

# Run the end-to-end test suite
echo "Running E2E tests..."
./gradlew e2eTest

# Capture the exit code of the test run.
TEST_EXIT_CODE=$?

# Stop and remove the Docker containers and networks
echo "Tearing down Docker environment..."
docker-compose down

# Exit with the same code as the test run, so the CI/CD pipeline knows if the tests passed or failed.
if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "E2E tests passed successfully."
else
  echo "E2E tests failed."
fi

exit $TEST_EXIT_CODE
