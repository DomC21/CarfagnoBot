import React, { useState, useRef, useEffect } from 'react';
import { Send, BookOpen } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent } from './ui/card';
import { Avatar } from './ui/avatar';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { Alert, AlertDescription } from './ui/alert';
import { Message, Topic } from '../types/chat';

interface ChatInterfaceProps {
  onSendMessage: (message: string) => Promise<void>;
  onSelectTopic: (topicId: string) => Promise<void>;
  messages: Message[];
  suggestedTopics: Topic[];
  disclaimer: string;
  isLoading: boolean;
}

export function ChatInterface({
  onSendMessage,
  onSelectTopic,
  messages,
  suggestedTopics,
  disclaimer,
  isLoading
}: ChatInterfaceProps) {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      await onSendMessage(inputValue);
      setInputValue('');
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat Messages */}
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex gap-3 max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <Avatar className={message.role === 'user' ? 'bg-blue-500' : 'bg-green-600'}>
                  <span className="text-white font-semibold">
                    {message.role === 'user' ? 'U' : 'C'}
                  </span>
                </Avatar>
                <Card className={`${message.role === 'user' ? 'bg-blue-50' : 'bg-green-50'}`}>
                  <CardContent className="p-3">
                    {message.role === 'assistant' ? (
                      <div className="prose prose-sm max-w-none">
                        {message.content.split('\n').map((line, i) => (
                          <p key={i}>{line}</p>
                        ))}
                      </div>
                    ) : (
                      <p>{message.content}</p>
                    )}
                  </CardContent>
                </Card>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      {/* Suggested Topics */}
      {suggestedTopics.length > 0 && (
        <div className="p-3 bg-gray-50">
          <p className="text-sm font-medium mb-2">Suggested topics:</p>
          <div className="flex flex-wrap gap-2">
            {suggestedTopics.map((topic) => (
              <Badge 
                key={topic.id} 
                variant="outline" 
                className="cursor-pointer hover:bg-gray-100"
                onClick={() => onSelectTopic(topic.id)}
              >
                {topic.title}
              </Badge>
            ))}
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <Alert className="mx-3 my-2 bg-amber-50 border-amber-200">
        <AlertDescription className="text-xs text-amber-800">
          {disclaimer}
        </AlertDescription>
      </Alert>

      {/* Input Form */}
      <div className="p-3 border-t">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask about investing..."
            className="flex-1"
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading || !inputValue.trim()}>
            <Send size={18} />
          </Button>
          <Button 
            type="button" 
            variant="outline" 
            onClick={() => onSelectTopic('main_menu')}
            title="Show topics menu"
          >
            <BookOpen size={18} />
          </Button>
        </form>
      </div>
    </div>
  );
}
