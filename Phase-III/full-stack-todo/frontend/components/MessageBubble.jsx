'use client';

import { motion } from 'framer-motion';
import { messageVariants, getReducedMotion } from '@/lib/animations';

const MessageBubble = ({ message, isOwn = false, isLast = false }) => {
  const isReducedMotion = getReducedMotion();

  // Determine bubble style based on message role
  const bubbleStyle = isOwn
    ? 'bg-primary text-primary-foreground rounded-br-none'
    : message.role === 'assistant'
    ? 'bg-secondary text-secondary-foreground rounded-bl-none'
    : 'bg-warning text-warning-foreground rounded-bl-none';

  return (
    <motion.div
      className={`max-w-xs lg:max-w-md px-4 py-3 rounded-xl ${bubbleStyle}`}
      initial="hidden"
      animate="visible"
      variants={isOwn ? messageVariants.user : messageVariants.ai}
      transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3 }}
    >
      <div className="whitespace-pre-wrap break-words">{message.content}</div>
      {message.timestamp && (
        <div className="text-xs opacity-70 mt-1 text-right">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      )}
    </motion.div>
  );
};

const UserMessageBubble = ({ message, isLast = false }) => {
  const isReducedMotion = getReducedMotion();

  return (
    <motion.div
      className="flex justify-end"
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3 }}
    >
      <MessageBubble message={message} isOwn={true} isLast={isLast} />
    </motion.div>
  );
};

const AiMessageBubble = ({ message, isLast = false }) => {
  const isReducedMotion = getReducedMotion();

  return (
    <motion.div
      className="flex justify-start"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3 }}
    >
      <MessageBubble message={message} isOwn={false} isLast={isLast} />
    </motion.div>
  );
};

export { MessageBubble, UserMessageBubble, AiMessageBubble };