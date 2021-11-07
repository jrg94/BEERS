var map = d3.choropleth()
    .geofile('/d3-geomap/topojson/countries/USA.json')
    .projection(d3.geoAlbersUsa)
    .column('2012')
    .unitId('fips')
    .scale(1000)
    .legend(true);

d3.csv('/data/venture-capital.csv').then(data => {
    map.draw(d3.select('#map').datum(data));
});