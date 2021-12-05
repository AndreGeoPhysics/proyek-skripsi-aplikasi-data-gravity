function sbaGridCalc(){
    var xhttp = new XMLHttpRequest();
    try{
        xhttp.onload = function() {
            localStorage.setItem('sbagrid', this.responseText);
        };    
    } catch (error){
        window.alert("belum ada data");
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/bouguer-map`, true);
    xhttp.send();  
};