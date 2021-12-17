function svdCalc(){
    var xhttp = new XMLHttpRequest();
    try{
        xhttp.onload = function() {
            let elkins = JSON.parse(JSON.parse(this.responseText)['elkins']);
            let x = JSON.parse(JSON.parse(localStorage.getItem('data'))['x_grid']);
            let y = JSON.parse(JSON.parse(localStorage.getItem('data'))['y_grid']); 
            mapPlot(x, y, elkins, "Peta SVD Elkins");
        };    
    } catch (error){
        window.alert("belum ada data");
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/get-svd`, true);
    xhttp.send();  
};