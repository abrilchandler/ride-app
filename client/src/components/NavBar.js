import React from "react";
import {NavLink} from "react-router-dom";

  function NavBar() {
    return (
          <div className="navBar">
              <div className="navLinks">
                <NavLink
                to="/"
                exact
                activeStyle={{
                  background: "darkred",
                }}
                >Home</NavLink>
              </div>
            
            <div className="navLinks">
              <NavLink 
              to="/contact"
              exact
              activeStyle={{
                background: "darkred",
              }}
              >Contact</NavLink>
            </div>

        <div className="navLinks">
          <NavLink 
          to="/about"
          exact
          activeStyle={{
            background: "darkred",
          }}
          >About</NavLink>
        </div>
        
      </div>

    )
  }

  export default NavBar;