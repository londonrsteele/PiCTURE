import logo from './logo.svg';
import './App.css';

function App() {
    const [greeting, setGreeting] = useState({
        greeting: "",
        name: "",
    });

    useEffect(() => {
        fetch("/home").then((res) =>
            res.json().then((greeting) => {
                setGreeting({
                    greeting: greeting.Greeting,
                    name: greeting.Name,
                });
            })
        );
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <p>Hello!</p>
                <p>{greeting.Greeting}</p>
                <p>{greeting.Name}</p>
            </header>
        </div>
  );
}

export default App;
