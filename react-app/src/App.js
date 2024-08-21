import React, { useState, useEffect } from "react";
import './App.css';
import Greeting from "./components/Greeting";
import DateTime from "./components/Time";
import WiFi from "./components/WiFi";

function App() {
    return (
        <div className="App">
            <DateTime />
            <WiFi />
        </div>
  );
}

export default App;
