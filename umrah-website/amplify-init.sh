#!/bin/bash

# Add Node to PATH
export PATH="/opt/homebrew/opt/node@20/bin:$PATH"

# Initialize Amplify with default settings
amplify init \
  --amplify '{"projectName":"umrahwebsite","envName":"prod","defaultEditor":"code"}' \
  --frontend '{"frontend":"javascript","framework":"react","config":{"SourceDir":"","DistributionDir":".next","BuildCommand":"npm run build","StartCommand":"npm run start"}}' \
  --providers '{"awscloudformation":{"configLevel":"project","useProfile":true,"profileName":"default"}}' \
  --yes
