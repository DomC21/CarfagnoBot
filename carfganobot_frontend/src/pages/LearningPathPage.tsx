import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import LearningPathList from '../components/learning/LearningPathList';
import { LoadingSpinner } from '../components/LoadingSpinner';

const LearningPathPage: React.FC = () => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  // Redirect to login if not authenticated
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-blue-800">Your Learning Journey</h1>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <LearningPathList />
        </div>
      </div>
    </div>
  );
};

export default LearningPathPage;
