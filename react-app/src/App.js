import './App.css';
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
                <div className="Clock">
                    <DateTime />
                </div>
                <div className="Sun">

                </div>
                <div className="QOTD">
                    
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
