'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Input from '@/components/ui/Input';

export default function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSignIn = async (e) => {
    e.preventDefault();

    try {
      // In a real implementation, this would call the Better Auth API
      // For now, we'll simulate a successful login and store a mock token
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        // Store the JWT token in localStorage
        localStorage.setItem('jwt_token', data.access_token);
        router.push('/dashboard');
      } else {
        const errorData = await response.json();

        // Safely handle different types of error responses
        let errorMessage = 'Invalid credentials';

        if (errorData.detail) {
          if (Array.isArray(errorData.detail)) {
            // If detail is an array of error objects, extract messages
            errorMessage = errorData.detail.map(err => err.msg || JSON.stringify(err)).join('; ');
          } else if (typeof errorData.detail === 'string') {
            // If detail is a string, use it directly
            errorMessage = errorData.detail;
          } else {
            // For other types, convert to string safely
            errorMessage = JSON.stringify(errorData.detail);
          }
        } else if (errorData.message) {
          // If there's a message property, use it
          errorMessage = errorData.message;
        }

        setError(errorMessage);
      }
    } catch (err) {
      setError('An error occurred during sign in');
      console.error('Sign in error:', err);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h2 className="mt-6 text-3xl font-bold text-foreground">
              Welcome back
            </h2>
            <p className="mt-2 text-muted-foreground">
              Sign in to your account to continue
            </p>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleSignIn}>
            {error && (
              <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded-lg" role="alert">
                <span className="block sm:inline">{error}</span>
              </div>
            )}
            <input type="hidden" name="remember" value="true" />
            <div className="space-y-4">
              <div>
                <label htmlFor="email-address" className="block text-sm font-medium text-foreground mb-2">
                  Email address
                </label>
                <Input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full"
                  placeholder="Enter your email"
                />
              </div>
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
                  Password
                </label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full"
                  placeholder="Enter your password"
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="text-sm">
                <Link href="/signup" className="font-medium text-primary hover:text-primary/80 transition-colors">
                  Don't have an account? Sign up
                </Link>
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors duration-200 shadow-sm hover:shadow-md"
              >
                Sign in
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}