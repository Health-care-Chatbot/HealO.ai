import './App.css'
import { ThemeProvider } from './components/theme-provider'
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from '@/pages/home'
import Chat from '@/pages/chat';

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </Router>
    </ThemeProvider>
  )
}

export default App;