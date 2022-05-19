import { initializeApp } from "firebase/app";
import { getDatabase, get, set, ref, child } from "firebase/database"
import firebaseConfig from "./config.mjs";

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// storage setter
export async function setStorages(name, passkey){
	await set(ref(db, "storages/" + name), {
		name,
		passkey
	})
}
// file setter
export async function setFiles(name, extension, storage, uploaded){
	await set(ref(db, "files/" + name), {
		name,
		extension,
		file : `${name}.${extension}`,
		storage,
		uploaded
	})
}

// storage getter
export async function getStorages(name=null){
	const dbRef = ref(db)
	let snapshot;
	if(name){
		snapshot = await get(child(dbRef, `storages/${name}`))
	}
	else {
		snapshot = await get(child(dbRef, `storages`))
	}

	if(snapshot.exists()){
		return snapshot.val()
	} else {
		return null;
	}
}

// file getter
export async function getFiles(name = null){
	const dbRef = ref(db)
	let snapshot;
	
	if(name){
		snapshot = await get(child(dbRef, `files/${name}`))
	}
	else {
		snapshot = await get(child(dbRef, `files`))
	}

	if(snapshot.exists()){
		return snapshot.val()
	} else {
		return null;
	}
}