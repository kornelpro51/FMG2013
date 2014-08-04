	$(function () {
    var sin = [], cos = [];
    for (var i = 0; i < 9; i += 0.8) {
        sin.push([i, Math.sin(i)]);
        cos.push([i, Math.cos(i)]);
    }

    var plot = $.plot($("#sidebar-chart"),
           [ { data: sin, label: "sin(x)"}, { data: cos, label: "cos(x)" } ], {
               series: {
                   lines: { show: true },
                   points: { 
					   show: true,
					   fill: true,
                        fillColor: "#333"

				   }
               },
                colors: ["#ffac53", "#6dd0fa"],
                grid: {
                    show: true,
                    color: "#dddddd", // primary color used for outline and labels
                    borderColor: "#efefef", // set if different from the grid color
                    tickColor: "rgba(255,255,255,0.06)", // color for the ticks, e.g. "rgba(0,0,0,0.15)"
                    hoverable: true
                },
			 legend: false,
               yaxis: { min: -1.1, max: 1.1 },
			   xaxis: { min: 0, max: 8 }
             });

    function showTooltip(x, y, contents) {
        $('<div id="tooltip1" class="chart-tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 5,
			'z-index': '9999',
			'color': '#fff',
			'font-size': '11px',
            opacity: 0.9
        }).appendTo("body").fadeIn(200);
    }

    var previousPoint = null;
    $("#sidebar-chart").bind("plothover", function (event, pos, item) {
        $("#x").text(pos.x.toFixed(2));
        $("#y").text(pos.y.toFixed(2));

        if ($("#sidebar-chart").length > 0) {
            if (item) {
                if (previousPoint != item.dataIndex) {
                    previousPoint = item.dataIndex;
                    
                    $("#tooltip1").remove();
                    var x = item.datapoint[0].toFixed(2),
                        y = item.datapoint[1].toFixed(2);
                    
                    showTooltip(item.pageX, item.pageY,
                                item.series.label + " of " + x + " = " + y);
                }
            }
            else {
                $("#tooltip1").remove();
                previousPoint = null;            
            }
        }
    });

    $("#sidebar-chart").bind("plotclick", function (event, pos, item) {
        if (item) {
            $("#clickdata").text("You clicked point " + item.dataIndex + " in " + item.series.label + ".");
            plot.highlight(item.series, item.datapoint);
        }
    });
});
