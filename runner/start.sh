#!/bin/bash

echo "REPO=${REPO}"
echo "RUNNER_NAME=${RUNNER_NAME}"
#echo "RUNNER_TOKEN=${RUNNER_TOKEN}"

if [ -z "${REPO}" -o -z "${RUNNER_NAME}" -o -z "${RUNNER_TOKEN}"  ]; then
  echo "REPO, RUNNER_NAME or RUNNER_TOKEN is not set. Exiting."
  exit 1
fi

echo "Config GitHub Actions..."
cd /home/docker/actions-runner || exit
./config.sh --url https://github.com/${REPO} --token ${RUNNER_TOKEN} --name ${RUNNER_NAME} --runnergroup Default --unattended --replace --work _work --labels docker,linux,x64

cleanup() {
  echo "Removing runner..."
  ./config.sh remove --unattended --token ${RUNNER_TOKEN}
}

trap 'cleanup; exit 130' INT
# trap 'cleanup; exit 143' TERM

echo "Starting GitHub Actions runner..."
./run.sh & wait $!