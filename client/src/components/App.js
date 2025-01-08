import React, { useEffect, useState } from "react";
import { Switch, Route, Redirect} from "react-router-dom";
import Navigation from './Navigation.js';
import Home from "./Home.js";
import CreateRides from './CreateRides.js';
import MyRides from "./MyRides.js";
import Login from './Login.js';
import Register from './Register.js';
import Header from './Header.js';
import MyBookings from './MyBookings.js';


function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/api/check_session").then((response) => {
      if (response.ok) {
        response.json().then((user) => setUser(user));
      }
    });
  }, []);

  function handleLogin(user) {
    setUser(user);
  }

  function handleLogout() {
    setUser(null);
  }


  return (
    <div>
      <Header user={user} />
      {user && <Navigation user={user} onLogout={handleLogout}/>}
      <h1>Project client</h1>
      <Switch>
        <Route path='/register'>
          {!user ? <Register onRegister={handleLogin} /> : <Redirect to='/' />}
        </Route>
        <Route path='/login'>
          {!user ? <Login onLogin={handleLogin} /> : <Redirect to='/' />}
        </Route>
        <Route path="/my-rides">
          {user ? <MyRides /> : <Redirect to='/register' />}
        </Route>
        <Route path="/create-rides">
          {user ? <CreateRides /> : <Redirect to='/register' />}
        </Route>
        <Route path="/my-bookings">
          {user ? <MyBookings /> : <Redirect to='/register' />}
        </Route>

        
        <Route exact path="/">
          {user ? <Home user={user} /> : <Redirect to='/register' />}
        </Route>
      </Switch>
      
    </div>
  
  )
}

export default App;

// i need my createbooking file to be integrated into my home file so i can have a button attached to each available ride to change the status of the ride, then have it moved to my bookings
// next i need updatebookings off the navbar and only available when in my bookings