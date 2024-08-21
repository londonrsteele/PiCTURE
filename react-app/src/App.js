import React, { useState, useEffect } from "react";
import './App.css';
import Greeting from "./components/Greeting";
import DateTime from "./components/Time";

function App() {
    return (
        <div className="App">
            <DateTime />
        </div>
  );
}

export default App;
