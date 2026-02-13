'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { messageVariants, getReducedMotion } from '@/lib/animations';
import { taskService } from '@/services/taskService';
import { useTheme } from '@/components/ThemeProvider';

export default function ChatModal({ isOpen, onClose }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const { theme } = useTheme();

  // Check if reduced motion is enabled
  const isReducedMotion = getReducedMotion();

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get JWT token
      const token = localStorage.getItem('jwt_token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      // Send message to backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: inputValue
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Process AI response to fix any hardcoded dates
      let processedResponse = data.response;

      // Replace any hardcoded dates in the response with current date information
      const currentDate = new Date();
      const currentMonth = currentDate.toLocaleDateString('en-US', { month: 'long' });
      const currentDay = currentDate.getDate();
      const currentYear = currentDate.getFullYear();
      const currentFormattedDate = `${currentMonth} ${currentDay}, ${currentYear}`;

      // Replace date patterns like "Month DD, YYYY" with current date
      processedResponse = processedResponse.replace(/\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b/g, currentFormattedDate);

      // Add AI response to messages
      const aiMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: processedResponse,
        timestamp: new Date().toISOString(),
        toolCalls: data.tool_calls || []
      };

      setMessages(prev => [...prev, aiMessage]);

      // Process any tool calls
      if (data.tool_calls && data.tool_calls.length > 0) {
        for (const toolCall of data.tool_calls) {
          await processToolCall(toolCall);
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to chat
      const errorMessage = {
        id: crypto.randomUUID(),
        role: 'system',
        content: `Error: ${error.message}`,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const processToolCall = async (toolCall) => {
    try {
      switch (toolCall.tool_name) {
        case 'create_task':
          if (toolCall.result && toolCall.result.success) {
            const taskInfoMessage = {
              id: crypto.randomUUID(),
              role: 'system',
              content: `Task created: **${toolCall.result.task_details?.title || 'New task'}**`,
              timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, taskInfoMessage]);
          }
          break;

        case 'list_tasks':
          if (toolCall.result && toolCall.result.success) {
            const taskCount = toolCall.result.count || 0;
            const taskListMessage = {
              id: crypto.randomUUID(),
              role: 'system',
              content: `Found ${taskCount} tasks`,
              timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, taskListMessage]);

            // Show task details if available
            if (toolCall.result.tasks && toolCall.result.tasks.length > 0) {
              for (const task of toolCall.result.tasks) {
                const taskDetailMessage = {
                  id: Date.now() + task.id,
                  role: 'system',
                  content: `• **${task.title}** (${task.completed ? '✓ Completed' : '○ Pending'})`,
                  timestamp: new Date().toISOString()
                };
                setMessages(prev => [...prev, taskDetailMessage]);
              }
            }
          }
          break;

        default:
          const unknownToolMessage = {
            id: crypto.randomUUID(),
            role: 'system',
            content: `Executed tool: ${toolCall.tool_name}`,
            timestamp: new Date().toISOString()
          };
          setMessages(prev => [...prev, unknownToolMessage]);
      }
    } catch (error) {
      console.error('Error processing tool call:', error);
      const errorMessage = {
        id: crypto.randomUUID(),
        role: 'system',
        content: `Error processing ${toolCall.tool_name}: ${error.message}`,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) return null;

  return (
    <motion.div
      className={`fixed inset-0 ${theme === 'dark' ? 'bg-black/50' : 'bg-black/30'} flex items-center justify-center z-50 p-4`}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.2 }}
    >
      <motion.div
        className={`${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} rounded-lg shadow-sm w-full max-w-2xl h-4/5 flex flex-col border`}
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        transition={isReducedMotion ? { duration: 0.01 } : { type: "spring", damping: 25, stiffness: 300 }}
      >
        {/* Header */}
        <div className={`flex justify-between items-center p-4 border-b ${theme === 'dark' ? 'border-gray-700' : 'border-gray-200'}`}>
          <motion.h2
            className={`text-lg font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-800'} flex items-center space-x-2`}
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3 }}
          >
            <span>🤖</span>
            <span>AI Task Assistant</span>
          </motion.h2>
          <motion.button
            onClick={onClose}
            className={`${theme === 'dark' ? 'text-gray-300 dark:hover:text-white dark:bg-gray-700 dark:hover:bg-gray-600' : 'text-gray-600 hover:text-gray-800 bg-gray-100 hover:bg-gray-200'} text-xl p-1 rounded hover:bg-gray-200 transition-colors`}
            whileHover={isReducedMotion ? {} : { scale: 1.1 }}
            whileTap={isReducedMotion ? {} : { scale: 0.9 }}
          >
            &times;
          </motion.button>
        </div>

        {/* Messages Container */}
        <div className={`flex-1 overflow-y-auto p-4 ${theme === 'dark' ? 'bg-gray-900/30' : 'bg-white'}`}>
          {messages.length === 0 ? (
            <motion.div
              className={`h-full flex flex-col items-center justify-center ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3, delay: 0.1 }}
            >
              <div className="text-center">
                <div className={`mx-auto w-16 h-16 rounded-lg flex items-center justify-center mb-4 ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'}`}>
                  <div className="text-2xl">🤖</div>
                </div>
                <p className={`font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-800'} mb-2`}>AI Task Assistant</p>
                <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-400'} mb-4`}>Ask me to create or manage tasks</p>
              </div>
            </motion.div>
          ) : (
            <div className="space-y-4">
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    initial="hidden"
                    animate="visible"
                    variants={message.role === 'user' ? messageVariants.user : messageVariants.ai}
                    transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3 }}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.role === 'user'
                          ? `${theme === 'dark' ? 'bg-blue-500 text-white' : 'bg-indigo-300 text-white'} border ${theme === 'dark' ? 'border-blue-500' : 'border-indigo-400'}`
                          : message.role === 'assistant'
                          ? `${theme === 'dark' ? 'bg-gray-700 text-gray-100' : 'bg-gray-100 text-gray-800'} border ${theme === 'dark' ? 'border-gray-600' : 'border-gray-300'}`
                          : `${theme === 'dark' ? 'bg-gray-700 text-gray-100' : 'bg-gray-100 text-gray-800'} border ${theme === 'dark' ? 'border-gray-600' : 'border-gray-300'}`
                      }`}
                    >
                      <div className={`whitespace-pre-wrap ${theme === 'dark' ? 'text-gray-100' : 'text-gray-800'}`}>
                        {message.content.split(/(\*\*[^*]+\*\*)/g).map((part, index) => {
                          if (part.startsWith('**') && part.endsWith('**')) {
                            const cleanText = part.slice(2, -2);
                            return (
                              <strong key={index} className={`font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                                {cleanText}
                              </strong>
                            );
                          }
                          return part;
                        })}
                      </div>
                      {message.timestamp && (
                        <div className={`text-xs opacity-70 mt-1 ${theme === 'dark' ? 'text-gray-200' : 'text-gray-700'}`}>
                          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>

              <AnimatePresence>
                {isLoading && (
                  <motion.div
                    className="flex justify-start"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.2 }}
                  >
                    <div className={`${theme === 'dark' ? 'bg-gray-800 text-gray-300 border-gray-700' : 'bg-gray-100 text-gray-800 border-gray-300'} px-4 py-2 rounded-lg max-w-xs border`}>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm">AI is typing</span>
                        <div className="flex space-x-1">
                          <motion.div
                            className={`w-2 h-2 ${theme === 'dark' ? 'bg-gray-400' : 'bg-gray-600'} rounded-full`}
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{
                              duration: 1,
                              repeat: Infinity,
                              ease: "easeInOut",
                              delay: 0
                            }}
                          />
                          <motion.div
                            className={`w-2 h-2 ${theme === 'dark' ? 'bg-gray-400' : 'bg-gray-600'} rounded-full`}
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{
                              duration: 1,
                              repeat: Infinity,
                              ease: "easeInOut",
                              delay: 0.2
                            }}
                          />
                          <motion.div
                            className={`w-2 h-2 ${theme === 'dark' ? 'bg-gray-400' : 'bg-gray-600'} rounded-full`}
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{
                              duration: 1,
                              repeat: Infinity,
                              ease: "easeInOut",
                              delay: 0.4
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <motion.div
          className={`p-4 border-t ${theme === 'dark' ? 'border-gray-700 bg-gray-800' : 'border-gray-200 bg-white'}`}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3, delay: 0.2 }}
        >
          <div className="flex space-x-2">
            <motion.textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me to create or manage tasks..."
              className={`flex-1 border rounded-md p-3 resize-none min-h-[60px] max-h-32 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 ${
                theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white placeholder:text-gray-400' : 'bg-white border-gray-300 text-gray-800 placeholder:text-gray-500'
              }`}
              disabled={isLoading}
            />
            <motion.button
              onClick={handleSend}
              disabled={isLoading || !inputValue.trim()}
              className={`px-4 py-2 rounded-md text-sm font-medium ${
                isLoading || !inputValue.trim()
                  ? `${theme === 'dark' ? 'bg-gray-700 text-gray-400' : 'bg-gray-200 text-gray-500'} cursor-not-allowed`
                  : `${theme === 'dark' ? 'bg-blue-600 hover:bg-blue-700' : 'bg-primary hover:bg-primary/90'} text-white`
              }`}
            >
              Send
            </motion.button>
          </div>
          <p className={`text-xs ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'} mt-2`}>
            Example: "Create a task to buy groceries tomorrow" or "Show me my tasks for today"
          </p>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}