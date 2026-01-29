'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Input from '@/components/ui/Input';

export default function SignUpPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState([]); // store errors as array of strings
  const router = useRouter();

  const handleSignUp = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/run/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('jwt_token', data.access_token);
        router.push('/signin');
      } else {
        const data = await response.json();
        let errorsArray = [];

        if (data.detail) {
           if (Array.isArray(data.detail)) {
            // Convert each object to a readable string
            errorsArray = data.detail.map(err => {
              if (typeof err === 'string') return err;       // Already a string
              if (err.msg) {                                 // Validation object
                const field = Array.isArray(err.loc) ? err.loc.join('.') : 'field';
                return `${field}: ${err.msg}`;
              }
              return JSON.stringify(err);                    // Fallback
            });
          } else if (typeof data.detail === 'string') {
            errorsArray = [data.detail];
          } else {
            errorsArray = [JSON.stringify(data.detail)];
          }
        }


        setError(errorsArray); // always set an array of strings
      }
    } catch (err) {
      setError(['An error occurred during sign up']);
      console.error('Sign up error:', err);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h2 className="mt-6 text-3xl font-bold text-foreground">
              Create your account
            </h2>
            <p className="mt-2 text-muted-foreground">
              Join us to get started with your tasks
            </p>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleSignUp}>
            {error.length > 0 && (
              <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded-lg" role="alert">
                <ul className="list-disc pl-5 space-y-1">
                  {error.map((errMsg, index) => (
                    <li key={index}>{errMsg}</li>
                  ))}
                </ul>
              </div>
            )}
            <input type="hidden" name="remember" value="true" />
            <div className="space-y-4">
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-foreground mb-2">
                  Username
                </label>
                <Input
                  id="username"
                  name="username"
                  type="text"
                  autoComplete="username"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full"
                  placeholder="Choose a username"
                />
              </div>
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
                  placeholder="Create a password"
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="text-sm">
                <Link href="/signin" className="font-medium text-primary hover:text-primary/80 transition-colors">
                  Already have an account? Sign in
                </Link>
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors duration-200 shadow-sm hover:shadow-md"
              >
                Sign up
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
