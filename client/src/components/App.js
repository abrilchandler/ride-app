import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Navigation from './Navigation.js';
import Home from "./Home.js";
import CreateRides from './CreateRides.js';
import MyRides from "./MyRides.js";
import AvailableRides from './AvailableRides.js';


function App() {
  return (
    <div>
      
      <Navigation />
      <h1>Project client</h1>
      <Switch>
        <Route path="/create-rides">
          <CreateRides />
        </Route>
        <Route path="/my-rides">
          <MyRides />
        </Route>
        <Route path='/available-rides'>
          <AvailableRides />
        </Route>
        <Route path='/'>
          <Home />
        </Route>
      </Switch>
      
    </div>
  
  )
}

export default App;
