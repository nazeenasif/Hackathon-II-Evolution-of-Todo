'use client';

import { motion } from 'framer-motion';
import { pageTransition } from '@/lib/animations';

export default function LayoutWithAnimations({ children }) {
  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageTransition}
    >
      {children}
    </motion.div>
  );
}