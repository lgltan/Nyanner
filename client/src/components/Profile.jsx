import React, { useEffect, useState } from 'react';

const Profile = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser();
  }, []);

  const get_user = () => {
    let user = {
        "username": "JohnDoe",
        "firstname": "John",
        "lastname": "Doe",
        "photo": "photo placeholder"
    }

    return user
  }

  const fetchUser = async () => {
    try {
      const response = await get_user(); // API CALL to return user
      setUser(response);
    } catch (error) {
      console.error('Failed to fetch user:', error);
    }
  };

  if (!user) return <div>Loading...</div>;

  return (
    <div className="profile">
      <img src={user.photo} alt="Profile" />
      <h1>{user.firstname} {user.lastname}</h1>
      <p>@{user.username}</p>
    </div>
  );
};

export default Profile;
