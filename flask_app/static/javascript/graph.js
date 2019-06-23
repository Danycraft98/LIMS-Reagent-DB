var svg = create_svg("bar_graph");

function update_bar_graph(data_json){
 	var stages = ["POCP", "AGILE", "OCT", "IDH"]
	/*d3.selectAll(".type").each(function(d){
		cb = d3.select(this);
		if(cb.property("checked")){
			stages.push(cb.property("value"));
		}
	});*/
	svg.selectAll("g").remove();

	create_legend(svg, stages);
	data_json.then(function(data) {
		x_bar0.domain(data.map(function(d) { return d.Stage; }));
		x_bar1.domain(stages).rangeRound([ 0, x_bar0.bandwidth()]);
		y.domain([0,35]);

		data.forEach(function(d) {
			d.bars = stages.map(function(key, i) {
				return {
					key: key,
					value: +d[key]
				};
			});
		});
		create_axis(svg, x_bar0);

		var groups = svg.selectAll(".groups")
			.data(data).enter().append("g")
			.attr("class", "group")
			.attr("transform", function(d) {
			return "translate(" + x_bar0(d.Stage) + ",0)";
		});

		groups.selectAll("rect")
			.data(function(d) { return d.bars; })
			.enter().append("rect")
				.attr("x", function(d) { return x_bar1(d.key); })
				.attr("y", function(d) { return y(d.value); })
				.attr("width", x_bar1.bandwidth())
				.attr("height", function(d) { return chart.height - y(d.value); })
				.attr("fill", function(d) { return color(d.key); });

	});
}