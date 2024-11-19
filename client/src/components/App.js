import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import NavBar from './NavBar.js';
import Home from "./Home.js";
import CreateRides from './CreateRides.js';
import MyRides from "./MyRides.js";

function App() {
  return (
    <div>
      
      <NavBar />
      <h1>Project client</h1>
      <Switch>
        <Route path="/create-rides">
          <CreateRides />
        </Route>
        <Route path="/my-rides">
          <MyRides />
        </Route>
        <Route path='/'>
          <Home />
        </Route>
      </Switch>
      
    </div>
  
  )
}

export default App;
