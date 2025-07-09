import { useState, useCallback } from 'react';
import { Message } from '@/types/chat';
import { sendChatMessage } from '@/app/api/chat/client';

interface UseChatOptions {
  sessionId: string;
  initialMessages: Message[];
  className?: string;
}

export function useChat({ sessionId, initialMessages }: UseChatOptions) {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [isTyping, setIsTyping] = useState(false);

  const append = useCallback(async (message: Message) => {
    
    setMessages((prev) => [...prev, message]);
    setIsTyping(true);
    
    try {
      const response = await sendChatMessage(sessionId, message.content);
      const reader = response.getReader();
      const decoder = new TextDecoder();
      let aiMessage = '';
      let messageId = '';
      
      setMessages((prev) => [
        ...prev,
        {
          id: 'temp-ai',
          role: 'assistant',
          content: '',
          createdAt: new Date().toISOString(),
        },
      ]);
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n').filter(line => line.trim());
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.replace('data: ', '');
            
            if (data === '[DONE]') {
              continue;
            }
            
            try {
              const parsed = JSON.parse(data);
              
              if (parsed.error) {
                throw new Error(parsed.error);
              }
              
              if (parsed.content) {
                aiMessage += parsed.content;
                setMessages((prev) => {
                  const last = prev[prev.length - 1];
                  if (last.role === 'assistant') {
                    return [
                      ...prev.slice(0, -1),
                      {
                        ...last,
                        content: aiMessage,
                      },
                    ];
                  }
                  return prev;
                });
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e);
            }
          } else if (line.startsWith('event: session_id')) {
            // Handle session ID if needed
          }
        }
      }
    } catch (error) {
      console.error('Error in chat stream:', error);
      // In your useChat hook or equivalent
      // if (error?.status === 429) {
      //   showRegistrationModal();
      // }
      setMessages((prev) => [
        ...prev,
        {
          id: 'error',
          role: 'error',
          content: 'Failed to get AI response',
          createdAt: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  }, [sessionId]);

  return {
    messages,
    append,
    isTyping,
    setMessages,
  };
}

