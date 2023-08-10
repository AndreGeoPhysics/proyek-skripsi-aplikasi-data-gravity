function fhdPlot(){
    var xhttp = new XMLHttpRequest();
    try{
        xhttp.onload = function() {
            let fhd = JSON.parse(JSON.parse(this.responseText)['fhd']);
            let x = JSON.parse(JSON.parse(localStorage.getItem('data'))['x_grid']);
            let y = JSON.parse(JSON.parse(localStorage.getItem('data'))['y_grid']); 
            mapPlot(x, y, fhd, "Peta FHD");
        };    
    } catch (error){
        window.alert("belum ada data");
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/get-fhd`, true);
    xhttp.send();  
};

