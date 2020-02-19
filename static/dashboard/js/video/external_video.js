


var videoAreaStatus = false
var videoEditArea = $('#video-edit-area');

$('#open-add-video-btn').click(function () {
    if(!videoAreaStatus){
        videoEditArea.show();
        videoAreaStatus = true
    }else {
         videoEditArea.hide();
         videoAreaStatus=false
    }
});