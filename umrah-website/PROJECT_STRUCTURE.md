# 📁 Project Structure

Complete overview of the Umrah Website project structure.

## 🌳 Directory Tree

```
umrah-website/
├── 📄 Configuration Files
│   ├── package.json              # Dependencies and scripts
│   ├── next.config.ts            # Next.js configuration
│   ├── tsconfig.json             # TypeScript configuration
│   ├── tailwind.config.ts        # Tailwind CSS configuration
│   ├── .gitignore                # Git ignore rules
│   └── .env.local                # Local environment variables (create this)
│
├── 📱 Application Code
│   ├── app/
│   │   ├── layout.tsx            # Root layout (header, footer)
│   │   ├── page.tsx              # Main page (multi-step wizard)
│   │   ├── globals.css           # Global styles
│   │   │
│   │   ├── api/                  # API Routes
│   │   │   └── generate-trip/
│   │   │       └── route.ts      # Trip generation endpoint
│   │   │
│   │   └── components/           # React components (future)
│   │       ├── TravelDatesForm.tsx
│   │       ├── TravelerForm.tsx
│   │       ├── HotelPreferences.tsx
│   │       └── TripResults.tsx
│   │
│   ├── lib/
│   │   ├── agentcore.ts          # AgentCore client
│   │   └── types.ts              # TypeScript types
│   │
│   └── public/                   # Static assets
│       ├── images/
│       └── icons/
│
├── 📚 Documentation
│   ├── README.md                 # Project overview
│   ├── DEPLOY_NOW.md             # Quick deployment guide ⭐
│   ├── DEPLOYMENT_CHECKLIST.md   # Deployment checklist
│   ├── TROUBLESHOOTING.md        # Troubleshooting guide
│   ├── PROJECT_STRUCTURE.md      # This file
│   └── deploy.sh                 # Deployment script
│
├── 🔧 Build Output (generated)
│   ├── .next/                    # Next.js build output
│   ├── node_modules/             # Dependencies
│   └── amplify/                  # Amplify configuration
│
└── 📝 Environment Files
    ├── .env.local                # Local development (create this)
    └── .env.example              # Example environment file
```

---

## 📄 Key Files Explained

### Configuration Files

#### `package.json`
```json
{
  "name": "umrah-website",
  "scripts": {
    "dev": "next dev",           // Local development
    "build": "next build",       // Production build
    "start": "next start",       // Production server
    "lint": "next lint"          // Code linting
  },
  "dependencies": {
    "@aws-sdk/client-bedrock-agent-runtime": "^3.700.0",
    "next": "15.1.3",
    "react": "^19.0.0",
    // ... more dependencies
  }
}
```

**Purpose**: Defines project dependencies and scripts

#### `next.config.ts`
```typescript
const nextConfig = {
  // Next.js configuration
  reactStrictMode: true,
  // ... more config
};
```

**Purpose**: Configures Next.js behavior

#### `tsconfig.json`
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]  // Allows @/lib/types imports
    }
  }
}
```

**Purpose**: TypeScript compiler settings

#### `tailwind.config.ts`
```typescript
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    // ... more paths
  ],
  theme: {
    extend: {
      // Custom colors, fonts, etc.
    }
  }
}
```

**Purpose**: Tailwind CSS customization

---

### Application Code

#### `app/layout.tsx`
```typescript
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

**Purpose**: Root layout wrapper for all pages

**Contains**:
- HTML structure
- Global providers
- Common layout elements

#### `app/page.tsx`
```typescript
export default function Home() {
  const [step, setStep] = useState(1);
  const [tripData, setTripData] = useState({});
  
  // Multi-step wizard logic
  // ...
  
  return (
    <div>
      {/* Step 1: Travel Dates */}
      {/* Step 2: Travelers */}
      {/* Step 3: Hotels */}
      {/* Step 4: Budget */}
      {/* Step 5: Review */}
      {/* Step 6: Results */}
    </div>
  );
}
```

**Purpose**: Main application page

**Contains**:
- Multi-step wizard
- Form handling
- Trip generation logic
- Results display

#### `app/globals.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --primary-green: #28a745;
  --primary-dark: #155724;
}

.btn-primary {
  @apply px-6 py-3 bg-green-700 text-white rounded-lg;
}
```

**Purpose**: Global styles and CSS variables

**Contains**:
- Tailwind imports
- Custom CSS classes
- Color variables
- Utility classes

#### `app/api/generate-trip/route.ts`
```typescript
export async function POST(request: NextRequest) {
  const body = await request.json();
  
  // Invoke orchestrator agent
  const aiResponse = await invokeOrchestrator(body);
  
  return NextResponse.json({
    success: true,
    data: { ai_response: aiResponse }
  });
}
```

**Purpose**: API endpoint for trip generation

**Handles**:
- POST requests from frontend
- Calls AgentCore orchestrator
- Returns AI-generated trip plan
- Error handling

#### `lib/agentcore.ts`
```typescript
export async function invokeOrchestrator(userData: any): Promise<string> {
  const client = new BedrockAgentRuntimeClient({
    region: process.env.AWS_REGION,
  });
  
  const command = new InvokeAgentCommand({
    agentId: process.env.ORCHESTRATOR_ARN,
    sessionId: crypto.randomUUID(),
    inputText: formatPromptForOrchestrator(userData),
  });
  
  const response = await client.send(command);
  // Parse streaming response
  // ...
  
  return fullResponse;
}
```

**Purpose**: AgentCore client library

**Handles**:
- AWS SDK initialization
- Agent invocation
- Streaming response parsing
- Prompt formatting

#### `lib/types.ts`
```typescript
export interface TripRequest {
  travel_dates: {
    departure_airport: string;
    departure: string;
    return: string;
    duration: number;
    arrival_city: string;
  };
  num_travelers: number;
  travelers: Traveler[];
  hotel_preferences: HotelPreferences;
  budget: Budget;
  flight_preferences: FlightPreferences;
  special_requirements: SpecialRequirements;
}

// ... more types
```

**Purpose**: TypeScript type definitions

**Contains**:
- Request/response types
- Data structures
- Type safety

---

## 🔄 Data Flow

```
User Input (Frontend)
    ↓
app/page.tsx (Collect data)
    ↓
POST /api/generate-trip
    ↓
app/api/generate-trip/route.ts
    ↓
lib/agentcore.ts (invokeOrchestrator)
    ↓
AWS Bedrock AgentCore
    ↓
Orchestrator Agent
    ↓ ↓ ↓ ↓ ↓
Flight  Hotel  Visa  Itinerary  (Sub-agents)
    ↓
Amadeus API Gateway
    ↓
Real flight/hotel data
    ↓
AI Response (streaming)
    ↓
Parse response
    ↓
Return to frontend
    ↓
Display results
```

---

## 🚀 Build Process

### Development Mode (`npm run dev`)
```
1. Start Next.js dev server
2. Hot reload on file changes
3. TypeScript compilation
4. Tailwind CSS processing
5. API routes available at /api/*
6. Server runs at http://localhost:3000
```

### Production Build (`npm run build`)
```
1. TypeScript compilation
2. Next.js optimization
3. Static page generation
4. API route bundling
5. CSS minification
6. Image optimization
7. Output to .next/ folder
```

### Amplify Deployment (`amplify publish`)
```
1. Run npm run build
2. Upload .next/ to S3
3. Configure CloudFront
4. Set up Lambda@Edge
5. Configure environment variables
6. Deploy to Amplify hosting
7. Generate URL
```

---

## 📦 Dependencies

### Production Dependencies

```json
{
  "@aws-sdk/client-bedrock-agent-runtime": "^3.700.0",  // AWS SDK
  "@emotion/react": "^11.13.5",                         // Material-UI
  "@emotion/styled": "^11.13.5",                        // Material-UI
  "@mui/icons-material": "^6.3.0",                      // Material-UI icons
  "@mui/material": "^6.3.0",                            // Material-UI components
  "aws-amplify": "^6.11.1",                             // Amplify SDK
  "next": "15.1.3",                                     // Next.js framework
  "react": "^19.0.0",                                   // React library
  "react-dom": "^19.0.0"                                // React DOM
}
```

### Development Dependencies

```json
{
  "@types/node": "^20",                    // Node.js types
  "@types/react": "^19",                   // React types
  "@types/react-dom": "^19",               // React DOM types
  "eslint": "^8",                          // Code linting
  "eslint-config-next": "15.1.3",          // Next.js ESLint config
  "typescript": "^5"                       // TypeScript compiler
}
```

---

## 🌐 Environment Variables

### Local Development (`.env.local`)
```bash
ORCHESTRATOR_ARN=arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo
AWS_REGION=us-west-2
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### Production (Amplify Console)
```bash
ORCHESTRATOR_ARN=arn:aws:bedrock-agentcore:us-west-2:985444479029:runtime/umrah_orchestrator-DFFg1bHZKo
AWS_REGION=us-west-2
```

**Note**: 
- Variables without `NEXT_PUBLIC_` prefix are server-side only
- Variables with `NEXT_PUBLIC_` prefix are exposed to browser
- Never put API keys in `NEXT_PUBLIC_` variables

---

## 🔧 Scripts

### `npm run dev`
- Starts development server
- Hot reload enabled
- Runs at http://localhost:3000
- Use for local development

### `npm run build`
- Creates production build
- Optimizes code
- Generates .next/ folder
- Use to test production build locally

### `npm run start`
- Starts production server
- Requires `npm run build` first
- Runs at http://localhost:3000
- Use to test production build

### `npm run lint`
- Runs ESLint
- Checks code quality
- Reports errors and warnings
- Use before committing code

---

## 📂 Folders to Ignore

### `.next/`
- Next.js build output
- Generated automatically
- Don't commit to git
- Recreated on each build

### `node_modules/`
- NPM dependencies
- Generated by `npm install`
- Don't commit to git
- Large folder (~200MB)

### `amplify/`
- Amplify configuration
- Generated by `amplify init`
- Some files committed, some ignored
- See `.gitignore` for details

---

## 🎨 Styling Approach

### Tailwind CSS (Utility-First)
```tsx
<button className="px-6 py-3 bg-green-700 text-white rounded-lg hover:bg-green-800">
  Click Me
</button>
```

### Custom CSS Classes
```css
/* globals.css */
.btn-primary {
  @apply px-6 py-3 bg-green-700 text-white rounded-lg;
}
```

### Material-UI Components (Future)
```tsx
import { Button, Card, TextField } from '@mui/material';

<Button variant="contained" color="primary">
  Click Me
</Button>
```

---

## 🔐 Security Considerations

### Environment Variables
- ✅ Server-side variables (ORCHESTRATOR_ARN)
- ✅ Not exposed to browser
- ✅ Set in Amplify Console
- ❌ Never in frontend code

### API Keys
- ✅ Stored in Gateway
- ✅ Not in environment variables
- ✅ Not in code
- ✅ Secured by AWS IAM

### Authentication (Future)
- 🔄 AWS Cognito
- 🔄 User pools
- 🔄 JWT tokens
- 🔄 Protected routes

---

## 📊 Performance Optimizations

### Next.js Features
- ✅ Server-side rendering (SSR)
- ✅ Static site generation (SSG)
- ✅ Automatic code splitting
- ✅ Image optimization
- ✅ Font optimization

### Amplify Features
- ✅ CloudFront CDN
- ✅ Edge caching
- ✅ Gzip compression
- ✅ HTTP/2 support
- ✅ Global distribution

---

## 🧪 Testing Strategy

### Local Testing
```bash
# Development mode
npm run dev

# Production build
npm run build
npm run start

# Linting
npm run lint
```

### Amplify Testing
```bash
# Deploy to staging
amplify publish --environment staging

# Test staging URL
# If good, deploy to production
amplify publish --environment prod
```

---

## 📈 Monitoring

### Amplify Console
- Build logs
- Deployment history
- Performance metrics
- Error tracking

### CloudWatch
- Lambda logs
- API Gateway logs
- Custom metrics
- Alarms

### X-Ray (Optional)
- Request tracing
- Performance analysis
- Bottleneck identification

---

## 🔄 CI/CD Pipeline

### GitHub Integration
```
1. Push code to GitHub
2. Amplify detects push
3. Triggers build
4. Runs npm run build
5. Deploys to hosting
6. Updates URL
7. Sends notification
```

### Manual Deployment
```bash
# Make changes
git add .
git commit -m "Update feature"

# Deploy
amplify publish
```

---

## 🎯 Next Steps

### Immediate
1. Deploy to Amplify
2. Test website
3. Configure custom domain

### Short-term
1. Add full form components
2. Add authentication
3. Add payment integration
4. Add email notifications

### Long-term
1. User dashboard
2. Booking history
3. Reviews and ratings
4. Multi-language support
5. Mobile app

---

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [AWS Amplify Documentation](https://docs.amplify.aws/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Material-UI Documentation](https://mui.com/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

---

**Ready to deploy?** Check `DEPLOY_NOW.md` for quick start guide!
