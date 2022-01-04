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
    let x = JSON.parse(JSON.parse(localStorage.getItem('data'))['x_grid']);
    let y = JSON.parse(JSON.parse(localStorage.getItem('data'))['y_grid']);
    let z = JSON.parse(JSON.parse(localStorage.getItem('data'))['z_grid']);
    mapPlot(x, y, z, "Peta Kontur Elevasi");
}

let faPlot = () => {
    let x = JSON.parse(localStorage.getItem('data'))['x'];
    let y = JSON.parse(localStorage.getItem('data'))['y'];
    let fa = JSON.parse(localStorage.getItem('data'))['freeair'];
    mapPlot(x, y, fa, "Peta Kontur Free Air");
}

let regPlot = (x, y, title) =>  {
    try {
        var trace1 = {
            x: x,
            y: y,
            mode: 'markers',
            type: 'scatter'
            };
          
        var data = [trace1];
        
        var layout = {
            title: title
            };

        Plotly.newPlot('elevDiv', data, layout);
    
    } catch (error) {
        window.alert("belum ada data")
    }
}  

window.onbeforeunload = function() {
    localStorage.clear();
}

