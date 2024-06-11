import "./landingpage.scss";
import TypewriterComponent from "typewriter-effect";
import { useNavigate } from "react-router-dom";
// @ts-ignore
import { Play } from "lucide-react";
const Landing = () => {
  const navigate = useNavigate();

  const user = true

  const handleStart = () => {
    if (!user) {
      navigate("/sign-in");
    } else {
      navigate("/start");
    }
  };
  return (
    <>
      <div className="bg bg-no-repeat bg-cover opacity-80 w-100 flex-box relative">
        <div className="flex-box w-100 flex-column flex-md-row">
          <div className="text-center overflow-hidden w-100 py-10 d-flex-box flex-column scroll-smooth">
            <div className="d-flex-box w-100 overflow-hidden opacity-100">
              <div className="d-flex-box">
                <div className="px-6 text-center text-white md:px-12 font-Bruno d-flex-box flex-column opacity-100">
                  <div className="wlcm mb-2 text-8xl font-weight-900 text-transparent bg-clip-text ">
                    Welcome <br /> to
                    <h2 className="text-5xl supt drop-shadow-sm shadow-black">
                      Violence
                      <span className="subt">AI</span>
                    </h2>
                  </div>
                  <p className="mb-6 font-weight-light text-primary font-weight-light drop-shadow-xl opacity-100">
                    Say goodbye to traditional Surveillance Management &
                    Pharmacies Location!
                    <br />
                    Our AI-Platform powered ensures precise and efficient
                    real-time pharmacies management, engagement and generation
                    personalization for pharmacists about their guards across
                    100+ smart countries and beautiful cities.
                    <br />
                    Join the revolution and experience the future of modern
                    Pharmacies with PharmaAI. This is your Gate for Pharmacies
                    Locations
                  </p>
                  <h2 className="tpw text-2xl pb-6 font-weight-bold text-transparent ">
                    <TypewriterComponent
                      options={{
                        strings: [
                          "#PharmaAI",
                          "#Map_Location",
                          "#Pharmacists_Management",
                        ],
                        autoStart: true,
                        loop: true,
                      }}
                    />
                  </h2>
                  <div className="mb-8 w-10 flex-box border rounded-lg shadow-lg shadow-sm--hover shadowred z-100 cursor-pointer inline-flex transition ease-linear text-base font-weight-normal text-center text-white bg-info hover-bg-hot-pink">
                    
                    <a
                      onClick={handleStart}
                      className="cursor-pointer inline-flex transition ease-linear items-center justify-center py-3 px-6 mr-3 text-base font-medium text-center text-white rounded-lg bg-blue-600 hover:bg-blue-700"
                    >
                      Get started
                      <svg
                        className="w-5 h-5 ml-2 -mr-1"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                          clipRule="evenodd"
                        ></path>
                      </svg>
                    </a>
                    <a
                      href="#demo"
                      className="bg-slate-100 font-semibold transition ease-linear text-slate-700 py-3 px-6 hover:bg-slate-300 rounded-lg cursor-pointer inline-flex items-center justify-center text-center"
                    >
                      <Play className="w-3 h-3 mr-2" fill="currentColor" />
                      See Demo
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Landing;
