// Animation presets and utilities for the UI/UX enhancements

// Common animation variants
export const fadeInVariant = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } }
};

export const fadeUpVariant = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3 } }
};

export const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

export const slideInRight = {
  hidden: { x: 50, opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { duration: 0.3 } }
};

export const slideInLeft = {
  hidden: { x: -50, opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { duration: 0.3 } }
};

export const scaleIn = {
  hidden: { scale: 0.8, opacity: 0 },
  visible: { scale: 1, opacity: 1, transition: { duration: 0.2 } }
};

export const scaleHover = {
  hover: { scale: 1.03, transition: { duration: 0.2 } }
};

export const bounceEffect = {
  tap: { scale: 0.95 }
};

export const slideInUp = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.3 } }
};

export const slideOutDown = {
  exit: { y: -20, opacity: 0, transition: { duration: 0.2 } }
};

// Page transition variants
export const pageTransition = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.3 } },
  exit: { opacity: 0, y: -10, transition: { duration: 0.2 } }
};

// Message animation variants
export const messageVariants = {
  user: {
    hidden: { opacity: 0, x: 50 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.3 } }
  },
  ai: {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.3 } }
  }
};

// Animation configuration presets
export const ANIMATION_PRESETS = {
  duration: {
    fast: 0.15,      // 150ms
    normal: 0.25,    // 250ms
    slow: 0.3        // 300ms
  },
  easing: {
    easeIn: [0.25, 0.1, 0.25, 1],
    easeOut: [0.215, 0.61, 0.355, 1],
    easeInOut: [0.455, 0.03, 0.515, 0.955]
  },
  spring: {
    stiffness: 300,
    damping: 20
  }
};

// Utility functions
export const getReducedMotion = () => {
  if (typeof window !== 'undefined') {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
  return false;
};

// Animation presets based on reduced motion preference
export const getAnimationProps = (defaultProps = {}) => {
  if (getReducedMotion()) {
    return { duration: 0.01, ...defaultProps };
  }
  return defaultProps;
};