'use client';

import { motion } from 'framer-motion';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

const PageTransition = ({ children }) => {
  const pathname = usePathname();
  const [previousPathname, setPreviousPathname] = useState(pathname);

  useEffect(() => {
    if (pathname !== previousPathname) {
      setPreviousPathname(pathname);
    }
  }, [pathname, previousPathname]);

  return (
    <motion.div
      key={pathname}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
    >
      {children}
    </motion.div>
  );
};

export default PageTransition;