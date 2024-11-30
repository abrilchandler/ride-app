import React from "react";
import {NavLink} from "react-router-dom";


  function Navigation() {
    return (
      
                  <div className="navBar">
                    <h1 className="navName">Site Name</h1>

                      <div className="navLinks">
                        <NavLink
                        to="/"
                        exact
                        activeStyle={{
                          background: "white",
                        }}
                        >Home</NavLink>
                      </div>
                    
                    <div className="navLinks">
                      <NavLink 
                      to="/available-rides"
                      exact
                      activeStyle={{
                        background: "white",
                      }}
                      >Available Ride</NavLink>
                    </div>  

                    <div className="navLinks">
                      <NavLink 
                      to="/create-rides"
                      exact
                      activeStyle={{
                        background: "white",
                      }}
                      >Create Ride</NavLink>
                    </div>

                    
                    <div className="navLinks">
                      <NavLink 
                      to="/my-rides"
                      exact
                      activeStyle={{
                        background: "white",
                      }}
                      >My Rides</NavLink>
                    </div>
                </div>
    )
  }

export default Navigation;