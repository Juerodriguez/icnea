idIinterval = setInterval(getReport, 3000);

function getReport() {
    let req = new XMLHttpRequest();
    const url = "http://" + window.location.hostname + "/detections/get_report";
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