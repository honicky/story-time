import React, { createContext, useState, useContext } from 'react';

const TokenContext = createContext();

export const useToken = () => useContext(TokenContext);

export const TokenProvider = ({ children }) => {

  const getToken = () => {
    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    return userToken?.access_token
  };

  const [token, setToken] = useState(getToken());

  const saveToken = userToken => {
    localStorage.setItem('token', JSON.stringify(userToken));
    setToken(userToken.access_token);
  };

  return (
    <TokenContext.Provider value={{setToken: saveToken, token }}>
      {children}
    </TokenContext.Provider>
  );

};
