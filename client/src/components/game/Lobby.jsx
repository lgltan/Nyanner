import React, { useState } from "react";
import "./lobby.css";
import api from "../../services/api";
import { fetchToken } from "../../services/authProvider";
import FormInput from "../form/FormInput";
import {
  validateLobbyCode,
  validateBotDifficulty,
} from "../../services/validation";

const Lobby = ({
  label,
  type,
  name,
  value,
  onChange,
  error,
  inGameCheck,
  ...props
}) => {
  const [lobbyCode, setLobbyCode] = useState("");
  const [diffLvl, setDiffLvl] = useState(0);
  const [lobbyError, setLobbyError] = useState(null);
  const [botsError, setBotsError] = useState(null);

  const createLobby = async () => {
    try {
      const token = fetchToken();
      const response = await api.post(
        "/lobby/create",
        {},
        {
          headers: {
            Content_Type: "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      inGameCheck(true);
    } catch (error) {
      console.error(error);
    }
  };

  const joinLobby = async () => {
    if (validateLobbyCode(lobbyCode)) {
      try {
        const token = fetchToken();
        const response = await api.put(
          `/lobby/join/${lobbyCode}`,
          {},
          {
            headers: {
              Content_Type: "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );
        inGameCheck(true);
      } catch (error) {
        console.error(error);
      }
    }
    setLobbyError("Invalid lobby code");
  };

  const playBots = async () => {
    if (validateBotDifficulty(diffLvl)) {
      try {
        const token = fetchToken();
        const request = { diffLvl: diffLvl };
        const response = await api.post("/lobby/create/bots", request, {
          headers: {
            Content_Type: "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
        inGameCheck(true);
      } catch (error) {
        console.error(error);
      }
    }
    else {
        setBotsError("Invalid difficulty level (1-10)");
    }
  };

  return (
    <div className="lobby-container">
      <button className="create-lobby primary-btn mt-10" onClick={createLobby}>
        Create Lobby
      </button>
      <hr />
      <div className="join-lobby">
        <FormInput
          className="input"
          label="Lobby Code"
          type="text"
          name="lobbyCode"
          value={lobbyCode}
          error={lobbyError}
          onChange={(e) => setLobbyCode(e.target.value)}
          {...props}
          isRequired={true}
        />
        <button className="primary-btn" onClick={joinLobby}>
          Join Lobby
        </button>
        {/* <label className="input-label" htmlFor={name}>
          Join Lobby
        </label>
        <input
          className="input"
          type={type}
          name={name}
          value={lobbyCode}
          onChange={(e) => setLobbyCode(e.target.value)}
          {...props}
          required
        /> */}
        {error && <p className="error">{error}</p>}
      </div>
      <div className="play-bots">
        <FormInput
          className="input"
          label="Difficulty Level"
          type="number"
          name="diffLvl"
          value={diffLvl}
          error={botsError}
          onChange={(e) => setDiffLvl(e.target.value)}
          {...props}
        />
        {/* <input
            className="input"
            type="number"
            value={diffLvl}
            onChange={(e) => setDiffLvl(e.target.value)}
            required
        /> */}
        <button className="primary-btn" onClick={playBots}>
          Play Bots
        </button>
      </div>
    </div>
  );
};

export default Lobby;
