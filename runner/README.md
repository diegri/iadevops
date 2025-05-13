# Environment Parameters
    REPO=<owner>/<repo>
    REG_TOKEN=<reg-token-for-self-hosted-runner>
    NAME=<runner-name>

# Build docker
    docker image build -t localrunner .

# Run docker
    docker run -d -t -i -e REPO='<owner>/<repo>' -e REG_TOKEN='<reg-token-for-self-hosted-runner>' -e NAME='<runner-name>' localrunner 

