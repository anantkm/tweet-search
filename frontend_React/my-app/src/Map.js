// import React, { useEffect, useRef } from 'react';
// import L from 'leaflet';
// import 'leaflet/dist/leaflet.css';
// import 'leaflet.markercluster/dist/MarkerCluster.css';
// import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
// import markerIcon from 'leaflet/dist/images/marker-icon.png';
// import markerShadow from 'leaflet/dist/images/marker-shadow.png';
// import MarkerClusterGroup from 'leaflet.markercluster';

// function Map({ tweets }) {
//   const mapRef = useRef(null);

//   useEffect(() => {
//     // initialize map and set its center
//     const map = L.map(mapRef.current);

//     // add OpenStreetMap tile layer to map
//     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//       attribution:
//         'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
//       maxZoom: 18,
//     }).addTo(map);

//     // add markers to map for each tweet with valid geolocation data
//     const markers = L.markerClusterGroup();
//     tweets.forEach((tweet) => {
//       const { Latitude, Longitude } = tweet.Geolocation;
//       if (Latitude && Longitude) {
//         const marker = L.marker([Latitude, Longitude], {
//           icon: L.icon({
//             iconUrl: markerIcon,
//             shadowUrl: markerShadow,
//             iconAnchor: [12, 41],
//             popupAnchor: [1, -34],
//           }),
//         }).bindPopup(tweet.Text);
//         markers.addLayer(marker);
//       }
//     });
//     map.addLayer(markers);

//     // fit the map bounds to the markers
//     if (markers.getLayers().length > 0) {
//       const bounds = markers.getBounds();
//       map.fitBounds(bounds);
//     } else {
//       // set default center and zoom level if there are no markers
//       map.setView([0, 0], 2);
//     }

//     // clean up map when component unmounts
//     return () => {
//       map.remove();
//     };
//   }, [tweets]);

//   return <div ref={mapRef} style={{ width: '700px', height: '400px' }} />;
// }

// export default Map;


// in below code I have added dummy location and just for the project illustration. 
import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import MarkerClusterGroup from 'leaflet.markercluster';

function Map({ tweets }) {
  const mapRef = useRef(null);

  useEffect(() => {
    // initialize map and set its center
    const map = L.map(mapRef.current);

    // add OpenStreetMap tile layer to map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      maxZoom: 18,
    }).addTo(map);

    // add markers to map for each tweet
    const markers = L.markerClusterGroup();
    tweets.forEach((tweet) => {
      const { Geolocation } = tweet;
      let latitude, longitude;
      if (Geolocation && Geolocation.Latitude && Geolocation.Longitude) {
        // use geolocation if available
        latitude = Geolocation.Latitude;
        longitude = Geolocation.Longitude;
      } else {
        // generate random location and map to specific city/region
        const randomLocation = Math.floor(Math.random() * 7);
        switch (randomLocation) {
          case 0:
            // London, England
            latitude = 51.5072 + Math.random() * 0.1 - 0.05;
            longitude = -0.1276 + Math.random() * 0.1 - 0.05;
            break;
          case 1:
            // Delhi, India
            latitude = 28.7041 + Math.random() * 0.1 - 0.05;
            longitude = 77.1025 + Math.random() * 0.1 - 0.05;
            break;
          case 2:
            // Bangalore, India
            latitude = 12.9716 + Math.random() * 0.1 - 0.05;
            longitude = 77.5946 + Math.random() * 0.1 - 0.05;
            break;
          case 3:
            // Sydney, Australia
            latitude = -33.8688 + Math.random() * 0.1 - 0.05;
            longitude = 151.2093 + Math.random() * 0.1 - 0.05;
            break;
          case 4:
            // San Francisco, United States
            latitude = 37.7749 + Math.random() * 0.1 - 0.05;
            longitude = -122.4194 + Math.random() * 0.1 - 0.05;
            break;
          case 5:
            // Mumbai, India
            latitude = 19.076 + Math.random() * 0.1 - 0.05;
            longitude = 72.8777 + Math.random() * 0.1 - 0.05;
            break;
          default:
            // Dallas, United States
            latitude = 32.7767 + Math.random() * 0.1 - 0.05;
            longitude = -96.797 + Math.random() * 0.1 - 0.05;
        }
      }
      const marker = L.marker([latitude, longitude], {
        icon: L.icon({
          iconUrl: markerIcon,
          shadowUrl: markerShadow,
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
        }),
      }).bindPopup(tweet.Text);
      markers.addLayer(marker);
    });
    map.addLayer(markers);

    // fit the map bounds to the markers
    if (markers.getLayers().length > 0) {
      const bounds = markers.getBounds();
      map.fitBounds(bounds);
    } else {
      // set default center and zoom level if there are no markers
      map.setView([0, 0], 2);
    }

    // clean up map when component unmounts
    return () => {
      map.remove();
    };
  }, [tweets]);

  // return <div ref={mapRef} style={{ width: '700px', height: '400px' }} />;
  return <div ref={mapRef} style={{ width: '100%', height: '100%' }} />;


}

export default Map;

