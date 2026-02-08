'use client';

import { motion } from 'framer-motion';
import { getReducedMotion } from '@/lib/animations';

export default function LoadingSkeleton({ rows = 3, type = 'default' }) {
  const isReducedMotion = getReducedMotion();

  // Different skeleton types for various UI elements
  const skeletons = {
    default: () => (
      <div className="h-16 bg-secondary rounded-lg"></div>
    ),
    card: () => (
      <div className="p-4 bg-card rounded-xl border shadow-sm">
        <div className="h-4 bg-secondary rounded w-3/4 mb-2"></div>
        <div className="h-3 bg-secondary rounded w-1/2 mb-3"></div>
        <div className="flex space-x-2">
          <div className="h-5 w-16 bg-secondary rounded-full"></div>
          <div className="h-5 w-20 bg-secondary rounded-full"></div>
        </div>
      </div>
    ),
    task: () => (
      <div className="p-4 bg-card rounded-lg border">
        <div className="flex items-center space-x-3">
          <div className="h-5 w-5 rounded-full border border-border"></div>
          <div className="flex-1">
            <div className="h-4 bg-secondary rounded w-3/4"></div>
          </div>
        </div>
      </div>
    )
  };

  const SkeletonType = skeletons[type] || skeletons.default;

  return (
    <div className="space-y-4">
      {Array.from({ length: rows }).map((_, index) => (
        <motion.div
          key={index}
          className="overflow-hidden"
          initial={isReducedMotion ? { opacity: 1 } : { opacity: 0 }}
          animate={isReducedMotion ? { opacity: 1 } : { opacity: 1 }}
          transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3, delay: index * 0.1 }}
        >
          <motion.div
            className="animate-pulse"
            animate={isReducedMotion ? {} : {
              backgroundColor: ['#f9fafb', '#e5e7eb', '#f9fafb'],
            }}
            transition={isReducedMotion ? {} : {
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut",
              delay: index * 0.2
            }}
          >
            <SkeletonType />
          </motion.div>
        </motion.div>
      ))}
    </div>
  );
}