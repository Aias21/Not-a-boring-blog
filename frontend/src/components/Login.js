// components/Login.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

function Login() {
  const [currentUser, setCurrentUser] = useState();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    client.post(
        "/api/login/",
        {
          email: email,
          password: password
        }
      ).then(function(res) {
        setCurrentUser(true);
      })
      .catch(function(error){
        setError("Invalid email or password");
      });

      
    }

  return (
    <div>
    {currentUser ? (
      <div>
        <h2>Welcome, User!</h2>
        <p>You are already logged in.</p>
      </div>
    ) : (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      <p className="error">{error}</p>
      <p>
        Don't have an account? <Link to="/register">Register here</Link>
      </p>
    </div>
          )}
          </div>
  );
}

export default Login;
