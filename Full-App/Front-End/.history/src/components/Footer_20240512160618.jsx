import "./footer.scss";

import Logo from "@/services/Logo";
import Copyright from "@/services/Copyright";
import Social from "@/services/Social";

const Footer = () => {
  // const navigate = useNavigate();
  return (
    <div className="footer page-content text-light">
      <div className="footer w-full bottom-0 px-5 py-10 flex-box flex-col bg-background text-foreground scroll-smooth text-center">
        <div className="bottom-footer w-full flex-box justify-around flex-col lg:flex-row flex-end lg:px-28">
          <Logo />
          <Copyright />
          <Social />
        </div>
      </div>
    </div>
  );
};
export default Footer;
