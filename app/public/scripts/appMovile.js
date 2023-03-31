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

            } else if (report_res.calibrateStatus == false) {
                const htmlMsg = 
                `<div class="alert alert-warning d-flex align-items-center" role="alert">
                    <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
                    <div style="padding-top: 60px; padding-bottom: 60px;">WARNING: se necesita calibración para vizualizar</div>
                </div>`
                document.querySelector('.res_presences').innerHTML = htmlMsg
                document.querySelector('.res_positions').innerHTML = htmlMsg
            }
        }
    }
}