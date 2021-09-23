var xhttp, topo_data;
xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        topo = this.responseText;
        topo = JSON.parse(topo);
        let x = topo['x'];
        let y = topo['y'];
        let z = topo['z'];
        let freeair = topo['freeair'];
        let topo_data = []
        for (let i = 0; i < x.length; i++) {
            temp = {};
            temp['x'] = x[i];
            temp['y'] = y[i];
            temp['z'] = z[i];
            temp['freeair'] = freeair[i];
            topo_data.append(temp);
        }
        function generateTableHead(table, datatabel) {
            let thead = table.createTHead();
            let row = thead.insertRow();
            for (let key of datatabel) {
                let th = document.createElement("th");
                let text = document.createTextNode(key);
                th.appendChild(text);
                row.appendChild(th);    
            }       
        } 

        function generateTable(table, datatabel) {
            for (let element of datatabel) {
                let row = table.insertRow();
                for (key in element) {
                    let cell = row.insertCell();
                    let text = document.createTextNode(element[key]);
                    cell.appendChild(text);
                }
            }
        }
        let table = document.getElementById("mainTable");
        let datatabel = Object.keys(topodata[0]);
        generateTable(table, topodata);
        generateTableHead(table, datatabel);
    }
};

xhttp.open("GET", "{% url 'get_topo' work_data.unique_id %}", true);
xhttp.send();