function densityPlot(){
    var xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        let x = JSON.parse(this.responseText)['sumbu_x'];
        let y = JSON.parse(localStorage.getItem('data'))['freeair'];
        let z = JSON.parse(this.responseText)['y_pred'];
        let legend = JSON.parse(this.responseText)['legend'];
        regPlot(x, y, z, legend, "Plot Regresi Linear Densitas");
    };    

    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/get-bouguer`, true);
    xhttp.send();  
};
