import "./index.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import React from "react";

function App() {
  return (
    <Router>
      {/* <ThemeProvider attribute="class" defaultTheme="system" storageKey="vite-ui-theme" enableSystem> */}

        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/start" element={<Start />} />

          <Route path="/sign-in" element={<SignIn />} />


        
        </Routes>
        
      {/* </ThemeProvider> */}
    </Router>
  );
}

export default App;
