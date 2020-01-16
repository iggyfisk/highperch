function drawApmSeries() {
    var elem = d3.select('.apmseries').node().getBoundingClientRect();

    var margin = {
        top: 20,
        right: 90,
        bottom: 20,
        left: 35
    },

        width = elem.width - margin.left - margin.right,
        height = 250 - margin.top - margin.bottom;

    var x = d3.scaleLinear()
        .range([0, width]);

    var y = d3.scaleLinear()
        .range([height, 0]);

    var color = d3.scaleOrdinal(player_colors);

    var xAxis = d3.axisBottom(x);

    var yAxis = d3.axisLeft(y);

    var line = d3.line()
        .defined(d => !isNaN(d.actions)) // handle early leavers' missing minutes
        .curve(d3.curveMonotoneX)
        .x(function (d) {
            return x(d.minute);
        })
        .y(function (d) {
            return y(d.actions);
        });

    var viewboxDims = "0 0 " + (width + margin.left + margin.right) + " " + (height + margin.top + margin.bottom);

    var series = d3.select(".apmseries").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .classed("graph", true)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    function onResize() {
        var newElem = d3.select('.apmseries').node().getBoundingClientRect();
        width = newElem.width - margin.left - margin.right,
            series
                .attr("width", width);
        console.log("resize", width);
    }

    color.domain(d3.keys(apm_data[0]).filter(function (key) {
        return key !== "minute";
    }));

    var players = color.domain().map(function (name) {
        return {
            name: name,
            values: apm_data.map(function (d) {
                return {
                    minute: d.minute,
                    actions: +d[name]
                };
            })
        };
    });

    x.domain(d3.extent(apm_data, function (d) {
        return d.minute;
    }));

    y.domain([
        d3.min(players, function (c) {
            return d3.min(c.values, function (v) {
                return v.actions;
            });
        }),
        d3.max(players, function (c) {
            return d3.max(c.values, function (v) {
                return v.actions;
            });
        })
    ]);

    var legend = series.selectAll('g')
        .data(players)
        .enter()
        .append('g')
        .attr('class', 'legend');

    legend.append('rect') // color sample in legend
        .attr('x', width + 14)
        .attr('y', function (d, i) {
            return i * 18 - 7;
        })
        .attr('width', 8)
        .attr('height', 8)
        .style('fill', function (d) {
            return color(d.name);
        });

    legend.append('text') // battletags in legend
        .attr('x', width + 25)
        .attr('y', function (d, i) {
            return (i * 18);
        })
        .text(function (d) {
            return d.name.replace(/#\d+/, '');
        })
        .classed("battletag hp-toggle", true)
        .on("click", function (d) {
            var active = d.active ? false : true,
                newOpacity = active ? 0 : 1;
            d3.selectAll("." + d.name.replace('#', ''))
                .style("opacity", newOpacity);
            d.active = active;
        });
    series.append("g") // X axis label
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    series.append("g") // Y axis label
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("APM");

    var player = series.selectAll(".player")
        .data(players)
        .enter().append("g")
        .attr("class", "player");

    player.append("path")
        .attr("d", function (d) {
            return line(d.values);
        })
        .style("stroke", function (d) {
            return color(d.name);
        })
        .attr("class", function (d) {
            return "line " + d.name.replace('#', '');
        });
    // .classed("battetag hp-toggle", true);

    var mouseG = series.append("g")
        .attr("class", "mouse-over-effects");

    mouseG.append("path") // this is the black vertical line to follow mouse
        .attr("class", "mouse-line")
        .style("stroke", "black")
        .style("stroke-width", "1px")
        .style("opacity", "0");

    var lines = document.getElementsByClassName('line');

    var mousePerLine = mouseG.selectAll('.mouse-per-line')
        .data(players)
        .enter()
        .append("g")
        // .attr("class", "mouse-per-line");
        .attr("class", function (d) {
            return "mouse-per-line " + d.name.replace('#', '');
        });

    mousePerLine.append("circle")
        .attr("r", 3)
        .style("fill", function (d) {
            return color(d.name);
        })
        // .style("fill", "none")
        .style("stroke-width", "1px")
        .style("opacity", "0");

    mousePerLine.append("text")
        .attr("transform", "translate(10,3)");

    mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
        .attr('width', width) // can't catch mouse events on a g element
        .attr('height', height)
        .attr('fill', 'none')
        .attr('pointer-events', 'all')
        .on('mouseout', function () { // on mouse out hide line, circles and text
            d3.select(".mouse-line")
                .style("opacity", "0");
            d3.selectAll(".mouse-per-line circle")
                .style("opacity", "0");
            d3.selectAll(".mouse-per-line text")
                .style("opacity", "0");
        })
        .on('mouseover', function () { // on mouse in show line, circles and text
            d3.select(".mouse-line")
                .style("opacity", "1");
            d3.selectAll(".mouse-per-line circle")
                .style("opacity", "1");
            d3.selectAll(".mouse-per-line text")
                .style("opacity", "1");
        })
        .on('mousemove', function () { // mouse moving over canvas
            var mouse = d3.mouse(this);
            d3.select(".mouse-line")
                .attr("d", function () {
                    var d = "M" + mouse[0] + "," + height;
                    d += " " + mouse[0] + "," + 0;
                    return d;
                });

            d3.selectAll(".mouse-per-line")
                .attr("transform", function (d, i) {
                    var xMinute = x.invert(mouse[0]),
                        bisect = d3.bisector(function (d) { return d.minute; }).right;
                    idx = bisect(d.values, xMinute);

                    var beginning = 0,
                        end = lines[i].getTotalLength(),
                        target = null;

                    while (true) {
                        target = Math.floor((beginning + end) / 2);
                        pos = lines[i].getPointAtLength(target);
                        if ((target === end || target === beginning) && pos.x !== mouse[0]) {
                            break;
                        }
                        if (pos.x > mouse[0]) end = target;
                        else if (pos.x < mouse[0]) beginning = target;
                        else break; //position found
                    }

                    d3.select(this).select('text')
                        .text(y.invert(pos.y).toFixed(0)) // line mouseover APM text
                        .classed("cursortext", true);
                    return "translate(" + mouse[0] + "," + pos.y + ")";
                });
        });
}

function redrawApmSeries() {
    d3.select("svg").remove();
    drawApmSeries();
}

(() => {
    document.addEventListener("DOMContentLoaded", () => {
        drawApmSeries();
        window.addEventListener('resize', redrawApmSeries);
        document.querySelectorAll('apmseriesbutton').forEach(element => {
            element.addEventListener('click', event => {
                drawApmSeries();
            });
        });
    });
})();