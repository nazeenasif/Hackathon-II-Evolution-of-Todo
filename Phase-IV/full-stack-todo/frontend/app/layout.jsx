import './globals.css';
import { Inter } from 'next/font/google';
import GlobalErrorBoundary from '@/components/GlobalErrorBoundary';
import { ThemeProvider } from '@/components/ThemeProvider';
import LayoutWithAnimations from '@/components/LayoutWithAnimations';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Todo App',
  description: 'A multi-user todo application with advanced features',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ThemeProvider>
          <GlobalErrorBoundary>
            <LayoutWithAnimations>
              {children}
            </LayoutWithAnimations>
          </GlobalErrorBoundary>
        </ThemeProvider>
      </body>
    </html>
  );
}