import express from "express"
import mysql from "mysql"

const app = express()
const PORT = process.env.PORT

const db = mysql.createConnection({
    host:"localhost",
    user:"root",
    password:"root",
    database:"test"
})

app.listen(PORT, () => {
    console.log("Listening on port: ", PORT)
})

// add app.get here