function fhdCalc(){
    var xhttp = new XMLHttpRequest();
    try{
        xhttp.onload = function() {
            let fhd = JSON.parse(JSON.parse(this.responseText)['fhd']);
            console.log(fhd);
            let x = JSON.parse(JSON.parse(localStorage.getItem('sbagrid'))['xgrid']);
            let y = JSON.parse(JSON.parse(localStorage.getItem('sbagrid'))['ygrid']); 
            fhdPlot(x, y, fhd)
        };    
    } catch (error){
        window.alert("belum ada data");
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/get-fhd`, true);
    xhttp.send();  
};

