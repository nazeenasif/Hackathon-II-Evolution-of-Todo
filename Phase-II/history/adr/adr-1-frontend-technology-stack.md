# ADR-1: Frontend Technology Stack Selection

## Title
Frontend Technology Stack: Next.js 16+ with App Router, Tailwind CSS, and Better Auth

## Status
Accepted

## Date
2026-01-11

## Context
We need to build a modern, responsive frontend for the multi-user todo application that integrates with our FastAPI backend. The frontend must support JWT-based authentication, provide advanced task management features (priorities, tags, search, filter, sort), and follow modern React best practices. We need to select technologies that will enable rapid development, maintainability, and scalability.

## Decision
We will use the following frontend technology stack:

- **Framework**: Next.js 16+ with App Router for server-side rendering, routing, and optimized performance
- **Styling**: Tailwind CSS for utility-first styling approach and responsive design
- **Authentication**: Better Auth for complete authentication solution with JWT support
- **API Client**: Axios for HTTP requests with JWT token interceptors
- **UI Components**: React with TypeScript for type safety and component architecture
- **Deployment**: Vercel platform for seamless Next.js deployment

## Alternatives Considered
1. **React + Vite + Traditional Routing**: More lightweight but lacks SSR and routing capabilities of Next.js App Router
2. **Remix + Tailwind**: Alternative framework with strong data loading patterns but smaller ecosystem than Next.js
3. **Next.js + Material UI**: Different styling approach but would add significant bundle size vs Tailwind's utility-first approach
4. **Custom Auth Solution**: Building authentication from scratch but would require more development time and security considerations
5. **NextAuth.js**: Alternative auth solution but Better Auth provides more integrated JWT support

## Consequences
### Positive
- Next.js App Router provides excellent performance with automatic code splitting and optimized loading
- Tailwind CSS enables rapid UI development with consistent design system
- Better Auth provides complete authentication solution reducing development time
- Strong TypeScript support throughout the stack
- Large community and ecosystem for all selected technologies
- Server-side rendering improves SEO and initial load performance
- Built-in API routes in Next.js simplify authentication endpoint creation

### Negative
- Learning curve for team members unfamiliar with Next.js App Router
- Bundle size considerations with full Next.js framework
- Vendor lock-in to Next.js patterns and Vercel deployment
- Additional complexity of managing both frontend and backend authentication

## References
- specs/003-frontend-integration/plan.md
- specs/003-frontend-integration/spec.md
- specs/003-frontend-integration/research.md