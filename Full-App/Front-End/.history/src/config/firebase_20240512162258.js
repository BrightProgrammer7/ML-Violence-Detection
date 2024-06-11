// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import {
	getAuth,
	GoogleAuthProvider,
	GithubAuthProvider,
	TwitterAuthProvider,
} from "firebase/auth";


// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA5-nu6UIlIg9wEBHYboq7ItOgIgWrcxo4",
  authDomain: "vigilanteye-badd5.firebaseapp.com",
  projectId: "vigilanteye-badd5",
  storageBucket: "vigilanteye-badd5.appspot.com",
  messagingSenderId: "981688284903",
  appId: "1:981688284903:web:4821b4c70f5c65b71e9442"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// TODO: Add SDKs for Firebase products that you want to use
export const auth = getAuth(app);

const googleProvider = new GoogleAuthProvider();
const githubProvider = new GithubAuthProvider();
const twitterProvider = new TwitterAuthProvider();

export const provider = {
	"google.com": googleProvider,
	"github.com": githubProvider,
	"twitter.com": twitterProvider,
};