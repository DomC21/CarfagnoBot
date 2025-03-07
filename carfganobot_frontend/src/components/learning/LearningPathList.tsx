import React, { useEffect, useState } from 'react';
import { getPersonalizedLearningPath, markTopicCompleted, LearningPathTopic } from '../../services/learning-paths';
import LearningPathCard from './LearningPathCard';
import { useToast } from '../../hooks/use-toast';
import { LoadingSpinner } from '../LoadingSpinner';

const LearningPathList: React.FC = () => {
  const [learningPath, setLearningPath] = useState<LearningPathTopic[]>([]);
  const [proficiencyLevel, setProficiencyLevel] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    const fetchLearningPath = async () => {
      try {
        setLoading(true);
        const response = await getPersonalizedLearningPath();
        setLearningPath(response.learning_path);
        setProficiencyLevel(response.proficiency_level);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching learning path:', err);
        setError('Failed to load your personalized learning path. Please try again later.');
        setLoading(false);
      }
    };

    fetchLearningPath();
  }, []);

  const handleMarkCompleted = async (topicId: string) => {
    try {
      await markTopicCompleted(topicId);
      toast({
        title: 'Topic Completed',
        description: 'Great job! This topic has been marked as completed.',
        variant: 'default',
      });
      
      // Remove the completed topic from the list
      setLearningPath(prevPath => prevPath.filter(topic => topic.id !== topicId));
    } catch (err) {
      console.error('Error marking topic as completed:', err);
      toast({
        title: 'Error',
        description: 'Failed to mark topic as completed. Please try again.',
        variant: 'destructive',
      });
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 text-red-800 rounded-md">
        <p>{error}</p>
        <button 
          className="mt-2 px-4 py-2 bg-red-100 hover:bg-red-200 text-red-800 rounded-md"
          onClick={() => window.location.reload()}
        >
          Try Again
        </button>
      </div>
    );
  }

  if (learningPath.length === 0) {
    return (
      <div className="p-6 bg-blue-50 rounded-lg text-center">
        <h3 className="text-xl font-semibold mb-2">All Caught Up!</h3>
        <p className="text-gray-700">
          You've completed all the recommended topics for your current proficiency level.
          Keep exploring other topics or take some quizzes to advance to the next level!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Your Personalized Learning Path</h2>
        <p className="text-gray-700">
          Based on your progress and quiz results, we've created a customized learning path 
          for your <span className="font-medium text-indigo-700 capitalize">{proficiencyLevel}</span> level.
          Follow these topics in order for the best learning experience.
        </p>
      </div>
      
      <div className="space-y-4">
        {learningPath.map((topic, index) => (
          <LearningPathCard 
            key={topic.id} 
            topic={topic} 
            index={index} 
            onComplete={handleMarkCompleted} 
          />
        ))}
      </div>
    </div>
  );
};

export default LearningPathList;
