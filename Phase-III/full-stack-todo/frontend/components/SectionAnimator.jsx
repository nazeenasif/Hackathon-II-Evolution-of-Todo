'use client';

import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';

const SectionAnimator = ({ children, delay = 0, duration = 0.5, stagger = false, className = "" }) => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: stagger ? 0.1 : 0,
        delayChildren: delay
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: {
      opacity: 1,
      y: 0,
      transition: {
        duration: duration,
        ease: "easeOut"
      }
    }
  };

  if (stagger) {
    return (
      <motion.div
        ref={ref}
        className={className}
        variants={container}
        initial="hidden"
        animate={isInView ? "show" : "hidden"}
      >
        {Array.isArray(children) ?
          children.map((child, index) => (
            <motion.div key={index} variants={item}>
              {child}
            </motion.div>
          )) :
          <motion.div variants={item}>{children}</motion.div>
        }
      </motion.div>
    );
  } else {
    return (
      <motion.div
        ref={ref}
        className={className}
        initial={{ opacity: 0, y: 20 }}
        animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
        transition={{
          duration: duration,
          ease: "easeOut",
          delay: delay
        }}
      >
        {children}
      </motion.div>
    );
  }
};

export default SectionAnimator;