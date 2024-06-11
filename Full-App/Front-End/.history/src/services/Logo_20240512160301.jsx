import { useNavigate } from "react-router-dom";

function Logo() {
  const navigate = useNavigate();

  return (
    <div
      onClick={() => navigate("/")}
      className="w-48 h-10 flex-box cursor-pointer"
    >
      <img className="w-10 h-10 mx-1" src="logo.png" alt="logo" />
      <div className="px-4">
        <span className="text-3xl font-bold">Vigilant</span>
        <span className=" text-3xl font-light">Eye</span>
      </div>
    </div>
  );
}

export default Logo;
