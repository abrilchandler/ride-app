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
                >Available Rides and Haulers</NavLink>
              </div>
            
            <div className="navLinks">
              <NavLink 
              to="/my-rides"
              exact
              activeStyle={{
                background: "darkred",
              }}
              >My Rides</NavLink>
            </div>

        <div className="navLinks">
          <NavLink 
          to="/create-rides"
          exact
          activeStyle={{
            background: "darkred",
          }}
          >Create Ride</NavLink>
        </div>
        
      </div>

    )
  }

  export default NavBar;