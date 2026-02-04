# Gateway Quickstart - Fix API Credentials Once and For All

## The Problem You're Facing

Every time you deploy agents, you need to pass API credentials:
```bash
agentcore deploy --env AMADEUS_API_KEY=xxx --env AMADEUS_API_SECRET=yyy
```

This is:
- ❌ Repetitive and annoying
- ❌ Error-prone
- ❌ Not scalable
- ❌ Security risk

## The Solution: AgentCore Gateway

**Store credentials in Gateway once, agents never need them again!**

```
Before: Agent → Amadeus API (needs credentials)
After:  Agent → Gateway → Amadeus API (Gateway has credentials)
```

## Quick Setup (5 Minutes)

### 1. Create the Gateway
```bash
python3 setup_amadeus_gateway.py
```

This creates:
- Gateway with OAuth authentication
- Amadeus API as MCP tools
- Credentials stored securely in Gateway
- Config saved to `amadeus_gateway_config.json`

### 2. Test It Works
```bash
python3 test_amadeus_gateway.py
```

Should show:
- ✓ 3 tools available (searchFlights, searchHotelsByCity, searchHotelsByLocation)
- ✓ Flight search working
- ✓ Hotel search working

### 3. Update Agents (Next Phase)

Agents will call Gateway tools instead of Amadeus API directly.

**Benefits:**
- No more `--env` flags needed
- Deploy with just: `agentcore deploy`
- Update credentials in Gateway only
- No agent redeployment needed

## What You Get

### Tools Available Through Gateway:

1. **searchFlights** - Real-time flight search
   - Parameters: origin, destination, dates, passengers, class
   - Returns: Real prices and availability

2. **searchHotelsByCity** - Find hotels in a city
   - Parameters: cityCode (MEC for Makkah, MED for Medina)
   - Returns: Hotel list with details

3. **searchHotelsByLocation** - Find hotels near coordinates
   - Parameters: latitude, longitude, radius
   - Returns: Hotels near Haram with distances

### Gateway Features:

- ✅ **Automatic OAuth** - Gateway handles token refresh
- ✅ **Secure Storage** - Credentials encrypted
- ✅ **Centralized** - One place to manage all APIs
- ✅ **Scalable** - Add more APIs easily
- ✅ **Monitored** - CloudWatch logs all calls
- ✅ **Production-Ready** - AWS managed service

## Updating Credentials

When you need to change API keys:

1. Update Gateway target (one command)
2. Done! No agent redeployment needed

```python
# Update credentials in Gateway
client.update_gateway_target(
    gatewayIdentifier=gateway_id,
    targetId=target_id,
    credentials={"clientId": "NEW_KEY", "clientSecret": "NEW_SECRET"}
)
```

## Adding More APIs

Want to add weather, currency, or other APIs?

1. Create OpenAPI spec
2. Add as Gateway target
3. Configure credentials
4. Agents automatically get new tools

No code changes in agents needed!

## Files Created

- `setup_amadeus_gateway.py` - Setup script
- `test_amadeus_gateway.py` - Test script
- `amadeus_gateway_config.json` - Configuration (auto-generated)
- `GATEWAY_SOLUTION.md` - Full documentation
- `GATEWAY_QUICKSTART.md` - This file

## Next Steps

1. ✅ **Run setup** - `python3 setup_amadeus_gateway.py`
2. ✅ **Test Gateway** - `python3 test_amadeus_gateway.py`
3. ⏳ **Update agents** - Modify to use Gateway tools (Phase 2)
4. ⏳ **Redeploy** - `agentcore deploy` (no --env needed!)
5. ⏳ **Test** - Verify end-to-end flow

## Why This is Better

| Aspect | Before (--env) | After (Gateway) |
|--------|---------------|-----------------|
| Deployment | `agentcore deploy --env KEY=x --env SECRET=y` | `agentcore deploy` |
| Update credentials | Redeploy all agents | Update Gateway only |
| Security | Credentials in multiple places | Centralized in Gateway |
| Scalability | Each agent needs credentials | Gateway handles all |
| Management | Manual per agent | Automated |
| Production-ready | ❌ Not recommended | ✅ AWS best practice |

## Support

- Full docs: `GATEWAY_SOLUTION.md`
- Troubleshooting: Check CloudWatch logs
- AWS docs: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html

## Summary

**The Gateway approach is the RIGHT way to handle API credentials in production.**

- One-time setup
- No more repetitive deployments
- Secure and scalable
- AWS managed service
- Industry best practice

Run `python3 setup_amadeus_gateway.py` now to get started!
