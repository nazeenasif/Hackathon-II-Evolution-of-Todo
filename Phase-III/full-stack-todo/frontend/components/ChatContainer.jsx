'use client';

import { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getReducedMotion } from '@/lib/animations';

const ChatContainer = ({ children, autoScroll = true, onScrollEnd = () => {} }) => {
  const containerRef = useRef(null);
  const isReducedMotion = getReducedMotion();

  useEffect(() => {
    if (autoScroll && containerRef.current) {
      const scrollContainer = containerRef.current;
      const shouldAnimate = !isReducedMotion;

      // Scroll to bottom with smooth animation if not reduced motion
      if (shouldAnimate) {
        scrollContainer.scrollTo({
          top: scrollContainer.scrollHeight,
          behavior: 'smooth'
        });
      } else {
        // Instant scroll if reduced motion
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [children, autoScroll, isReducedMotion]);

  const handleScroll = () => {
    if (containerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
      // Check if scrolled to bottom (within 10px tolerance)
      if (scrollTop + clientHeight >= scrollHeight - 10) {
        onScrollEnd();
      }
    }
  };

  return (
    <motion.div
      ref={containerRef}
      className="flex-1 overflow-y-auto p-4 bg-gray-50"
      onScroll={handleScroll}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.2 }}
    >
      {children}
    </motion.div>
  );
};

export default ChatContainer;