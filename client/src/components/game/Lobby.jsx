// create lobby or join lobby

// initialize game state in DB

import React, { useState } from 'react'
import './lobby.css'

const Lobby = () => {
    return (
        <div className="lobby-container">
            <div className="button-container">
                <button>Create Lobby</button>
                <button>Join Lobby</button>
            </div>
            {/* toggle between create lobby and join lobby */}
            <div className="create-lobby-container">
                
            </div>
            <div className="join-lobby-container">

            </div>
        </div>
    )
}