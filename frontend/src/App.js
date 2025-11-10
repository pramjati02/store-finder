import logo from './logo.svg';
import './App.css';
import axios from "axios";

import React, {useState, useEffect} from "react";

const backendURL = process.env.REACT_APP_FASTAPI_BASE;
console.log("URL: ", backendURL)

function App() {
  const [stores, setStores] = useState([]);
  const [address, setAddress] = useState("");
  const [nearbyStores, setNearbyStores] = useState([]);
  const [loading, setLoading] = useState(false);

  // Connecting to the backend, loading all stores initially
  // useEffect: use to synchronize frontend components to external systems
  useEffect( () => {
    axios.get(`${backendURL}/stores/`)
    .then(res => setStores(res.data))
    .catch(err => console.error(err));
}, [])
// [] = only runs this effect once on the first load, does not rerun every re-render

  const handleFindNearby = async() => {
    // If no address is entered, do nothing
    if (!address.trim()) return;

    // sets a searching message while waiting
    setLoading(true);

    // based on parameters "address" and "radius_km", 
    // send a GET request to {backendURL}/stores/nearby
    // Backend will receive this as /stores/nearby?address=<userinput>&radius_km=3
    // if successful, updates NearbyStores with SetNearbyStores(res.data)
    // If there is an error, catch error and set NearbyStores to nothing
    try {
      const res = await axios.get(`${backendURL}/stores/nearby`, {
        params: { address, radius_km: 3}
      });
      setNearbyStores(res.data);
    } catch (error) {
      console.error("Error fetching nearby stores:", error)
      setNearbyStores([]);
    }

    // hides the loading message
    setLoading(false)

  };

  return (
    <div style ={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Nottingham Store Finder 😅</h1>
      
      <section style={{ marginBottom: "2rem" }}>
        {/*Sets the address through a text input*/}
        <h2> Find Nearby Stores 🤪</h2>
        <input
          type="text"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="Enter an address or postcode"
          style={{ padding: "0.5rem", width: "300px" }}
        />
        {/*Button that executes handleFindNearby*/}
        <button onClick={handleFindNearby} style={{ marginLeft: "1rem", padding: "0.5rem 1rem"}}>
          Search
        </button>

        {/* Using the loading state to get "Searching" to appear after clicking the button*/}
        {loading && <p>Searching...</p>}

        {/*All nearby stores only appears if list of nearbyStores is longer than 0*/}
        {nearbyStores.length > 0 && (
          <div style={{ marginTop: "1rem" }}>
            <h3>Nearest Stores:</h3>
            <ul>
              {nearbyStores.map((store) => (
                <li key={store.id}>
                  <strong>{store.name}</strong> — {store.type}, {store.address}
                </li>
              ))}
            </ul>
          </div>
        )}

      </section>
    </div>
  );
}

export default App;
