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
        let bouguer = JSON.parse(JSON.parse(localStorage.getItem('sbagrid'))['sbagrid']);
        let x = JSON.parse(JSON.parse(localStorage.getItem('sbagrid'))['xgrid']);
        let y = JSON.parse(JSON.parse(localStorage.getItem('sbagrid'))['ygrid']);
        if (bouguer === null) {console.log("empty")}; 
        var data = [{
            z : bouguer,
            x : x,
            y : y,
            type: 'contour',
            colorscale: 'Jet',
            contours: {
                coloring: 'heatmap',
                showlabels: true,
                labelfont: {
                  family: 'Raleway',
                  size: 12,
                  color: 'white',
                    }
                }
            ,}];
        var layout = {
            title: 'Peta Kontur Bouguer'
            };
        Plotly.newPlot('elevDiv', data);            
    } catch (error) {
        window.alert("belum ada data");
    }
}   

window.onbeforeunload = function() {
    localStorage.clear();
}

let spectrumplot = () =>  {
    try {
        let k = JSON.parse(JSON.parse(localStorage.getItem('spectrumdict'))['k']);
        let lnA_1 = JSON.parse(JSON.parse(localStorage.getItem('spectrumdict'))['lnA_1']);
        let lnA_2 = JSON.parse(JSON.parse(localStorage.getItem('spectrumdict'))['lnA_2']);
        let lnA_3 = JSON.parse(JSON.parse(localStorage.getItem('spectrumdict'))['lnA_3']);

        var trace1 = {
            x: k,
            y: lnA_1,
            mode: 'markers',
            type: 'scatter'
            };
          
        var trace2 = {
            x: k,
            y: lnA_2,
            mode: 'markers',
            type: 'scatter'
            };

        var trace3 = {
            x: k,
            y: lnA_3,
            mode: 'markers',
            type: 'scatter'
            };

        var data = [trace1, trace2, trace3];
        
        var layout = {
            grid: {rows: 1, columns: 3, pattern: 'independent'},
            };
        
        Plotly.newPlot('myDiv', data, layout);
    
    } catch (error) {
        window.alert("belum ada data")
    }
}  