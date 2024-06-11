import Footer from "@/components/Footer";
import Header from "@/components/Header";
import Landing from "@/components/Landing";

export const Home = () => {
  return (
    <>
      <Header />
      <div className="w-full flex flex-col">
        <Landing />
      </div>
      <Footer />
    </>
  );
};
