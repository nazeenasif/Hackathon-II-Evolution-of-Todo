import Link from 'next/link';
import Navbar from '@/components/Navbar';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 bg-background sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-16 mx-auto max-w-7xl px-4 sm:mt-20 sm:px-6 md:mt-24 lg:mt-28 lg:px-8 xl:mt-32">
              <div className="sm:text-center lg:text-left">
                <h1 className="text-4xl tracking-tight font-extrabold text-foreground sm:text-5xl md:text-6xl">
                  <span className="block xl:inline">Manage your tasks</span>{' '}
                  <span className="block text-primary xl:inline">efficiently</span>
                </h1>
                <p className="mt-3 text-base text-muted-foreground sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                  A powerful todo application with advanced features like priorities, tags, search, and filtering. Sign up to get started!
                </p>
                <div className="mt-8 sm:mt-10 sm:flex sm:justify-center lg:justify-start space-y-4 sm:space-y-0 sm:space-x-4">
                  <div className="rounded-lg shadow-sm">
                    <Link
                      href="/signup"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 transition-colors duration-200 md:py-4 md:text-lg md:px-10 shadow-sm hover:shadow-md"
                    >
                      Get started
                    </Link>
                  </div>
                  <div className="mt-3 sm:mt-0">
                    <Link
                      href="/signin"
                      className="w-full flex items-center justify-center px-8 py-3 border border-input text-base font-medium rounded-lg text-foreground bg-background hover:bg-accent transition-colors duration-200 md:py-4 md:text-lg md:px-10 shadow-sm hover:shadow-md"
                    >
                      Sign in
                    </Link>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </div>

        {/* Decorative background elements */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-secondary/5 -z-10"></div>
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-primary/5 to-transparent -z-10"></div>
      </div>
    </div>
  );
}