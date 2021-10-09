function sbaCalc(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            bouguer = this.responseText;
            let data = JSON.parse(localStorage.getItem('data'));
            data['sba'] = bouguer;
            let x = data['x'];
            let y = data['y'];
            let z = data['z'];
            let freeair = data['freeair'];
            let bouguer = data['sba'];
            console.log(data);
            let sba_data = []
            for (let i = 0; i < x.length; i++) {
                temp = {};
                temp['x'] = x[i];
                temp['y'] = y[i];
                temp['z'] = z[i];
                temp['freeair'] = freeair[i];
                temp['bouguer'] = bouguer[i];
                sba_data.push(temp);
            }
            let table = document.getElementById("mainTable");
            let datatabel = Object.keys(sba_data[0]);
            generateTable(table, sba_data);
            generateTableHead(table, datatabel);
            
        }
    }
    const splittedPathname = window.location.pathname.split("/");
    const uniqueId = splittedPathname[splittedPathname.length-1];
    xhttp.open("GET", `/dashboard/workspace/${uniqueId}/get-bouguer`, true);
    xhttp.send();
};
