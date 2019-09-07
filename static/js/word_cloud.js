let wordcloud_width = $(window).width();
if (wordcloud_width > 800){
    wordcloud_width = 800;
}
word_cloud(
    wordcloud_width, //width
    600, //height
    "/static/example.csv", //file_path
    ["#C30E2E","#0D8ACF","#405275","#8FBB33","#fbc280"], //color_list
    5000, //change interval
    "overwatch", //font
    "div.test" //tag_select
); 