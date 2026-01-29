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
