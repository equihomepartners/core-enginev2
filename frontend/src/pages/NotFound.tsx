import { NonIdealState, Button } from '@blueprintjs/core';
import { useNavigate } from 'react-router-dom';

const NotFound = () => {
  const navigate = useNavigate();
  
  return (
    <div className="flex items-center justify-center h-[calc(100vh-theme(spacing.14))]">
      <NonIdealState
        icon="error"
        title="Page Not Found"
        description="The page you're looking for doesn't exist or has been moved."
        action={
          <Button 
            intent="primary" 
            text="Go to Dashboard" 
            onClick={() => navigate('/')}
          />
        }
      />
    </div>
  );
};

export default NotFound;
