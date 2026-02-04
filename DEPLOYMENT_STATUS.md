# Umrah Trip Creator - AgentCore Deployment Status

## Current Status

### ✅ Completed
1. **Infrastructure Setup**
   - Memory resources created (STM and LTM)
   - Gateway created with Cognito authentication
   - IAM roles and S3 buckets configured
   - AgentCore CLI installed and working

2. **Configuration**
   - `.env` file updated with all credentials
   - Model configuration updated to use Claude 3.5 Sonnet v2 (available for on-demand use)
   - All agent runtime files created and simplified

3. **Agent Code**
   - All 5 agent runtime files created (orchestrator, flight, hotel, visa, itinerary)
   - Code tested locally and works correctly
   - Simplified to remove complex memory hooks

### ⚠️ Current Issues

**Runtime Deployment Error (HTTP 424)**
- Agents deploy successfully but fail when invoked
- Error code: `-32505` (Runtime client error)
- CloudWatch logs are empty, suggesting runtime isn't starting
- Local testing works perfectly

**Root Cause Analysis:**
The issue appears to be related to how the A2A protocol expects the code to be structured vs. how we're using BedrockAgentCoreApp. The documentation shows A2A servers should:
- Run on port 9000
- Use FastAPI with uvicorn
- Mount at root path `/`

Our current approach uses `BedrockAgentCoreApp` which may not be compatible with A2A protocol in direct_code_deploy mode.

## Working Configuration

### Models (Available for On-Demand Use)
```
ORCHESTRATOR_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
FLIGHT_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
HOTEL_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
VISA_AGENT_MODEL=anthropic.claude-3-5-haiku-20241022-v1:0
ITINERARY_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

### Memory IDs
```
MEMORY_STM_ID=UmrahTrip_STM_904e3a89-42bqoi6aBl
MEMORY_LTM_ID=UmrahTrip_LTM_22d963c0-n4uMLy61a6
```

### Gateway Configuration
```
GATEWAY_URL=https://umrahtrip-gateway-95c76ff1-zlwkpbuhif.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp
GATEWAY_ID=umrahtrip-gateway-95c76ff1-zlwkpbuhif
GATEWAY_ACCESS_TOKEN=eyJraWQiOiJUTGR5eFh6cU5SNUlueGJEa004bEdUVjBCRkVFRld5QUoyMW02cHlCNUprPSIsImFsZyI6IlJTMjU2In0...
```

## Next Steps to Resolve

### Option 1: Use HTTP Protocol Instead of A2A
The simplest solution is to switch from A2A to HTTP protocol:

1. Reconfigure agents with HTTP protocol:
```bash
cd agents/orchestrator
agentcore configure --entrypoint orchestrator_runtime.py --name umrah_orchestrator --deployment-type direct_code_deploy --runtime PYTHON_3_12 --requirements-file requirements.txt --protocol HTTP --non-interactive
```

2. Update runtime files to use HTTP entrypoint structure (port 8080, path `/invocations`)

### Option 2: Fix A2A Implementation
Follow the A2A documentation pattern:

1. Restructure runtime files to use FastAPI + uvicorn
2. Use A2AServer from strands to wrap agents
3. Run on port 9000 with root path mounting
4. Test locally first with `python orchestrator_runtime.py`

### Option 3: Use Container Deployment
Switch to container deployment which may handle A2A better:

1. Install Docker/Finch/Podman
2. Reconfigure with container deployment type
3. Let CodeBuild handle the container building

## Recommended Immediate Action

**Try Option 1 (HTTP Protocol)** as it's the simplest and most likely to work:

```bash
# For each agent directory
cd agents/orchestrator
agentcore destroy --agent umrah_orchestrator  # Answer 'y'
agentcore configure --entrypoint orchestrator_runtime.py --name umrah_orchestrator --deployment-type direct_code_deploy --runtime PYTHON_3_12 --requirements-file requirements.txt --protocol HTTP --non-interactive
agentcore deploy --agent umrah_orchestrator
```

Then test:
```bash
agentcore invoke '{"prompt": "Hello"}' --agent umrah_orchestrator
```

## Testing Commands

### Local Testing (Works)
```bash
source .venv/bin/activate
python3 test_orchestrator_local.py
```

### Check Agent Status
```bash
cd agents/orchestrator
source ../../.venv/bin/activate
agentcore status --agent umrah_orchestrator
```

### View Logs
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/umrah_orchestrator-<ID>-DEFAULT --since 5m --follow
```

### List Configured Agents
```bash
cd agents/orchestrator
agentcore configure list
```

## Resources Created

- **IAM Role**: AmazonBedrockAgentCoreSDKRuntime-us-west-2-f2c3ec8729
- **S3 Bucket**: bedrock-agentcore-codebuild-sources-985444479029-us-west-2
- **Memory (STM)**: umrah_orchestrator_mem-naHpFmCuVl
- **Memory (LTM)**: UmrahTrip_LTM_22d963c0-n4uMLy61a6
- **Gateway**: umrahtrip-gateway-95c76ff1-zlwkpbuhif
- **Cognito User Pool**: us-west-2_AAvuQJ0g6

## Files Modified

- `.env` - Updated with all credentials and correct models
- `agents/orchestrator/orchestrator_runtime.py` - Simplified runtime
- `agents/flight_agent/flight_runtime.py` - Created simplified version
- `agents/hotel_agent/hotel_runtime.py` - Created simplified version
- `agents/visa_agent/visa_runtime.py` - Created simplified version
- `agents/itinerary_agent/itinerary_runtime.py` - Created simplified version
- `test_orchestrator_local.py` - Local testing script (works!)

## Key Learnings

1. **Model Availability**: Claude 4.5 models require inference profiles and aren't available for on-demand use yet. Use Claude 3.5 models instead.

2. **Protocol Choice**: A2A protocol has specific requirements (port 9000, FastAPI structure). HTTP protocol may be simpler for initial deployment.

3. **Local Testing**: Always test agent code locally first before deploying to AgentCore.

4. **Logs**: CloudWatch logs can take time to appear. Empty logs suggest runtime isn't starting at all.

5. **IAM Permissions**: Auto-created execution roles have all necessary permissions for Bedrock model invocation.
