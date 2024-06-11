import { initializeApp } from "firebase/app";
import {
	getAuth,
	GoogleAuthProvider,
	GithubAuthProvider,
	TwitterAuthProvider,
} from "firebase/auth";

import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

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

const firebaseConfig = {
	apiKey: import.meta.env.VITE_API_KEY,
	authDomain: "teethsegmentation-42aaa.firebaseapp.com",
	projectId: "teethsegmentation-42aaa",
	storageBucket: "teethsegmentation-42aaa.appspot.com",
	messagingSenderId: import.meta.env.VITE_MESSAGING_SENDER_ID,
	appId: import.meta.env.VITE_APP_ID,
	measurementId: import.meta.env.VITE_MEASUREMENT_ID,
};

const googleProvider = new GoogleAuthProvider();
const githubProvider = new GithubAuthProvider();
const twitterProvider = new TwitterAuthProvider();

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const provider = {
	"google.com": googleProvider,
	"github.com": githubProvider,
	"twitter.com": twitterProvider,
};