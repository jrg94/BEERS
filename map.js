chart = {
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, 975, 610]);
  
    svg.append("g")
        .attr("transform", "translate(610,20)")
        .append(() => legend({color, title: data.title, width: 260}));
  
    svg.append("g")
      .selectAll("path")
      .data(topojson.feature(us, us.objects.states).features)
      .join("path")
        .attr("fill", d => color(data.get(d.properties.name)))
        .attr("d", path)
      .append("title")
        .text(d => `${d.properties.name}
  ${format(data.get(d.properties.name))}`);
  
    svg.append("path")
        .datum(topojson.mesh(us, us.objects.states, (a, b) => a !== b))
        .attr("fill", "none")
        .attr("stroke", "white")
        .attr("stroke-linejoin", "round")
        .attr("d", path);
  
    return svg.node();
  }