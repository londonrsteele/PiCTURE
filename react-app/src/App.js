import React, { useState, useEffect } from "react";
import './App.css';
import Greeting from "./components/Greeting";
import DateTime from "./components/Time";
import WiFi from "./components/WiFi";
import Updated from "./components/Updated";
function App() {
    return (
        <div className="App">
            <DateTime />
            <WiFi />
            <Updated />
        </div>
  );
}

export default App;
