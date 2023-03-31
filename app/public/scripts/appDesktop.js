let intervalIdGetReport = null
let intervalIdCaliReady = null
let flagReadyToCalibrate = false

intervalIdCaliReady = setInterval(calibrateReady, 3000);

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
        flagReadyToCalibrate = true
        clearInterval(intervalIdCaliReady)
      } else if (caliReady_res.status == "error") {
        status = `
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>`
        flagReadyToCalibrate = false
      }
      document.querySelector('.response_calibrateReady').innerHTML = status;
    }
  }
}


function calibrate(e) {
  let statusHtml;
  let req = new XMLHttpRequest();
  const url = "http://localhost/detections/calibrate";

  const renderStatus = (html) => {
    document.querySelector('.response_calibrate').innerHTML = html;
  }

  if (flagReadyToCalibrate == false) {
    statusHtml = "<p> Preparando la calibración... </p>";
    renderStatus(statusHtml);
    return statusHtml;
  } else {
    req.open("GET", url);
    req.send();
    req.onreadystatechange = (e) => {
      if (req.readyState == 4 && req.status == 201) {
        let calibrate_res = JSON.parse(req.responseText);
        if (calibrate_res[1]) {
          statusHtml = "<p> Calibración lista </p>"
          intervalIdGetReport = setInterval(getReport, 3000);
        } else if (req.status == 304) {
          statusHtml = "<p> Error al calibrar, intente nuevamente </p>";
        }
        renderStatus(statusHtml);
      } else {
        statusHtml = "<p> ERROR DE CALIBRACIÓN. Prepare la calibración nuevamente</p>";
        renderStatus(statusHtml);
      }
    }
  }
}


function getReport() {
  let req = new XMLHttpRequest();
  const url = "http://localhost/detections/get_report";
  req.open("GET", url);
  req.send();
  req.onreadystatechange = (e) => {
    if (req.readyState == 4 && req.status == 200) {

      let report_res = JSON.parse(req.responseText);

      if (report_res.calibrateStatus == true){
        let liPositionsHtml = `<ul class="list-group">`
        let liPresencesHtml = `<ul class="list-group">`;

        let positions = report_res.position
        let presences = report_res.presence

        for (const property in positions) {
          if (positions[property] == true) {
            liPositionsHtml += `<li class="list-group-item list-group-item-info">${property}: En posición</li>`;
          } else if (positions[property] == false){
            liPositionsHtml += `<li class="list-group-item list-group-item-danger"> ${property}: Fuera de posición </li>`;
          } else return {error:'FATAL ERROR'}
        }

        for (const property in presences) {
          if (presences[property] == true){
            liPresencesHtml += `<li <li class="list-group-item list-group-item-info">${property}: Detectado correctamente</li>`;
          } else if (positions[property] == false) {
            liPresencesHtml += `<li <li class="list-group-item list-group-item-danger">${property}: No se pudo detectar</li>`;
          } else return {error:'FATAL ERROR'}
        }

        document.querySelector('.res_presences').innerHTML = liPresencesHtml + "</ul><br>";
        document.querySelector('.res_positions').innerHTML = liPositionsHtml + "</ul>";

      }
    }
  }
}