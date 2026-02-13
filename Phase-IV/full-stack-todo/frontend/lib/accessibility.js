// Accessibility utilities for animation support

// Check if reduced motion is enabled
export const isReducedMotionEnabled = () => {
  if (typeof window !== 'undefined' && window.matchMedia) {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
  return false;
};

// Hook to subscribe to reduced motion changes
export const watchReducedMotion = (callback) => {
  if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
    return () => {};
  }

  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

  const handleChange = () => callback(mediaQuery.matches);

  mediaQuery.addEventListener('change', handleChange);

  return () => mediaQuery.removeEventListener('change', handleChange);
};

// Get appropriate animation props based on user preferences
export const getAccessibleAnimationProps = (animationProps, reducedMotionProps = {}) => {
  const isReduced = isReducedMotionEnabled();

  if (isReduced) {
    return {
      ...animationProps,
      // Override animation properties for reduced motion
      transition: {
        ...animationProps.transition,
        duration: reducedMotionProps.duration || 0.01,
      },
      // Simplify animations to reduce motion
      ...(reducedMotionProps.transforms || {})
    };
  }

  return animationProps;
};

// Apply reduced motion to framer-motion components
export const applyReducedMotion = (variants) => {
  const isReduced = isReducedMotionEnabled();

  if (isReduced) {
    // Return simplified variants with minimal animation
    const reducedVariants = {};
    Object.keys(variants).forEach(key => {
      reducedVariants[key] = {
        ...variants[key],
        transition: {
          duration: 0.01,
          ...variants[key].transition
        }
      };
    });
    return reducedVariants;
  }

  return variants;
};

// Get animation duration based on user preferences
export const getAnimationDuration = (normalDuration = 0.3, reducedDuration = 0.01) => {
  return isReducedMotionEnabled() ? reducedDuration : normalDuration;
};

// Utility to create animation variants that respect reduced motion
export const createAccessibleVariants = (varientsCreator) => {
  const isReduced = isReducedMotionEnabled();

  if (isReduced) {
    // Return variants with minimal animation for reduced motion
    return {
      hidden: { opacity: 0 },
      visible: { opacity: 1, transition: { duration: 0.01 } }
    };
  }

  // Return normal variants
  return varientsCreator();
};