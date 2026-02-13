'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FaBars, FaTimes } from 'react-icons/fa';
import { useTheme } from '@/components/ThemeProvider';
import { motion } from 'framer-motion';
import { getReducedMotion } from '@/lib/animations';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();
  const { theme, toggleTheme } = useTheme();

  // Check if reduced motion is enabled
  const isReducedMotion = getReducedMotion();

  const isActive = (path) => pathname === path;

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/signin', label: 'Sign In' },
    { href: '/signup', label: 'Sign Up' },
  ];

  // Close mobile menu when route changes
  useEffect(() => {
    setIsOpen(false);
  }, [pathname]);

  return (
    <motion.nav
      className="sticky top-0 z-50 bg-card border-b border-border shadow-sm backdrop-blur-sm bg-opacity-90"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: isReducedMotion ? 0.01 : 0.3 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <motion.span
                className="text-xl font-bold text-foreground"
                whileHover={isReducedMotion ? {} : { scale: 1.05 }}
                transition={{ type: "spring", stiffness: 400, damping: 17 }}
              >
                TodoApp
              </motion.span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  isActive(link.href)
                    ? 'text-primary bg-primary/10'
                    : 'text-foreground/80 hover:text-foreground hover:bg-accent'
                }`}
              >
                <motion.div
                  whileHover={isReducedMotion ? {} : { y: -2 }}
                  whileTap={isReducedMotion ? {} : { scale: 0.95 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                >
                  {link.label}
                </motion.div>
              </Link>
            ))}

            {/* Theme Toggle */}
            <motion.button
              onClick={toggleTheme}
              className="p-2 rounded-md text-foreground/80 hover:text-foreground hover:bg-accent transition-colors duration-200"
              aria-label="Toggle theme"
              whileHover={isReducedMotion ? {} : { y: -2, scale: 1.05 }}
              whileTap={isReducedMotion ? {} : { scale: 0.9 }}
              transition={{ type: "spring", stiffness: 400, damping: 17 }}
            >
              {theme === 'dark' ? '☀' : '🌙'}
            </motion.button>
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <motion.button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-foreground/80 hover:text-foreground hover:bg-accent focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary transition-colors duration-200"
              aria-expanded="false"
              whileHover={isReducedMotion ? {} : { scale: 1.1 }}
              whileTap={isReducedMotion ? {} : { scale: 0.9 }}
              transition={{ type: "spring", stiffness: 400, damping: 17 }}
            >
              <span className="sr-only">Open main menu</span>
              {isOpen ? <FaTimes className="h-6 w-6" /> : <FaBars className="h-6 w-6" />}
            </motion.button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          transition={{ duration: isReducedMotion ? 0.01 : 0.2 }}
        >
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-card border-t border-border">
            {navLinks.map((link) => (
              <motion.div
                key={link.href}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: isReducedMotion ? 0.01 : 0.2, delay: 0.1 }}
              >
                <Link
                  href={link.href}
                  className={`block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 ${
                    isActive(link.href)
                      ? 'text-primary bg-primary/10'
                      : 'text-foreground/80 hover:text-foreground hover:bg-accent'
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  {link.label}
                </Link>
              </motion.div>
            ))}

            {/* Mobile Theme Toggle */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: isReducedMotion ? 0.01 : 0.2, delay: 0.15 }}
            >
              <button
                onClick={toggleTheme}
                className="w-full text-left px-3 py-2 rounded-md text-base font-medium text-foreground/80 hover:text-foreground hover:bg-accent transition-colors duration-200"
              >
                {theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
              </button>
            </motion.div>
          </div>
        </motion.div>
      )}
    </motion.nav>
  );
}