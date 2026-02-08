'use client';

import { motion } from 'framer-motion';
import { getReducedMotion } from '@/lib/animations';

const AnimatedWrapper = ({
  children,
  type = 'div',
  animation = 'fadeIn',
  delay = 0,
  duration = 0.3,
  className = '',
  ...props
}) => {
  const isReducedMotion = getReducedMotion();

  // Define animation variants
  const variants = {
    fadeIn: {
      hidden: { opacity: 0 },
      visible: { opacity: 1, transition: { delay, duration: isReducedMotion ? 0.01 : duration } }
    },
    fadeUp: {
      hidden: { opacity: 0, y: 20 },
      visible: { opacity: 1, y: 0, transition: { delay, duration: isReducedMotion ? 0.01 : duration } }
    },
    scaleIn: {
      hidden: { opacity: 0, scale: 0.95 },
      visible: { opacity: 1, scale: 1, transition: { delay, duration: isReducedMotion ? 0.01 : duration } }
    },
    slideInLeft: {
      hidden: { opacity: 0, x: -20 },
      visible: { opacity: 1, x: 0, transition: { delay, duration: isReducedMotion ? 0.01 : duration } }
    },
    slideInRight: {
      hidden: { opacity: 0, x: 20 },
      visible: { opacity: 1, x: 0, transition: { delay, duration: isReducedMotion ? 0.01 : duration } }
    }
  };

  const animationProps = {
    initial: 'hidden',
    animate: 'visible',
    variants: variants[animation],
    className,
    ...props
  };

  // If reduced motion is enabled, don't use motion component
  if (isReducedMotion) {
    return (
      <div className={className} {...props}>
        {children}
      </div>
    );
  }

  const MotionComponent = motion[type];

  return (
    <MotionComponent {...animationProps}>
      {children}
    </MotionComponent>
  );
};

export default AnimatedWrapper;