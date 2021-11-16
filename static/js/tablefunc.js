function generateTableHead(table, datatabel) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of datatabel) {
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        th.appendChild(text);
        row.appendChild(th);    
    }       
};

function generateTable(table, datatabel) {
    for (let element of datatabel) {
        let row = table.insertRow();
        for (key in element) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text);
        }
    }
};

function clearTable(key) {
    const table = document.getElementById(key);
    table.textContent = "";
}