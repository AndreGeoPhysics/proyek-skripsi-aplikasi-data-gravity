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
    Plotly.newPlot('elevDiv', data, layout);
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
    Plotly.newPlot('elevDiv', data, layout);    
}

let sbaPlot = (bouguer, x, y) => {
    try {
        let bouguer = JSON.parse(JSON.parse(localStorage.getItem('sbagrid'))['sbagrid']);
        let x = JSON.parse(JSON.parse(localStorage.getItem('sbagrid'))['xgrid']);
        let y = JSON.parse(JSON.parse(localStorage.getItem('sbagrid'))['ygrid']);
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
        Plotly.newPlot('elevDiv', data, layout);            
    } catch (error) {
        window.alert("belum ada data");
    }
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
            type: 'scatter',
            xaxis: 'x2',
            yaxis: 'y2'
            };

        var trace3 = {
            x: k,
            y: lnA_3,
            mode: 'markers',
            type: 'scatter',
            xaxis: 'x3',
            yaxis: 'y3'
            };

        var data = [trace1, trace2, trace3];
        
        var layout = {
            xaxis: {domain: [0, 0.3]},
            xaxis2: {domain: [0.31, 0.61]},
            xaxis3: {domain: [0.62, 0.92]},
            yaxis: {domain: [0, .9]},
            yaxis2: {anchor: 'x2',domain: [0, .9]},
            yaxis3: {anchor: 'x3', domain: [0, .9]}        

            };
            
        Plotly.newPlot('elevDiv', data, layout);
    
    } catch (error) {
        window.alert("belum ada data")
    }
}  

let fhdPlot = (x, y, fhd) => {
        var data = [{
            z : fhd,
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
            title: 'Peta FHD'
            };
        Plotly.newPlot('elevDiv', data, layout);            
    
}   

let svdPlot = (x, y, elkins) =>  {
    try {
        var data = [{
            z : elkins,
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

        Plotly.newPlot('elevDiv', data);
    
    } catch (error) {
        window.alert("belum ada data")
    }
}  


window.onbeforeunload = function() {
    localStorage.clear();
}

