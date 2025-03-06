import { useState, useEffect } from 'react';
import { ChatInterface } from './components/ChatInterface';
import { Message, Topic } from './types/chat';
import { chatApi } from './services/api';
import './App.css';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [suggestedTopics, setSuggestedTopics] = useState<Topic[]>([]);
  const [disclaimer, setDisclaimer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  // Removed unused initialMessage state

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
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-blue-600 text-white p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-blue-700 rounded flex items-center justify-center text-white font-bold">CE</div>
          <div>
            <h1 className="text-xl font-bold">CarfganoBot</h1>
            <p className="text-xs opacity-80">by Carfgano Enterprises</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="font-medium">Investing Education</span>
        </div>
      </header>
      <main className="flex-1 overflow-hidden">
        <div className="container mx-auto h-full max-w-4xl bg-white shadow-md">
          <ChatInterface
            onSendMessage={handleSendMessage}
            onSelectTopic={handleSelectTopic}
            messages={messages}
            suggestedTopics={suggestedTopics}
            disclaimer={disclaimer}
            isLoading={isLoading}
          />
        </div>
      </main>
      <footer className="bg-gray-100 p-2 text-center text-xs text-gray-500">
        © {new Date().getFullYear()} Carfgano Enterprises. All rights reserved.
      </footer>
    </div>
  );
}

export default App;
