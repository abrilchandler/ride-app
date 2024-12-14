import React, { useEffect, useState } from "react";
import { Switch, Route, Redirect} from "react-router-dom";
import Navigation from './Navigation.js';
import Home from "./Home.js";
import CreateRides from './CreateRides.js';
import MyRides from "./MyRides.js";
import AvailableRides from './AvailableRides.js';
import Login from './Login.js';
import Register from './Register.js';
import Header from './Header.js';
import ClaimedRides from './ClaimedRides.js';


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
        <Route path='/available-rides'>
          {user ? <AvailableRides /> : <Redirect to='/register' />}
        </Route>
        <Route path="/create-rides">
          {user ? <CreateRides /> : <Redirect to='/register' />}
        </Route>
        <Route>
          {user ? <Home /> : <Redirect to='/register' />}
        </Route>
        <Route path='/claimed-rides'>
          {user ? <ClaimedRides /> : <Redirect to='/register' />}
        </Route>
      </Switch>
      
    </div>
  
  )
}

export default App;
