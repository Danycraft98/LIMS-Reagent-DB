// Graph dimensions
var chart = {width: 650, height: 400};
var margin = {width: 30, height: 30};

// Bar colors
var color = d3.scaleOrdinal()
    	.range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

//---------------------------------------Scale Parameters---------------------------------------
// y scale
var y = d3.scaleLinear()
    	.range([chart.height, 0]);

//  x Scale for groups
var x_bar0 = d3.scaleBand()
   	.rangeRound([0, chart.width])
   	.paddingInner(0.1);

// x Scale for each groups
var x_bar1 = d3.scaleBand()

//--------------------------------------Graphing Functions--------------------------------------
// Create SVG
function create_svg(name) {
	return d3.select( "#chart" )
		.append( "svg" )
		        .attr("id", name)
			.attr( "width", chart.width + margin.width*2)
			.attr( "height", chart.height + margin.height*2)
			.append( "g" )
			.attr("transform", "translate(" + margin.width + "," + margin.height + ")");
}

// Legend Function
function create_legend(svg, keys) {
	var legend =  svg.append( "g" )
		.attr("font-family", "sans-serif")
		.attr("font-sicolore", 10)
		.attr("text-anchor", "end")
		.selectAll("g")
			.data(keys.slice().reverse())
			.enter().append("g")
			.attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

	legend.append("rect")
		.attr("x", chart.width - 17)
		.attr("width", 15)
		.attr("height", 15)
		.attr("fill", color)
		.attr("stroke", color)
		.attr("stroke-width",2)

	legend.append("text")
		.attr("x", chart.width - 24)
		.attr("y", 9.5)
		.attr("dy", "0.32em")
		.text(function(d) { return d; });
}


function create_axis(svg, x_scale) {
    	svg.append( "g" )
        	.attr("class", "y_axis")
        	.call(d3.axisLeft(y))
            .append("text")
		.attr("x", 2)
		.attr("dy", "0.32em")
		.attr("font-weight", "bold")
		.attr("text-anchor", "start")
		.text("Population");

	svg.append( "g" )
		.attr("class", "x_axis")
		.attr("transform", "translate(0," + chart.height + ")")
		.call(d3.axisBottom(x_scale));
}