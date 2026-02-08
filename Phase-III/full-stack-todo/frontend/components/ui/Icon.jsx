'use client';

import { motion } from 'framer-motion';
import { getReducedMotion } from '@/lib/animations';

const Icon = ({
  icon: IconComponent,
  size = 24,
  className = "",
  animateOnHover = true,
  onClick,
  ...props
}) => {
  // Check if reduced motion is enabled
  const isReducedMotion = getReducedMotion();

  // Base classes for the icon container
  const baseClasses = `inline-flex items-center justify-center ${className}`;

  // If reduced motion is enabled, use normal div without motion
  if (isReducedMotion || !animateOnHover) {
    return (
      <div
        className={baseClasses}
        onClick={onClick}
        style={{ width: size, height: size }}
        {...props}
      >
        <IconComponent size={size} />
      </div>
    );
  }

  return (
    <motion.div
      className={baseClasses}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      onClick={onClick}
      style={{ width: size, height: size }}
      {...props}
    >
      <IconComponent size={size} />
    </motion.div>
  );
};

export default Icon;