import './App.css';
import DateTime from "./components/Time";
import WiFi from "./components/WiFi";
import Updated from "./components/Updated";
import Calendar from "./components/Calendar";
import Quote from "./components/Quote";
import Weather from "./components/Weather"

function App() {
    return (
        <div className="App">
            <div className="LeftColumn">
                <div>
                    <Weather />
                </div>
                <div>
                    <Calendar />
                </div>
            </div>
            <div className="RightColumn">
                <div className="Clock">
                    <DateTime />
                </div>
                <div className="Sun">

                </div>
                <div className="QOTD">
                    <Quote />
                </div>
                <div className="Status">
                    <Updated />
                    <WiFi />
                </div>
            </div>
        </div>
  );
}

export default App;
