'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { pageTransition } from '@/lib/animations';
import SectionAnimator from '@/components/SectionAnimator';

export default function HomePageClient() {
  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageTransition}
      className="min-h-screen bg-background relative overflow-hidden flex items-center justify-center"
    >
      {/* Background decoration */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative overflow-hidden w-full">
        <div className="max-w-4xl mx-auto px-4">
          <div className="bg-background/80 backdrop-blur-sm rounded-2xl p-8 md:p-12 text-center">
            <main>
              <SectionAnimator>
                <div>
                  <motion.h1
                    className="text-4xl tracking-tight font-extrabold text-foreground sm:text-5xl md:text-6xl bg-gradient-to-r from-foreground to-primary bg-clip-text text-transparent"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    <span className="block xl:inline">Manage your tasks</span>{' '}
                    <span className="block text-transparent bg-gradient-to-r from-primary to-purple-600 bg-clip-text xl:inline">efficiently</span>
                  </motion.h1>
                  <motion.p
                    className="mt-6 text-base text-muted-foreground sm:text-lg md:text-xl max-w-2xl mx-auto"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                  >
                    A powerful todo application with advanced features like priorities, tags, search, and filtering. Sign up to get started!
                  </motion.p>
                  <motion.div
                    className="mt-10 flex flex-col sm:flex-row gap-4 justify-center items-center"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                  >
                    <div className="rounded-lg shadow-sm">
                      <Link
                        href="/signup"
                        className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-xl text-primary-foreground bg-gradient-to-r from-primary to-blue-600 hover:from-primary/90 hover:to-blue-700 transition-all duration-200 md:py-4 md:text-lg md:px-10 shadow-lg hover:shadow-xl hover:scale-105 active:scale-95"
                      >
                        <span className="flex items-center space-x-2">
                          <span>Get started</span>
                        </span>
                      </Link>
                    </div>
                    <div className="mt-3 sm:mt-0">
                      <Link
                        href="/signin"
                        className="w-full flex items-center justify-center px-8 py-3 border border-border text-base font-medium rounded-xl text-foreground bg-card hover:bg-accent transition-all duration-200 md:py-4 md:text-lg md:px-10 shadow-sm hover:shadow-md hover:scale-105 active:scale-95"
                      >
                        <span className="flex items-center space-x-2">
                          <span>Sign in</span>
                          <span>🔐</span>
                        </span>
                      </Link>
                    </div>
                  </motion.div>
                </div>
              </SectionAnimator>
            </main>
          </div>
        </div>
      </div>
    </motion.div>
  );
}