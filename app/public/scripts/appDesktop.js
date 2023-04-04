let intervalIdGetReport = null
let intervalIdCaliReady = null
let flagReadyToCalibrate = false

intervalIdCaliReady = setInterval(calibrateReady, 4000);

async function calibrateReady() {
  let req = new XMLHttpRequest();
  const url = "http://localhost/detections/calibrate_ready";
  req.open("GET", url);
  req.send();
  
  req.onreadystatechange = (e) => {
    let status;
    if (req.readyState == 4 && req.status == 200) {
      let caliReady_res = JSON.parse(req.responseText);
      if (caliReady_res.status == "ready") {
        status = "&nbsp; ¡Ready to calibrate!"
        flagReadyToCalibrate = true
        document.querySelector('.response_calibrateReady').innerHTML = status;
        clearInterval(intervalIdCaliReady)
      }
    }
  }
}


function calibrate(e) {
  let statusHtml;
  let req = new XMLHttpRequest();
  const url = "http://localhost/detections/calibrate";

  if (flagReadyToCalibrate == true) {
    req.open("GET", url);
    req.send();
    req.onreadystatechange = (e) => {
      if (req.readyState == 4 && req.status == 201) {
        let calibrate_res = JSON.parse(req.responseText);
        if (calibrate_res[1]) {
          statusHtml = "&nbsp; Calibrate ready"
          intervalIdGetReport = setInterval(getReport, 3000);
        } else {
          statusHtml = "Error al calibrar, intente nuevamente";
        }
        document.querySelector('.response_calibrateReady').innerHTML = statusHtml;
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
        let liPositionsHtml = `<ul class="list-group">`;
        let liPresencesHtml = `<ul class="list-group">`;

        let positions = report_res.position;
        let presences = report_res.presence;

        for (const property in positions) {
          if (property !== "Box"){
            if (positions[property] == true) {
              liPositionsHtml += `<li class="list-group-item list-group-item-info">${property}: In position</li>`;
            } else if (positions[property] == false){
              liPositionsHtml += `<li class="list-group-item list-group-item-danger"> ${property}: Out of position </li>`;
            } else return {error:'FATAL ERROR'}
          }
        }

        for (const property in presences) {
          if (presences[property] == true){
            if (property == 'Box'){
              warningBox()
            } else {
              liPresencesHtml += `<li <li class="list-group-item list-group-item-info">${property}: Successfully detected</li>`;
            }
          } else if (positions[property] == false) {
            if (property !== 'Box'){
              liPresencesHtml += `<li <li class="list-group-item list-group-item-danger">${property}: Could not be detected</li>`;
            }
          } else return {error:'FATAL ERROR'}
        }

        document.querySelector('.res_presences').innerHTML = liPresencesHtml + "</ul><br>";
        document.querySelector('.res_positions').innerHTML = liPositionsHtml + "</ul>";

      }
    }
  }
}

function warningBox() {
  document.getElementById('miAudio').play();
  document.querySelector('.toast').style.display = 'block';
}

function closeTastwarningBox(e) {
  document.querySelector('.toast').style.display = 'none';
}