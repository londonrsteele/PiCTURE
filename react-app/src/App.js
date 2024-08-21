import React, { useState, useEffect } from "react";
import './App.css';

function App() {
    const [greeting, setGreeting] = useState({
        greeting: "",
        name: "",
    });

    useEffect(() => {
        fetch("/home").then(res =>
            res.json().then(data => {
                setGreeting({
                    greeting: data.Greeting,
                    name: data.Name,
                });
            })
        );
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <p>{greeting.greeting}{greeting.name}</p>
            </header>
        </div>
  );
}

export default App;
