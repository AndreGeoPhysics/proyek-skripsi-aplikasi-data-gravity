function sbaGridCalc(){
    var xhttp = new XMLHttpRequest();
    try{
        xhttp.onload = function() {
            let bouguer = JSON.parse(JSON.parse(this.responseText)['sbagrid']);
            let x = JSON.parse(JSON.parse(localStorage.getItem('data'))['x_grid']);
            let y = JSON.parse(JSON.parse(localStorage.getItem('data'))['y_grid']);    
            mapPlot(x, y, bouguer, "Peta Anomali Bouguer");
        };    
    } catch (error){
        window.alert("belum ada data");
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/bouguer-map`, true);
    xhttp.send();  
};