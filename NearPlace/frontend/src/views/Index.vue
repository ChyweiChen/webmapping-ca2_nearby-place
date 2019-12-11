<template>
  <div>
    <!-- <div v-if="errorStr">
      Sorry, but the following error occurred: {{ errorStr }}
    </div>
    <div v-if="gettingLocation">
      <i>Getting your location...</i>
    </div> -->
    <div id="map" ref="map"></div>
    <div class="distance" v-show="places.length != 0">
      <p>Nearby {{ category }}:</p>
      <div v-for="(place, index) of places" :key="index">
        <div>{{ place.name }}</div>
        <div>{{ parseFloat(place.distance).toFixed(0) }}m</div>
      </div>
    </div>
    <div class="button-group">
      <button
        :class="{ active: category == 'bar' }"
        title="Show nearby bars"
        @click="
          category = 'bar';
          getNearby();
        "
      >
        Bars
      </button>
      <button
        :class="{ active: category == 'restaurant' }"
        title="Show nearby restaurant"
        @click="
          category = 'restaurant';
          getNearby();
        "
      >
        Restaurants
      </button>
      <button
        :class="{ active: category == 'station' }"
        title="Show nearby stations"
        @click="
          category = 'station';
          getNearby();
        "
      >
        Stations
      </button>
      <button
        :class="{ active: category == 'toilets' }"
        title="Show nearby toilets"
        @click="
          category = 'toilets';
          getNearby();
        "
      >
        Toilets
      </button>
    </div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet-routing-machine";

import { getNearbyPlaceApi } from "@/api.js";
import locationImg from "@/assets/img/position.png";

export default {
  mounted() {
    // if (!("geolocation" in navigator)) {
    //   this.errorStr = "Geolocation is not available.";
    //   return;
    // }
    // this.gettingLocation = true;
    // // get position
    // navigator.geolocation.getCurrentPosition(
    //   pos => {
    //     this.gettingLocation = false;
    //     this.location = pos;
    //   },
    //   err => {
    //     this.gettingLocation = false;
    //     this.errorStr = err.message;
    //   }
    // );

    // const [lat, lng] = [
    //   this.location.coords.latitude,
    //   this.location.coords.longitude
    // ];

    const [lat, lng] = [53.3322511, -6.2575719];
    const zoom = 15;
    const accessToken =
      "pk.eyJ1IjoiY2h5d2VpY2hlbiIsImEiOiJjazN1ZjlucDAwYzFpM2VxOGpsMHhyaTI4In0.ckLW5vTO6u2-omo0kwnGAA";
    this.map = L.map("map").setView([lat, lng], zoom);
    L.tileLayer(
      `https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${accessToken}`,
      {
        attribution:
          'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: "mapbox/streets-v11",
        minZoom: 12,
        accessToken: accessToken
      }
    ).addTo(this.map);
    /** POSITION MARKER BEGIN **/
    // position Icon
    let positionIcon = L.icon({
      iconUrl: locationImg,
      iconSize: [40, 40],
      iconAnchor: [20, 32],
      popupAnchor: [0, -20]
    });
    // position Marker Popup
    let positionPopup = L.popup().setContent(
      `<div class="position">Your position is <span>( ${lat}, ${lng} )</span></div>`
    );
    L.marker([lat, lng], {
      icon: positionIcon
    })
      .bindPopup(positionPopup)
      .addTo(this.map);
    this.lat = lat;
    this.lng = lng;
    /** POSITION MARKER END **/
  },
  data() {
    return {
      lat: 0,
      lng: 0,
      places: [],
      gettingLocation: false,
      errorStr: "",
      location: null,
      category: "",
      map: null,
      controls: []
    };
  },
  methods: {
    async getNearby() {
      for (let index in this.controls) {
        this.map.removeControl(this.controls[index]);
      }
      /** ROUTING BEGIN */
      const colors = ["RED", "ORANGE", "GREEN", "BLUE", "INDIGO", "VIOLET"];
      const accessToken =
        "pk.eyJ1IjoiY2h5d2VpY2hlbiIsImEiOiJjazN1ZjlucDAwYzFpM2VxOGpsMHhyaTI4In0.ckLW5vTO6u2-omo0kwnGAA";
      // get nearby places
      await getNearbyPlaceApi(this.category, this.lat, this.lng).then(res => {
        this.places = res.data.slice(0, 6);
      });
      // create control
      for (let index in this.places) {
        let waypoints = [
          L.latLng(this.lat, this.lng),
          L.latLng(
            this.places[index].waypoint.lat,
            this.places[index].waypoint.lng
          )
        ];
        let name = this.places[index].name;
        let distance = this.places[index].distance;
        this.controls.push(
          L.Routing.control({
            waypoints: waypoints,
            router: L.Routing.mapbox(accessToken),
            fitSelectedRoutes: false,
            plan: L.Routing.plan(waypoints, {
              draggableWaypoints: false,
              addWaypoints: false,
              createMarker: function(i, wp) {
                let best = index == 0 ? "best" : "";
                // if marker is user position
                if (i == 0) {
                  return;
                }
                let routerMarker = L.marker(wp.latLng, {
                  draggable: false
                }).bindTooltip(
                  `<span class="bold ${best}">${name}</span> [${parseFloat(
                    distance
                  ).toFixed(0)}m]`
                );
                return routerMarker;
              }
            }),
            lineOptions: {
              styles: [
                { color: "black", opacity: 0.3, weight: 9 },
                { color: "white", opacity: 0.8, weight: 6 },
                { color: colors[index], opacity: 1, weight: 2 }
              ]
            }
          }).addTo(this.map)
        );
      }
      // // add to map
      // for (let index in controls) {
      //   L.Routing.control(controls[index]).addTo(this.$refs.map);
      // }
      /** ROUTING END */
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/assets/scss/index.scss";
</style>
