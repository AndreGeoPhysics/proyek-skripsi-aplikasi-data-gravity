function regionalPlot(){
    var xhttp = new XMLHttpRequest();
    try{
        xhttp.onload = function() {
            let regional = JSON.parse(JSON.parse(this.responseText)['regional']);
            let x = JSON.parse(JSON.parse(localStorage.getItem('data'))['x_grid']);
            let y = JSON.parse(JSON.parse(localStorage.getItem('data'))['y_grid']); 
            mapPlot(x, y, regional, "Peta Kontur Regional");
        };    
    } catch (error){
        window.alert("belum ada data");
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/moving-average`, true);
    xhttp.send();  
};

function residualPlot(){
    var xhttp = new XMLHttpRequest();
    try{
        xhttp.onload = function() {
            let residual = JSON.parse(JSON.parse(this.responseText)['residual']);
            let x = JSON.parse(JSON.parse(localStorage.getItem('data'))['x_grid']);
            let y = JSON.parse(JSON.parse(localStorage.getItem('data'))['y_grid']); 
            mapPlot(x, y, residual, "Peta Kontur Residual");
        };    
    } catch (error){
        window.alert("belum ada data");
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/moving-average`, true);
    xhttp.send();  
};
