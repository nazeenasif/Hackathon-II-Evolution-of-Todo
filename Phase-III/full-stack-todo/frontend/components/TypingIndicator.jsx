'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { getReducedMotion } from '@/lib/animations';

const TypingIndicator = ({ isVisible = true }) => {
  const isReducedMotion = getReducedMotion();

  if (!isVisible) return null;

  return (
    <motion.div
      className="flex justify-start"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.2 }}
    >
      <div className="bg-secondary text-secondary-foreground px-4 py-3 rounded-xl max-w-xs flex items-center space-x-2">
        <motion.div
          className="w-2 h-2 bg-foreground rounded-full"
          animate={isReducedMotion ? {} : { scale: [1, 1.2, 1] }}
          transition={{
            duration: 1.4,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 0
          }}
        />
        <motion.div
          className="w-2 h-2 bg-foreground rounded-full"
          animate={isReducedMotion ? {} : { scale: [1, 1.2, 1] }}
          transition={{
            duration: 1.4,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 0.2
          }}
        />
        <motion.div
          className="w-2 h-2 bg-foreground rounded-full"
          animate={isReducedMotion ? {} : { scale: [1, 1.2, 1] }}
          transition={{
            duration: 1.4,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 0.4
          }}
        />
      </div>
    </motion.div>
  );
};

export default TypingIndicator;