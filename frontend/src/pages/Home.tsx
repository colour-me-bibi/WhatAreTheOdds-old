import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

interface Props {}

interface User {
  pk?: number;
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
}

const getUser = async (): Promise<User | undefined> => {
  const token = localStorage.getItem("token");

  if (!token) throw new Error("No user is logged in");

  return fetch("http://localhost:8000/api/auth/user/", {
    headers: { Authorization: `Token ${token}` },
  })
    .then(async (response) => {
      const data = await response.json();
      if (!response.ok) throw new Error(JSON.stringify(data));
      return data;
    })
    .catch(console.error);
};

const Home: React.FC<Props> = () => {
  const [user, setUser] = useState<User>();

  useEffect(() => {
    getUser().then((user) => {
      console.log(user);
      setUser(user);
    });
  }, []);

  return (
    <div className="container mt-5">
      <h1>Home</h1>
      <p>Welcome, {user?.username}</p>
      <p>
        <Link to="/login">Login</Link>
      </p>
      <p>
        <Link to="/signup">Sign Up</Link>
      </p>
    </div>
  );
};

export default Home;
