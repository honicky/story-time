import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { ErrorProvider } from './ErrorContext';
import { TokenProvider } from './TokenContext';
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <TokenProvider><ErrorProvider>
      <App />
    </ErrorProvider></TokenProvider>
  </React.StrictMode>,
)
