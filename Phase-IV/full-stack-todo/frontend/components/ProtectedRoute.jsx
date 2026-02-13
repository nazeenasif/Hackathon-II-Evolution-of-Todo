'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

// Note: Better Auth may not have a direct React hook like useSession
// For now, using localStorage to check for JWT token
export default function ProtectedRoute({ children }) {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    // Check if JWT token exists in localStorage
    const token = localStorage.getItem('jwt_token');
    const authStatus = !!token;

    setIsAuthenticated(authStatus);
    setChecked(true);

    if (!authStatus) {
      router.push('/signin');
    }
  }, [router]);

  if (!checked) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    ); // Redirect happens in useEffect
  }

  return children;
}