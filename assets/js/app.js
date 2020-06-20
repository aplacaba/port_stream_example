// We need to import the CSS so that webpack will load it.
// The MiniCssExtractPlugin is used to separate it out into
// its own CSS file.
import "../css/app.scss"

// webpack automatically bundles all modules in your
// entry points. Those entry points can be configured
// in "webpack.config.js".
//
// Import deps with the dep name or local files with a relative path, for example:
//
//     import {Socket} from "phoenix"
//     import socket from "./socket"
//
import "phoenix_html"
import socket from './socket'


let channel = socket.channel("image:stream", {})
channel.join()
                    .receive("ok", resp => { console.log("Joined successfully", resp) })
                    .receive("error", resp => { console.log("Unable to join", resp) })


channel.on("image_data", (payload) => {
  console.log('Image received')
  const img = document.querySelector('#b64_image_data')
  img.src = `data:image/jpg;base64, ${payload.data}`
})


window.onload = function () {
  const startStreamBtn = document.querySelector('#start_stream')
  const stopStreamBtn = document.querySelector('#stop_stream')

  startStreamBtn.addEventListener('click', () => {
    channel.push('start_stream')
  })

  stopStreamBtn.addEventListener('click', () => {
    channel.push('stop_stream')
  })
}
