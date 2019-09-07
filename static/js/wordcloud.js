function word_cloud(width_, height_, file_, color_list_, interval_, font_, select_) {
    var svg = d3.select(select_).append("svg")
            .attr("width", width_)
            .attr("height", height_);
    d3.csv(file_, function (data) {
            showCloud(data)
            setInterval(function(){
                 showCloud(data)
                 //console.log(data)
            },interval_) 
    });
    wordScale = d3.scale.linear().domain([0, 200]).range([0, 100]).clamp(true);
    var svg = d3.select("svg")
                    .append("g")
                    .attr("transform", "translate(" + width_ / 2 + "," + height_ / 2 + ")")

    function showCloud(data) {
            d3.layout.cloud().size([width_, height_])
                //클라우드 레이아웃에 데이터 전달
                .words(data)
                .rotate(function (d) {
                    // return d.text.length > 3 ? 0 : 90;
                    return 0;
                })
                //스케일로 각 단어의 크기를 설정
                .fontSize(function (d) {
                    return wordScale(d.frequency);
                })
                //클라우드 레이아웃을 초기화 > end이벤트 발생 > 연결된 함수 작동  
                .on("end", draw)
                .start();

            function draw(words) { 
                var cloud = svg.selectAll("text").data(words)
                //Entering words
                cloud.enter()
                    .append("text")
                    .style("font-family", font_)
                    .style("fill", function (d) {
                        if(d.text[0]=="0"){
                            return color_list_[0];
                        }
                        return color_list_[Math.floor(Math.random() * color_list_.length + 1)];
                    })
                    .style("fill-opacity", .5)
                    .attr("text-anchor", "middle") 
                    .attr('font-size', 1)
                    .text(function (d) {
                        return d.text.substr(1,d.text.length-1).toLowerCase();
                    });
                cloud
                    .transition()
                    .duration(600)
                    .style("font-size", function (d) {
                        return d.size + "px";
                    })
                    .attr("transform", function (d) {
                        var rot_ = (d.text == "모닥불") ? 0:d.rotate;
                        return "translate(" + [d.x, d.y] + ")rotate(" + rot_ + ")";
                    })
                    .style("fill-opacity", 1); 
            }
    }
}