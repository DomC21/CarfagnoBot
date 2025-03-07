import { useState, useEffect } from 'react';
import { ChatInterface } from '../components/ChatInterface';
import { Message, Topic } from '../types/chat';
import { chatApi, streamChatMessage } from '../services/api';

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [suggestedTopics, setSuggestedTopics] = useState<Topic[]>([]);
  const [disclaimer, setDisclaimer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);

  // Initialize chat with welcome message and topics
  useEffect(() => {
    const initializeChat = async () => {
      try {
        setIsLoading(true);
        const topicsData = await chatApi.getTopics();
        setTopics(topicsData.topics);
        setDisclaimer(topicsData.disclaimer);

        // Get main menu content
        const mainMenuResponse = await chatApi.getTopic('main_menu');
        setSuggestedTopics(mainMenuResponse.suggested_topics || []);

        // Add welcome message to chat
        setMessages([
          {
            role: 'assistant' as const,
            content: 'Hello! I\'m CarfganoBot from Carfgano Enterprises, here to help you learn about investing. What would you like to know about today?'
          }
        ]);
      } catch (error) {
        console.error('Error initializing chat:', error);
        setMessages([
          {
            role: 'assistant',
            content: 'Sorry, I\'m having trouble connecting to the server. Please try again later.'
          }
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    initializeChat();
  }, []);

  // Handle sending a message
  const handleSendMessage = async (message: string) => {
    try {
      setIsLoading(true);
      
      // Add user message to chat
      const updatedMessages = [
        ...messages,
        { role: 'user' as const, content: message }
      ];
      setMessages(updatedMessages);

      // Get response from API
      const response = await chatApi.sendMessage(
        message, 
        updatedMessages.map(m => ({ role: m.role, content: m.content }))
      );

      // Add assistant response to chat
      setMessages([
        ...updatedMessages,
        { role: 'assistant' as const, content: response.message }
      ]);

      // Update suggested topics
      setSuggestedTopics(response.suggested_topics || []);
      
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages([
        ...messages,
        { role: 'user', content: message },
        { 
          role: 'assistant' as const, 
          content: 'Sorry, I encountered an error processing your request. Please try again.' 
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle streaming a message
  const handleStreamMessage = async (
    message: string,
    onChunk: (chunk: string) => void,
    onComplete: () => void
  ) => {
    try {
      setIsStreaming(true);
      
      // Add user message to chat
      const updatedMessages = [
        ...messages,
        { role: 'user' as const, content: message }
      ];
      setMessages(updatedMessages);
      
      // Collect the full response
      let fullResponse = '';
      
      console.log('ChatPage: Starting streaming request for message:', message);
      
      // Stream message from API
      await streamChatMessage(
        message,
        updatedMessages,
        (chunk) => {
          console.log('ChatPage: Received chunk of length:', chunk.length);
          fullResponse += chunk;
          onChunk(chunk);
        },
        async () => {
          console.log('ChatPage: Streaming complete, full response length:', fullResponse.length);
          
          // Add assistant response to chat
          setMessages([
            ...updatedMessages,
            { role: 'assistant' as const, content: fullResponse }
          ]);
          
          // Get suggested topics based on the full message
          try {
            const response = await chatApi.sendMessage(
              message, 
              updatedMessages
            );
            
            if (response.suggested_topics) {
              setSuggestedTopics(response.suggested_topics);
            }
          } catch (error) {
            console.error('Error getting suggested topics:', error);
          }
          
          onComplete();
        }
      );
      
    } catch (error) {
      console.error('Error streaming message:', error);
      setMessages([
        ...messages,
        { role: 'user', content: message },
        { 
          role: 'assistant' as const, 
          content: 'Sorry, I encountered an error processing your request. Please try again.' 
        }
      ]);
    } finally {
      setIsStreaming(false);
    }
  };

  // Handle selecting a topic
  const handleSelectTopic = async (topicId: string) => {
    try {
      setIsLoading(true);
      
      // Get topic content from API
      const response = await chatApi.getTopic(topicId);
      
      // Add topic selection to chat
      const topicTitle = topics.find(t => t.id === topicId)?.title || 
                        suggestedTopics.find(t => t.id === topicId)?.title || 
                        topicId;
      
      const updatedMessages = [
        ...messages,
        { role: 'user' as const, content: `Tell me about ${topicTitle}` },
        { role: 'assistant' as const, content: response.message }
      ];
      
      setMessages(updatedMessages);
      
      // Update suggested topics
      setSuggestedTopics(response.suggested_topics || []);
      
    } catch (error) {
      console.error('Error selecting topic:', error);
      setMessages([
        ...messages,
        { 
          role: 'assistant' as const, 
          content: 'Sorry, I encountered an error retrieving that topic. Please try another one.' 
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto h-full max-w-4xl bg-white shadow-md">
      <ChatInterface
        onSendMessage={handleSendMessage}
        onStreamMessage={handleStreamMessage} // This will be used by default
        onSelectTopic={handleSelectTopic}
        messages={messages}
        suggestedTopics={suggestedTopics}
        disclaimer={disclaimer}
        isLoading={isLoading}
        isStreaming={isStreaming}
      />
    </div>
  );
}
