function calibrateReady(e) {
  let req = new XMLHttpRequest();
  const url = "http://localhost/detections/calibrate_ready";
  req.open("GET", url);
  req.send();
  
  req.onreadystatechange = (e) => {
    let status;
    if (req.readyState == 4 && req.status == 200) {
      let caliReady_res = JSON.parse(req.responseText);
      if (caliReady_res.status == "ready") {
        status = "Listo para calibrar"
      } else if (caliReady_res.status == "error") {
        status = "Faltan datos para calibrar, intente de nuevo mas tarde"
      }
      const html = `<p> ${status} </p>`;
      document.querySelector('.response_calibrateReady').innerHTML = html;
    } else {
      document.querySelector('.response_calibrateReady').innerHTML = "<p>ERROR DE PREPARACIÓN</p>";
    }
  }
}

function calibrate(e) {
  let req = new XMLHttpRequest();
  const url = "http://localhost/detections/calibrate";
  req.open("GET", url);
  req.send();

  req.onreadystatechange = (e) => {
    let status;
    if (req.readyState == 4 && req.status == 201) {
      let calibrate_res = JSON.parse(req.responseText);
      console.log(calibrate_res)
      if (calibrate_res[1]) {
        status = "Calibración lista"
        connectWs()
      } else if (req.status == 304) {
        status = "Error al calibrar, intente nuevamente"
      }
      const html = `<p> ${status} </p>`;
      document.querySelector('.response_calibrate').innerHTML = html;
    } else {
      document.querySelector('.response_calibrate').innerHTML = "<p>ERROR DE CALIBRACIÓN</p>";
    }
  }
}

// Socket
function connectWs() {
  ws = new WebSocket("ws://localhost/detections/get_report_socket");
  ws.onmessage = function(event) {
    console.log(event)
    //console.log(JSON.parse(event.data));
  }
  ws.onclose = function(event) {
    console.log("WebSocket closed");
  }
}