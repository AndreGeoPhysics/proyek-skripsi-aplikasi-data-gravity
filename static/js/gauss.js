function gaussPlot(){
    var xhttp = new XMLHttpRequest();
    try{
        xhttp.onload = function() {
            let gauss = JSON.parse(JSON.parse(this.responseText)['gauss']);
            let x = JSON.parse(JSON.parse(localStorage.getItem('data'))['x_grid']);
            let y = JSON.parse(JSON.parse(localStorage.getItem('data'))['y_grid']); 
            mapPlot(x, y, gauss, "Peta kontur gaussian");
        };    
    } catch (error){
        window.alert("belum ada data");
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/get-gauss`, true);
    xhttp.send();  
};
