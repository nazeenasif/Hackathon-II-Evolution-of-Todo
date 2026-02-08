import { useState } from 'react';
import Header from '@/components/Header';

export default function ResponsiveLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-40 lg:hidden ${sidebarOpen ? '' : 'hidden'}`} onClick={() => setSidebarOpen(false)}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" />
      </div>

      {/* Static sidebar for desktop */}
      <div className="hidden lg:fixed lg:inset-y lg:left-0 lg:block lg:w-64 lg:overflow-y-auto">
        <div className="pt-5 pb-4">
          <div className="flex items-center px-4">
            <div className="text-xl font-bold text-gray-900">Todo App</div>
          </div>
          <nav className="mt-5 px-2 space-y-1">
            <a
              href="/dashboard"
              className="bg-blue-100 text-blue-900 group flex items-center px-2 py-2 text-base font-medium rounded-md"
            >
              Dashboard
            </a>
            <a
              href="/settings"
              className="text-gray-700 hover:bg-gray-50 group flex items-center px-2 py-2 text-base font-medium rounded-md"
            >
              Settings
            </a>
          </nav>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        <Header />
        <main className="py-6">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}