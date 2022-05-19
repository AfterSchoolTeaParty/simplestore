import express from "express";
import { setStorages, setFiles, getFiles, getStorages } from "./dbhandler.mjs";

const app = express()
const port = process.env.PORT || 3000;

app.use(express.urlencoded())
app.use(express.json())

app.get("/storages", async (req, res)=>{
    const data = await getStorages() 
    res.json(data)
})

app.get("/storages/:name", async (req, res)=>{
    const data = await getStorages(req.params.name)
    res.json(data)
})

app.post("/storages", async (req, res)=>{
    const data = {}
    if(req.body.name && req.body.passkey){
        data.name = req.body.name
        data.passkey = req.body.passkey
    } else {
        res.json({msg : "Failed to create new storage"})
    }
    await setStorages(data.name, data.passkey)
    res.json({msg : "Storage set"})
})

app.get("/files", async (req, res)=>{
    const data = await getFiles() 
    res.json(data)
})

app.get("/files/:name", async (req, res)=>{
    const data = await getFiles(req.params.name) 
    res.json(data)
})

app.post("/files", async (req, res)=>{
    const data = {}
    try{
        if(req.body.name && req.body.extension && req.body.storage && req.body.uploaded){
            data.name = req.body.name
            data.extension = req.body.extension
            data.storage = req.body.storage
            data.uploaded = req.body.uploaded
        } else {
            res.json({msg : "Failed to create new storage"})
        }
        await setFiles(data.name, data.extension, data.storage, data.uploaded)
        res.json({msg : "File set"})
    } catch(e){
        console.log(e)
    }
})

app.listen(port, ()=> console.log("It's now listening in port 3000"))