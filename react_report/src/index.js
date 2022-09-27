import React from 'react';
import { hydrateRoot, createRoot } from 'react-dom/client';
import './index.css';
import App from './App';


const rootElement = document.getElementById("root");
if (rootElement.hasChildNodes()) {
  hydrateRoot(rootElement).render(<App />);
} else {
  createRoot(rootElement).render(<App />);
}
