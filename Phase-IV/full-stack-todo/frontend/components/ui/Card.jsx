'use client';

import { motion } from 'framer-motion';
import { getReducedMotion } from '@/lib/animations';

const Card = ({
  children,
  className = "",
  hoverable = false,
  clickable = false,
  onClick,
  ...props
}) => {
  // Check if reduced motion is enabled
  const isReducedMotion = getReducedMotion();

  // Base classes for the card
  const baseClasses = `rounded-xl border bg-card text-card-foreground shadow-sm ${className}`;

  // If reduced motion is enabled or hoverable is false, use normal div without motion
  if (isReducedMotion || !hoverable) {
    return (
      <div
        className={baseClasses}
        onClick={clickable ? onClick : undefined}
        style={clickable ? { cursor: 'pointer' } : {}}
        {...props}
      >
        {children}
      </div>
    );
  }

  return (
    <motion.div
      className={baseClasses}
      whileHover={hoverable ? { y: -5, boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)" } : {}}
      whileTap={clickable ? { scale: 0.98 } : {}}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 25,
        duration: clickable ? 0.2 : 0.3
      }}
      onClick={clickable ? onClick : undefined}
      {...props}
    >
      {children}
    </motion.div>
  );
};

const CardHeader = ({ children, className = "", ...props }) => {
  const classes = `p-6 ${className}`;
  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

const CardTitle = ({ children, className = "", ...props }) => {
  const classes = `text-2xl font-semibold leading-none tracking-tight ${className}`;
  return (
    <h3 className={classes} {...props}>
      {children}
    </h3>
  );
};

const CardDescription = ({ children, className = "", ...props }) => {
  const classes = `text-sm text-muted-foreground ${className}`;
  return (
    <p className={classes} {...props}>
      {children}
    </p>
  );
};

const CardContent = ({ children, className = "", ...props }) => {
  const classes = `p-6 pt-0 ${className}`;
  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

const CardFooter = ({ children, className = "", ...props }) => {
  const classes = `flex items-center p-6 pt-0 ${className}`;
  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

export {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter
};