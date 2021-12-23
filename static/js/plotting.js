let mapPlot = (x, y, z, title) => {
    try{
            var data = [{
                z : z,
                x : x,
                y : y,
                type: 'contour',
                colorscale: 'Jet',
                contours: {
                    coloring: 'heatmap',
                    labelfont: {
                    family: 'Raleway',
                    size: 12,
                    color: 'white',
                        }
                    }
                ,}];
            var layout = {
                title: title
                };
            Plotly.newPlot('elevDiv', data, layout);
    }  catch (error) {
        window.alert("belum ada data")
    }              
}   

let elevPlot = () => {
    let x = JSON.parse(localStorage.getItem('data'))['x'];
    let y =JSON.parse(localStorage.getItem('data'))['y'];
    let z = JSON.parse(localStorage.getItem('data'))['z'];
    mapPlot(x, y, z, "Peta Kontur Elevasi");
}

let faPlot = () => {
    let x = JSON.parse(localStorage.getItem('data'))['x'];
    let y = JSON.parse(localStorage.getItem('data'))['y'];
    let fa = JSON.parse(localStorage.getItem('data'))['freeair'];
    mapPlot(x, y, fa, "Peta Kontur Free Air");
}

let spectrumPlot = () =>  {
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

window.onbeforeunload = function() {
    localStorage.clear();
}

