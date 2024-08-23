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
            <div className="LeftColumn">
                <div>

                </div>
                <div>
                    <Calendar />
                </div>
            </div>
            <div className="RightColumn">
                <div>
                    <DateTime />
                </div>
                <div>
                    <Updated />
                </div>
                <div>
                    
                </div>
                <div>
                    
                </div>
                <div>
                    <WiFi />
                </div>
            </div>
        </div>
  );
}

export default App;
