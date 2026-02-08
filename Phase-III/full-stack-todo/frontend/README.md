# Todo Frontend Application

A modern, responsive frontend for the multi-user todo application built with Next.js, Tailwind CSS, and integrated with a FastAPI backend.

## Features

- User authentication with JWT tokens
- Task management (CRUD operations)
- Advanced features: priorities, tags, search, filter, sort
- Responsive design for desktop, tablet, and mobile
- Clean, modern UI with Tailwind CSS

## Tech Stack

- Next.js 16+ with App Router
- React 18
- Tailwind CSS
- TypeScript
- Axios for API calls
- Better Auth for authentication

## Prerequisites

- Node.js 18+
- npm or yarn

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment Variables**
   Create a `.env.local` file in the root directory with the following:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Visit [http://localhost:3000](http://localhost:3000) to see the application.

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: The base URL for the backend API (default: http://localhost:8000)
- `NEXT_PUBLIC_BETTER_AUTH_URL`: The URL for Better Auth (default: http://localhost:3000)

## Available Scripts

- `npm run dev`: Starts the development server
- `npm run build`: Builds the application for production
- `npm run start`: Starts the production server
- `npm run lint`: Runs ESLint to check for code issues

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── api/             # API routes
│   ├── signin/          # Sign in page
│   ├── signup/          # Sign up page
│   ├── dashboard/       # Dashboard page
│   └── layout.jsx       # Root layout
├── components/          # Reusable React components
│   ├── ui/              # Basic UI components
│   └── ProtectedRoute.jsx # Authentication wrapper
├── lib/                 # Utility functions
│   ├── auth.js          # Better Auth configuration
│   └── api.js           # API client with interceptors
├── services/            # API service functions
│   └── taskService.js   # Task-related API calls
├── types/               # TypeScript type definitions
│   └── taskTypes.ts     # Task-related types
└── public/              # Static assets
```

## API Integration

The frontend communicates with the backend API using axios with JWT token interceptors. All authenticated requests automatically include the JWT token in the Authorization header.

## Authentication

Authentication is handled using JWT tokens stored in localStorage. The Better Auth library provides the authentication flow.

## Development

The application follows a component-based architecture with clear separation of concerns. New features should be added following the existing patterns:

- Components in the `components/` directory
- API calls through the service layer in `services/`
- Type definitions in `types/`
- Utility functions in `lib/`

## Animation Guidelines

The application includes rich animations and micro-interactions to enhance the user experience. When adding new UI elements:

### Animation Principles

1. **Subtlety**: Animations should be subtle and not distract from the core functionality
2. **Performance**: All animations should maintain 60fps performance
3. **Accessibility**: All animations respect user's reduced motion preferences
4. **Consistency**: Use consistent animation durations and easing functions

### Animation Durations

- **Fast animations**: 150ms (0.15s) - for quick feedback like button taps
- **Normal animations**: 250ms (0.25s) - for most UI transitions
- **Slow animations**: 300ms (0.3s) - for page transitions and major state changes

### Animation Components

#### Framer Motion Usage

All animations use Framer Motion. When implementing new animations:

```jsx
import { motion } from 'framer-motion';
import { getReducedMotion } from '@/lib/animations';

// Check for reduced motion preference
const isReducedMotion = getReducedMotion();

// Apply conditional animations
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3 }}
>
  Content
</motion.div>
```

#### Animation Utilities

The `@/lib/animations.js` file contains common animation presets and utilities:

- `fadeInVariant` - Fade in animation
- `fadeUpVariant` - Fade up animation
- `staggerContainer` - Staggered child animations
- `ANIMATION_PRESETS` - Duration and easing presets
- `getReducedMotion()` - Check user's reduced motion preference

#### Accessibility

- Always check `getReducedMotion()` before applying animations
- Use shorter durations (0.01s) when reduced motion is enabled
- Maintain semantic HTML structure for screen readers
- Ensure all interactive elements have proper focus states
