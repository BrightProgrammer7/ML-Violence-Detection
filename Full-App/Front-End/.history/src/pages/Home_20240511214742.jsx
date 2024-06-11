import Landing from "../components/Landing";

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
