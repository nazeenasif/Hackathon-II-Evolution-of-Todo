'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { getReducedMotion } from '@/lib/animations';

const Button = ({ children, onClick, variant = 'primary', size = 'md', className = '', disabled = false, ...props }) => {
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none shadow-sm hover:shadow-md';

  const variantsClasses = {
    primary: 'bg-primary hover:bg-primary/90 text-primary-foreground shadow-sm hover:shadow-md transition-all duration-200',
    secondary: 'bg-secondary hover:bg-secondary/80 text-secondary-foreground border border-border hover:border-border/70 shadow-sm hover:shadow-sm transition-all duration-200',
    outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground shadow-sm hover:shadow-sm transition-all duration-200',
    ghost: 'hover:bg-accent hover:text-accent-foreground transition-all duration-200',
    link: 'underline-offset-4 hover:underline text-primary transition-all duration-200',
    destructive: 'bg-destructive hover:bg-destructive/90 text-destructive-foreground shadow-sm hover:shadow-md transition-all duration-200',
  };

  const sizes = {
    sm: 'h-9 px-3 text-sm',
    md: 'h-10 px-4 py-2',
    lg: 'h-11 px-8 text-base',
    xl: 'h-12 px-6 text-lg',
  };

  const buttonClasses = `${baseClasses} ${variantsClasses[variant]} ${sizes[size]} ${className} ${disabled ? 'opacity-50 pointer-events-none' : ''}`;

  // Check if reduced motion is enabled
  const isReducedMotion = getReducedMotion();

  // If reduced motion is enabled, use normal button without motion
  if (isReducedMotion) {
    return (
      <button
        className={buttonClasses}
        onClick={onClick}
        disabled={disabled}
        {...props}
      >
        {children}
      </button>
    );
  }

  return (
    <motion.button
      className={buttonClasses}
      onClick={onClick}
      disabled={disabled}
      whileHover={{ scale: disabled ? 1 : 1.02 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      {...props}
    >
      {children}
    </motion.button>
  );
};

export default Button;