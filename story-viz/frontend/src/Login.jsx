import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './Login.css';
import { login } from './api'
import { useToken } from './TokenContext'
import { useError } from './ErrorContext'
import ErrorMessage from './ErrorMessage';

export default function Login() {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const { setToken } = useToken();
  const { setError } = useError();

  const handleSubmit = async e => {
    e.preventDefault();
    try {
        setError('');

        const token = await login(
        username,
        password
        );

        setToken(token);

    } catch (error) {
        if (error?.response?.status == 401) {
          setError("Invalid username or password")
        } else {
          setError("Oof: " + error?.message)
        }
    }
  }

  return(
    <div className="login-wrapper">
      <ErrorMessage />

      <h1>Please Log In</h1>

      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input type="text" onChange={e => setUserName(e.target.value)} />
        </label>
        <label>
          <p>Password</p>
          <input type="password" onChange={e => setPassword(e.target.value)} />
        </label>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  )
}