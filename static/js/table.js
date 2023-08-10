var xhttp = new XMLHttpRequest();
xhttp.onload = function() {
    localStorage.setItem('data', this.responseText);
    const topo = JSON.parse(this.responseText);
    let x = topo['x'];
    let y = topo['y'];
    let z = topo['z'];
    let freeair = topo['freeair'];
    let topo_data = [];
    for (let i = 0; i < x.length; i++) {
        temp = {};
        temp['x'] = x[i];
        temp['y'] = y[i];
        temp['z'] = z[i];
        temp['freeair'] = freeair[i];
        topo_data.push(temp);
    }
    let table = document.getElementById("mainTable");
    let datatabel = Object.keys(topo_data[0]);
    generateTable(table, topo_data);
    generateTableHead(table, datatabel);
};
const splittedPathname = window.location.pathname.split("/");
const uniqueId = splittedPathname[splittedPathname.length-1];
xhttp.open("GET", `/dashboard/workspace/${uniqueId}/get-topo`, true);
xhttp.send();