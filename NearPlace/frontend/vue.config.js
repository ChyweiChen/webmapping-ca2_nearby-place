module.exports = {
  // ...other vue-cli plugin options...
  pwa: {
    name: "Nearby Bar",
    themeColor: "#4DBA87",
    msTileColor: "#000000",
    appleMobileWebAppCapable: "yes",
    appleMobileWebAppStatusBarStyle: "black",
    icons: [
      {
        src: "./img/icons/android-chrome-192x192.png",
        sizes: "192x192",
        type: "image/png"
      },
      {
        src: "./img/icons/android-chrome-512x512.png",
        sizes: "512x512",
        type: "image/png"
      }
    ],
    // configure the workbox plugin
    workboxPluginMode: "InjectManifest",
    workboxOptions: {
      // swSrc is required in InjectManifest mode.
      swSrc: "src/registerServiceWorker.js"
      // ...other Workbox options...
    }
  }
};
