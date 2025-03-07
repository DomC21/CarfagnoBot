import React from 'react';
import { LearningPathTopic } from '../../services/learning-paths';
import { useNavigate } from 'react-router-dom';

interface LearningPathCardProps {
  topic: LearningPathTopic;
  index: number;
  onComplete: (topicId: string) => void;
}

const LearningPathCard: React.FC<LearningPathCardProps> = ({ topic, index, onComplete }) => {
  const navigate = useNavigate();

  const handleTopicClick = () => {
    // Navigate to chat page with the selected topic
    navigate(`/chat?topic=${topic.id}`);
  };

  const handleMarkCompleted = (e: React.MouseEvent) => {
    e.stopPropagation();
    onComplete(topic.id);
  };

  return (
    <div 
      className="bg-white rounded-lg shadow-md p-4 mb-4 border-l-4 border-blue-500 hover:shadow-lg transition-shadow cursor-pointer"
      onClick={handleTopicClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className="bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center mr-3">
            {index + 1}
          </div>
          <h3 className="text-lg font-semibold">{topic.title}</h3>
        </div>
        <button
          onClick={handleMarkCompleted}
          className="bg-green-100 hover:bg-green-200 text-green-800 px-3 py-1 rounded-full text-sm font-medium"
        >
          Mark Complete
        </button>
      </div>
    </div>
  );
};

export default LearningPathCard;
