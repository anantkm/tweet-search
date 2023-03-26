import React, { useState } from 'react';
import axios from 'axios';
import { Input, Button, Select, Row, Col } from 'antd';
import Map from './Map';
import 'leaflet/dist/leaflet.css';

const { Option } = Select;

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('lucene');
  const [searchResults, setSearchResults] = useState([]);
  // const [tweets, setTweets] = useState([]);
  const [tweets, setTweets] = useState([]);





  const handleSelectChange = (value) => {
    setSearchType(value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // axios.get(`http://127.0.0.1:8080/search?search_query=${searchQuery}&k=100&search_type=${searchType}`)
    axios.get(`http://class-050.cs.ucr.edu:8888/search?search_query=${searchQuery}&k=100&search_type=${searchType}`)
      .then((response) => {
        console.log(response.data);
        const dataArray = JSON.parse(response.data);
        setSearchResults(dataArray);
        setTweets(dataArray);
        // setTweets(Array.isArray(response.data) ? response.data : []);
        document.querySelector('.map-container').style.opacity = '100';
        document.querySelector('.container').style.display = 'block';
      //   const mapContainer = document.querySelector('.map-container');
      //   if (mapContainer) {
      //     mapContainer.style.opacity = '100';
      //   }

      //   const container = document.querySelector('.container');
      //   if (container) {
      //     container.style.display = 'block';
      //   }
      })
      .catch((error) => {
          console.log(error);
        });
  };

  const handleSearchQueryChange = (event) => {
    setSearchQuery(event.target.value);
  };
  const renderTweetText = (text, tweetUrl) => {
    const parts = text.split(tweetUrl);
    return (
      <>
        {parts[0]}
        <a href={tweetUrl} target="_blank" rel="noopener noreferrer">
          {tweetUrl}
        </a>
        {parts[1]}
      </>
    );
  };


  return (
    <div className="container">
      <h1 className="text-center mb-4">Covid 19 related Tweet Search Engine</h1>
      <form onSubmit={handleSubmit}>
        <Row align="middle" style={{ marginBottom: "20px" }}>
          <Col flex={1}>
            <Input placeholder="Enter your search query" value={searchQuery} onChange={handleSearchQueryChange} />
          </Col>
          <Col>
            <Select value={searchType} onChange={handleSelectChange} style={{ width: 120 }}>
              <Option value="lucene">Lucene</Option>
              <Option value="bert">BERT</Option>
            </Select>
          </Col>
          <Col style={{ marginLeft: "10px" }}>
            <Button type="primary" htmlType="submit" className="btn btn-lg">Search</Button>
          </Col>
        </Row>
      </form>
      <div className="map-container">
        <div className="test">
          Geolocating the Twittersphere
        </div>
        <Map tweets={tweets} />
      </div>
      {Array.isArray(tweets) && tweets.length > 0 ? (
        <>

          <div className="search-results mt-4">
            {tweets.map((result) => (
              <div key={result.id} className="search-result mb-4">
                <a href={result['Tweet URL']} target="_blank" rel="noopener noreferrer" className="search-result-title">{result.Text.replace(result['Tweet URL'], `<a href="${result['Tweet URL']}" target="_blank">${result['Tweet URL']}</a>`)}</a>
                <p className="search-result-snippet">{result.User} - {result.Timestamp}</p>
                {result.Geolocation ? (
                  <p className="search-result-geolocation">
                    {result.Geolocation.Latitude && result.Geolocation.Longitude ? (
                      <p>
                        Latitude:<span> {result.Geolocation.Latitude}</span> Longitude:<span> {result.Geolocation.Longitude}</span>
                      </p>
                    ) : (
                      <span>User has not shared the Location</span>
                    )}
                  </p>
                ) : (
                  <p className="search-result-geolocation"><span>Location is empty</span></p>
                )}
              </div>
            ))}
          </div>
        </>
      ) : (
        <p className="text-center mt-4">Please enter a search query and select the model.</p>
      )}
    </div>
  );

}

export default App;