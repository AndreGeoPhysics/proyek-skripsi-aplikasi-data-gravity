function densityPlot(){
    var xhttp = new XMLHttpRequest();
    try{
        xhttp.onload = function() {
            let x = JSON.parse(this.responseText)['sumbu_x'];
            let y = JSON.parse(localStorage.getItem('data'))['freeair'];
            regPlot(x, y, "Plot Regresi Linear Densitas");
        };    
    } catch (error){
        window.alert("belum ada data");
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/get-bouguer`, true);
    xhttp.send();  
};
