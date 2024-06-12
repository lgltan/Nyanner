// create lobby or join lobby

// initialize game state in DB

import React, { useState } from 'react'
import './lobby.css'

const Lobby = ({
    label,
    type,
    name,
    value,
    onChange,
    error,
    ...props
  }) => {
    return (
        <div className="lobby-container">
            <div className="form-input">
                <label className="input-label" htmlFor={lobbyName}>Create Lobby</label>
                <input
                    className="input"
                    type={type}
                    name={lobbyName}
                    value={value}
                    onChange={onChange}
                    {...props}
                    required
                />
                {error && <p className="error">{error}</p>}
            </div>
            <button>Create Lobby</button>

            <hr />

            <div className="form-input">
                <label className="input-label" htmlFor={lobbyID}>Join Lobby</label>
                <input
                    className="input"
                    type={type}
                    name={lobbyID}
                    value={value}
                    onChange={onChange}
                    {...props}
                    required
                />
                {error && <p className="error">{error}</p>}
            </div>
            <button>Join Lobby</button>
        </div>
    )
}