import "./index.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import React from "react";

function App() {
  return (
    <Router>
      {/* <ThemeProvider attribute="class" defaultTheme="system" storageKey="vite-ui-theme" enableSystem> */}

        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/docs" element={<Docs />} />

          <Route path="/start" element={<Start />} />

          <Route path="/about" element={<About />} />

          <Route path="/sign-in" element={<SignIn />} />

          <Route path="/sign-up" element={<SignUp />} />

        
        </Routes>
        
      {/* </ThemeProvider> */}
    </Router>
  );
}

export default App;
