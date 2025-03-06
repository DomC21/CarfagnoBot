import { Topic } from '../types/chat';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { BookOpen } from 'lucide-react';

interface TopicMenuProps {
  topics: Topic[];
  onSelectTopic: (topicId: string) => Promise<void>;
}

export function TopicMenu({ topics, onSelectTopic }: TopicMenuProps) {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BookOpen size={20} />
          <span>Investing Topics</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {topics.map((topic) => (
            <Button
              key={topic.id}
              variant="outline"
              className="justify-start h-auto py-3 px-4 text-left"
              onClick={() => onSelectTopic(topic.id)}
            >
              {topic.title}
            </Button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
