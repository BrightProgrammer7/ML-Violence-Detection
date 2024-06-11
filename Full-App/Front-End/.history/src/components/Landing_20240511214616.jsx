import PhoneMockup from 'app/shared/components/phone/PhoneMockup';
import React from 'react';
import { Container, Row, Col, Card, CardBody, CardTitle, CardText, CardImg, Button } from 'reactstrap';
import './landingpage.scss';
import { Translate } from 'react-jhipster';
import TypewriterComponent from 'typewriter-effect';
import { useNavigate } from 'react-router-dom';
// @ts-ignore
import { Play } from 'lucide-react';

const Landing = () => {
  const navigate = useNavigate();

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
                      Pharma
                      <span className="subt">AI</span>
                    </h2>
                  </div>
                  <p className="mb-6 font-weight-light text-primary font-weight-light drop-shadow-xl opacity-100">
                    Say goodbye to traditional Pharmacist Management & Pharmacies Location!
                    <br />
                    Our AI-Platform powered ensures precise and efficient real-time pharmacies management, engagement and generation
                    personalization for pharmacists about their guards across 100+ smart countries and beautiful cities.
                    <br />
                    Join the revolution and experience the future of modern Pharmacies with PharmaAI. This is your Gate for Pharmacies
                    Locations
                  </p>
                  <h2 className="tpw text-2xl pb-6 font-weight-bold text-transparent ">
                    <TypewriterComponent
                      options={{
                        strings: ['#PharmaAI', '#Map_Location', '#Pharmacists_Management'],
                        autoStart: true,
                        loop: true,
                      }}
                    />
                  </h2>
                  <div className="mb-8 w-10 flex-box border rounded-lg shadow-lg shadow-sm--hover shadowred z-100 cursor-pointer inline-flex transition ease-linear text-base font-weight-normal text-center text-white bg-info hover-bg-hot-pink">
                    <a className="" onClick={() => navigate('/map')}>
                      <p className="pl-3 p-2 flex-box text-center font-weight-bolder text-xl w-100">
                        <Play className="w-3 fa-text-height mr-2" fill="currentColor" />
                        Explore the Map Now
                      </p>
                    </a>
                    <div
                      style={{
                        width: '50px',
                        minWidth: '20px',
                        height: '50px',
                        position: 'relative',
                        padding: '2px',
                        borderRadius: '15px',
                        background: '#fff',
                        boxShadow: '0px 25px 40px 0px rgba(0, 0, 0, 0.15)',
                        marginLeft: '30px',
                      }}
                    >
                      <img src="/content/images/uploads/qrcode.png" alt="Barcode" className="img-fluid" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <Col md={4} className="mb-1 d-flex justify-content-center">
            <div className="phone-mockup">
              <PhoneMockup>
                <img src="/content/images/uploads/app.png" alt="Mobile App Image" className="device-screen" />
              </PhoneMockup>
            </div>
          </Col>
        </div>
      </div>

      <Col>
        <Row className="my-5">
          <Col>
            <div>
              <Row>
                <div className="col">
                  <div className="card card-stats">
                    <div className="card-body">
                      <div className="row">
                        <div className="col">
                          <h5 className="card-title text-uppercase text-muted mb-0">REAL-TIME PHARMACY MANAGEMENT</h5>
                          <span className="h4 font-weight-bold mb-0">
                            Empower pharmacists with the ability to access and manage their pharmacy information in real-time.{' '}
                          </span>
                        </div>
                        <div className="col-auto">
                          <div className="icon icon-shape bg-gradient-red text-white rounded-circle shadow">
                            <i className="ni ni-active-40"></i>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Row>
              <Row>
                <div className="col">
                  <div className="card card-stats">
                    <div className="card-body">
                      <div className="row">
                        <div className="col">
                          <h5 className="card-title text-uppercase text-muted mb-0">USER-FRIENDLY PHARMACY LOCATOR</h5>
                          <span className="h4 font-weight-bold mb-0">
                            Enable users to explore and locate pharmacies on a map for convenient access to healthcare services.{' '}
                          </span>
                        </div>
                        <div className="col-auto">
                          <div className="icon icon-shape bg-gradient-orange text-white rounded-circle shadow">
                            <i className="ni ni-chart-pie-35"></i>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Row>
              <Row>
                <div className="col">
                  <div className="card card-stats">
                    <div className="card-body">
                      <div className="row">
                        <div className="col">
                          <h5 className="card-title text-uppercase text-muted mb-0">ADMINISTRATION MADE EASY</h5>
                          <span className="h4 font-weight-bold mb-0">
                            Streamline platform management for administrators, providing robust tools for efficient administration.{' '}
                          </span>
                        </div>
                        <div className="col-auto">
                          <div className="icon icon-shape bg-gradient-green text-white rounded-circle shadow">
                            <i className="ni ni-money-coins"></i>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Row>
              <Row>
                <div className="col">
                  <div className="card card-stats">
                    <div className="card-body">
                      <div className="row">
                        <div className="col">
                          <h5 className="card-title text-uppercase text-muted mb-0">EXPLORE PHARMACIES NEAR YOU</h5>
                          <span className="h4 font-weight-bold mb-0">
                            Discover and explore nearby pharmacies easily, ensuring convenient access to healthcare services wherever you
                            are.{' '}
                          </span>
                        </div>
                        <div className="col-auto">
                          <div className="icon icon-shape bg-gradient-info text-white rounded-circle shadow">
                            <i className="ni ni-chart-bar-32"></i>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Row>
            </div>
          </Col>
        </Row>
      </Col>
    </>
  );
};

export default Landing;