$(function () {
    var previousPoint;
 

    //Display horizontal graph
    var d1_h = [];
    for (var i = 0; i <= 3; i += 1)
        d1_h.push([parseInt(Math.random() * 30),i ]);

    var d2_h = [];
    for (var i = 0; i <= 3; i += 1)
        d2_h.push([parseInt(Math.random() * 30),i ]);

    var d3_h = [];
    for (var i = 0; i <= 3; i += 1)
        d3_h.push([ parseInt(Math.random() * 30),i]);
                
    var ds_h = new Array();
    ds_h.push({
        data:d1_h,
        bars: {
            horizontal:true, 
            show: true, 
            barWidth: 0.2, 
            order: 1,
        }
    });
ds_h.push({
    data:d2_h,
    bars: {
        horizontal:true, 
        show: true, 
        barWidth: 0.2, 
        order: 2
    }
});
ds_h.push({
    data:d3_h,
    bars: {
        horizontal:true, 
        show: true, 
        barWidth: 0.2, 
        order: 3
    }
});

    //tooltip function
    function showTooltip(x, y, contents, areAbsoluteXY) {
        var rootElt = 'body';
	
        $('<div id="tooltip3" class="chart-tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y - 35,
            left: x - 5,
			'z-index': '9999',
			'color': '#fff',
			'font-size': '11px',
            opacity: 0.9
        }).prependTo(rootElt).show();
    }

$.plot($("#sidebar-bars-horizontal"), ds_h, {
                colors: ["#bde07e", "#6dd0fa", "#ffac53", "#ea5f5f"],
                series: {
                    bars: {
                        fill: true,
                        fillColor: { colors: [ { opacity: 0.9 }, { opacity: 1 } ] },
						lineWidth: 0
                    }
                },
                grid: {
                    show: true,
                    color: "#dddddd", // primary color used for outline and labels
                    borderColor: "#efefef", // set if different from the grid color
                    tickColor: "rgba(255,255,255,0.06)", // color for the ticks, e.g. "rgba(0,0,0,0.15)"
                    hoverable: true
                }
});

//add tooltip event
$("#sidebar-bars-horizontal").bind("plothover", function (event, pos, item) {
    if (item) {
        if (previousPoint != item.datapoint) {
            previousPoint = item.datapoint;
 
            //delete de prГ©cГ©dente tooltip
            $('.chart-tooltip').remove();
 
            var x = item.datapoint[0];
 
            //All the bars concerning a same x value must display a tooltip with this value and not the shifted value
            if(item.series.bars.order){
                for(var i=0; i < item.series.data.length; i++){
                    if(item.series.data[i][3] == item.datapoint[0])
                        x = item.series.data[i][0];
                }
            }
 
            var y = item.datapoint[1];
 
            showTooltip(item.pageX+5, item.pageY+5,x + " = " + y);
 
        }
    }
    else {
        $('.chart-tooltip').remove();
        previousPoint = null;
    }
 
});

 
});