const zbox = document.querySelectorAll('td.z');
let zarray = []
for (let i = 0; i < zbox.length; i++) {
    zarray.push(zbox[i].innerHTML)
}
const xbox = document.querySelectorAll('td.x');
let xarray = []
for (let i = 0; i < xbox.length; i++) {
    xarray.push(xbox[i].innerHTML)
}
const ybox = document.querySelectorAll('td.y');
let yarray = []
for (let i = 0; i < ybox.length; i++) {
    yarray.push(ybox[i].innerHTML)
}

var data = [{
            z : zarray,
            x : xarray,
            y : yarray,
            type: 'contour',
            colorscale: 'Jet'
            }];
var layout = {
            title: 'Peta Kontur Elevasi'
            };
Plotly.newPlot('elevDiv', data, layout);
