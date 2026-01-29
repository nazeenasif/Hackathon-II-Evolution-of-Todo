import './globals.css';
import { Inter } from 'next/font/google';
import GlobalErrorBoundary from '@/components/GlobalErrorBoundary';
import { ThemeProvider } from '@/components/ThemeProvider';

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
            {children}
          </GlobalErrorBoundary>
        </ThemeProvider>
      </body>
    </html>
  );
}