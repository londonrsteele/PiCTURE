import React, { useState, useEffect } from "react";
export default function Greeting() {
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
        <div>
            <p>{greeting.greeting}{greeting.name}</p>
        </div>
    );
}