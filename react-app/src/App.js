import React, { useState, useEffect } from "react";
import './App.css';
import Greeting from "./components/Greeting";
import DateTime from "./components/Time";
import WiFi from "./components/WiFi";
import Updated from "./components/Updated";
import Calendar from "./components/Calendar";

function App() {
    return (
        <div className="App">
            <DateTime />
            <WiFi />
            <Updated />
            <Calendar />
        </div>
  );
}

export default App;
