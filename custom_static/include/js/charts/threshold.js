$(function () {
    var d1 = [];
    for (var i = 0; i <= 60; i += 1)
	d1.push([i, parseInt(Math.random() * 30 - 10)]);
	
    function plotWithOptions(t) {
        $.plot($("#placeholder-threshold"), [ {
            data: d1,
            color: "rgb(30, 180, 20)",
            threshold: { below: t, color: "rgb(200, 20, 30)" },
            lines: { steps: true }
        } ]);
    }

    plotWithOptions(0);

    $(".threshold-buttons input").click(function (e) {
        e.preventDefault();
        var t = parseFloat($(this).val().replace('Threshold at ', ''));
        plotWithOptions(t);
    });

});
