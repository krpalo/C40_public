import React, { useState } from 'react';

const ProfileForm: React.FC = () => {
  const [name, setName] = useState('');
  const [interests, setInterests] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');

    const profile = {
        name,
        interests: interests.split(',').map(s => s.trim())
      };
  
    try {
      const response = await fetch('http://localhost:8000/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile)
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 409) {
          setErrorMsg(errorData.detail);
        } else {
          setErrorMsg('Something went wrong while saving the profile.');
        }
        return;
      }
  
      const data = await response.json();
      console.log(data.message);
      setErrorMsg(''); // Clear error if successful
    } catch (err) {
      setErrorMsg('Network error. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="handle-submit">
      <h2>Your Profile</h2>
      <div className="profile-input-area">
      <input
        type="text"
        className="profile-input-name"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="text"
        className="profile-input-interests"
        placeholder="Interests (comma separated)"
        value={interests}
        onChange={(e) => setInterests(e.target.value)}
      />
      <button
        type="submit"
        className="profile-submit"
        disabled={submitted}
      >
        {submitted ? 'Saved!' : 'Save Profile'}
      </button>
      </div>
      {errorMsg && (
        <p className="profile-error-msg">{errorMsg}</p>
      )}
    </form>
  );
};

export default ProfileForm;