$(function() {
    var converter = new showdown.Converter();
    var html = converter.makeHtml($('#article_content').val());
    $('#article_viewer').html(html);
});
