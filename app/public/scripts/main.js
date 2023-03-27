
let intervalId = null

function calibrateReady(e) {
  try {
    window.clearInterval(intervalId)
  } catch (error) {
    console.log(error)
  }
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
    let statusHtml;
    if (req.readyState == 4 && req.status == 201) {
      let calibrate_res = JSON.parse(req.responseText);
      if (calibrate_res[1]) {
        statusHtml = "<p> Calibración lista <p/>"
        intervalId = setInterval(getReport, 1000);
      } else if (req.status == 304) {
        statusHtml = "<p> Error al calibrar, intente nuevamente <p/>"
      }
      document.querySelector('.response_calibrate').innerHTML = statusHtml;
    } else {
      document.querySelector('.response_calibrate').innerHTML = "<p> ERROR DE CALIBRACIÓN </p>";
    }
  }
}

// Pseudosocket con XML
function getReport() {
  let req = new XMLHttpRequest();
  const url = "http://localhost/detections/get_report";
  req.open("GET", url);
  req.send();
  req.onreadystatechange = (e) => {
    if (req.readyState == 4 && req.status == 200) {
      let liPositionsHtml = "<ul>", liPresencesHtml = "<ul>";
      let report_res = JSON.parse(req.responseText);
      let positions = report_res.position
      let presences = report_res.presence
      for (const property in positions) {
        liPositionsHtml += `<li>${property}: ${positions[property]}</li>
        `;
      }
      for (const property in presences) {
        liPresencesHtml += `<li>${property}: ${presences[property]}</li>
        `;
      }
      document.querySelector('.res_presences').innerHTML = liPresencesHtml + "</ul>";
      document.querySelector('.res_positions').innerHTML = liPositionsHtml + "</ul>";
    }
  }
}

// Socket
/* 
function connectWs() {
  ws = new WebSocket("ws://localhost/detections/get_report_socket");
  ws.onmessage = function(event) {
    console.log(event)
    //console.log(JSON.parse(event.data));
  }
  ws.onclose = function(event) {
    console.log("WebSocket closed");
  }
} */