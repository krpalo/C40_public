import React from 'react';

interface AuthProps {
  signedInUser: string | null;
  onSignIn: (username: string) => void;
  onSignOut: () => void;
}

// Stub implementation for authentication. Currently mocking sign in functionality.
const Authentication: React.FC<AuthProps> = ({ signedInUser, onSignIn, onSignOut }) => {
  const handleClick = () => {
    if (signedInUser) {
      onSignOut();
    } else {
      onSignIn("MsFire");  // Always signs in as MsFire for now
    }
  };

  return (
    <div className="auth-controls">
      <button onClick={handleClick}>
        {signedInUser ? 'Sign out' : 'Sign in'}
      </button>
    </div>
  );
};

export default Authentication;