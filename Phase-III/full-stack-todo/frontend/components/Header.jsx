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
    <header className="bg-card border-b sticky top-0 z-10 backdrop-blur-sm bg-background/90 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-foreground flex items-center group">
              <span className="text-xl font-bold text-foreground">
                TodoApp
              </span>
            </Link>
          </div>
          <div className="flex items-center space-x-3">
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
              className="h-9 w-9 p-0 rounded-full hover:bg-accent transition-colors duration-200"
            >
              {theme === 'light' ? '🌙' : '☀️'}
            </Button>
            {user ? (
              <div className="flex items-center space-x-3">
                <div className="flex flex-col items-end">
                  <span className="text-sm font-medium text-foreground">
                    👋 Hi, {user.email.split('@')[0]}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    Ready to tackle your tasks!
                  </span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleSignOut}
                  className="hover:bg-destructive hover:text-destructive-foreground transition-colors duration-200"
                >
                  <span className="hidden sm:inline">Sign Out</span>
                  <span className="sm:hidden">Logout</span>
                </Button>
              </div>
            ) : (
              <div className="flex space-x-2">
                <Link href="/signin">
                  <Button variant="outline" size="sm">Sign In</Button>
                </Link>
                <Link href="/signup">
                  <Button size="sm">Get Started</Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}