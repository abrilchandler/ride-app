import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import NavBar from './NavBar.js';
import Home from "./Home.js";
import Contact from './Contact.js';
import About from "./About.js";

function App() {
  return (
    <div>
      
      <NavBar />
      <h1>Project client</h1>
      <Switch>
        <Route path="/contact">
          <Contact />
        </Route>
        <Route path="/about">
          <About />
        </Route>
        <Route path='/'>
          <Home />
        </Route>
      </Switch>
      
    </div>
  
  )
}

export default App;
