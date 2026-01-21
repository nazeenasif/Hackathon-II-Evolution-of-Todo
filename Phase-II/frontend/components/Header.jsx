'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Button from '@/components/ui/Button';
import { useTheme } from '@/components/ThemeProvider';

export default function Header() {
  const [user, setUser] = useState(null);
  const router = useRouter();
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    // Check if user is logged in by checking for JWT token
    const token = localStorage.getItem('jwt_token');
    if (token) {
      // In a real implementation, we would decode the JWT or make an API call to get user info
      // For now, we'll just set a mock user object
      try {
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        setUser({
          email: tokenPayload.email,
          id: tokenPayload.sub
        });
      } catch (e) {
        console.error('Error decoding token:', e);
      }
    }
  }, []);

  const handleSignOut = () => {
    // Remove JWT token from localStorage
    localStorage.removeItem('jwt_token');
    // Redirect to sign in page
    router.push('/signin');
  };

  return (
    <header className="bg-card border-b sticky top-0 z-10 backdrop-blur-sm bg-background/95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-foreground">
              Todo App
            </Link>
          </div>
          <div className="flex items-center space-x-3">
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
              className="h-9 w-9 p-0"
            >
              {theme === 'light' ? '🌙' : '☀️'}
            </Button>
            {user ? (
              <div className="flex items-center space-x-3">
                <span className="text-sm text-foreground hidden sm:block">
                  Welcome, {user.email.split('@')[0]}
                </span>
                <Button variant="outline" size="sm" onClick={handleSignOut}>
                  Sign Out
                </Button>
              </div>
            ) : (
              <div className="flex space-x-2">
                <Link href="/signin">
                  <Button variant="outline" size="sm">Sign In</Button>
                </Link>
                <Link href="/signup">
                  <Button size="sm">Sign Up</Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}