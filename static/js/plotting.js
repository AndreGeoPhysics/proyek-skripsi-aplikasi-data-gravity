let elevPlot = () => {
    let dataplot = JSON.parse(localStorage.getItem('data')); 
    var data = [{
        z : dataplot['z'],
        x : dataplot['x'],
        y : dataplot['y'],
        type: 'contour',
        colorscale: 'Jet'
        }];
    var layout = {
        title: 'Peta Kontur Elevasi'
        };
    Plotly.newPlot('elevDiv', data);
}

let faPlot = () => {
    let dataplot = JSON.parse(localStorage.getItem('data')); 
    var data = [{
        z : dataplot['freeair'],
        x : dataplot['x'],
        y : dataplot['y'],
        type: 'contour',
        colorscale: 'Jet'
        }];
    var layout = {
        title: 'Peta Kontur Free Air'
        };
    Plotly.newPlot('elevDiv', data);    
}

let sbaPlot = () => {
    try {
        let dataplot = JSON.parse(localStorage.getItem('data')); 
        let bouguer = JSON.parse(JSON.parse(localStorage.getItem('bouguer'))['sba']);
        if (bouguer === null) {console.log("empty")}; 
        var data = [{
            z : bouguer,
            x : dataplot['x'],
            y : dataplot['y'],
            type: 'contour',
            colorscale: 'Jet'
            }];
        var layout = {
            title: 'Peta Kontur Bouger'
            };
        Plotly.newPlot('elevDiv', data);            
    } catch (error) {
        window.alert("belum ada data");
    }
}   

window.onbeforeunload = function() {
    localStorage.clear();
}